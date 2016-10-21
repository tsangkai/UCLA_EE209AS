//NodeMCU/ESP8266 implement WebSocketsServer
//arduino-er.blogspot.com

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <WebSocketsServer.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <Hash.h>

#include "FS.h"


// WiFi Module
ESP8266WiFiMulti WiFiMulti;

ESP8266WebServer server = ESP8266WebServer(80);
WebSocketsServer webSocket = WebSocketsServer(81);

// Output Module
const int LED_PIN = LED_BUILTIN;

String html_home;
String css_code;

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t lenght) {
    switch(type) {
        case WStype_DISCONNECTED:
            Serial.printf("[%u] Disconnected!\n", num);
            break;
        case WStype_CONNECTED: 
           {
                IPAddress ip = webSocket.remoteIP(num);
                Serial.printf("[%u] Connected from %d.%d.%d.%d url: %s\n", num, ip[0], ip[1], ip[2], ip[3], payload);

                // send message to client
                webSocket.sendTXT(num, "Connected");
            }
            break;
        case WStype_TEXT:  // TODO
            Serial.printf("[%u] get text: %s\n", num, payload);

            if(payload[0] == '#') {

                if(payload[1] == 'O') {
                    digitalWrite(LED_PIN, LOW);
                }
                else {
                    digitalWrite(LED_PIN, HIGH);
                 
                }
            }

            break;
    }

}

void prepareFile(){
  
    Serial.println("Prepare file system");
    SPIFFS.begin();
  
    File file = SPIFFS.open("/home.html", "r");
    if (!file) {
        Serial.println("HTML file open failed");  
    } 
    else {
        Serial.println("HTML file open success");

        html_home = "";
        while (file.available()) {
            //Serial.write(file.read());
            String line = file.readStringUntil('\n');
            html_home += line + "\n";
        }
        file.close();

        //Serial.print(html_home);
    }

    File css_file = SPIFFS.open("/style.css", "r");
    if (!css_file) {
        Serial.println("CSS file open failed");  
    } 
    else {
        Serial.println("CSS file open success");

        css_code = "";
        while (css_file.available()) {
            //Serial.write(file.read());
            String line = css_file.readStringUntil('\n');
            css_code += line + "\n";
        }
        css_file.close();

        Serial.println(css_code);
    }


}

//void handleResponse() {
//    if (server.uri() == "/style.css") {
//        server.send(200, "text/css", css_code);
//        Serial.println("CSS load!");
//        return;
//    }
//    else {
//        server.send(200, "text/html", html_home);
//        Serial.println("HTML load!");
//        return;
     
//    }
//}


void setup() {
    Serial.begin(115200);

    //Serial.setDebugOutput(true);
    Serial.println();



    // setup harware output // TODO
    Serial.println("Setup LED pins");
    pinMode(LED_PIN, OUTPUT);    //GPIO16 is an OUTPUT pin;
    digitalWrite(LED_PIN, HIGH); //Initial state is ON

    // read the html code to html_homes
    prepareFile();

    WiFi.softAP("Cannon_wifi", "00000000");
    IPAddress myIP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(myIP);

    // start webSocket server
    webSocket.begin();
    webSocket.onEvent(webSocketEvent);

    if(MDNS.begin("esp8266")) {
        Serial.println("MDNS responder started");
    }

    // handle index
    //server.on("/", handleResponse);
    server.on("/", []() {
        // send home.html
        server.send(200, "text/html", html_home);
    });

    server.on("/style.css", []() {
        // send home.html
        server.send(200, "text/css", css_code);
    });



    server.begin();

    // Add service to MDNS
    MDNS.addService("http", "tcp", 80);
    MDNS.addService("ws", "tcp", 81);

    Serial.printf("Server Start\n");

}

void loop() {
    webSocket.loop();
    server.handleClient();
}


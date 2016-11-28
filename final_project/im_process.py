import cv2
import numpy as np
import math

# parameter
SIZE = 2048
THRESHOLD = 40

BLUE = [255, 0, 0]
GREEN = [0, 255, 0]
RED = [0, 0 ,255]

file_id = '0126'

up_arr = [0] * SIZE
down_arr = [0] * SIZE


# input is the gray scale of array with size SIZE=2048
def strip_analysis(img_array):
	first = 0
	last = 0

	DETECTED_FLAG = False

	for x in range(SIZE):
		if(img_array[x] > THRESHOLD):
			if(not DETECTED_FLAG):
				first = x
				DETECTED_FLAG = True

			else:
				last = x

	return [first, last]






print("   - load image ...")
img = cv2.imread('ori_image/Frames' + file_id + '.jpg', cv2.IMREAD_GRAYSCALE)

# main
## first step analysis
print("   - first step analysis ...")

for y in range(SIZE):
	[up_arr[y], down_arr[y]] = strip_analysis(img[:, y])



## find mean square line
## x = ay + b
print("   - find mean square line for upper and lower data points...")

sum_1 = 0
sum_x = 0
sum_y = 0
sum_xy = 0
sum_y_2 = 0

for y in range(SIZE):
	x = up_arr[y]
	if(x!=0):
		sum_1 = sum_1 +1
		sum_x = sum_x + x
		sum_y = sum_y + y
		sum_xy = sum_xy + x*y
		sum_y_2 = sum_y_2 + y*y


a_up = float(sum_1*sum_xy - sum_x * sum_y) / (sum_1 * sum_y_2 - sum_y*sum_y)
b_up = float(sum_x - a_up*sum_y) / sum_1
y_up_avg = float(sum_y) / sum_1


#print("a_up = " + str(a_up))



sum_1 = 0
sum_y = 0

for y in range(SIZE):
	x = up_arr[y]
	if(x!=0):
		if(x > a_up*y + b_up):
			sum_1 = sum_1 + 1
			sum_y = sum_y + y


up_mid_y = float(sum_y) / sum_1
up_mid_x = up_mid_y * a_up + b_up


###################

sum_1 = 0
sum_x = 0
sum_y = 0
sum_xy = 0
sum_y_2 = 0

for y in range(SIZE):
	x = down_arr[y]
	if(x!=0):
		sum_1 = sum_1 +1
		sum_x = sum_x + x
		sum_y = sum_y + y
		sum_xy = sum_xy + x*y
		sum_y_2 = sum_y_2 + y*y


a_down = float(sum_1*sum_xy - sum_x * sum_y) / (sum_1 * sum_y_2 - sum_y*sum_y)
b_down = float(sum_x - a_down*sum_y) / sum_1
y_down_avg = float(sum_y) / sum_1

#print("a_down = " + str(a_down))



sum_1 = 0
sum_y = 0

for y in range(SIZE):
	x = down_arr[y]
	if(x!=0):
		if(x < a_down*y + b_down):
			sum_1 = sum_1 + 1
			sum_y = sum_y + y


down_mid_y = float(sum_y) / sum_1
down_mid_x = down_mid_y * a_down + b_down



mid_y = int(0.5*(up_mid_y + down_mid_y))
mid_x = int(0.5*(up_mid_x + down_mid_x))


## find vertical line
print("   - find perpendicular line ...")


a = 0.5 * (a_up + a_down)
b = mid_x - mid_y * a
a_perp = (-1) / a
b_perp = mid_x - mid_y * a_perp

sum_of_width_around_mid_y = sum(down_arr[mid_y-2: mid_y+3])-sum(up_arr[mid_y-2: mid_y+3])
output_width = math.sqrt(1+a_perp*a_perp)*sum_of_width_around_mid_y/(5*a_perp)



# compute the width
print("   - compute the width ...")
print("       " + "mid_y = " + str(mid_y))
print("       " + "width = " + str(output_width))

# preparing output file
print("   - write output file ...")

img = cv2.imread('ori_image/Frames' + file_id + '.jpg', cv2.IMREAD_COLOR)

for y in range(SIZE):
	x = down_arr[y]
	if(not x==0):
		img[x, y] = RED
		img[int(a*y+b), y] = RED
		img[up_arr[y], y] = BLUE
		img[down_arr[y], y] = BLUE


for x in range(SIZE):
	img[x, int(a*(b_perp-x))] = GREEN

cv2.imwrite('out_image/Frames' + file_id + '.jpg',img)

#cv2.imshow('image',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

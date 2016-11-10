import cv2
import numpy as np
import math

# parameter
SIZE = 2048
THRESHOLD = 40

BLUE = [255, 0, 0]
GREEN = [0, 255, 0]
RED = [0, 0 ,255]

file_id = '0013'


width_arr = [0] * SIZE
center_arr = [0] * SIZE
inten_arr = [0] * SIZE


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

	return [int((first+last)/2), last-first]






print("   - load image ...")
img = cv2.imread('ori_image/Frames' + file_id + '.jpg', cv2.IMREAD_GRAYSCALE)

# main
## first step analysis
print("   - first step analysis ...")

for y in range(SIZE):
	[center_arr[y], width_arr[y]] = strip_analysis(img[:, y])
	#print([center_arr[x], width_arr[x]])



## find mean square line
print("   - find mean square line ...")

sum_1 = 0
sum_x = 0
sum_y = 0
sum_xy = 0
sum_y_2 = 0

for y in range(SIZE):
	x = center_arr[y]
	if(x!=0):
		sum_1 = sum_1 +1
		sum_x = sum_x + x
		sum_y = sum_y + y
		sum_xy = sum_xy + x*y
		sum_y_2 = sum_y_2 + y*y


a = float(sum_1*sum_xy - sum_x * sum_y) / (sum_1 * sum_y_2 - sum_y*sum_y)
b = float(sum_x - a*sum_y) / sum_1



## find vertical line
print("   - find perpendicular line ...")

#min_id = SIZE
#min_width = SIZE


for y in range(SIZE):
	if(width_arr[y]!=0):
		cut_arr = 0
		initial = center_arr[y] - int(0.5*width_arr[y])

		for x in range(initial, initial+width_arr[y]):
			cut_arr += min(img[x, y], 60)
		inten_arr[y] = cut_arr / float(width_arr[y])


max_id = 0
max_intensity = 0

for y in range(20, SIZE-20):
	if(center_arr[y]!=0):
		intensity = sum(inten_arr[y-19:y+19])
		if(intensity > max_intensity):
			max_id = y
			max_intensity = intensity
			#min_width = width_arr[y] #width

a_perp = (-1) / a
b_perp = center_arr[max_id] - max_id * a_perp



# compute the width
print("   - compute the width ...")
print("       " + str(math.sqrt(1+a_perp*a_perp)*sum(width_arr[max_id-3: max_id+2])/(5*a_perp)  ))

# preparing output file
print("   - write output file ...")

img = cv2.imread('ori_image/Frames' + file_id + '.jpg', cv2.IMREAD_COLOR)

for y in range(SIZE):
	x = center_arr[y]
	if(not x==0):
		img[x, y] = RED
		img[int(a*y+b), y] = RED
		img[x + int(0.5*width_arr[y]), y] = BLUE
		img[x - int(0.5*width_arr[y]), y] = BLUE


for x in range(SIZE):
	img[x, int(a*(b_perp-x))] = GREEN

cv2.imwrite('out_image/Frames' + file_id + '.jpg',img)

#cv2.imshow('image',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

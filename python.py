import cv2
import time
import numpy

four_cc = cv2.VideoWriter_fourcc(*"XVID")
output_file = cv2.VideoWriter("output.avi", four_cc, 20.0, (640, 480))
cap = cv2.VideoCapture(0)

time.sleep(2)
bg = 0

for i in range(60):
    ret, bg = cap.read()

bg = numpy.flip(bg, axis=1)

while cap.isOpened():
    ret, img = cap.read()

    if not ret:
        break

    img = numpy.flip(img, axis=1)

    # hsv - heu saturation value
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = numpy.array([0, 120, 50])
    upper_red = numpy.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = numpy.array([170, 120, 70])
    upper_red = numpy.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN,
                             numpy.ones((3, 3), numpy.uint8))

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE,
                             numpy.ones((3, 3), numpy.uint8))

    mask2 = cv2.bitwise_not(mask1)

    res1 = cv2.bitwise_and(img, img, mask=mask2)
    res2 = cv2.bitwise_and(bg, bg, mask=mask1)

    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    output_file.write(final_output)

    cv2.imshow("Magic", final_output)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()

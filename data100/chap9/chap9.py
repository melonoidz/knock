# pip3 install -U pip
# python3 -m pip install opencv-contrib-python
import cv2

# 81 read img
img = cv2.imread("img/img01.jpg")
height, width = img.shape[:2]
# print(str(width))
# print(height)
# cv2.imshow("img", img)
# cv2.waitKey(0)
# cv2.imwrite("test.png", img)

# 82 read avi
cap = cv2.VideoCapture("mov/mov01.avi")
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
# print(width)
# print(count)
# print(fps)

# 83 divide avi into jpg
num = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        filepath = "snapshot/snapshot_"+str(num)+".jpg"
        cv2.imwrite(filepath, frame)
        if cv2.waitKey(1):
            break
    num += 1
cap.release()

# 84 HOG
hog = cv2.HOGDescriptor()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray.png", gray)

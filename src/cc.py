import cv2
from services.index.pdfium import pdfium_wrapper

# Loading the image
img = cv2.imread(r"C:\Users\admin\Desktop\test_img3.png")
# img = pdfium_wrapper.render_page_to_numpy(r"E:\LUU NHAN VIEN CU\DK4- DIEU\C&K METAL PRESSING\120CKC\120CKC-CN.PDF", 0)
#D:\DK4- DIEU\2016\base_test_img.JPG C:\Users\admin\Desktop\test_img2.png

# preprocess the image
gray_img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

# Applying threshold
threshold = cv2.threshold(gray_img, 150, 255,
    cv2.THRESH_BINARY_INV)[1] 

# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# grouped = cv2.dilate(threshold, kernel, iterations=1)

# Apply the Component analysis function
analysis = cv2.connectedComponentsWithStats(threshold,
                                            4,
                                            cv2.CV_32S)
(totalLabels, label_ids, values, centroid) = analysis

vis = img.copy()
count = 0
for i in range(1, totalLabels):
    x, y, w, h, area = values[i]

    if h >= 35 and w >= 35:
        count += 1
        cv2.rectangle(
            vis,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            2
        )
print(count)
cv2.imshow("Detected Objects", vis)
cv2.waitKey(0)
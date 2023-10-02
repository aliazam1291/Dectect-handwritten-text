import cv2
import pytesseract

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# Load the image
# Replace with the actual path to your image
image = cv2.imread("C:\Image1.jpg")

# Preprocess the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
gray = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel, iterations=1)

# Perform text detection using contour detection
contours, _ = cv2.findContours(
    gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Recognize text using Tesseract OCR for each detected contour
roi_texts = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    roi = gray[y:y + h, x:x + w]
    roi_text = pytesseract.image_to_string(roi, config='--psm 6', lang='eng')
    print(roi_text)
    roi_texts.append((roi_text, (x, y, w, h)))

# Sort ROIs from left to right based on their x-coordinate
roi_texts = sorted(roi_texts, key=lambda x: x[1][0])

# Combine the recognized text from all ROIs
combined_text = ' '.join([roi_text[0] for roi_text in roi_texts])
# Save the combined recognized text to a text file
output_file = "output.txt"
with open(output_file, "w") as file:
    file.write(combined_text)

print("Text saved to", output_file)

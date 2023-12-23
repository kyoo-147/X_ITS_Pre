import cv2

# Mở ba camera
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
cap3 = cv2.VideoCapture(2)

while True:
    # Đọc khung từ ba camera
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()

    # Hiển thị video từ ba camera
    cv2.imshow('Camera 1', frame1)
    cv2.imshow('Camera 2', frame2)
    cv2.imshow('Camera 3', frame3)

    # Kiểm tra phím nhấn để thoát (ấn 'q' để thoát)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng camera và đóng cửa sổ
cap1.release()
cap2.release()
cap3.release()
cv2.destroyAllWindows()

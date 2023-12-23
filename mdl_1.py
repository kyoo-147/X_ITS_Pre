# Nhập thư viện cần thiết
import cv2

# Khởi tạo biến chuột để tạo vùng ROI tùy chỉnh
drawing = False
point1 = ()
point2 = ()

drawingTwo = False
pointTwo_1 = ()
pointTwo_2 = ()
Mouse_count = False

congestion_status_ROI1 = ""
congestion_status_ROI2 = ""

# Hàm vẽ vùng ROI tùy chỉnh
def mouse_drawing(event, x, y, flags, params):
    global point1, point2, drawing
    global pointTwo_1, pointTwo_2, drawingTwo, Mouse_count

    # Chuột 1
    if Mouse_count == False:
        if event == cv2.EVENT_LBUTTONDOWN:
            if drawing is False:
                drawing = True
                point1 = (x, y)

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing is True:
                point2 = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            Mouse_count = True
            
    # Chuột 2
    if Mouse_count == True:
        if event == cv2.EVENT_LBUTTONDOWN:
            if drawingTwo is False:
                drawingTwo = True
                pointTwo_1 = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawingTwo is True:
                pointTwo_2 = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            if drawingTwo is True:
                drawingTwo = False
                Mouse_count = False

# Đọc dữ liệu từ camera hoặc video file
cap = cv2.VideoCapture('./test_vid/2.mp4')

# Tên của sổ cần thiết
cv2.namedWindow("ITS")
cv2.setMouseCallback("ITS", mouse_drawing)


while True:
    ret, frame = cap.read()

    if not ret:
        break  # Thoát khỏi vòng lặp nếu không đọc được khung hình

    car_cascade = cv2.CascadeClassifier('cars.xml')

    # Vùng quan tâm 1
    if point1 and point2:
        # Kiểm tra xem có thể cắt vùng quan tâm từ khung hình hay không
        if frame is not None:
            # Khởi tạo hình vuông 1
            r = cv2.rectangle(frame, point1, point2, (100, 100, 200), 2)
            frame_ROI = frame[point1[1]:point2[1], point1[0]:point2[0]]

            # Nhận diện xe trong vùng quan tâm 1
            if drawing is False:
                # Chuyển đổi video sang khung màu xám của mỗi khung hình 1
                ROI_grayscale = cv2.cvtColor(frame_ROI, cv2.COLOR_BGR2GRAY)
                # Nhận diện xe trong video 1
                cars_ROI = car_cascade.detectMultiScale(ROI_grayscale, 1.1, 3)

                # Kiểm tra xem có xe nào được phát hiện hay không
                if len(cars_ROI) > 0:
                    # Vẽ hộp giới hạn cho mỗi xe trong vùng 1
                    for (x, y, w, h) in cars_ROI:
                        cv2.rectangle(frame_ROI, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame_ROI, "Number of vehicles: " + str(len(cars_ROI)), (10, frame_ROI.shape[0] - 25), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 255, 0), 1)

                    num_cars_ROI1 = len(cars_ROI)
                    if num_cars_ROI1 >= 10:
                        congestion_status_ROI1 = "Street is Congested"
                    else:
                        congestion_status_ROI1 = "Street is not Congested"
                    cv2.putText(frame, f"Zone 1: {congestion_status_ROI1}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    # Nếu không có xe nào được phát hiện
                    num_cars_ROI1 = 0

    # Vùng quan tâm 2
    if pointTwo_1 and pointTwo_2:
        # Kiểm tra xem có thể cắt vùng quan tâm từ khung hình hay không
        if frame is not None:
            # Khởi tạo hình vuông 2
            r2 = cv2.rectangle(frame, pointTwo_1, pointTwo_2, (0, 255, 255), 2)
            frameTWO_ROI = frame[pointTwo_1[1]:pointTwo_2[1], pointTwo_1[0]:pointTwo_2[0]]

            # Nhận diện xe trong vùng quan tâm 2
            if drawingTwo is False:
                # Chuyển đổi video sang khung màu xám của mỗi khung hình 2
                frame_grayscale = cv2.cvtColor(frameTWO_ROI, cv2.COLOR_BGR2GRAY)
                # Nhận diện xe trong video 2
                carsTwo_ROI = car_cascade.detectMultiScale(frame_grayscale, 1.1, 3)

                # Kiểm tra xem có xe nào được phát hiện hay không
                if len(carsTwo_ROI) > 0:
                    # Vẽ hộp giới hạn cho mỗi xe trong vùng 2
                    for (x, y, w, h) in carsTwo_ROI:
                        cv2.rectangle(frameTWO_ROI, (x, y), (x+w, y+h), (255, 255, 100), 2)
                        cv2.putText(frameTWO_ROI, "Number of vehicles: " + str(len(carsTwo_ROI)), (10, frameTWO_ROI.shape[0] - 25), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 100), 1)

                    num_cars_ROI2 = len(carsTwo_ROI)
                    if num_cars_ROI2 >= 10:
                        congestion_status_ROI2 = "Street is Congested"
                    else:
                        congestion_status_ROI2 = "Street is not Congested"
                    cv2.putText(frame, f"Zone 2: {congestion_status_ROI2}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    # Nếu không có xe nào được phát hiện
                    num_cars_ROI2 = 0

    cv2.imshow("ITS", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

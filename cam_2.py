import cv2
import time
import sys

class TrafficMonitoring:
    def __init__(self, video_path, window_name="ITS"):
        self.video_path = video_path
        self.window_name = window_name
        self.cap = cv2.VideoCapture(video_path)

        self.cap = cv2.VideoCapture(4)
    
        self.drawing = False
        self.point1 = ()
        self.point2 = ()

        self.drawing_two = False
        self.point_two_1 = ()
        self.point_two_2 = ()
        self.mouse_count = False

        self.congestion_status_roi1 = ""
        self.congestion_status_roi2 = ""

        self.car_cascade = cv2.CascadeClassifier('cars.xml')
        
        self.start_time = time.time()
        self.frame_count = 0

        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_drawing)

    def mouse_drawing(self, event, x, y, flags, params):
        if not self.mouse_count:
            if event == cv2.EVENT_LBUTTONDOWN:
                if not self.drawing:
                    self.drawing = True
                    self.point1 = (x, y)
            elif event == cv2.EVENT_MOUSEMOVE:
                if self.drawing:
                    self.point2 = (x, y)
            elif event == cv2.EVENT_LBUTTONUP:
                self.drawing = False
                self.mouse_count = True

        if self.mouse_count:
            if event == cv2.EVENT_LBUTTONDOWN:
                if not self.drawing_two:
                    self.drawing_two = True
                    self.point_two_1 = (x, y)
            elif event == cv2.EVENT_MOUSEMOVE:
                if self.drawing_two:
                    self.point_two_2 = (x, y)
            elif event == cv2.EVENT_LBUTTONUP:
                if self.drawing_two:
                    self.drawing_two = False
                    self.mouse_count = False

    def process_frame(self, frame):
        self.process_zone1(frame)
        self.process_zone2(frame)

    def process_zone1(self, frame):
        color = (100, 100, 200)  # Màu mặc định cho Zone 1
        car_color = (0, 255, 0)  # Màu khi nhận diện xe trong Zone 1
        self.process_zone(frame, self.point1, self.point2, self.congestion_status_roi1, zone_name="Zone 1", position=(10, 50), color=color, car_color=car_color)

    def process_zone2(self, frame):
        color = (0, 255, 255)  # Màu mặc định cho Zone 2
        car_color = (255, 255, 100)  # Màu khi nhận diện xe trong Zone 2
        self.process_zone(frame, self.point_two_1, self.point_two_2, self.congestion_status_roi2, zone_name="Zone 2", position=(10, 80), color=color, car_color=car_color)

    def process_zone(self, frame, point1, point2, congestion_status_roi, zone_name, position, color=None, car_color=None):
        if point1 and point2:
            if color is None:
                # Lấy màu từ ảnh gốc tại vị trí bounding box
                color = frame[int(point1[1]):int(point1[1] + 1), int(point1[0]):int(point1[0] + 1)].mean(axis=0).mean(axis=0)

            r = cv2.rectangle(frame, point1, point2, tuple(map(int, color)), 2)
            frame_roi = frame[point1[1]:point2[1], point1[0]:point2[0]]

            roi_grayscale = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2GRAY)
            cars_roi = self.car_cascade.detectMultiScale(roi_grayscale, 1.1, 3)

            if len(cars_roi) > 0:
                for (x, y, w, h) in cars_roi:
                    cv2.rectangle(frame_roi, (x, y), (x+w, y+h), car_color, 2)
                    cv2.putText(frame_roi, "Number of vehicles: " + str(len(cars_roi)),
                                (10, frame_roi.shape[0] - 25), cv2.FONT_HERSHEY_TRIPLEX, 0.5, car_color, 1)

                num_cars_roi = len(cars_roi)
                congestion_status_roi = "Street is Congested" if num_cars_roi >= 10 else "Street is not Congested"
                
                if 5 <= num_cars_roi <= 10:
                    congestion_status_roi = "Potential Congestion"
                elif num_cars_roi > 10:
                    congestion_status_roi = "Street is Congested"
                else:
                    congestion_status_roi = "Street is not Congested"
                
                cv2.putText(frame, f"{zone_name}: {congestion_status_roi}", position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                num_cars_roi = 0
                
    

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.process_frame(frame)

            

            self.frame_count += 1
            elapsed_time = time.time() - self.start_time
            fps = self.frame_count / elapsed_time

            cv2.putText(frame, f"FPS: {fps:.2f}", (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.imshow(self.window_name, frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python3 test_oop.py video_path")
#     else:
#         video_path = sys.argv[1]
#         traffic_monitoring = TrafficMonitoring(video_path)
#         traffic_monitoring.run()


if __name__ == "__main__":
    video_path = './test_vid/2.mp4'
    traffic_monitoring = TrafficMonitoring(video_path)
    traffic_monitoring.run()

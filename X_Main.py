import subprocess

if __name__ == "__main__":
    # Đường dẫn đến 4 chương trình của bạn
    program_paths = ["cam_0.py", "cam_1.py"]

    # Danh sách để lưu trữ các tiến trình
    processes = []

    # Bắt đầu mỗi chương trình trong một tiến trình riêng biệt
    for program_path in program_paths:
        process = subprocess.Popen(["python3", program_path])
        processes.append(process)

    try:
        # Chờ cho tất cả các tiến trình hoàn thành
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        # Ngắt chương trình nếu có sự kiện ngắt từ bàn phím (Ctrl+C)
        for process in processes:
            process.terminate()



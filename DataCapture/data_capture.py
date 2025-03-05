import cv2
import os
import time
import threading


def capture_data(source=0, save_path=None):
    """
    Capture data from a source.
    :param source: Video source (0 for webcam, file path for video file).
    :param save_path: Path to save the captured video (optional).
    """
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Error: Unable to access the source.")
        return

    # Optional: Video saving
    out = None
    if save_path:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(save_path, fourcc, 20.0, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Captured Data', frame)
        if out:
            out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()


def capture_from_camera(camera_index, save_path, duration=5):
    """
    Capture video from a specific camera and save to file.
    :param camera_index: Index of the camera (e.g., 0, 1, 2, ...).
    :param save_path: Path to save the video file.
    :param duration: Duration to capture in seconds.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Unable to access camera {camera_index}")
        return

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(save_path, fourcc, 20.0, (640, 480))

    start_time = time.time()
    print(f"Camera {camera_index} started capturing...")
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            print(f"Camera {camera_index} disconnected.")
            break
        out.write(frame)
        cv2.imshow(f'Camera {camera_index}', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Allow early exit
            break

    cap.release()
    out.release()
    cv2.destroyWindow(f'Camera {camera_index}')
    print(f"Camera {camera_index} video saved to {save_path}")

# Start threads for multiple cameras
def capture_from_multiple_cameras(camera_indices, save_paths, duration=5):
    threads = []
    for i, camera_index in enumerate(camera_indices):
        thread = threading.Thread(target=capture_from_camera, args=(camera_index, save_paths[i], duration))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    print("All cameras have finished capturing.")

# Example: Capture from two cameras (index 0 and 1)
camera_indices = [0, 1]  # Adjust indices based on your setup
save_paths = ["camera_0_output.avi", "camera_1_output.avi"]
capture_from_multiple_cameras(camera_indices, save_paths, duration=10)


# 下为测试部分
def test_camera_capture():
    try:
        capture_data(source=0)  # 默认摄像头
        print("Camera capture test passed.")
    except Exception as e:
        print(f"Camera capture test failed: {e}")


def test_video_file_reading():
    try:
        capture_data(source="1.mp4")  # 替换为实际视频文件路径
        print("Video file reading test passed.")
    except Exception as e:
        print(f"Video file reading test failed: {e}")


def test_video_saving():
    try:
        capture_data(source=0, save_path="output_test.avi")
        print("Video saving test passed. Check the 'output_test.avi' file.")
    except Exception as e:
        print(f"Video saving test failed: {e}")


def test_integrated_capture_and_save():
    try:
        print("Starting integrated test for capturing and saving...")
        capture_data(source=0, save_path="integrated_output.avi")
        print("Integrated test passed. Check the 'integrated_output.avi' file.")
    except Exception as e:
        print(f"Integrated test failed: {e}")


def test_frame_rate(video_path="integrated_output.avi", expected_fps=20):
    """
    Test if the video file has the correct frame rate.
    :param video_path: Path to the video file.
    :param expected_fps: Expected frames per second.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    assert abs(fps - expected_fps) < 1e-3, f"Frame rate test failed. Expected: {expected_fps}, Got: {fps}"
    print(f"Frame rate test passed. FPS: {fps}")


def test_resolution(video_path="output_test.avi", expected_width=640, expected_height=480):
    """
    Test if the video file has the correct resolution.
    :param video_path: Path to the video file.
    :param expected_width: Expected width of the video.
    :param expected_height: Expected height of the video.
    """
    assert os.path.exists(video_path), f"File not found: {video_path}"
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    assert width == expected_width and height == expected_height, (
        f"Resolution test failed. Expected: {expected_width}x{expected_height}, Got: {width}x{height}"
    )
    print(f"Resolution test passed. Resolution: {width}x{height}")


def run_all_tests():
    print("Running all tests...")
    test_camera_capture()
    test_video_file_reading()
    test_video_saving()
    test_integrated_capture_and_save()
    test_frame_rate("integrated_output.avi", expected_fps=20)
    test_resolution("integrated_output.avi", expected_width=640, expected_height=480)
    print("All tests completed.")


if __name__ == "__main__":
    run_all_tests()

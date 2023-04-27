import cv2

# ���ǰ10���豸�ļ������Ը�����Ҫ���ķ�Χ
max_devices = 10

for device_id in range(max_devices):
    device_path = f'/dev/video{device_id}'
    cap = cv2.VideoCapture(device_path)

    if cap.isOpened():
        print(f"Device {device_path} is available.")
        cap.release()
    else:
        print(f"Device {device_path} is not available.")
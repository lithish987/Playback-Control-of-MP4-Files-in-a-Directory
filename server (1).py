import socket
import cv2
import numpy as np
import os
import glob

UDP_PORT = 50001
VIDEO_DIR = r'C:\Users\lenovo\Documents\MPCA\videos'
CHUNK_SIZE = 65535

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', UDP_PORT))

while True:
    print('waiting for instruction')
    data, addr = sock.recvfrom(1024)
    if data.decode() == "CONNECT":
        video_files = glob.glob('./*.mp4')
        video_list = []
        for v in video_files:
            a = v.split('\\')[1]
            video_list.append(a)
        sock.sendto('\n'.join(video_list).encode(), addr)
        print('Video list sent')
        data, addr = sock.recvfrom(1024)
        video_name = data.decode()
        if video_name == 'q':
            continue

        else:
            video_path = os.path.join(VIDEO_DIR, video_name)
            if os.path.exists(video_path):
                cap = cv2.VideoCapture(video_name)
                while(cap.isOpened()):
                    ret, frame = cap.read()
                    if ret:
                        frame = cv2.resize(frame, (250, 250))
                        # encode the frame
                        encoded_frame, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                        # convert buffer to bytes
                        data = buffer.tobytes()
                        # send the data in chunks
                        for i in range(0, len(data), CHUNK_SIZE):
                            chunk = data[i:i+CHUNK_SIZE]
                            sock.sendto(chunk, addr)
                    else:
                        break
                cap.release()
            else:
                print('Video not found:', video_path)
sock.close()

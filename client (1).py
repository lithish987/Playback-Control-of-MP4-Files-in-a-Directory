import socket
import cv2
import numpy as np
import sys

UDP_IP = '192.168.13.1'
UDP_PORT = 50001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto('CONNECT'.encode(), (UDP_IP, UDP_PORT))

print('Fetching video list...')
data, addr = sock.recvfrom(1024)
video_list = data.decode().split('\n')
print('Available videos:')
for video in video_list:
    print(video)

while True:
    video_name = input('Enter video name (or q to quit): ')
    if video_name == 'q':
        print('Exiting...')
        sock.sendto(video_name.encode(), (UDP_IP, UDP_PORT))
        sys.exit()
    elif video_name not in video_list:
        print('Video not found:', video_name)
        continue

    sock.sendto(video_name.encode(), (UDP_IP, UDP_PORT))

    while True:
        try:
            data, addr = sock.recvfrom(1<<17) #max limit of bytes received from call

            if len(data) == 0:
                printf('Empty video')
        
            nparr = np.frombuffer(data, np.uint8)# convert the bytes to numpy array
            
            vid = cv2.imdecode(nparr, cv2.IMREAD_COLOR)# decode the numpy array to image
            
            cv2.imshow('Received',vid)# show the image
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                sock.close()
                cv2.destroyAllWindows()
                
            if cv2.waitKey(1) & 0xFF == ord('p'):
                cv2.waitKey(-1) #wait until any key is pressed

        except:
                print('Done playing :', video_name)
                cv2.destroyAllWindows()
                break

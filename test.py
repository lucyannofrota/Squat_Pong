import cv2

addr = 'https://192.168.1.118:8080/video'

cap = cv2.VideoCapture(addr)

while(1):
    ret, frame = cap.read()
    
    cv2.imshow('VIDEO', frame)
    if cv2.waitKey(1) == 27:
        break
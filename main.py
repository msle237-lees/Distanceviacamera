import numpy as np
import cv2

cap = cv2.VideoCapture(0)

cx_data = []
cy_data = []
Z = 76.2

def fpointcal(cx_data, cy_data):
    fx = ((sum(cx_data) / len(cx_data)) * Z) / (8.26)
    fy = ((sum(cy_data) / len(cy_data)) * Z) / (13.97)

    print(fx)
    print(fy)

    return fx, fy

def distance(fx, fy, cx_data, cy_data, object_dim_x, object_dim_y):
    Zx = (cx_data / object_dim_x) * fx
    Zy = (cy_data / object_dim_y) * fy

    print(Zx)
    print(Zy)

    return Zx, Zy

while(True):
    ret, frame = cap.read()

    buf1 = cv2.flip(frame, 1)
    buf2 = cv2.resize(buf1, (1280, 720))
    buf3 = cv2.GaussianBlur(buf2, (5, 5), 0)
    buf4 = cv2.cvtColor(buf3, cv2.COLOR_BGR2GRAY)
    buf5 = cv2.adaptiveThreshold(buf4, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, hierarchy = cv2.findContours(buf5, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        M = cv2.moments(cnt)
        if M['m00'] is None or M['m00'] == 0:
            cx = 1
            cy = 1
        else:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
        print(cx, cy)
        cx_data.append(cx)
        cy_data.append(cy)
    cv2.imshow('buf5', buf5)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        fpointcal(cx_data, cy_data)
        break

cap.release()
cv2.destroyAllWindows()

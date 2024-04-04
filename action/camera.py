import cv2
import matplotlib as plt

cap=cv2.VideoCapture(1, cv2.CAP_DSHOW) 

while True:
    ret,frame=cap.read()


    cv2.imshow("window",frame)
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
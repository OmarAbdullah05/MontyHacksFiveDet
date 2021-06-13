import cv2
import numpy as np
import math
import time
import smtplib
from twilio.rest import Client
cap = cv2.VideoCapture(0)

count = 0
count1 =0
slope=0
slope1 = 100
minArea = 120*100
radianToDegree=57.324
minimumLengthOfLine=150.0
minAngle=18
maxAngle=72
list_falls=[]
count_fall=0
firstFrame= None

time.sleep(1)

def convertFrame(frame):
    r = 750.0 / frame.shape[1]
    dim = (750, int(frame.shape[0] * r))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31,31),0)

    return frame,gray

def email():
    sender_email = "omar.ghanima06@gmail.com"
    rec_email = "omar.ahmedaf@gmail.com"
    password = "Passcode618"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("omar.ghanima06@gmail.com", password)
    print("It logged in")
    SUBJECT = "Emergency!"
    TEXT="One of your loved ones has collapsed, this may be due to a stroke or a heart-related issue. Medical assistance is on the way. Visit Orli, and use the password: obomt63 to track your loved one."
    server.sendmail(sender_email, rec_email, 'Subject: {}\n\n{}'.format(SUBJECT, TEXT))
    server.quit()
    print("Email has been sent to ", rec_email)

def texting():
    account_sid = "AC4c12692fe7d2052d6f9e2438483f5de0"
    auth_token  = "1b8883cda788b896061c839a6df84b3f"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+16096138831",
        from_= "+17039911570",
        body="This is the Hackathon Project AI. A medical emergency has been detected, please send help immediately")
    
    print(message.sid)
det = True
while det:

    ret,frame= cap.read()
    if frame is None:
        break
    frame,gray = convertFrame(frame);

    if firstFrame is None:
        time.sleep(1.0)
        _,frame= cap.read()
        frame,gray=convertFrame(frame)
        firstFrame = gray
        continue

    frameDelta= cv2.absdiff(firstFrame,gray)
    thresh1 = cv2.threshold(frameDelta,20,255,cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh1,None,iterations = 15)

    contour,_ = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for con in contour:

        if len(con)>=5 and cv2.contourArea(con)>minArea:
            ellipse = cv2.fitEllipse(con)
            cv2.ellipse(frame,ellipse,(255,255,0),5)

            extTop = tuple(con[con[:, :, 1].argmin()][0])
            extBot = tuple(con[con[:, :, 1].argmax()][0])
            extLeft = tuple(con[con[:, :, 0].argmin()][0])
            extRight = tuple(con[con[:, :, 0].argmax()][0])

            line1 = math.sqrt((extTop[0]-extBot[0])*(extTop[0]-extBot[0])+(extTop[1]-extBot[1])*(extTop[1]-extBot[1]))
            midPoint = [extTop[0]-int((extTop[0]-extBot[0])/2),extTop[1]-int((extTop[1]-extBot[1])/2)]
            if line1>minimumLengthOfLine:
                if (extTop[0]!=extBot[0]):
                    slope = abs(extTop[1]-extBot[1])/(extTop[0]-extBot[0])

            else:
                if (extRight[0] != extLeft[0]):
                    slope = abs(extRight[1]-extLeft[1])/(extRight[0]-extLeft[0])

            originalAngleP = np.arctan((slope1 - slope) / (1 + slope1 * slope))
            originalAngleH = np.arctan(slope)
            originalAngleH = originalAngleH*radianToDegree
            originalAngleP=originalAngleP*radianToDegree
            if (abs(originalAngleP) > minAngle and abs(originalAngleH) < maxAngle and abs(originalAngleP)+abs(originalAngleH)>89 and abs(originalAngleP)+abs(originalAngleH)<91):
                count += 1
                if (count > 16):
                    count_fall+=1
                    list_falls.append((time.time()))
                    if(count_fall>1):
                        if(list_falls[len(list_falls)-1]-list_falls[len(list_falls)-2]<.5):
                            print ("Fall detected")
                            email()
                            texting()
                            time.sleep(2)
                            det = False
                            break
                        else:
                            continue

                    count = 0

    cv2.imshow('Frame', frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.waitKey(1)
cv2.destroyAllWindows()

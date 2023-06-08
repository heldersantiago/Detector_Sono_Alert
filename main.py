import cv2
import cvzone
import time
import serial
from cvzone.FaceMeshModule import FaceMeshDetector

# COMxx   format on Windows
#SerialObj = serial.Serial('COM8')

#SerialObj.baudrate = 9600  # set Baud rate to 9600
#SerialObj.bytesize = 8  # Number of data bits = 8
#SerialObj.parity = 'N'  # No parity
#SerialObj.stopbits = 1  # Number of Stop bits = 1

detector = FaceMeshDetector(maxFaces=1)

cap = cv2.VideoCapture(0)

idList = [23, 159, 386, 23]

ratioList1 = []
ratioList2 = []

previousTime = 0;

# O tempo que demora para determinar se esta dormindo ou não.
intervalo = 5

avgAnterior = 0
ratioAvgTotal = 0

while True:
    _, img = cap.read()

    img, faces = detector.findFaceMesh(img, draw=False)

    currentTime = int(time.process_time())

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 2, (255, 0, 255), cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]

        RightUp = face[257]
        RightDown = face[253]
        RightLeft = face[463]
        RightRight = face[359]

        lenghtVer1, _ = detector.findDistance(leftUp, leftDown)
        lenghtHor1, _ = detector.findDistance(leftLeft, leftRight)

        lenghtVer2, _ = detector.findDistance(RightUp, RightDown)
        lenghtHor2, _ = detector.findDistance(RightLeft, RightRight)

        cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)

        cv2.line(img, RightUp, RightDown, (0, 200, 0), 3)

        ratio1 = int((lenghtVer1 / lenghtHor1 * 100))
        ratio2 = int((lenghtVer2 / lenghtHor2 * 100))

        ratioList1.append(ratio1)
        ratioList2.append(ratio2)

        if len(ratioList1) > 10:
            ratioList1.pop(0)

        if len(ratioList2) > 10:
            ratioList2.pop(0)

        ratioAvg1 = sum(ratioList1) / len(ratioList1)
        ratioAvg2 = sum(ratioList2) / len(ratioList2)
        # print(f"Ratio1: {ratioAvg1} Ratio2: {ratioAvg2}")

        ratioAvgTotal = (ratioAvg1 + ratioAvg2) / 2
        print(ratioAvgTotal)

        # Executa quando fecha o olho.

        if ratioAvgTotal < 40:
            tempo = currentTime - previousTime

            cvzone.putTextRect(img, f"Tempo: {tempo}", (100, 100))

            if currentTime - previousTime >= intervalo:
                previousTime = currentTime
                # print(currentTime)
                print('Dormindo')
                #SerialObj.write(b'd')
            #else:
                #SerialObj.write(b'a')
        else:
            previousTime = currentTime

    else:
        cvzone.putTextRect(img, f"Sem Rostos detetados", (100, 100))

    cv2.imshow('Frame', img)
    cv2.waitKey(1)

#SerialObj.close()
cv2.destroyAllWindows()

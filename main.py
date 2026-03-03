import cv2
import numpy as np
import mediapipe as mp
import time
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)

canvas = np.zeros((480,640,3),dtype=np.uint8)

colors=[(255,0,255),(255,0,0),(0,255,0),(0,255,255)]
colorIndex=0
brushThickness=3

prev_x,prev_y=0,0

undo_stack=[]

def fingers_up(lm):
    tips=[8,12,16,20]
    fingers=[]
    for t in tips:
        fingers.append(lm[t].y<lm[t-2].y)
    return fingers

while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    h,w,c=img.shape

    # UI BAR
    cv2.rectangle(img,(0,0),(640,60),(40,40,40),-1)

    for i,col in enumerate(colors):
        cv2.circle(img,(40+i*60,30),20,col,-1)

    cv2.putText(img,"ERASE",(300,40),0,1,(255,255,255),2)
    cv2.putText(img,"UNDO",(420,40),0,1,(255,255,255),2)
    cv2.putText(img,"SAVE",(520,40),0,1,(255,255,255),2)

    rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hands.process(rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm=handLms.landmark

            x=int(lm[8].x*w)
            y=int(lm[8].y*h)

            mx=int(lm[12].x*w)
            my=int(lm[12].y*h)

            dist=math.hypot(x-mx,y-my)
            brushThickness=int(dist/3)

            fingers=fingers_up(lm)

            # SELECTION MODE
            if fingers[0] and fingers[1]:
                prev_x,prev_y=0,0

                if y<60:
                    if x<80: colorIndex=0
                    elif x<140: colorIndex=1
                    elif x<200: colorIndex=2
                    elif x<260: colorIndex=3

                    elif 280<x<360: colorIndex=4  # eraser

                    elif 400<x<480 and undo_stack:
                        canvas=undo_stack.pop()

                    elif 500<x<620:
                        cv2.imwrite(f"AI_board_{time.time()}.png",canvas)

            # DRAW MODE
            elif fingers[0] and not fingers[1]:

                if prev_x==0:
                    prev_x,prev_y=x,y
                    undo_stack.append(canvas.copy())

                cx=int((prev_x+x)/2)
                cy=int((prev_y+y)/2)

                draw_color=(0,0,0) if colorIndex==4 else colors[colorIndex]

                cv2.line(canvas,(prev_x,prev_y),(cx,cy),
                         draw_color,brushThickness)

                prev_x,prev_y=cx,cy

            mp_draw.draw_landmarks(img,handLms,
                                   mp_hands.HAND_CONNECTIONS)

    # Merge canvas
    gray=cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
    _,inv=cv2.threshold(gray,50,255,cv2.THRESH_BINARY_INV)
    inv=cv2.cvtColor(inv,cv2.COLOR_GRAY2BGR)

    img=cv2.bitwise_and(img,inv)
    img=cv2.bitwise_or(img,canvas)

    cv2.imshow("AI Virtual Whiteboard",img)

    if cv2.waitKey(1)&0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

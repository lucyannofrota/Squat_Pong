import time as t
import cv2
import numpy as np
import pygame
from cvzone.HandTrackingModule import HandDetector
from pygame import *
import auxFuncs as myAux
import game
import sys
import os

import imutils
from imutils.video import VideoStream

# VideoStream()

pygame.init()

state: 0

start_button_size = [400, 400]
logo_size = [1000, 300]  # ALTERAR AS COORDENADAS DO LOGO E FAZER AS ALTERAÇÕES ÀS OUTRAS IMAGENS
deec_size = [350, 84]
atari_size = [445, 150]
note_size = [600, 60]
left_size = [600, 150]
right_size = [600, 150]
cam_size = [200, 150]

imgPlay = pygame.image.load('Images/play3.png').convert_alpha()
rectPlay = imgPlay.get_rect()
rectPlay.x, rectPlay.y = game.Screen_Width / 2 - start_button_size[0] / 2, game.Screen_Height / 2 - start_button_size[1] / 2

imgcam = pygame.image.load('Images/cam.png').convert_alpha()
rectcam = imgcam.get_rect()
rectcam.x, rectcam.y = game.Screen_Width / 2 + 7.5 * cam_size[0] / 2, game.Screen_Height / 2 - 6.5 * cam_size[1] / 2

# Webcam

def get_inputs(scale = 0.7, hscale=(-1,-1), detector = []):
    frame = vid_stream.read()
    hands = []
    res = (1920*0.7,1080*0.7)

    if(hscale[0] == -1):
        height, width = frame.shape[0], frame.shape[1]
        hscale = (res[0]/width,res[1]/height)

    frame = cv2.flip(frame, 1)

    if detector == []:
        frame = cv2.resize(frame, (round(game.Screen_Width*scale), round(game.Screen_Height*scale)), interpolation=cv2.INTER_AREA)
    else:
        hands, frame = detector.findHands(frame, flipType=False)
        frame = cv2.resize(frame, (round(res[0]), round(res[1])), interpolation=cv2.INTER_AREA)
    return frame, hands, hscale


vid_stream = VideoStream(src=0).start()
frame, _, hscale = get_inputs()

window = pygame.display.set_mode((game.Screen_Width, game.Screen_Height))
pygame.display.set_caption("Images/Pong Arcade Game")

# Initialize Clock for FPS
fps = 60
clock = pygame.time.Clock()


# Variables
speed = 10
startTime = t.time()
totalTime = 18000

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Main loop
start = True
ctime = []
ctime_mean = 0
tcount = 0



# success, img = cap.read()
# img = cv2.flip(img, 1)
ct = 0
while start:
    ctime_i = t.time_ns()
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                start = False
                pygame.quit()
                sys.exit()

    # Apply Logic
    timeRemain = int(totalTime - (t.time() - startTime))
    if timeRemain < 0:
        window.fill((255, 255, 255))



    else:
        index = sum([len(files) for r, d, files in os.walk("Pictures")])
        # OpenCV


        # success, img = cap.read()
        # img = cv2.flip(img, 1)
        img, hands, hscale = get_inputs(hscale=hscale,detector=detector)


        if(tcount >= 60):
            # ctime_mean
            print("Exec Time (main): "+str(round((sum(ctime)/60)/(1000*1000)))+" (ms)")
            ctime.pop(0)
    
        # hands, img = detector.findHands(img, flipType=False)
        # hands = []
        # img = flip

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        # imgRGB_2 = (66, 207, 223)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)

        window.blit(frame, (0, 0))


        if hands:
            for hand in hands:
                x, y, c = hand['lmList'][8]

                if hand['type'] == 'Right':
                    pygame.draw.circle(window, (148, 25, 134), (x*hscale[0], y*hscale[1]), 15)
                else:
                    pygame.draw.circle(window, (191, 39, 28), (x*hscale[0], y*hscale[1]), 15)
                if rectPlay.collidepoint(x, y):
                    game.startgame(window, cap)
                if rectcam.collidepoint(x, y):
                    if index != 0:
                        myAux.pic_screen(cap, window)

    # Update Display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)
    ctime.append(t.time_ns() - ctime_i)
    tcount += 1

cap.release()
cv2.destroyAllWindows()

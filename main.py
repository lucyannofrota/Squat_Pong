from distutils.log import error
from msilib.schema import Class
import time as t
from turtle import left, right, screensize
import cv2
import numpy as np
import pygame
# from cvzone.HandTrackingModule import HandDetector
from pygame import *
import myTools as myAux
import game
import sys
import os
# import utility

import images

if(len(sys.argv) > 1):
    if (sys.argv[1] == '--cam' and sys.argv[2] == '1'):
        camSrc = 'https://192.168.1.118:8080/video'
else:
    camSrc = 0

pygame.init()

# BackGround Sound
mixer.music.load('Sounds/BoxCat-Games-Epic-Song.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.2)
scale = 0.7
start_button_size = [scale*400, scale*400]
logo_size = [scale*1000, scale*300]  # ALTERAR AS COORDENADAS DO LOGO E FAZER AS ALTERAÇÕES ÀS OUTRAS IMAGENS
deec_size = [scale*350, scale*84]
atari_size = [scale*445, scale*150]
note_size = [scale*600, scale*60]
left_size = [scale*600, scale*150]
right_size = [scale*600, scale*150]
cam_size = [scale*200, scale*150]
gif_size = [scale*600, scale*400]

state: 0

# Detector
# detector = HandDetector(detectionCon=0.8, maxHands=2)

# Images
screen_size = [(game.Screen_Width - scale*game.Screen_Width)/2, (game.Screen_Height - scale*game.Screen_Height)/2]

# Webcam inputs
Winputs = myAux.webcamInputs(src=camSrc,scale=0.7,subSampling=3,windowRes=(game.Screen_Width,game.Screen_Height),offset=(screen_size[0],screen_size[1]),detector='Menu')

window = pygame.display.set_mode((game.Screen_Width, game.Screen_Height))
pygame.display.set_caption("Images/Pong Arcade Game")

fps = 60
clock = pygame.time.Clock()

# Play button -> done
imgPlay, rectPlay = images.load_image(file_name='Images/play3.png',
                                      img_size=start_button_size,
                                      translation = (1, 0.75))
# Logo "PONG" -> done
imgLogo, rectLogo = images.load_image(file_name='Images/logo3.png',
                                      img_size=logo_size,
                                      translation = (1, 3.5))
# Logo "deec"
imgDeec, rectDeec = images.load_image(file_name='Images/deec2.png',
                                      img_size=deec_size,
                                      translation = (5, -9.5))
# Logo "atari"
imgAtari, rectAtari = images.load_image(file_name='Images/atari.png',
                                      img_size=atari_size,
                                      translation = (-2.2, -5))

# note
imgNote, rectNote = images.load_image(file_name='Images/note.png',
                                      img_size=note_size,
                                      translation = (1, -15))

# Purple player
imgLeft, rectLeft = images.load_image(file_name='Images/purple.png',
                                      img_size=left_size,
                                      translation = (2.5, 2),
                                      resize=0)
# Right player
imgRight, rectRight = images.load_image(file_name='Images/red.png',
                                      img_size=right_size,
                                      translation = (-1.5, 2),
                                      resize=0)

# icone fotos
imgCam, rectCam = images.load_image(file_name='Images/cam.png',
                                      img_size=cam_size,
                                      translation = (-7.5, 6.5))
gifSquat_Right = images.load_gif("Image_right", "right", gif_size, (-1.2, 0.4))

#left side squat gif
gifSquat_Left = images.load_gif("Image_left","left", gif_size, (2.8, 0.4))

# Variables
speed = 10
startTime = t.time()
totalTime = 18000

# Main loop
start = True
ctime = []
ctime_mean = 0
tcount = 0

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

    window.fill((0, 0, 0))
    index = sum([len(files) for r, d, files in os.walk("Pictures")])
    # OpenCV
    img, hands = Winputs.get_inputs()
    if(tcount >= 60):
        # print("Exec Time (main): "+str(round((sum(ctime)/60)/(1000*1000)))+" (ms)")
        ctime.pop(0)

    myAux.transform_cap(img, window, (screen_size[0],screen_size[1]))

    # imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # imgRGB = np.rot90(imgRGB)
    # frame = pygame.surfarray.make_surface(imgRGB).convert()
    # frame = pygame.transform.flip(frame, True, False)
    # window.blit(frame, (0, 0))

    window.blit(imgPlay, rectPlay)
    window.blit(imgLogo, rectLogo)
    window.blit(imgDeec, rectDeec)
    window.blit(imgAtari, rectAtari)
    window.blit(imgNote, rectNote)
    window.blit(imgLeft, rectLeft)
    window.blit(imgRight, rectRight)
    window.blit(imgCam, rectCam)

    gifSquat_Right.update()
    gifSquat_Left.update()

    gifSquat_Right.draw(window)
    gifSquat_Left.draw(window)
    if hands:
        for hand in hands:
            # x, y, c = hand['lmList'][8]

            # x = hscale[0]*x
            # y = hscale[1]*y

            if hand != (-1,-1):
                pygame.draw.circle(window, (191, 39, 28), hand, 15)
            else:
                if hand != (-1,-1):
                    pygame.draw.circle(window, (148, 25, 134), hand, 15)
                
            if rectPlay.collidepoint(hand[0], hand[1]):
                game.startgame(window, Winputs)
            if rectCam.collidepoint(hand[0], hand[1]):
                if index != 0:
                    myAux.pic_screen(Winputs, window)

    # Update Display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)
    ctime.append(t.time_ns() - ctime_i)
    tcount += 1

cap.release()
cv2.destroyAllWindows()

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
import utility


pygame.init()

# BackGround Sound
mixer.music.load('Sounds/BoxCat-Games-Epic-Song.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.2)

start_button_size = [400, 400]
logo_size = [1000, 300]  # ALTERAR AS COORDENADAS DO LOGO E FAZER AS ALTERAÇÕES ÀS OUTRAS IMAGENS
deec_size = [350, 84]
atari_size = [445, 150]
note_size = [600, 60]
left_size = [600, 150]
right_size = [600, 150]
cam_size = [200, 150]

state: 0

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Webcam inputs
Winputs = utility.webcamInputs(scale=0.7,windowRes=(game.Screen_Width,game.Screen_Height),detector=detector)
subSampling = 3

window = pygame.display.set_mode((game.Screen_Width, game.Screen_Height))
pygame.display.set_caption("Images/Pong Arcade Game")

# Initialize Clock for FPS
fps = 60
clock = pygame.time.Clock()

# Images
# Play button -> done
imgPlay = pygame.image.load('Images/play3.png').convert_alpha()
rectPlay = imgPlay.get_rect()
rectPlay.x, rectPlay.y = game.Screen_Width / 2 - start_button_size[0] / 2, game.Screen_Height / 2 - start_button_size[1] / 2

# Logo "PONG" -> done
imgLogo = pygame.image.load('Images/logo3.png').convert_alpha()
rectLogo = imgLogo.get_rect()
rectLogo.x, rectLogo.y = game.Screen_Width / 2 - logo_size[0] / 2, game.Screen_Height / 2 - 3.5 * logo_size[1] / 2

# Logo "deec"
imgDeec = pygame.image.load('Images/deec2.png').convert_alpha()
rectDeec = imgDeec.get_rect()
rectDeec.x, rectDeec.y = game.Screen_Width / 2 - 5 * deec_size[0] / 2, game.Screen_Height / 2 + 9.5 * deec_size[1] / 2

# Logo "atari"
imgAtari = pygame.image.load('Images/atari.png').convert_alpha()
rectAtari = imgDeec.get_rect()
rectAtari.x, rectAtari.y = game.Screen_Width / 2 + 2.2 * atari_size[0] / 2, game.Screen_Height / 2 + 5 * atari_size[1] / 2

# note
imgNote = pygame.image.load('Images/note.png').convert_alpha()
rectNote = imgNote.get_rect()
rectNote.x, rectNote.y = game.Screen_Width / 2 - note_size[0] / 2, game.Screen_Height / 2 + 15 * note_size[1] / 2

# note about hands
imgleft = pygame.image.load('Images/left_player.png').convert_alpha()
rectleft = imgleft.get_rect()
rectleft.x, rectleft.y = game.Screen_Width / 2 - 3 * left_size[0] / 2, game.Screen_Height / 2 - 1.1 * left_size[1] / 2

imgright = pygame.image.load('Images/right_player.png').convert_alpha()
rectright = imgright.get_rect()
rectright.x, rectright.y = game.Screen_Width / 2 + 1 * right_size[0] / 2, game.Screen_Height / 2 - 1.1 * right_size[1] / 2

# icone fotos
imgcam = pygame.image.load('Images/cam.png').convert_alpha()
rectcam = imgcam.get_rect()
rectcam.x, rectcam.y = game.Screen_Width / 2 + 7.5 * cam_size[0] / 2, game.Screen_Height / 2 - 6.5 * cam_size[1] / 2

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

    # Apply Logic
    timeRemain = int(totalTime - (t.time() - startTime))
    if timeRemain < 0:
        window.fill((255, 255, 255))



    else:
        index = sum([len(files) for r, d, files in os.walk("Pictures")])
        # OpenCV
        img, hands, hscale = Winputs.get_inputs(subSampling=subSampling,menu=True)
        if(tcount >= 60):
            # print("Exec Time (main): "+str(round((sum(ctime)/60)/(1000*1000)))+" (ms)")
            ctime.pop(0)

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)

        window.blit(frame, (0, 0))
        window.blit(imgPlay, rectPlay)
        window.blit(imgLogo, rectLogo)
        window.blit(imgDeec, rectDeec)
        window.blit(imgAtari, rectAtari)
        window.blit(imgNote, rectNote)
        window.blit(imgleft, rectleft)
        window.blit(imgright, rectright)
        window.blit(imgcam, rectcam)

        if hands:
            for hand in hands:
                x, y, c = hand['lmList'][8]

                x = hscale[0]*x
                y = hscale[1]*y

                if hand['type'] == 'Right':
                    pygame.draw.circle(window, (148, 25, 134), (x, y), 15)
                else:
                    pygame.draw.circle(window, (191, 39, 28), (x, y), 15)
                if rectPlay.collidepoint(x, y):
                    game.startgame(window, Winputs, subSampling)
                if rectcam.collidepoint(x, y):
                    if index != 0:
                        myAux.pic_screen(Winputs, window, subSampling)

    # Update Display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)
    ctime.append(t.time_ns() - ctime_i)
    tcount += 1

cap.release()
cv2.destroyAllWindows()

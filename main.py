from distutils.log import error
from msilib.schema import Class
import time as t
from turtle import left
import cv2
import numpy as np
import pygame
# from cvzone.HandTrackingModule import HandDetector
from pygame import *
import auxFuncs as myAux
import game
import sys
import os
import utility

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
# detector = HandDetector(detectionCon=0.8, maxHands=2)

# Webcam inputs
Winputs = utility.webcamInputs(src=camSrc,scale=0.7,windowRes=(game.Screen_Width,game.Screen_Height),detector='Menu')
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
imgleft = pygame.image.load('Images/purple.png').convert_alpha()
rectleft = imgleft.get_rect()
rectleft.x, rectleft.y = game.Screen_Width / 2 - 2.5* left_size[0] / 2, game.Screen_Height / 2 - 2 * left_size[1] / 2

imgright = pygame.image.load('Images/red.png').convert_alpha()
rectright = imgright.get_rect()
rectright.x, rectright.y = game.Screen_Width / 2 + 1.5 * right_size[0] / 2, game.Screen_Height / 2 - 2 * right_size[1] / 2

# icone fotos
imgcam = pygame.image.load('Images/cam.png').convert_alpha()
rectcam = imgcam.get_rect()
rectcam.x, rectcam.y = game.Screen_Width / 2 + 7.5 * cam_size[0] / 2, game.Screen_Height / 2 - 6.5 * cam_size[1] / 2

# squat gif
def loadimgs(folder_name, direction, gif):
    # Used to load multiple images from folder and store them in the variable "gif"
    for item in range(1,21):
        if(item < 10):
            squat_img = pygame.image.load("Images/" + folder_name + "/Image_"+str(direction)+".00"+str(item)+".png").convert_alpha()
        else:
            squat_img = pygame.image.load("Images/"+folder_name+"/Image_"+str(direction)+".0"+str(item)+".png").convert_alpha()
        gif.append(squat_img)

class squatGif(pygame.sprite.Sprite):
    # Used to animate gif
    def __init__(self, position, imgs):
        super(squatGif, self).__init__()
        size = (50,30)
        self.rect = pygame.Rect(position, size)
        self.index = 0
        self.images= imgs
        self.image = imgs[self.index]

        self.animation_frames = 6
        self.current_frame = 0

    def update(self):
        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

# right side squat gif
squat_right = imgcam.get_rect()
squat_right.x, squat_right.y = game.Screen_Width/2 + 1.2*right_size[0]/2, game.Screen_Height/2 - 0.5*right_size[1]/2

mygif = []
loadimgs("Image_right", "right",mygif)
squat_gif = squatGif(position=(squat_right.x, squat_right.y), imgs=mygif)
my_sprites = pygame.sprite.Group(squat_gif)

#left side squat gif
squat_L = imgcam.get_rect()
squat_L.x, squat_L.y = game.Screen_Width/2 - 2.8*left_size[0]/2, game.Screen_Height/2 - 0.5*left_size[1]/2

mygif_L = []
loadimgs("Image_left","left", mygif_L)
squat_gif_L = squatGif(position=(squat_L.x, squat_L.y), imgs=mygif_L)
my_sprites_L = pygame.sprite.Group(squat_gif_L)

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
        img, hands = Winputs.get_inputs(subSampling=subSampling)
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

        my_sprites.update()
        my_sprites_L.update()

        my_sprites.draw(window)
        my_sprites_L.draw(window)
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
                    game.startgame(window, Winputs.vid_stream, subSampling)
                if rectcam.collidepoint(hand[0], hand[1]):
                    if index != 0:
                        myAux.pic_screen(Winputs.vid_stream, window, subSampling)

    # Update Display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)
    ctime.append(t.time_ns() - ctime_i)
    tcount += 1

cap.release()
cv2.destroyAllWindows()

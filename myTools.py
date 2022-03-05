import cv2
import time as t
from cv2 import resize
from isort import file
import numpy as np

import pygame
from pygame import *
import pyautogui
import game
from tkinter.filedialog import *
import os

import imutils
from imutils.video import VideoStream

#Hand Detector
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

from images import load_image

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)


def TakePic():

    # Conta Número de Ficheiros Em Pictures
    index = sum([len(files) for r, d, files in os.walk("Pictures")])
    screen_shot = pyautogui.screenshot()
    save_path = "Pictures"
    screen_shot.save(save_path + "/screenshot_" + str(index) +".png")


def pic_screen(in_Winputs, window):
    # Conta Número de Ficheiros Em Pictures
    total_files = sum([len(files) for r, d, files in os.walk("Pictures")])

    font = pygame.font.Font("font.TTF", 60)
    text_x = game.Screen_Width / 2.3
    text_y = game.Screen_Height / 1.1

    Winputs = webcamInputs(webcamInputs=in_Winputs,vid_stream=in_Winputs.vid_stream,offset=in_Winputs.offset,subSampling=in_Winputs.subSampling,detector='Menu')

    index = 0
    running = True
    Arrow_Left, Arrow_Left_coord = load_image(file_name='Images/Arrow_Left.png',
                                                  img_size = (150, 150),
                                                  translation=(9,1))
        
    Arrow_Right, Arrow_Right_coord = load_image(file_name='Images/Arrow_Right.png',
                                                  img_size = (150, 150),
                                                  translation=(-6.8, 1))
    imgBg, rectBg = load_image(file_name='Images/arcade.jpg',
                                img_size=(1920, 1080),
                                translation=(1,1))
    # retangulo semi transparente
    menuBg = pygame.Surface((0.7*game.Screen_Width, 0.7*game.Screen_Height))
    menuBg.fill((255,255,255))
    menuBg.set_alpha(100)
    menuBgPos = [(game.Screen_Width - 0.7*game.Screen_Width)/2, 
                 (game.Screen_Height - 0.7*game.Screen_Height)/2]

    while running:
        game.event()
        window.blit(imgBg, rectBg)

        img, hands = Winputs.get_inputs()
        transform_cap(img, window, Winputs.offset)

        Imagem, Imagem_coord = load_image(file_name="Pictures/screenshot_" + str(index) + ".png",
                                          img_size=(game.Screen_Width*0.5, game.Screen_Height*0.5),
                                          translation=(1,1))
        window.blit(menuBg, menuBgPos)
        window.blit(Imagem, Imagem_coord)
        window.blit(Arrow_Left, Arrow_Left_coord)
        window.blit(Arrow_Right, Arrow_Right_coord)

        #Background
        BackGround, BackGround_coord = load_image(file_name='Images/BackGround.png',
                                                  img_size= (0.55*game.Screen_Width, 0.7*game.Screen_Height),
                                                  translation=(1,1))
        window.blit(BackGround, BackGround_coord)

        # Menu
        menu_size = [250, 100]
        menu, menu_coord = load_image(file_name='Images/menu.png',
                                      img_size = menu_size,
                                      translation=(1, 7.5))
        window.blit(menu, menu_coord)

        # Contador da imagem a mostrar
        page = font.render(str(index + 1) + "/" + str(total_files), True, (0, 0, 0))

        window.blit(page, (text_x+50, text_y-125))

        # if count % 4 == 0:
        #     hands, img = detector.findHands(img, flipType=False)
        #     if hands:
        #         for hand in hands:
        #             x, y, c = hand['lmList'][8]
        #             pygame.draw.circle(window, (255, 0, 0), (x, y), 15)
        #             if Arrow_Right_coord.collidepoint(x, y):
        #                 index += 1
        #                 if index >= total_files:
        #                     index = 0
        #                 time.delay(500)
        #             if Arrow_Left_coord.collidepoint(x, y):
        #                 index -= 1
        #                 if index < 0:
        #                     index = total_files - 1
        #                 time.delay(500)
        #             if menu_coord.collidepoint(x, y):
        #                 running = False

        if hands:
            for hand in hands:
                if hand != (-1,-1):
                        pygame.draw.circle(window, (191, 39, 28), hand, 15)
                else:
                    if hand != (-1,-1):
                        pygame.draw.circle(window, (148, 25, 134), hand, 15)
                        
                if Arrow_Right_coord.collidepoint(hand[0], hand[1]):
                    index += 1
                    if index >= total_files:
                        index = 0
                    pygame.time.delay(500)
                if Arrow_Left_coord.collidepoint(hand[0], hand[1]):
                    index -= 1
                    if index < 0:
                        index = total_files - 1
                    pygame.time.delay(500)
                if menu_coord.collidepoint(hand[0], hand[1]):
                    running = False

        pygame.display.update()


def Text(screen, winner_x, winner_y, loser_x, loser_y):

    Winner = pygame.image.load('Images/winner.png').convert_alpha()
    Winner = pygame.transform.scale(Winner, (int(game.Screen_Width / 5), int(game.Screen_Height / 10)))

    Loser = pygame.image.load('Images/loser.png').convert_alpha()
    Loser = pygame.transform.scale(Loser, (int(game.Screen_Width / 6), int(game.Screen_Height / 10)))

    screen.blit(Winner, (winner_x - game.Screen_Width / 20, winner_y))
    screen.blit(Loser, (loser_x, loser_y))

#################
#   FUNCTIONS   #
#################


def transform_cap(img, screen, offset=(0,0)):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    screen.blit(frame, offset)


def define_winner(in_Winputs, screen, coord_x_crown, coord_y_crown, result):
    Winputs = webcamInputs(webcamInputs=in_Winputs,vid_stream=in_Winputs.vid_stream,offset=in_Winputs.offset,subSampling=in_Winputs.subSampling,detector='Menu')
    # Winputs = webcamInputs(webcamInputs=in_Winputs,detector='Menu')
    running = True
    count = 0
    start_time = t.time()
    while running:
        game.event()
        img, hands = Winputs.get_inputs()
        transform_cap(img, screen, Winputs.offset)

        # Crown e Joker
        Crown, Crown_coord = load_image(file_name='Images/Crown.png',
                                        img_size=(400,400),
                                        translation=(0,0),
                                        resize=1)

        # Joker = pygame.image.load('Images/joker.png').convert_alpha()
        # Joker_coord = Joker.get_rect()

        Joker, Joker_coord = load_image(file_name='Images/joker.png',
                                        img_size=(450,400),
                                        translation=(0,0),
                                        resize=1)

        Tears, Tears_coord = load_image(file_name='Images/tears.png',
                                        img_size=(450,400),
                                        translation=(0,0),
                                        resize=1)

        Pic = pygame.image.load('Images/picture.png').convert_alpha()
        Pic_coord = Pic.get_rect()
        Pic_coord.x, Pic_coord.y = game.Screen_Width / 2.2, game.Screen_Height / 1.2

        Crown_coord.x, Crown_coord.y = int(coord_x_crown), int(coord_y_crown)
        screen.blit(Crown, Crown_coord)

        if result == 1:
            Joker_coord.x, Joker_coord.y = int(coord_x_crown + 0.7*game.Screen_Width / 2.1), int(coord_y_crown)
            Tears_coord.x, Tears_coord.y = int(coord_x_crown + 0.7*game.Screen_Width / 2.1), int(coord_y_crown + 0.8*game.Screen_Height / 2.2)

            #Texto Winner/Loser
            Text(screen, coord_x_crown, coord_y_crown + game.Screen_Height / 3, coord_x_crown + game.Screen_Width / 3.2, coord_y_crown + game.Screen_Height / 2)
        else:
            Joker_coord.x, Joker_coord.y = int(coord_x_crown - 0.7*game.Screen_Width / 1.9), int(coord_y_crown)
            Tears_coord.x, Tears_coord.y = int(coord_x_crown - 0.7*game.Screen_Width / 1.9), int(coord_y_crown + 0.8*game.Screen_Height / 2.2)

            # Texto Winner/Loser
            Text(screen, coord_x_crown, coord_y_crown + game.Screen_Height / 3, coord_x_crown - game.Screen_Width / 3.2, coord_y_crown + game.Screen_Height / 2)

        screen.blit(Joker, Joker_coord)
        screen.blit(Tears, Tears_coord)

        if hands:
            for hand in hands:
                if hand != (-1,-1):
                        pygame.draw.circle(screen, (191, 39, 28), hand, 15)
                else:
                    if hand != (-1,-1):
                        pygame.draw.circle(screen, (148, 25, 134), hand, 15)
                        
                if Pic_coord.collidepoint(hand[0], hand[1]):
                        TakePic()
                        running = False
        # print("Tick")
        screen.blit(Pic, Pic_coord)
        pygame.display.update()
        count += 1
        end_time = t.time()
        if int(end_time-start_time) >= 10:
            break


def winner_screen(screen, in_Winputs, result):
    # Player A Ganha
    if result == 1:
        define_winner(in_Winputs, screen, game.Screen_Width / 5, game.Screen_Height/10, result)
    # Player B Ganha
    else:
        define_winner(in_Winputs, screen, game.Screen_Width/1.8,  game.Screen_Height/10, result)


def showFPS(prev_frame_time, new_frame_time):
    new_frame_time = t.time()
    fps = str(int(1/(new_frame_time-prev_frame_time)))
    prev_frame_time = new_frame_time
    return prev_frame_time, new_frame_time, fps


def getNewFrameOpenCV(cap, width, height):
    retval,frame = cap.read()
    frame = cv2.resize(frame, (width, height))
    if not retval:
        return retval, 0, 0, 0, 0

    # frame = cv2.resize(frame,(1080,720))
    h, w, c = frame.shape
    return retval, h, w, c, frame


def frameCV2Py(frame):
    frame = np.rot90(frame)
    frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_RGB = pygame.surfarray.make_surface(frame_RGB)
    return frame_RGB


class webcamInputs:
    def __init__(self,webcamInputs=[],vid_stream=[],subSampling=0,src=0,scale=0.7,windowRes=(1920,1080),offset=(0,0),detector='Menu'):
        if(webcamInputs != []):
            self.vid_stream=webcamInputs.vid_stream
            self.scale=webcamInputs.scale
            self.windowRes=webcamInputs.windowRes
            self.offset=webcamInputs.offset
            self.detector=webcamInputs.detector
            self.subSampling=webcamInputs.subSampling

            if(self.windowRes != (1920,1080)):
                self.windowRes = windowRes
            if(self.scale != 0.7):
                self.scale = scale
            if(self.offset != (0,0)):
                self.offset = offset
            if(self.subSampling != 0):
                self.subSampling = subSampling
        else:
            self.windowRes = windowRes
            self.scale = scale
            self.offset = offset
            self.subSampling = subSampling

        if(vid_stream == []):
            self.vid_stream = VideoStream(src=src).start()
        else:
            self.vid_stream = vid_stream


        self.outRes = (round(self.windowRes[0]*scale),round(self.windowRes[1]*scale))
        frame = self.vid_stream.read()
        height, width = frame.shape[0], frame.shape[1]
        self.hscale = (self.outRes[0]/width,self.outRes[1]/height)

        self.detectorType = detector

        self.l_hands = []
        self.l_hands.append((-1,-1)) #Left Hand
        self.l_hands.append((-1,-1)) #Right Hand

        if self.detectorType == 'Menu':
            self.detector = HandDetector(detectionCon=0.8, maxHands=2)
        else:
            if self.detectorType == 'GameHand':
                mp_drawing = mp.solutions.drawing_utils
                mp_drawing_styles = mp.solutions.drawing_styles
                self.mp_hands = mp.solutions.hands
                self.detector = self.mp_hands.Hands(model_complexity=0, min_detection_confidence=0.3, min_tracking_confidence=0.3)

        self.subSampCounter = self.subSampling

        self.l_frame = []
        self.l_detected = []

    # def GameHand():


    def get_inputs(self):
        if(self.subSampCounter <= (self.subSampling-1) or self.l_frame == []):
            frame = self.vid_stream.read()

            if self.detectorType == 'Menu':
                frame = cv2.flip(frame, 1)
                hands, frame = self.detector.findHands(frame, flipType=False)

                self.l_hands[0] = (-1,-1)
                self.l_hands[1] = (-1,-1)
                if hands:
                    for hand in hands:
                        x, y, c = hand['lmList'][8]
                        if hand['type'] == 'Left':
                            self.l_hands[0] = (x*self.hscale[0]+self.offset[0],y*self.hscale[1]+self.offset[1])
                        else:
                            self.l_hands[1] = (x*self.hscale[0]+self.offset[0],y*self.hscale[1]+self.offset[1])

            else:
                if self.detectorType == 'GameHand':
                    frameCV_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    results = self.detector.process(frameCV_RGB) # convert from BGR to RGB
                    if results.multi_hand_landmarks is not None:
                        # EACH HAND #
                        for handLms, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                            handedness_dict1 = MessageToDict(handedness)
                            # RIGHT HAND  #
                            if handedness_dict1['classification'][0]['label'] == 'Right':
                                # EACH POINTS OF THE HAND #
                                for id, lm in enumerate(handLms.landmark):
                                    if id == self.mp_hands.HandLandmark.INDEX_FINGER_TIP:
                                        x, y = self.outRes[0]-int(lm.x*self.outRes[0])+self.offset[0], int(lm.y*self.outRes[1])+self.offset[1]
                                        self.l_hands[1] = (x,y)
                            # LEFT HAND #
                            if handedness_dict1['classification'][0]['label'] == 'Left':
                                # EACH POINTS OF THE HAND #
                                for id, lm in enumerate(handLms.landmark):
                                    if id == self.mp_hands.HandLandmark.INDEX_FINGER_TIP:
                                        x, y = self.outRes[0]-int(lm.x*self.outRes[0])+self.offset[0], int(lm.y*self.outRes[1])+self.offset[1]
                                        self.l_hands[0] = (x,y)

            frame = cv2.resize(frame, (self.outRes[0], self.outRes[1]), interpolation=cv2.INTER_AREA)
            self.l_frame = frame
            self.subSampCounter = self.subSampling

        self.subSampCounter -= 1

        if self.detectorType == 'Menu':
            return self.l_frame, self.l_hands
        else:
            if self.detectorType == 'GameHand':
                #  GET NEW BACKGROUND  #
                self.l_frame = frameCV2Py(self.l_frame)
                return self.l_frame, self.l_hands

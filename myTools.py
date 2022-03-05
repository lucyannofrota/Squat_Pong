import cv2
import time as t
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
    count = 0

    while running:
        game.event()

        img, hands = Winputs.get_inputs()
        transform_cap(img, window, Winputs.offset)
        # img = cv2.resize(img, (game.Screen_Width, game.Screen_Height))
        # img = cv2.flip(img, 1)

        # transform_cap(img, window)

        # Load Imagem
        Imagem = pygame.image.load("Pictures/screenshot_" + str(index) + ".png").convert_alpha()
        Imagem = pygame.transform.scale(Imagem, (int(game.Screen_Width / 1.3), int(game.Screen_Height / 1.35)))
        Imagem_coord = Imagem.get_rect()
        Imagem_coord.x, Imagem_coord.y = int(game.Screen_Width / 8), int(game.Screen_Height / 7.4)
        window.blit(Imagem, Imagem_coord)
        # Arrows
        Arrow_Left = pygame.image.load('Images/Arrow_Left.png').convert_alpha()
        Arrow_Left = pygame.transform.scale(Arrow_Left, (150, 150))
        Arrow_Left_coord = Arrow_Left.get_rect()
        Arrow_Left_coord.x, Arrow_Left_coord.y = int(game.Screen_Width / 52), int(game.Screen_Height / 2)
        window.blit(Arrow_Left, Arrow_Left_coord)

        Arrow_Right = pygame.image.load('Images/Arrow_Right.png').convert_alpha()
        Arrow_Right = pygame.transform.scale(Arrow_Right, (150, 150))
        Arrow_Right_coord = Arrow_Right.get_rect()
        Arrow_Right_coord.x, Arrow_Right_coord.y = int(game.Screen_Width / 1.1), int(game.Screen_Height / 2)
        window.blit(Arrow_Right, Arrow_Right_coord)

        #Background
        BackGround = pygame.image.load('Images/BackGround.png').convert_alpha()
        BackGround = pygame.transform.scale(BackGround, (game.Screen_Width / 1.2, game.Screen_Height))
        BackGround_coord = BackGround.get_rect()
        BackGround_coord.x, BackGround_coord.y = game.Screen_Width / 11, 0
        window.blit(BackGround, BackGround_coord)

        # Menu
        menu_size = [250, 100]
        menu = pygame.image.load('Images/menu.png').convert_alpha()
        menu_coord = menu.get_rect()
        menu_coord.x, menu_coord.y = game.Screen_Width / 2 - menu_size[0] / 2, game.Screen_Height / 2 - 10.5 * menu_size[1] / 2
        window.blit(menu, menu_coord)

        # Contador da imagem a mostrar
        page = font.render(str(index + 1) + "/" + str(total_files), True, (0, 0, 0))

        window.blit(page, (text_x, text_y))

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
                    time.delay(500)
                if Arrow_Left_coord.collidepoint(hand[0], hand[1]):
                    index -= 1
                    if index < 0:
                        index = total_files - 1
                    time.delay(500)
                if menu_coord.collidepoint(hand[0], hand[1]):
                    running = False

        pygame.display.update()


def Text(screen, winner_x, winner_y, loser_x, loser_y):

    Winner = pygame.image.load('Images/winner.png').convert_alpha()
    Winner = pygame.transform.scale(Winner, (int(game.Screen_Width / 3), int(game.Screen_Height / 6.1)))

    Loser = pygame.image.load('Images/loser.png').convert_alpha()
    Loser = pygame.transform.scale(Loser, (int(game.Screen_Width / 3.7), int(game.Screen_Height / 5.7)))

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


def define_winner(in_Winputs, screen, coord_x_crown, coord_y_crown, coord_x_rect, coord_y_rect, result):
    Winputs = webcamInputs(webcamInputs=in_Winputs,vid_stream=in_Winputs.vid_stream,offset=in_Winputs.offset,subSampling=in_Winputs.subSampling,detector='Menu')
    # Winputs = webcamInputs(webcamInputs=in_Winputs,detector='Menu')
    running = True
    count = 0
    start_time = t.time()
    while running:
        game.event()
        # success, img = cap.read()
        # img = cv2.resize(img, (game.Screen_Width, game.Screen_Height))
        # img = cv2.flip(img, 1)
        img, hands = Winputs.get_inputs()
        transform_cap(img, screen, Winputs.offset)

        # Crown e Joker
        Crown = pygame.image.load('Images/Crown.png').convert_alpha()
        Crown_coord = Crown.get_rect()

        Joker = pygame.image.load('Images/joker.png').convert_alpha()
        Joker_coord = Joker.get_rect()

        Tears = pygame.image.load('Images/tears.png').convert_alpha()
        Tears_coord = Tears.get_rect()

        Pic = pygame.image.load('Images/picture.png').convert_alpha()
        Pic_coord = Pic.get_rect()
        Pic_coord.x, Pic_coord.y = game.Screen_Width / 2.2, game.Screen_Height / 1.2

        Crown_coord.x, Crown_coord.y = int(coord_x_crown), int(coord_y_crown)
        screen.blit(Crown, Crown_coord)

        if result == 1:
            Joker_coord.x, Joker_coord.y = int(coord_x_crown + game.Screen_Width / 2.1), int(coord_y_crown)
            Tears_coord.x, Tears_coord.y = int(coord_x_crown + game.Screen_Width / 2.1), int(coord_y_crown + game.Screen_Height / 2.2)

            #Texto Winner/Loser
            Text(screen, coord_x_crown, coord_y_crown + game.Screen_Height / 1.2, coord_x_crown + game.Screen_Width / 1.95, coord_y_crown + game.Screen_Height / 1.2)
        else:
            Joker_coord.x, Joker_coord.y = int(coord_x_crown - game.Screen_Width / 1.9), int(coord_y_crown)
            Tears_coord.x, Tears_coord.y = int(coord_x_crown - game.Screen_Width / 1.9), int(coord_y_crown + game.Screen_Height / 2.2)

            # Texto Winner/Loser
            Text(screen, coord_x_crown, coord_y_crown + game.Screen_Height / 1.2, coord_x_crown - game.Screen_Width / 1.95, coord_y_crown + game.Screen_Height / 1.2)

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
        define_winner(in_Winputs, screen, game.Screen_Width / 8, 0, game.Screen_Width / 2.3, game.Screen_Height / 1.5, result)
    # Player B Ganha
    else:
        define_winner(in_Winputs, screen, game.Screen_Width / 1.6, 0, game.Screen_Width / 2.3, game.Screen_Height / 1.5, result)


def showFPS(prev_frame_time, new_frame_time):
    new_frame_time = time.time()
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

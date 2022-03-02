import cv2
import time as t
import numpy as np
import pygame
from pygame import *
import pyautogui
from cvzone.HandTrackingModule import HandDetector
import game
from tkinter.filedialog import *
import os

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)


def TakePic():

    # Conta Número de Ficheiros Em Pictures
    index = sum([len(files) for r, d, files in os.walk("Pictures")])
    screen_shot = pyautogui.screenshot()
    save_path = "Pictures"
    screen_shot.save(save_path + "/screenshot_" + str(index) +".png")


def pic_screen(cap, window):
    # Conta Número de Ficheiros Em Pictures
    total_files = sum([len(files) for r, d, files in os.walk("Pictures")])

    font = pygame.font.Font("font.TTF", 60)
    text_x = game.Screen_Width / 2.3
    text_y = game.Screen_Height / 1.1

    index = 0
    running = True
    count = 0
    while running:
        game.event()

        success, img = cap.read()
        img = cv2.resize(img, (game.Screen_Width, game.Screen_Height))
        img = cv2.flip(img, 1)

        transform_cap(img, window)

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

        if count % 4 == 0:
            hands, img = detector.findHands(img, flipType=False)
            if hands:
                for hand in hands:
                    x, y, c = hand['lmList'][8]
                    pygame.draw.circle(window, (255, 0, 0), (x, y), 15)
                    if Arrow_Right_coord.collidepoint(x, y):
                        index += 1
                        if index >= total_files:
                            index = 0
                        time.delay(500)
                    if Arrow_Left_coord.collidepoint(x, y):
                        index -= 1
                        if index < 0:
                            index = total_files - 1
                        time.delay(500)
                    if menu_coord.collidepoint(x, y):
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


def transform_cap(img, screen):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    screen.blit(frame, (0, 0))


def define_winner(cap, screen, coord_x_crown, coord_y_crown, coord_x_rect, coord_y_rect, result):
    running = True
    count = 0
    start_time = t.time()
    while running:
        game.event()
        success, img = cap.read()
        img = cv2.resize(img, (game.Screen_Width, game.Screen_Height))
        img = cv2.flip(img, 1)

        transform_cap(img, screen)

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

        if count % 2 == 0:
            hands, img = detector.findHands(img, flipType=False)
            if hands:
                for hand in hands:
                    x, y, c = hand['lmList'][8]
                    pygame.draw.circle(screen, (255, 0, 0), (x, y), 15)
                    if Pic_coord.collidepoint(x, y):
                        TakePic()
                        running = False
        screen.blit(Pic, Pic_coord)
        pygame.display.update()
        count += 1
        end_time = t.time()
        if int(end_time-start_time) >= 10:
            break


def winner_screen(cap, screen, result):
    # Player A Ganha
    if result == 1:
        define_winner(cap, screen, game.Screen_Width / 8, 0, game.Screen_Width / 2.3, game.Screen_Height / 1.5, result)
    # Player B Ganha
    else:
        define_winner(cap, screen, game.Screen_Width / 1.6, 0, game.Screen_Width / 2.3, game.Screen_Height / 1.5, result)


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

import cv2
import pygame
from pygame import *
import mediapipe as mp
import auxFuncs as myAux
from google.protobuf.json_format import MessageToDict
import pyautogui
import sys

pygame.init()
Screen_Width, Screen_Height = pyautogui.size()
window = pygame.display.set_mode((Screen_Width, Screen_Height))

# Sounds
mixer.init()
Paddle = mixer.Sound("Sounds/Paddle.wav")
Wall = mixer.Sound("Sounds/Wall.wav")
Score = mixer.Sound("Sounds/Score.wav")

score_0_size = [250, 100]
score_0_0_size = [250, 100]
score_1_size = [250, 100]
score_1_1_size = [250, 100]
score_2_size = [250, 100]
score_2_2_size = [250, 100]
score_3_size = [250, 100]
score_3_3_size = [250, 100]

menu_size = [250, 100]
sep_size = [2100, 50]

# imagens
# score_0
imgscore_0 = pygame.image.load('Images/score_0.png').convert_alpha()
rectscore_0 = imgscore_0.get_rect()
rectscore_0.x, rectscore_0.y = Screen_Width/2 + 4*score_0_size[0]/2, Screen_Height/2 - 10*score_0_size[1]/2

imgscore_0_0 = pygame.image.load('Images/score_0_0.png').convert_alpha()
rectscore_0_0 = imgscore_0_0.get_rect()
rectscore_0_0.x, rectscore_0_0.y = Screen_Width/2 - 6*score_0_0_size[0]/2, Screen_Height/2 - 10*score_0_0_size[1]/2

# score_1
imgscore_1 = pygame.image.load('Images/score_1.png').convert_alpha()
rectscore_1 = imgscore_1.get_rect()
rectscore_1.x, rectscore_1.y = Screen_Width/2 + 4*score_1_size[0]/2, Screen_Height/2 - 10*score_1_size[1]/2

imgscore_1_1 = pygame.image.load('Images/score_1_1.png').convert_alpha()
rectscore_1_1 = imgscore_1_1.get_rect()
rectscore_1_1.x, rectscore_1_1.y = Screen_Width/2 - 6*score_1_1_size[0]/2, Screen_Height/2 - 10*score_1_1_size[1]/2

# score_2
imgscore_2 = pygame.image.load('Images/score_2.png').convert_alpha()
rectscore_2 = imgscore_2.get_rect()
rectscore_2.x, rectscore_2.y = Screen_Width/2 + 4*score_2_size[0]/2, Screen_Height/2 - 10*score_2_size[1]/2

imgscore_2_2 = pygame.image.load('Images/score_2_2.png').convert_alpha()
rectscore_2_2 = imgscore_2_2.get_rect()
rectscore_2_2.x, rectscore_2_2.y = Screen_Width/2 - 6*score_2_2_size[0]/2, Screen_Height/2 - 10*score_2_2_size[1]/2

# score_3
imgscore_3 = pygame.image.load('Images/score_3.png').convert_alpha()
rectscore_3 = imgscore_3.get_rect()
rectscore_3.x, rectscore_3.y = Screen_Width/2 + 4*score_3_size[0]/2, Screen_Height/2 - 10*score_3_size[1]/2

imgscore_3_3 = pygame.image.load('Images/score_3_3.png').convert_alpha()
rectscore_3_3 = imgscore_3_3.get_rect()
rectscore_3_3.x, rectscore_3_3.y = Screen_Width/2 - 6*score_3_3_size[0]/2, Screen_Height/2 - 10*score_3_3_size[1]/2

# Menu
imgmenu = pygame.image.load('Images/menu.png').convert_alpha()
rectmenu = imgmenu.get_rect()
rectmenu.x, rectmenu.y = Screen_Width/2 - menu_size[0]/2, Screen_Height/2 - 10*menu_size[1]/2

# separação
imgsep = pygame.image.load('Images/sep_op1.png').convert_alpha()
rectsep = imgsep.get_rect()
rectsep.x, rectsep.y = Screen_Width/2 - sep_size[0]/2, 3*sep_size[1]
topBar = (3+1)*sep_size[1]


#Player color
Player_color = (148,25,134)
Opponent_color = (191, 39, 28)



#Controller Parameters
filter_components = 3 #Maior reduz a responsividade
Controller_Kp = 0.35 #"Velocidade" que as barras se movem


def event():
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

def controller_lim(pos,min,max):
    if pos > max:
        return max
    else:
        if pos < min:
            return min
        else:
            return pos

        
        

def controller_filter(list,val):
    list.append(val)

    if len(list) > filter_components:
        del list[0]

    return sum(list)/len(list)


def startgame(screen, camera):
    state: 1
    pygame.time.delay(500)

    #####################
    #   GET FIRST FRAME #
    #####################
    (retval_original, h_original,w_original,c_original,frame_original) = myAux.getNewFrameOpenCV(camera, Screen_Width, Screen_Height)
    w_original,h_original = pygame.display.get_surface().get_size()

    #############
    #   PYGAME  #
    #############
    clock = pygame.time.Clock()
    #############
    # MEDIAPIPE #
    #############
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.3, min_tracking_confidence=0.3)
    doHandPose = True
    drawHands = False

    #############
    #   PONG    #
    #############
    multiplayer = True

    ballRadius = 50
    ballSpeed = 350
    deltaSpeed = 1
    dtime = 0
    ballSpeedX = ballSpeed
    ballSpeedY = ballSpeed
    ball = pygame.Rect( w_original/2 - ballRadius/2, h_original/2 - ballRadius/2, ballRadius, ballRadius)

    playerScore = 0
    playerSpeed = ballSpeed*2
    playerLength = int(h_original/5)
    playerThickness = 30
    player = pygame.Rect( 0, h_original/2, playerThickness, playerLength )

    opponentScore = 0
    opponentSpeed = ballSpeed*2
    opponent = pygame.Rect( w_original - playerThickness, h_original/2, playerThickness, playerLength )

    player_y_list = []
    opponent_y_list = []

    controller_max = h_original - playerLength # Limite superior que a barra pode alcançar
    controller_min = topBar # Limite inferior que a barra pode alcançar

    #############################################
    #   ONLY MOVE IF THE BALL IS AN OFFSET AWAY #
    #############################################
    offset = playerLength * (2/3)

    #############
    # MAIN LOOP #
    #############
    getTicksLastFrame = pygame.time.get_ticks()
    running = True
    while running:
        event()
        #############
        #   FPS     #
        #############
        clock.tick(60)  # locks MAX FPS
        fps = clock.get_fps()

        #################
        #   DELTA TIME  #
        #################
        t = pygame.time.get_ticks()
        deltaTime = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t

        #####################
        #   GET NEW FRAME   #
        #####################
        (retval, frameHeight, frameWidth, frameChannels, frameCV) = myAux.getNewFrameOpenCV(camera, Screen_Width, Screen_Height)
        if not retval:
            break
        frameCV = cv2.resize(frameCV, (w_original, h_original), interpolation = cv2.INTER_AREA)
        frameCV_RGB = cv2.cvtColor(frameCV, cv2.COLOR_BGR2RGB)

        #################
        # GET HAND POSE #
        #################
        LEFT_INDEX_FINGER_TIP_X, LEFT_INDEX_FINGER_TIP_Y = -1, -1
        RIGHT_INDEX_FINGER_TIP_X, RIGHT_INDEX_FINGER_TIP_Y = -1, -1
        if doHandPose:
            results = hands.process(frameCV_RGB) # convert from BGR to RGB
            if results.multi_hand_landmarks is not None:
                #############
                # EACH HAND #
                #############
                for handLms, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    #############
                    # DRAW HAND #
                    #############
                    if drawHands:
                        mp_drawing.draw_landmarks(
                            frameCV,
                            handLms,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())

                    handedness_dict1 = MessageToDict(handedness)
                    ###############
                    # RIGHT HAND  #
                    ###############
                    if handedness_dict1['classification'][0]['label'] == 'Right':
                        ###########################
                        # EACH POINTS OF THE HAND #
                        ###########################
                        for id, lm in enumerate(handLms.landmark):
                            if id == mp_hands.HandLandmark.INDEX_FINGER_TIP:
                                RIGHT_INDEX_FINGER_TIP_X, RIGHT_INDEX_FINGER_TIP_Y = w_original-int(lm.x*w_original), int(lm.y*h_original)

                    #############
                    # LEFT HAND #
                    #############
                    if handedness_dict1['classification'][0]['label'] == 'Left':
                        ###########################
                        # EACH POINTS OF THE HAND #
                        ###########################
                        for id, lm in enumerate(handLms.landmark):
                            if id == mp_hands.HandLandmark.INDEX_FINGER_TIP:
                                LEFT_INDEX_FINGER_TIP_X, LEFT_INDEX_FINGER_TIP_Y = w_original-int(lm.x*w_original), int(lm.y*h_original)


        #########################
        #   GET NEW BACKGROUND  #
        #########################
        framePy = myAux.frameCV2Py(frameCV)
        screen.blit(framePy, (0, 0))

        #################
        # PROCESS DATA  #
        #################
        if LEFT_INDEX_FINGER_TIP_X != -1:
            raio_bola_left = 15
            left = pygame.draw.circle(screen, Player_color, (LEFT_INDEX_FINGER_TIP_X, LEFT_INDEX_FINGER_TIP_Y), raio_bola_left)

        if RIGHT_INDEX_FINGER_TIP_X != -1:
            raio_bola_right = 15
            right = pygame.draw.circle(screen, Opponent_color, (RIGHT_INDEX_FINGER_TIP_X, RIGHT_INDEX_FINGER_TIP_Y), raio_bola_right)

        #########################
        #   PLAYER CONTROLLERS  #
        #########################
        if LEFT_INDEX_FINGER_TIP_Y == -1:
            if len(player_y_list) != 0:
                player_y = player_y_list[len(player_y_list)-1]
            else:
                player_y = 100
        else:
            player_y = LEFT_INDEX_FINGER_TIP_Y

        error_player = controller_filter(player_y_list, player_y) - (player.y + playerLength/2)
        command_player = Controller_Kp*error_player
        player.y = controller_lim(player.y + command_player, controller_min, controller_max)

        #############################
        #   OPPONENT CONTROLLERS    #
        #############################
        if multiplayer:
            if RIGHT_INDEX_FINGER_TIP_Y == -1:
                if len(opponent_y_list) != 0:
                    opponent_y = opponent_y_list[len(opponent_y_list)-1]
                else:
                    opponent_y = 100
            else:
                opponent_y = RIGHT_INDEX_FINGER_TIP_Y

        error_opponent = controller_filter(opponent_y_list, opponent_y) - (opponent.y + playerLength/2)
        command_opponent = Controller_Kp*error_opponent
        opponent.y = controller_lim(opponent.y + command_opponent, controller_min,controller_max)

        # tip to menu
        if rectmenu.collidepoint(RIGHT_INDEX_FINGER_TIP_X, RIGHT_INDEX_FINGER_TIP_Y) or rectmenu.collidepoint(LEFT_INDEX_FINGER_TIP_X, LEFT_INDEX_FINGER_TIP_Y):
            return

        #####################
        #   BALL PHYSICS    #
        #####################
        ball.x += ballSpeedX/abs(ballSpeedX)*(abs(ballSpeedX)+dtime*deltaSpeed) * deltaTime
        ball.y += ballSpeedY/abs(ballSpeedY)*(abs(ballSpeedY)+dtime*deltaSpeed) * deltaTime

        if ball.colliderect(player):
            ballSpeedX = +ballSpeed
            ball.x += ballSpeedX * deltaTime
            ball.y += ballSpeedY * deltaTime
            pygame.mixer.Sound.play(Paddle)

        if ball.colliderect(opponent):
            ballSpeedX = -ballSpeed
            ball.x += ballSpeedX * deltaTime
            ball.y += ballSpeedY * deltaTime
            pygame.mixer.Sound.play(Paddle)

        if ball.top <= topBar:
            ballSpeedY = ballSpeed
            pygame.mixer.Sound.play(Wall)

        if ball.bottom >= h_original:
            ballSpeedY = -ballSpeed
            pygame.mixer.Sound.play(Wall)

        if ball.left <= 0:
            ballSpeedX = ballSpeed
            playerScore += 1
            dtime = 0
            ball.x = w_original/2
            ball.y = h_original/2
            pygame.mixer.Sound.play(Score)

        if ball.right >= w_original:
            ballSpeedX = -ballSpeed
            opponentScore += 1
            dtime = 0
            ball.x = w_original/2
            ball.y = h_original/2
            pygame.mixer.Sound.play(Score)

        if  opponentScore >= 3:
            myAux.winner_screen(camera, window, 1)
            pygame.display.update()
            pygame.event.pump()
            pygame.time.delay(1500)
            return

        if  playerScore >= 3:
            myAux.winner_screen(camera, window, 2)
            pygame.display.update()
            pygame.event.pump()
            pygame.time.delay(1500)
            return

        #################
        #   DRAW GAME   #
        #################
        # to show scores
        if opponentScore == 0:
            window.blit(imgscore_0_0, rectscore_0_0)
        if playerScore == 0:
            window.blit(imgscore_0, rectscore_0)
        if playerScore == 1:
            window.blit(imgscore_1, rectscore_1)
        if opponentScore == 1:
            window.blit(imgscore_1_1, rectscore_1_1)
        if playerScore == 2:
            window.blit(imgscore_2, rectscore_2)
        if opponentScore == 2:
            window.blit(imgscore_2_2, rectscore_2_2)
        if playerScore == 3:
            window.blit(imgscore_3, rectscore_3)
        if opponentScore == 3:
            window.blit(imgscore_3_3, rectscore_3_3)
        window.blit(imgmenu, rectmenu)
        window.blit(imgsep, rectsep)
        pygame.draw.ellipse(screen, (3, 173, 254), ball)
        pygame.draw.rect(screen, Player_color, player)
        pygame.draw.rect(screen, Opponent_color, opponent)

        # Flip the display
        pygame.display.flip()

        dtime += 1


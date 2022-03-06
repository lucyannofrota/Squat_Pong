import pygame
from pygame import *
import myTools as myAux
import pyautogui
import sys
import images

pygame.init()
Screen_Width, Screen_Height = pyautogui.size()
window = pygame.display.set_mode((Screen_Width, Screen_Height))

# Sounds
mixer.init()
#Paddle = mixer.Sound("Sounds/Paddle.wav")
#Wall = mixer.Sound("Sounds/Wall.wav")
Score = mixer.Sound("Sounds/Score.wav")

scale = 0.7
score_size = [scale*250, scale*100]

menu_size = [scale*250, scale*100]
sep_size = [scale*1920, scale*50]

# imagens
# score_0
imgscore_0, rectscore_0 = images.load_image(file_name='Images/score_0.png',
                                            img_size=score_size,
                                            translation=(-4, 10))


imgscore_0_0, rectscore_0_0 = images.load_image(file_name='Images/score_0_0.png',
                                                img_size=score_size,
                                                translation=(6, 10))
# score_1
imgscore_1, rectscore_1 = images.load_image(file_name='Images/score_1.png',
                                            img_size=score_size,
                                            translation=(-4, 10))

imgscore_1_1, rectscore_1_1 = images.load_image(file_name='Images/score_1_1.png',
                                                img_size=score_size,
                                                translation=(6, 10))

# score_2
imgscore_2, rectscore_2 = images.load_image(file_name='Images/score_2.png',
                                            img_size=score_size,
                                            translation=(-4, 10))

imgscore_2_2, rectscore_2_2 = images.load_image(file_name='Images/score_2_2.png',
                                            img_size=score_size,
                                            translation=(6, 10))

# score_3
imgscore_3, rectscore_3 = images.load_image(file_name='Images/score_3.png',
                                            img_size=score_size,
                                            translation=(-4, 10))

imgscore_3_3, rectscore_3_3 = images.load_image(file_name='Images/score_3_3.png',
                                            img_size=score_size,
                                            translation=(6, 10))
# Menu
imgmenu, rectmenu = images.load_image(file_name='Images/menu.png',
                                      img_size=menu_size,
                                      translation=(1,10))

# background
imgBg, rectBg = images.load_image(file_name='Images/arcade.jpg',
                                  img_size=(1920, 1080),
                                  translation=(1,1))

# separação
imgsep, rectsep = images.load_image(file_name='Images/sep_op1.png',
                                    img_size=sep_size,
                                    translation=(1, 16))

# retangulo semi transparente
menuBg = pygame.Surface((0.7*Screen_Width, 120))
menuBg.fill((255,255,255))
menuBg.set_alpha(100)
menuBgPos = [(Screen_Width - scale*Screen_Width)/2, (Screen_Height - scale*Screen_Height)/2]

topBar = 0 #Screen_Height / 2 - 16 * sep_size[1] / 2


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


def startgame(screen, in_Winputs, Max, Min):
    state: 1
    pygame.time.delay(500)

    # Valores Máximos de Cada Jogador
    Max_Player, Max_Opponent, = Max
    Min_Player, Min_Opponent = Min

    #####################
    #   GET FIRST FRAME #
    #####################

    w_original,h_original = pygame.display.get_surface().get_size()

    #############
    #   PYGAME  #
    #############
    clock = pygame.time.Clock()

    Winputs = myAux.webcamInputs(webcamInputs=in_Winputs, vid_stream=in_Winputs.vid_stream, offset=in_Winputs.offset,
                                 detector='FaceDetection', subSampling=0)

    Winputs_Hands = myAux.webcamInputs(vid_stream=in_Winputs.vid_stream,subSampling=0,scale=in_Winputs.scale,windowRes=in_Winputs.windowRes,offset=in_Winputs.offset,detector='GameHand')
    # Winputs = myAux.webcamInputs(vid_stream=in_Winputs.vid_stream,subSampling=0,src=0,scale=0.7,windowRes=(1920,1080),offset=in_Winputs.offset,detector='GameHand')

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
    player = pygame.Rect( 0, h_original/2, playerThickness, playerLength)

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
        window.fill((0, 0, 0))
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
        # (retval, frameHeight, frameWidth, frameChannels, frameCV) = myAux.getNewFrameOpenCV(camera, Screen_Width, Screen_Height)
        frameCV, face = Winputs.get_inputs()
        frameCV, hands = Winputs_Hands.get_inputs()
        # frameCV_RGB = cv2.cvtColor(frameCV, cv2.COLOR_BGR2RGB)


        #########################
        #   GET NEW BACKGROUND  #
        #########################
        # framePy = myAux.frameCV2Py(frameCV)
        # print(Winputs.offset)
        window.blit(imgBg, rectBg)
        screen.blit(frameCV, Winputs.offset)

        #################
        # PROCESS DATA  #
        #################
        if face[1][1] != -1:
            raio_bola_left = 15
            left = pygame.draw.circle(screen, Player_color, (face[1][0], face[1][1]), raio_bola_left)

        if face[0][1] != -1:
            raio_bola_right = 15
            right = pygame.draw.circle(screen, Opponent_color, (face[0][0], face[0][1]), raio_bola_right)

        #########################
        #   PLAYER CONTROLLERS  #
        #########################
        if face[1][1] == -1:
            if len(player_y_list) != 0:
                player_y = player_y_list[len(player_y_list)-1]
            else:
                player_y = 100
        else:
            # Normalização Do Y do Player
            y_norm = (face[1][1] - Min_Player)/(Max_Player - Min_Player)
            player_y = face[1][1] * y_norm

        error_player = controller_filter(player_y_list, player_y) - (player.y + playerLength/2)
        command_player = Controller_Kp*error_player
        player.y = controller_lim(player.y + command_player, controller_min, controller_max)

        #############################
        #   OPPONENT CONTROLLERS    #
        #############################
        if multiplayer:
            if face[0][1] == -1:
                if len(opponent_y_list) != 0:
                    opponent_y = opponent_y_list[len(opponent_y_list)-1]
                else:
                    opponent_y = 100
            else:
                # Normalização Do Y do Opponent
                y_norm = (face[0][1] - Min_Opponent) / (Max_Opponent - Min_Opponent)
                opponent_y = face[0][1] * y_norm

        error_opponent = controller_filter(opponent_y_list, opponent_y) - (opponent.y + playerLength/2)
        command_opponent = Controller_Kp*error_opponent
        opponent.y = controller_lim(opponent.y + command_opponent, controller_min,controller_max)

        # tip to menu
        if rectmenu.collidepoint(hands[0][0], hands[0][1]) or rectmenu.collidepoint(hands[0][0], hands[0][1]):
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
            #pygame.mixer.Sound.play(Paddle)

        if ball.colliderect(opponent):
            ballSpeedX = -ballSpeed
            ball.x += ballSpeedX * deltaTime
            ball.y += ballSpeedY * deltaTime
            #pygame.mixer.Sound.play(Paddle)

        if ball.top <= topBar:
            ballSpeedY = ballSpeed
            #pygame.mixer.Sound.play(Wall)

        if ball.bottom >= h_original:
            ballSpeedY = -ballSpeed
            #pygame.mixer.Sound.play(Wall)

        if ball.left <= 0:
            ballSpeedX = ballSpeed
            playerScore += 1
            dtime = 0
            ball.x = w_original/2
            ball.y = h_original/2
            #pygame.mixer.Sound.play(Score)

        if ball.right >= w_original:
            ballSpeedX = -ballSpeed
            opponentScore += 1
            dtime = 0
            ball.x = w_original/2
            ball.y = h_original/2
            #pygame.mixer.Sound.play(Score)

        if  opponentScore >= 1:
            myAux.winner_screen(window,in_Winputs, 1)
            pygame.display.update()
            pygame.event.pump()
            pygame.time.delay(1500)
            return

        if  playerScore >= 1:
            myAux.winner_screen(window, in_Winputs, 2)
            pygame.display.update()
            pygame.event.pump()
            pygame.time.delay(1500)
            return

        #################
        #   DRAW GAME   #
        #################
        # to show scores
        window.blit(menuBg, menuBgPos) # draw menu background
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


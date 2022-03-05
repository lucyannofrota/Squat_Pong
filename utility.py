import imutils
from imutils.video import VideoStream
import cv2

#Hand Detector
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

class webcamInputs:
    def __init__(self,vid_stream=[],src=0,scale=0.7,windowRes=(1920,1080),detector='Menu'):
        if(vid_stream == []):
            self.vid_stream = VideoStream(src=src).start()
        else:
            self.vid_stream = vid_stream
        self.windowRes = windowRes
        self.scale = scale


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

        self.subSampCounter = 0

        self.l_frame = []
        self.l_detected = []

    # def GameHand():


    def get_inputs(self,subSampling=0):
        if(self.subSampCounter >= (subSampling-1) or self.l_frame == []):
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
                            self.l_hands[0] = (x*self.hscale[0],y*self.hscale[1])
                        else:
                            self.l_hands[1] = (x*self.hscale[0],y*self.hscale[1])

            else:
                if self.detectorType == 'GameHand':
                    # detected, frame = self.detector.findHands(frame, flipType=False)
                    # frame = cv2.resize(frame, (self.outRes[0], self.outRes[1]), interpolation=cv2.INTER_AREA)
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
                                        x, y = self.windowRes[0]-int(lm.x*self.windowRes[0]), int(lm.y*self.windowRes[1])
                                        self.l_hands[1] = (x*self.hscale[0],y*self.hscale[1])
                            # LEFT HAND #
                            if handedness_dict1['classification'][0]['label'] == 'Left':
                                # EACH POINTS OF THE HAND #
                                for id, lm in enumerate(handLms.landmark):
                                    if id == self.mp_hands.HandLandmark.INDEX_FINGER_TIP:
                                        x, y = self.windowRes[0]-int(lm.x*self.windowRes[0]), int(lm.y*self.windowRes[1])
                                        self.l_hands[0] = (x*self.hscale[0],y*self.hscale[1])

            frame = cv2.resize(frame, (self.outRes[0], self.outRes[1]), interpolation=cv2.INTER_AREA)
            self.l_frame = frame
            self.subSampCounter = 0

        self.subSampCounter += 1

        if self.detectorType == 'Menu':
            return self.l_frame, self.l_hands
        else:
            if self.detectorType == 'GameHand':
                return self.l_frame, self.l_hands

import imutils
from imutils.video import VideoStream
import cv2

class webcamInputs:
    def __init__(self,src=0,scale=0.7,windowRes=(1920,1080),detector=[]):
        self.vid_stream = VideoStream(src=src).start()
        self.windowRes = windowRes
        self.scale = scale


        self.outRes = (round(self.windowRes[0]*scale),round(self.windowRes[1]*scale))
        frame = self.vid_stream.read()
        height, width = frame.shape[0], frame.shape[1]
        self.hscale = (self.outRes[0]/width,self.outRes[1]/height)

        self.detector = detector

        self.subSampCounter = 0

        self.l_frame = []
        self.l_hands = []


    def get_inputs(self,subSampling=0,menu=True):
        if(self.subSampCounter >= (subSampling-1) or self.l_frame == []):
            frame = self.vid_stream.read()
            frame = cv2.flip(frame, 1)

            if self.detector == []:
                frame = cv2.resize(frame, (round(self.windowRes[0]*scale), round(self.windowRes[1]*scale)), interpolation=cv2.INTER_AREA)
                hands = []
            else:
                if menu == True:
                    hands, frame = self.detector.findHands(frame, flipType=False)
                    frame = cv2.resize(frame, (self.outRes[0], self.outRes[1]), interpolation=cv2.INTER_AREA)
                else:
                    b = []

            self.l_frame = frame
            self.l_hands = hands
            # print(self.subSampCounter)
            self.subSampCounter = 0
        self.subSampCounter += 1
        return self.l_frame, self.l_hands, self.hscale

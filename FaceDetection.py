import cv2
import math
from typing import List, Mapping, Optional, Tuple, Union
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

circle_radius = 5
color = (0, 0, 255)
thickness = 10


def _normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int,
    image_height: int) -> Union[None, Tuple[int, int]]:
  """Converts normalized value pair to pixel coordinates."""

  # Checks if the float value is between 0 and 1.
  def is_valid_normalized_value(value: float) -> bool:
    return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                      math.isclose(1, value))

  if not (is_valid_normalized_value(normalized_x) and
          is_valid_normalized_value(normalized_y)):
    # TODO: Draw coordinates even if it's outside of the image bounds.
    return None
  x_px = min(math.floor(normalized_x * image_width), image_width - 1)
  y_px = min(math.floor(normalized_y * image_height), image_height - 1)
  return x_px, y_px


# For webcam input:
cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)
        image_rows, image_cols, _ = image.shape

        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.detections:
            for detection in results.detections:
                # Indice 0: Olho Direito
                # Indice 1: Olho Esquerdo
                # Indice 2: Nariz
                # Indice 3: Meio da Boca
                # Indice 4: Ouvido Direito
                # Indice 5: Olho
                location_1 = detection.location_data.relative_keypoints[4]
                location = detection.location_data.relative_keypoints
                location_px = _normalized_to_pixel_coordinates(location_1.x, location_1.y,
                                                               image_cols, image_rows)
                cv2.circle(image, location_px, circle_radius, color, thickness)

                #mp_drawing.draw_detection(image, location_px)
                #for keypoint in location:
                    #keypoint_px = _normalized_to_pixel_coordinates(keypoint.x, keypoint.y,
                    #                                               image_cols, image_rows)
                    #cv2.circle(image, keypoint_px, circle_radius, color, thickness)
                #mp_drawing.draw_detection(image, detection)
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()

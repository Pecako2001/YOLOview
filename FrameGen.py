import cv2
import os
import numpy as np
import random

class framegen:
    def generator(self, video):
        # Read the video from the specified path
        cam = cv2.VideoCapture(video)

        try:
            # Creating a folder named 'data'
            if not os.path.exists('data'):
                os.makedirs('data')
        except OSError:
            print('Error: Creating directory of data')

        # Frame counter
        currentframe = 0

        while(True):
            # Reading from frame
            ret, frame = cam.read()

            if ret:
                # If the video is still playing, continue creating images every 500 frames
                if currentframe % 20 == 0:
                    name = './data/frame' + str(currentframe) + str(video) +'.jpg'
                    print('Creating...' + name)
                    cv2.imwrite(name, frame)

                    # 1. Grayscaling
                    name = './data/frame' + str(currentframe) + str(video) + 'grayscale.jpg'
                    grayscale_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(name, grayscale_img)

                    # 2. Rotation
                    name = './data/frame' + str(currentframe) + str(video) +  'rotated.jpg'
                    angle =  random.randrange(0,360,1)
                    rows, cols, _ = frame.shape
                    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
                    rotated_img = cv2.warpAffine(frame, M, (cols, rows))
                    cv2.imwrite(name, rotated_img)

                    # 3. Resizing
                    name = './data/frame' + str(currentframe) + str(video) +  'resized.jpg'
                    temp = random.randrange(100,1000,1)
                    resized_img = cv2.resize(frame, (temp, temp))
                    cv2.imwrite(name, resized_img)

                    # 4. Cropping
                    #name = './data/frame' + str(currentframe) + str(video) +  'cropped.jpg'
                    #cropped_img = frame[100:400, 100:400]
                    #cv2.imwrite(name, cropped_img)

                    # 5. Flipping
                    name = './data/frame' + str(currentframe) + str(video) +  'flipped.jpg'
                    temp = random.randrange(-1,1,1)
                    flipped_img = cv2.flip(frame, temp)
                    cv2.imwrite(name, flipped_img)

                    # 6. Blurring
                    name = './data/frame' + str(currentframe) + str(video) +  'blurred.jpg'
                    temp = random.choice(range(1, 26, 2))
                    blurred_img = cv2.GaussianBlur(frame, (temp, temp), 0)
                    cv2.imwrite(name, blurred_img)

                    # 7. Sharpening
                    name = './data/frame' + str(currentframe) + str(video) +  'sharpened.jpg'
                    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                    sharpened_img = cv2.filter2D(frame, -1, kernel)
                    cv2.imwrite(name, sharpened_img)

                    # 8. Edge Detection
                    #name = './data/frame' + str(currentframe) + str(video) +  'edges.jpg'
                    #edges_img = cv2.Canny(grayscale_img, 100, 200)
                    #cv2.imwrite(name, edges_img)

                    # 9. Negative Transformation
                    name = './data/frame' + str(currentframe) + str(video) +  'negative.jpg'
                    negative_img = 255 - frame
                    cv2.imwrite(name, negative_img)

                    # 10. Brightness Adjustment
                    name = './data/frame' + str(currentframe) + str(video) +  'brighter.jpg'
                    brighter_img = cv2.convertScaleAbs(frame, alpha=random.randrange(1,2,1), beta=random.randrange(20,30,1))
                    cv2.imwrite(name, brighter_img)

                # Increasing the counter so that it will show how many frames are created
                currentframe += 1
            else:
                break

        # Release all space and windows once done
        cam.release()
        cv2.destroyAllWindows()
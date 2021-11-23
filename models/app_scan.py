import cv2
import numpy as np
import streamlit as st
from models import utlis

###############################################
kernel = np.ones((5,5), np.uint8)
width, height = 540, 640
###############################################

def app():
    st.write(
        """
        # Demo app scan file picture
        """
    )
    pic_upload = st.file_uploader('Upload your picture', type =['jpg', 'png'])
    st.header('This is your image')
    if pic_upload is not None:
        thres_0 = st.slider("Threshold1", 200,255, 220, 5)
        thres_1 = st.slider("Threshold2", 200,255, 220, 5)
        file_bytes = np.asarray(bytearray(pic_upload.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        img = cv2.resize(img, (width, height))

        imgBlank = np.zeros((height,width, 3), np.uint8) # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
        # thres=utlis.valTrackbars() # GET TRACK BAR VALUES FOR THRESHOLDS
        # thres_0 = st.slider("Threshold1", 200,255, 220, 5)
        # thres_1 = st.slider("Threshold2", 200,255, 220, 5)
        imgThreshold = cv2.Canny(imgBlur,thres_0,thres_1) # APPLY CANNY BLUR
        kernel = np.ones((5, 5))
        imgDial = cv2.dilate(imgThreshold, kernel, iterations=2) # APPLY DILATION
        imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION

        ## FIND ALL COUNTOURS
        imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS


        # FIND THE BIGGEST COUNTOUR
        biggest, maxArea = utlis.biggestContour(contours) # FIND THE BIGGEST CONTOUR
        if biggest.size != 0:
            biggest=utlis.reorder(biggest)
            cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
            imgBigContour = utlis.drawRectangle(imgBigContour,biggest,2)
            pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0],[width, 0], [0, height],[width, height]]) # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (width, height))

            #REMOVE 20 PIXELS FORM EACH SIDE
            imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
            imgWarpColored = cv2.resize(imgWarpColored,(width,height))

            # APPLY ADAPTIVE THRESHOLD
            imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
            imgAdaptiveThre= cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
            imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
            imgAdaptiveThre=cv2.medianBlur(imgAdaptiveThre,3)

            # Image Array for Display
            imageArray = ([img,imgGray,imgThreshold,imgContours],
                        [imgBigContour,imgWarpColored, imgWarpGray,imgAdaptiveThre])

        else:
            imageArray = ([img,imgGray,imgThreshold,imgContours],
                        [imgBlank, imgBlank, imgBlank, imgBlank])

        # LABELS FOR DISPLAY
        lables = [["Original","Gray","Threshold","Contours"],
                ["Biggest Contour","Warp Prespective","Warp Gray","Adaptive Threshold"]]

        stackedImage = utlis.stackImages(imageArray,0.75,lables)
        st.image(stackedImage, channels="BGR")

        # img_copy = img.copy()
        # img_Erode = xu_ly_anh(img)
        # big_approx = do_duong_bao(img_Erode)
        # # big_approx
        # cv2.drawContours(img_copy, big_approx, -1, (255, 0, 0), 20)
        # if big_approx.size != 0:
        #     img_Warp = getWarp(img, big_approx)
        #     img_stack = ([img_copy, img_Warp])
        #     st.image(img_Warp, channels="BGR")
        # else:
        #     img_stack = ([img_copy, img])
        
        # stackedImages = stackImages(0.6, img_stack)

        # st.image(stackedImages, channels="BGR")




# cap = cv2.VideoCapture(1)
# cap.set(10,150)
# # cap.set(3,640)
# # cap.set(4,480)

# while True:
#     sucsess, img = cap.read()
#     img = cv2.resize(img, (width, height))
#     img_copy = img.copy()

#     img_Erode = xu_ly_anh(img)
#     big_approx = do_duong_bao(img_Erode)
#     cv2.drawContours(img_copy, big_approx, -1, (255, 0, 0), 20)

#     if big_approx.size != 0:
#         img_Warp = getWarp(img, big_approx)
#         img_stack = ([img_copy, img_Warp])
#         cv2.imshow("ImageWarped", img_Warp)
#     else:
#         img_stack = ([img_copy, img])
    
#     stackedImages = stackImages(0.6, img_stack)

#     cv2.imshow("WorkFlow", stackedImages)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
import cv2
import numpy as np
import streamlit as st
import utlis

###############################################
kernel = np.ones((5,5), np.uint8)
width, height = 540, 640
###############################################
# def xu_ly_anh(img):
#     img_Gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     img_Blur = cv2.GaussianBlur(img_Gray, (5,5), 1)
#     img_Canny = cv2.Canny(img_Blur, 100, 100)
#     img_Dilate = cv2.dilate(img_Canny, kernel, iterations= 2)
#     img_Erode = cv2.erode(img_Dilate, kernel, iterations= 1)
#     return img_Erode

# def do_duong_bao(img):
#     contours,hierarchy = cv2.findContours(img ,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
#     max_area = 0
#     big_approx = np.array([])
#     for cnt in contours:
#         area = cv2.contourArea(cnt)
#         if area > 500:
#             peri = cv2.arcLength(cnt,True)
#             approx = cv2.approxPolyDP(cnt,0.02*peri,True)
#             len_ = len(approx)
#             if len_ == 4 and area > max_area:
#                 max_area = area
#                 big_approx = approx
#     return big_approx

# # lay 4 diem cua khung hinh
# def lay_4_diem (myPoints):
#     myPoints = myPoints.reshape((4,2))
#     myPointsNew = np.zeros((4,1,2),np.int32)
#     add = myPoints.sum(1)
#     myPointsNew[0] = myPoints[np.argmin(add)]
#     myPointsNew[3] = myPoints[np.argmax(add)]
#     diff = np.diff(myPoints,axis=1)
#     myPointsNew[1]= myPoints[np.argmin(diff)]
#     myPointsNew[2] = myPoints[np.argmax(diff)]
#     return myPointsNew

# def getWarp(img, big_approx):
#     # img = xu_ly_anh(img)
#     # big_approx = do_duong_bao(img)
#     _4_diem = lay_4_diem(big_approx)
#     pts1 = np.float32(_4_diem)
#     pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
#     matrix = cv2.getPerspectiveTransform(pts1, pts2)
#     img_output = cv2.warpPerspective(img, matrix, (width, height))
#     img_resize = cv2.resize(img_output,(width,height))
#     return img_resize

# def stackImages(scale,imgArray):
#     rows = len(imgArray)
#     cols = len(imgArray[0])
#     rowsAvailable = isinstance(imgArray[0], list)
#     width = imgArray[0][0].shape[1]
#     height = imgArray[0][0].shape[0]
#     if rowsAvailable:
#         for x in range ( 0, rows):
#             for y in range(0, cols):
#                 if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
#                     imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
#                 else:
#                     imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
#                 if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
#         imageBlank = np.zeros((height, width, 3), np.uint8)
#         hor = [imageBlank]*rows
#         hor_con = [imageBlank]*rows
#         for x in range(0, rows):
#             hor[x] = np.hstack(imgArray[x])
#         ver = np.vstack(hor)
#     else:
#         for x in range(0, rows):
#             if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
#                 imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
#             else:
#                 imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
#             if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
#         hor= np.hstack(imgArray)
#         ver = hor
#     return ver

def app():
    st.write(
        """
        # Demo app scan file picture
        """
    )
    pic_upload = st.file_uploader('Upload your picture', type =['jpg', 'png'])
    st.header('This is your image')
    if pic_upload is not None:
        file_bytes = np.asarray(bytearray(pic_upload.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        img = cv2.resize(img, (width, height))

        imgBlank = np.zeros((height,width, 3), np.uint8) # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
        thres=utlis.valTrackbars() # GET TRACK BAR VALUES FOR THRESHOLDS
        imgThreshold = cv2.Canny(imgBlur,thres[0],thres[1]) # APPLY CANNY BLUR
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
            pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

            #REMOVE 20 PIXELS FORM EACH SIDE
            imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
            imgWarpColored = cv2.resize(imgWarpColored,(widthImg,heightImg))

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
import cv2 
import numpy as np 
#from picamera import PiCamera
#from picamera.array import PiRGBArray



#load templates
up = cv2.imread("templates//upt.png",0)
ret,upt = cv2.threshold(up,127,255, cv2.THRESH_BINARY_INV)

down = cv2.imread("templates//downt.png",0)
ret,downt = cv2.threshold(down,127,255, cv2.THRESH_BINARY_INV)

left = cv2.imread("templates//leftt.png",0)
ret,leftt = cv2.threshold(left,127,255, cv2.THRESH_BINARY_INV)

right = cv2.imread("templates//rightt.png",0)
ret,rightt = cv2.threshold(right,127,255, cv2.THRESH_BINARY_INV)

_1 = cv2.imread("templates//_1t.png",0)
ret,_1t = cv2.threshold(_1,127,255, cv2.THRESH_BINARY_INV)

_2 = cv2.imread("templates//_2t.png",0)
ret,_2t = cv2.threshold(_2,127,255, cv2.THRESH_BINARY_INV)

_3 = cv2.imread("templates//_3t.png",0)
ret,_3t = cv2.threshold(_3,127,255, cv2.THRESH_BINARY_INV)

_4 = cv2.imread("templates//_4t.png",0)
ret,_4t = cv2.threshold(_4,127,255, cv2.THRESH_BINARY_INV)

_5 = cv2.imread("templates//_5t.png",0)
ret,_5t = cv2.threshold(_5,127,255, cv2.THRESH_BINARY_INV)

a = cv2.imread("templates//at.png",0)
ret,at = cv2.threshold(a,127,255, cv2.THRESH_BINARY_INV)
a = cv2.Canny(a, 50, 200)

b = cv2.imread("templates//bt.png",0)
ret,bt = cv2.threshold(b,127,255, cv2.THRESH_BINARY_INV)

c = cv2.imread("templates//ct.png",0)
ret,ct = cv2.threshold(c,127,255, cv2.THRESH_BINARY_INV)

d = cv2.imread("templates//dt.png",0)
ret,dt = cv2.threshold(d,127,255, cv2.THRESH_BINARY_INV)

e = cv2.imread("templates//et.png",0)
ret,et = cv2.threshold(e,127,255, cv2.THRESH_BINARY_INV)

cir = cv2.imread("templates//cirt.png",0)
ret,cirt = cv2.threshold(cir,127,255, cv2.THRESH_BINARY_INV)

contours_up, hierachy_up = cv2.findContours(upt,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_down, hierachy_down = cv2.findContours(downt,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_left, hierachy_left = cv2.findContours(leftt,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_right, hierachy_right = cv2.findContours(rightt,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours_1, hierachy_1 = cv2.findContours(_1t,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_2, hierachy_2 = cv2.findContours(_2t,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_3, hierachy_3 = cv2.findContours(_3t,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_4, hierachy_4 = cv2.findContours(_4t,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_5, hierachy_5 = cv2.findContours(_5t,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours_a, hierachy_a = cv2.findContours(at,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_b, hierachy_b = cv2.findContours(bt,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_c, hierachy_c = cv2.findContours(ct,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_d, hierachy_d = cv2.findContours(dt,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_e, hierachy_e = cv2.findContours(et,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours_cir, hierachy_cir = cv2.findContours(cirt,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

templates_cnt = {'blue': [contours_1[0], contours_d[0], contours_left[0]],
                 'green': [contours_2[0], contours_b[0], contours_right[0]],
                 'red': [contours_3[0], contours_a[0], contours_down[0]],
                 'white': [contours_4[0], contours_c[0], contours_up[0]],
                 'yellow': [contours_5[0], contours_e[0], contours_cir[0]]}

templatesName = {'blue': ['1', 'D', 'left'],
                 'green': ['2', 'B', 'right'],
                 'red': ['3', 'A', 'down'],
                 'white': ['4', 'C', 'up'],
                 'yellow': ['5', 'E', 'circle']}

templatesSize = {'blue': [_1.shape[:2], d.shape[:2], left.shape[:2]],
                 'green': [_2.shape[:2], b.shape[:2], right.shape[:2]],
                 'red': [_3.shape[:2], a.shape[:2], down.shape[:2]],
                 'white': [_4.shape[:2], c.shape[:2], up.shape[:2]],
                 'yellow': [_5.shape[:2], e.shape[:2], cir.shape[:2]]}

templatesIndex = {'blue': [6, 14, 4],
                 'green': [7, 12, 3],
                 'red': [8, 11, 2],
                 'white': [9, 13, 1],
                 'yellow': [10, 15, 5]}

templatesMatch = {'blue': [_1t, dt, leftt],
                  'green': [_2t, bt, rightt],
                  'red': [_3t, at, downt],
                  'white': [_4t, ct, upt],
                  'yellow': [_5t, et, cirt]}

#print(templates_cnt)

############################################################################
#threshold settings

imagTaken=0
rectangle_left_masking_height = 10
rectangle_right_masking_height = 10
rectangle_top_masking_height = 200
rectangle_btm_masking_height = 30
ret_margin_threshold = 0.2

# the largest ret value from sampling
ret_threshold = {'blue': [0.9590938909326517, 0.027731239646934802, 0.10811550487408136],
                 'green': [0.9918321013166647, 0.04651825790402825, 0.08749998916573853],
                 'red': [1.4275981072950545, 0.1804923339535247, 0.13453766020302216],
                 'white': [0.12847745281465406, 0.9157420172441716, 0.09564249503367056],
                 'yellow':[0.8049514394640092, 0.907807402642542, 0.0025588783637848778]}

match_template_margin = 0.8
match_template_threshold = {'blue': [0.2836098074913025*match_template_margin, 0.8332169651985168*match_template_margin, 0.8435372710227966*match_template_margin],
                            'green': [0.7369934320449829*match_template_margin, 0.7381596565246582*match_template_margin, 0.8470184206962585*match_template_margin],
                            'red': [0.754944384098053*match_template_margin, 0.848374605178833*match_template_margin, 0.8675277233123779*match_template_margin],
                            'white': [0.6084819436073303*match_template_margin, 0.823283314704895*match_template_margin, 0.8667778372764587*match_template_margin],
                            'yellow':[0.759052038192749*match_template_margin, 0.65*match_template_margin, 0.8877317905426025*match_template_margin]}

contour_area_threshold = 1000

############################################################################

def extractRed(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define range of red color in HSV
    lower_red = np.array([0, 100,40])
    upper_red = np.array([15,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
 
    # Range for upper range
    lower_red = np.array([140,100,40])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_red,upper_red)
 
    # Generating the final mask to detect red color
    mask = mask1+mask2
    #cv2.imshow('red',mask)
    #cv2.waitKey()

    return mask

def extractGreen(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define range of green color in HSV
    lower_green = np.array([35,70,35])
    upper_green = np.array([105,255,255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
 
    #cv2.imshow('green',mask)
    #cv2.waitKey()

    return mask

def extractBlue(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([90,70,40])
    upper_blue = np.array([116,255,255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
 
    #cv2.imshow('blue',mask)
    #cv2.waitKey()

    return mask

def extractYellow(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define range of red color in HSV
    lower_yellow = np.array([15,70,50])
    upper_yellow = np.array([35,255,255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
 
    #cv2.imshow('yellow',mask)
    #cv2.waitKey()

    return mask

def extractWhite(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define range of white color in HSV
    lower_red = np.array([0,0,100])
    upper_red = np.array([255,110,255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
 
    #cv2.imshow('white',mask)
    #cv2.waitKey()

    return mask

def capture():
    resol = (640,480)
    
    camera = PiCamera()
    camera.resolution = resol
    
    output = PiRGBArray(camera)
    camera.capture(output,'bgr')
    src = output.array
    #print 'Capture %dx%d image' %(src.shape[1], src.shape[0])
    
    return src
    
#image processing and detection
def ScanImage(debug, image):
    found = False
    global imagTaken
    imagTaken += 1
    
    colours = ['blue', 'green', 'red', 'white', 'yellow']
    extractColour = [extractBlue, extractGreen, extractRed, extractWhite, extractYellow]

    # crop
    image = image[rectangle_top_masking_height : 480 - rectangle_btm_masking_height, rectangle_left_masking_height : 640 - rectangle_right_masking_height]
    width = 640 - rectangle_left_masking_height - rectangle_right_masking_height

    possible_ret = []
    possible_colour = []
    possible_template_index = []
    possible_match_contour = []
    possible_area = []
    possible_margin = []
    possible_matching = []

    for i in range(len(colours)):
        colour = colours[i]
        p("colour "+colour, debug)

        gray = extractColour[i](image)
        gray = cv2.GaussianBlur(gray, (3,3),0)
        x = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        contours, hierachy = cv2.findContours(gray, 1, cv2.CHAIN_APPROX_SIMPLE)
            
        # find the possible matched contours
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if(area > contour_area_threshold):
                p("match area threshold" + str(area), debug)

                for template_index in range(3):
                    ret = cv2.matchShapes(cnt, templates_cnt[colour][template_index], 1, 0.0)
                    th = ret_threshold[colour][template_index]
                    margin = (ret - th) / th
                    p('   '+str(ret)+' '+str(margin), debug)

                    if margin < ret_margin_threshold:
                        # crop and match
                        # template size (88,88), image in template roughly (66,66)
                        try:
                            x,y,w,h = cv2.boundingRect(cnt)
                            half_side = max(w,h) / 2.0
                            new_half_side = half_side / 33.0 * 40.0
                            centre_x = x + w/2.0
                            centre_y = y + h/2.0
                            x_crop = max(centre_x - new_half_side, 0)
                            y_crop = max(centre_y - new_half_side, 0)
                            gray_crop = gray[int(y_crop) : int(centre_y + new_half_side), int(x_crop) : int(centre_x + new_half_side)]
                            gray_crop = cv2.resize(gray_crop, (88,88))
                            p(str(x_crop) +' '+ str(y_crop) + ' ' + str(half_side), debug)

                            match_result = cv2.matchTemplate(gray_crop, templatesMatch[colour][template_index], cv2.TM_CCOEFF_NORMED)
                            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(match_result)
                            p("      match result: "+ str(maxVal), debug)
                        
                            if debug:
                                cv2.imshow('hahaha', gray_crop)
                                cv2.waitKey()

                            if maxVal > match_template_threshold[colour][template_index]:
                                possible_ret.append(ret)
                                possible_colour.append(colour)
                                possible_template_index.append(template_index)
                                possible_match_contour.append(cnt)
                                possible_area.append(area)
                                possible_margin.append(margin)
                                possible_matching.append(maxVal)
                                
                        except Exception as e:
                            print( "------error in template match:" + str(e))

    if (len(possible_matching) == 0):
        return '-1|0|0'
    else:
        p("possible contours found", debug)

    # find the best matched template
    best_matching = max(possible_matching)
    best_index = possible_matching.index(best_matching)
    best_ret = possible_ret[best_index]
    best_colour = possible_colour[best_index]
    best_template_index = possible_template_index[best_index]
    best_match_contour = possible_match_contour[best_index]
    best_area = possible_area[best_index]
        
    # draw bounding rectangle
    x, y, w, h = cv2.boundingRect(best_match_contour)
    cv2.rectangle(image, (int(x-2),int(y-2),int(w+4),int(h+4)), (0, 0, 255), 2)
    cv2.putText(image, templatesName[best_colour][best_template_index], ((int(x)), int(y)-15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 1, cv2.LINE_AA)
    saveimag(debug, "test_Match.png", image)
    p("width of image: "+ str(w), debug)
    p("top: "+ str(y), debug)
    p("btm: "+ str((y+h)), debug)

    # check position of the image
    l = int((x + w/4) / (width/3))
    r = int((x + w/4*3) / (width/3))
    if l == 1 and r == 2:
        pos = 2
    else:
        pos = l

    imag_index = templatesIndex[best_colour][best_template_index]
    return "1|" + str(imag_index) + "|" + str(pos)

def p(str, debug):
    if(debug):
        print(str)

def saveimag(debug, filename, imag):
    global imagTaken
    if (debug):
        cv2.imwrite(str(imagTaken) + filename, imag)

def main():
    for i in range(1,8):
        print('image', i)
        image = cv2.imread('images/'+str(i)+'.png')
        res = ScanImage(1, image)
        print(res)
        cv2.imshow("label", image)
        cv2.waitKey()
    
if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

#import argparse as arg

import numpy as np
import cv2 as cv
import os

# brg
MaskColor = (['backgroud', (0,0,0)],
             ['coal', (255, 0, 0)],
             ['stone', (0, 255, 0)],
             ['mix', (0, 0, 255)]
             )

calibration_size = (400, 400)
g_line_size = 8
g_init_on_mouse_callback = False
g_color = None
g_mask = None

def merge_image(img, mask):
    dst = img*0.7 + mask*.3
    return np.uint8(dst)

def get_mask_filename(strfn):
    path, ext = os.path.splitext(strfn)
    return path + "_mask.bmp"
def is_mask_file_ornot(strfn):
    path, fn = os.path.split(strfn)
    return fn.find('_mask.') > 0   

###################################################################
## Draw
###################################################################
drawing = False 
ix,iy=-1,-1
def drawing(event,x,y,flags, param):
    global ix,iy,drawing, g_line_size, g_mask
    
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy=x,y
        #print("EVENT_LBUTTONDOWN")
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            cv.line(g_mask, (ix,iy), (x,y), g_color, g_line_size)
            ix,iy=x,y
            #print("EVENT_MOUSEMOVE", color)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        #print("EVENT_LBUTTONUP")
        
###################################################################
## Draw One Color
###################################################################
def calibrate_one_color(img, mask_fn, maskcolor) -> int:
    global calibration_size, g_line_size, g_init_on_mouse_callback
    global g_color, g_mask
    
    print("---------------------------------------------------")
    path, fn = os.path.split(mask_fn)
    print("image:", fn, " label = ", maskcolor[0], ", color = ", maskcolor[1])

    g_color = maskcolor[1]
    
    wnd_name = 'calibrate'
    cv.namedWindow(wnd_name, 0)
    if g_init_on_mouse_callback is False:
        g_init_on_mouse_callback = True
        cv.setMouseCallback(wnd_name, drawing)

    return_val = 0
    while True:
        show_img = merge_image(img, g_mask)
        cv.imshow(wnd_name, show_img)
        k = cv.waitKeyEx(1)
        if k in [ord('q'), 27] :
            return_val = 0
            break
        elif k == 2490368:  # arraw up
            return_val = -1
            break
        elif k == 2621440:  # arraw down
            return_val = 1
            break
        elif k == 2424832:  # arraw left
            g_line_size = max(2, g_line_size - 2)
            print("line size = ", g_line_size)
        elif k == 2555904:  # arraw right
            g_line_size = min(16, g_line_size + 2) 
            print("line size = ", g_line_size)

    #cv.destroyWindow(wnd_name)
    return return_val
    
###################################################################
## Draw One Image
###################################################################
def calibrate_one_image(imgname) -> int:
    global g_mask
    # Read mask image    
    mask_fn = get_mask_filename(imgname)
    mask = None
    if os.path.exists(mask_fn):
        mask = cv.imdecode(np.fromfile(mask_fn, dtype=np.uint8), -1)
    else:
        mask = np.zeros((calibration_size[0],calibration_size[1],3),np.uint8)
        
    # Read src image
    src = cv.imdecode(np.fromfile(imgname, dtype=np.uint8), -1)
    if src is None:
        print("can't imread: ", imgname)
        return 0
    
    # Calibrate one class for resizeed image
    rsz = cv.resize(src, calibration_size)
    clsNum = len(MaskColor)
    clsidx = 0

    cv.namedWindow("src", 1)
    cv.imshow("src", rsz)
    
    g_mask = mask
    while True:
        next_idx = calibrate_one_color(rsz, mask_fn, MaskColor[clsidx])
        if next_idx == 0:
            print("Calibrate current image finish")
            break
        clsidx += next_idx
        if clsidx < 0:
            clsidx = 0
            print("Have been first class, can't backward again")
        if clsidx >= clsNum:
            clsidx = clsNum - 1
            print("Have been last class, can't forward again") 

    # Save Mask
    print("Save mask image: ", mask_fn)
    cv.imwrite(mask_fn, g_mask)
    #cv.imencode(np.fromfile(mask_fn, dtype=np.uint8), g_mask)
    
    cv.namedWindow("LastResult", 1)
    cv.imshow("LastResult", merge_image(rsz, g_mask))
    key = cv.waitKey(0)
    return_val = 0
    if key == ord('q'):
        print("Press key q")
        print("Current image has been calibarted finish, want to exit")
        return_val = 0
    elif key == ord('u'):
        print("Press key u: up")
        print("Want to calibrate last image")
        return_val =  -1
    elif key == ord('d'):
        print("Press key d: down")
        print("Want to calibrate next image")
        return_val =  1
    else:
        print("Press reset key, continue next image")
        return_val =  1
    cv.destroyWindow("LastResult")
    return return_val

def main(imgdir):
    print("=========================")
    print("imgdir=", imgdir)
    print("=========================")
    
    imglist = []
    # start loop directory, find all image for calibrating
    for subdir, dirs, files in os.walk(imgdir):
        for file in files:
            fullname = os.path.join(subdir, file)
            if is_mask_file_ornot(fullname) is False:
                imglist.append(fullname)
            #print(fullname)
            
    imgnum = len(imglist)
    if imgnum < 1:
        print("file folder empty")
        return
    
    idx = 0
    while True:
        nextid = calibrate_one_image(imglist[idx])
        if nextid == 0:
            print("Exit all!!!")
            break
        idx = idx + nextid
        if idx < 0:
            print("Processing first image, can't backward again")
            idx = 0
        if idx >= imgnum:
            print("Processing last image, can't forward again")  
            idx = imgnum - 1
       
    cv.destroyAllWindows();
    
if __name__ == '__main__':
    #parser = arg.ArgumentParser(description="parsing parameter")
    #parser.add_argument("--imgdir", help="procces image directory")
    #parser.add_argument("cls", type=int, help="segment class number")
    #parser.parse_args();
    #print(parser.imgdir)
    
    #imgdir = "C:\\SandyWork\\chongqing_work\\煤炭_岩石分类\\煤和岩石样本\\"
    imgdir = "C:\\SandyWork\\chongqing_work\\coal_stone_sample\\"
    #imgdir = "/C/SandyWork/chongqing_work/煤炭_岩石分类/煤和岩石样本/"
    main(imgdir)
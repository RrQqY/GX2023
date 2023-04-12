from maix import image, display, camera
import time
import serial
ser = serial.Serial("/dev/ttyS1",115200)    # 连接串口
print('serial test start ...')              

img_width = 320
def judge_center(cx1, cx2):
    if(abs(cx1 - img_width/2) <= abs(cx2 - img_width/2)):
        return True
    else:
        return False
    
color_list = ["r", "g", "b"]
thresh_list = [[0,100,34,127,-128,127],
               [0,100,-128,-13,-128,127],
               [0,100,-10,29,-63,-19]]
pixels_thresh = 20000
detect_list = []

while True:
#     stime = time.time()
    
    img = camera.capture()
    img = img.rotate(180, adjust=0)
    img = img.resize(size=(img_width, img_width))
#     display.show(img)         #将图像显示出来
    
    max_pixels = 0
    center_cx = img_width
    
    for color_i in range(3):
        thresh = thresh_list[color_i]
        thresh = [tuple(thresh)]
        blobs = img.find_blobs(thresh, merge=True)    #在图片中查找lab阈值内的颜色色块 merge 合并小框

        if blobs:
            for i in blobs:
                if i["pixels"] > pixels_thresh:
                    detect = {
                        "cx" : i["x"] + 0.5*i["w"],
                        "cy" : i["y"] + 0.5*i["h"],
                        "pixels" : i["pixels"],
                        "color" : color_list[color_i],
                        "x0" : i["x"], 
                        "y0" : i["y"], 
                        "x1" : i["x"] + i["w"], 
                        "y1" : i["y"] + i["h"]
                    }
                    detect_list.append(detect)
#                     print(detect_list)
            
            if len(detect_list) > 0:
                for i in range(len(detect_list)):
                    # 如果更靠近中间
                    if (detect_list[i]["pixels"] > max_pixels) and (judge_center(detect_list[i]["cx"], center_cx)):
                        max_pixels = detect_list[i]["pixels"]
                        center_cx = detect_list[i]["cx"]
                        res_i = i
            else:
                res_i = -1
    
    if res_i != -1:
#         img.draw_rectangle(detect_list[res_i]["x0"], detect_list[res_i]["y0"], detect_list[res_i]["x1"], detect_list[res_i]["y1"], 
#                            color=(0, 0, 255), thickness=1) #将找到的颜色区域画出来
        
        s = "S" + detect_list[res_i]["color"] + "@"
        print(s)
        ser.write(s.encode())             # 输入需要通讯的内容
    else:
        s = "S" + "n" + "@"
        print(s)
        ser.write(s.encode())             # 输入需要通讯的内容
    
    detect_list = []
    
#     etime = time.time()
#     print(etime-stime)
#     display.show(img)
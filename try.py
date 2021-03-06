# -*-coding:utf8-*-#
"""
Created on Wed Feb 04 21:53:05 2015
@author: http://2hwp.com/
"""


import os
import cv2
from PIL import Image,ImageDraw

#detectFaces()返回图像中所有人脸的矩形坐标（矩形左上、右下顶点）
#使用haar特征的级联分类器haarcascade_frontalface_default.xml，在haarcascades目录下还有其他的训练好的xml文件可供选择。
#注：haarcascades目录下训练好的分类器必须以灰度图作为输入。
def detectFaces(image_name):
    img = cv2.imread(image_name)
    face_cascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")
    face_cascade.load('E:/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img #if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图

    faces = face_cascade.detectMultiScale(gray, 1.2, 5)#1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
    result = []
    for (x,y,width,height) in faces:
        result.append((x,y,x+width,y+height))
    return result


#保存人脸图
def saveFaces(image_name):
    faces = detectFaces(image_name)
    if faces:
        #将人脸保存在save_dir目录下。
        #Image模块：Image.open获取图像句柄，crop剪切图像(剪切的区域就是detectFaces返回的坐标)，save保存。
        save_dir = image_name.split('.')[0]+"_faces"
        os.mkdir(save_dir)
        count = 0
        for (x1,y1,x2,y2) in faces:
            file_name = os.path.join(save_dir,str(count)+".jpg")
            Image.open(image_name).crop((1/6*x2+5/6*x1,5/7*y1+2/7*y2,5/6*x2+1/6*x1,1/2*y2+1/2*y1)).save(file_name)
            count+=1


#在原图像上画矩形，框出所有人脸。
#调用Image模块的draw方法，Image.open获取图像句柄，ImageDraw.Draw获取该图像的draw实例，然后调用该draw实例的rectangle方法画矩形(矩形的坐标即
#detectFaces返回的坐标)，outline是矩形线条颜色(B,G,R)。
#注：原始图像如果是灰度图，则去掉outline，因为灰度图没有RGB可言。drawEyes、detectSmiles也一样。
def drawFaces(image_name):
    faces = detectFaces(image_name)
    if faces:
        img = Image.open(image_name)
        draw_instance = ImageDraw.Draw(img)
        for (x1,y1,x2,y2) in faces:
            draw_instance.rectangle((x1,y1,x2,y2), outline=(255, 0,0))
        img.save('drawfaces_'+image_name)






#在原图像上框出眼睛.
def drawEyes(image_name):
    faces = detectFaces(image_name)
    if faces:
        img = Image.open(image_name)
        draw_instance = ImageDraw.Draw(img)
        for (x1,y1,x2,y2) in faces:
            draw_instance.rectangle((x1,y1,x2,y2), outline=(255, 0,0))
            draw_instance.rectangle((1/6*x2+5/6*x1,5/7*y1+2/7*y2,5/6*x2+1/6*x1,1/2*y2+1/2*y1), outline=(0, 0,255))
        img.save('draweyes_'+image_name)




#检测笑脸
def detectSmiles(image_name):
    img = cv2.imread(image_name)
    smiles_cascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_smile.xml")
    smiles_cascade.load('E:/opencv/sources/data/haarcascades//haarcascade_smile.xml')
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img #if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图

    smiles = smiles_cascade.detectMultiScale(gray,4,5)
    result = []
    for (x,y,width,height) in smiles:
        result.append((x,y,x+width,y+height))
    return result


#在原图像上框出笑脸
def drawSmiles(image_name):
    smiles = detectSmiles(image_name)
    if smiles:
        img = Image.open(image_name)
        draw_instance = ImageDraw.Draw(img)
        for (x1,y1,x2,y2) in smiles:
            draw_instance.rectangle((x1,y1,x2,y2), outline=(100, 100,0))
        img.save('drawsmiles_'+image_name)


if __name__ == '__main__':
    #drawFaces('lalala.jpg')
    drawEyes('50.jpg')
    saveFaces('50.jpg')


"""
上面的代码将眼睛、人脸、笑脸在不同的图像上框出，如果需要在同一张图像上框出，改一下代码就可以了。
总之，利用opencv里训练好的haar特征的xml文件，在图片上检测出人脸的坐标，利用这个坐标，我们可以将人脸区域剪切保存，也可以在原图上将人脸框出。剪切保存人脸以及用矩形工具框出人脸，本程序使用的是PIL里的Image、ImageDraw模块。
此外，opencv里面也有画矩形的模块，同样可以用来框出人脸。
"""

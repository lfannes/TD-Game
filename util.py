import pygame

def interpol(xa, ya, xb, yb, x):
    #voor path x = tijd ya en yb = pos
    m = float(yb - ya)/float(xb - xa)
    q = ya - m*xa
    return m*x + q

def pressedImage(mousePos, imageRect):
    if mousePos[1] < imageRect[1] + imageRect[3] and mousePos[1] > imageRect[1]:
        if mousePos[0] > imageRect[0] and mousePos[0] < imageRect[0] + imageRect[2]:
            return True

def scaleList(imageList, factor):
    scaledImageList = list()
    for image in imageList:
        scaledImageList.append(pygame.transform.scale(image, (image.get_width()*factor, image.get_height()*factor)))

    return scaledImageList

def scaleSingleImage(image, factor):
    return pygame.transform.scale(image, (int(image.get_width()*factor), int(image.get_height()*factor)))
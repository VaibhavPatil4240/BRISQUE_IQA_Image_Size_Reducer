from cv2 import imwrite
import imquality.brisque as brisque
import cv2
import numpy as np
import time

color = (255, 0, 0)
thickness = 4

def get_blurrness_score(image):
    image = cv2.cvtColor((image), cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(image, cv2.CV_64F).var()
    return fm

def isPrime(num):
    if num > 1:
        for i in range(2, int(num/2)+1):
            if (num % i) == 0:
                return False
    return True

def divideImage(img):
    divisions=[]
    row=img.shape[0]
    col=img.shape[1]
    color = (255, 0, 0)
    thickness = 6
    r_inc=int(row/4)
    curr_r=0
    while(curr_r<=(row-r_inc)):
        curr_c=0
        c_inc=int(col/4)
        while(curr_c<=(col-c_inc)):
            # cv2.rectangle(img,(curr_c,curr_r),(curr_c+c_inc,curr_r+r_inc),color=color,thickness=thickness)
            divisions.append([curr_r,(curr_r+r_inc),curr_c,(curr_c+c_inc)])
            if(curr_c+c_inc>col):
                c_inc=col-curr_c
            curr_c+=c_inc
        if(curr_r+r_inc>row):
            r_inc=row-curr_r
        curr_r+=r_inc
    return divisions

def getBlurnessMatrix(img,divisions):
    blurrness_mat=[]
    for division in divisions:
        segment=img[division[0]:division[1],division[2]:division[3]]
        blurrness=get_blurrness_score(segment)
        blurrness_mat.append([blurrness,division[0],division[1],division[2],division[3]])
    blurrness_mat=np.array(blurrness_mat)
    blurrness_mat=blurrness_mat[blurrness_mat[:,0].argsort()]
    shape=blurrness_mat.shape
    s=shape[0]
    i=0
    while(i<s):
        if(i>=3 and i<s-3):
            blurrness_mat=np.delete(blurrness_mat,i,0)
            s-=1
            i-=1
        i+=1
    shape=blurrness_mat.shape
    return blurrness_mat

def getQuality(blurrness_mat,img):
    quality_score=[]
    start=time.time()
    for i in blurrness_mat:
        img_segment=img[int(i[1]):int(i[2]),int(i[3]):int(i[4])]
        quality_score.append( brisque.score(img_segment,kernel_size=5))
    end=time.time()
    print("Time: ",end-start)
    quality_score=np.array(quality_score)
    return np.mean(quality_score)

def reduce_size(image):
    print(image)
    img = cv2.imread("uploads/"+image)
    filename=image.split(".")
    print(filename)
    shape=img.shape
    divisions=divideImage(img.copy())
    blurrness_mat=getBlurnessMatrix(img,divisions)
    mean_quality=getQuality(blurrness_mat,img)
    print("Quality: ",mean_quality)
    mean_blurr=np.mean(blurrness_mat[:,0])
    org_blurr=get_blurrness_score(img)
    reduce =(org_blurr%100)-mean_quality
    if(reduce<1):
        reduce=mean_quality
    cv2.imwrite(f"uploads/{filename[0]}_compressed.jpg",img,[cv2.IMWRITE_JPEG_QUALITY,int(reduce)])
    return f"{filename[0]}_compressed.jpg"
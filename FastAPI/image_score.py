import imquality.brisque as brisque
import cv2
import numpy as np

color = (255, 0, 0)
thickness = 4

def get_blurrness_score(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(image, cv2.CV_64F).var()
    return fm

def isPrime(num):
    if num > 1:
        for i in range(2, int(num/2)+1):
            if (num % i) == 0:
                return False
    return True

def getImageBlock(shape):
    rows=shape[0]
    columns=shape[1]
    r_divide=4
    c_divide=4
    r_inc=0
    c_inc=0
    while(isPrime(rows)):
        rows+=1
        r_inc+=1
    while(isPrime(columns)):
        columns+=1
        c_inc+=1
    while(not rows%r_divide==0):
        r_divide+=1
    while(not columns%c_divide==0):
        c_divide+=1
    return r_divide,c_divide,r_inc,c_inc

def get_increment(shape):
    r_increament=int(shape[0]/4)
    c_increament=int(shape[1]/4)
    return r_increament,c_increament

def getBlurnessMatrix(r_increament,c_increament,shape,img):
    print("IMage shape",img.shape)
    blurrness_mat=[]
    for i in range(0,shape[0]-r_increament-1,r_increament):
        for j in range(0,shape[0]-c_increament-1,c_increament):
            if(i+r_increament<shape[0] and j+c_increament<shape[1]):
                blurrness=get_blurrness_score(img[i:i+r_increament,j:j+c_increament])
                blurrness_mat.append([blurrness,i,j])

    blurrness_mat=np.array(blurrness_mat)
    blurrness_mat=blurrness_mat[blurrness_mat[:,0].argsort()]
    shape=blurrness_mat.shape
    print("Shape: ",shape)
    s=shape[0]
    i=0
    while(i<s):
        if(i>=3 and i<s-3):
            blurrness_mat=np.delete(blurrness_mat,i,0)
            s-=1
            i-=1
        i+=1
    shape=blurrness_mat.shape
    print("Shape: ",shape)
    return blurrness_mat

def getQuality(r_increament,c_increament,blurrness_mat,image,img):
    quality_score=[]
    for i in blurrness_mat:
        r=int(i[1])
        c=int(i[2])
        img_segment=img[r:r+r_increament,c:c+c_increament]
        quality_score.append( brisque.score(img_segment))
    quality_score=np.array(quality_score)
    return np.mean(quality_score)

def reduce_size(image):
    img = cv2.imread("uploads/"+image)
    filename=image.split(".")
    shape=img.shape
    r_increament,c_increament=get_increment(shape)
    blurrness_mat=getBlurnessMatrix(r_increament,c_increament,shape,img)
    mean_quality=getQuality(r_increament,c_increament,blurrness_mat,image,img)
    mean_blurr=np.mean(blurrness_mat[:,0])
    org_blurr=get_blurrness_score(img)
    reduce =(org_blurr%100)-mean_quality
    if(reduce<1):
        reduce=mean_quality
    cv2.imwrite(f"uploads/{filename[0]}_compressed.jpg",img,[cv2.IMWRITE_JPEG_QUALITY,int(reduce)])
    return f"{filename[0]}_compressed.jpg"

'''
Created on 06-Sep-2019

@author: somsh
'''
from PIL import Image
import random
import numpy as np
import matplotlib.pyplot as plt

#encryption
def share_segmentation(img,n):
    width, height = img.size
    img.putalpha(0)
    share_list=[]
    
    pixel_list=[]
    for i in range(width):
        for j in range(height):
            pixel_list.append((i,j))
    used_pixel=[]
    
    loop=int(width*height*(1/n))
    for _ in range(n):
        share=np.array(img)
        rem_pixel=(set(pixel_list)-set(used_pixel))
        chosen_pixel=random.sample(rem_pixel,loop)
        for (i,j) in chosen_pixel:
            share[j][i][3]=255
            used_pixel.append((i,j))
        share_list.append(share)
        
    for i in share_list:
        plt.imshow(i)
        plt.show()
    return share_list

def keygen(share_list,m):
    keys=[]
    for _ in share_list:
        B=np.random.randint(m,size=(4,4))
        keys.append(B)
    return keys 

def encryption(share_list,keys):
    encrypt_list=[]
    for i,j in zip(share_list,keys):
        encrypt_list.append(np.tensordot(i, j, 1))
    return encrypt_list
    
#decryption
def decryption(encrypt_list,user_keys):
    try:
        if user_keys!=keys:
            raise Exception("Warning: keys do not match")
        else:
            keys_inv=[]
            decrypt_list=[]
            for k in keys:
                keys_inv.append(np.linalg.inv(k))
            for i,j in zip(encrypt_list,keys_inv):
                decrypt_list.append(np.tensordot(i,j,1).astype(int))
            new_img=0
            for i in decrypt_list: 
                new_img = np.maximum(new_img,i)  
            plt.imshow(new_img)
            plt.show()       
    except Exception as e:
        print(str(e))
        
#main
img_path="C:/Users/somsh/Downloads/download.jpg"
img=Image.open(img_path)
img=img.convert("RGBA")
# n=int(input("Enter number of shares: "))
n=10
m=10
share_list=share_segmentation(img,n)
keys=keygen(share_list, m)
encrypt_list=encryption(share_list,keys)  

user_keys=keys       
decryption(encrypt_list,user_keys)            
    

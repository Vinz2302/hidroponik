#SUDAH JADI AMBIL UKURAN BESARNYA SAJA, eksperimen HSV, tidak per tile
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date
import os
import time
import serial
from motor import*
from servo import*

home()
segment1()                                              

if os.path.isfile('record.csv'):                                #Mengecek apakah file record sudah ada
    record=pd.read_csv('record.csv',index_col=[0])              #jika sudah ada file akan dibaca sebagai dataframe
else:
    record=pd.DataFrame(index=['1','2','3','4'])                #jika belum ada akan buat dataframe baru, 1234 itu lubang dari selada hidroponik

if not os.path.isdir('Hasil'):                                  #mengecek apakah folder hasil sudah ada
    os.mkdir('Hasil')                                           #jika belum ada maka akan dibuat, folder ini untuk simpan hasil gambar program
   
cap=cv2.VideoCapture(0)         #menyalakan kamera
ret,frame=cap.read()            #membaca gambar dari kamera, gambar yang dibaca formatnya BGR
cap.release()                   #melepaskan kamera

#Baca Gambar
image=frame
lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)            #mengubah dari format BGR menjadi CIELAB
(thresh, BnW_image)= cv2.threshold(lab[:,:,1], 119, 255, cv2.THRESH_BINARY) #Melakukan intensity transformation agar gambar jadi biner
# plt.imsave('Hasil/'+'lab'+'.jpg',lab)                                     #Threshold bisa disesuaikan bisa juga pakai THRESH_OTSU biar otomatis
# plt.imsave('Hasil/'+'laba'+'.jpg',lab[:,:,1])
# plt.imsave('Hasil/'+'bnw'+'.jpg',BnW_image)

save={}         #dictionary untuk simpan hasil
big=[]          #list untuk simpan selada kategori besar, sedang, dan kecil untuk nanti ubah warna seladanya
med=[]
small=[]
outcode=[]      #untuk menentukan posisi mana yang sudah siap dipanen
areal=[2,1,4,3,0]
area=areal[0]
areai=1
numrows, numcols = 2, 2
height = int(image.shape[0] / numrows)      #untuk membagi gambar jadi 4 bidang
width = int(image.shape[1] / numcols)
imcop=image.copy()
imcop=cv2.cvtColor(imcop,cv2.COLOR_BGR2RGB) #untuk ubah color space BGR jadi RGB
# plt.imsave('Hasil/'+'awal'+'.jpg',imcop)

for row in range(numrows):
    for col in range(numcols):
        y0 = row * height
        y1 = y0 + height                    #mengolah bidang yang sudah dibagi jadi 4 satu persatu
        x0 = col * width
        x1 = x0 + width
        individual =  (BnW_image[y0:y1, x0:x1])     #untuk ambil gambar biner dari bidang yang mau diolah
        individual = cv2.copyMakeBorder(individual,2,2,2,2,cv2.BORDER_CONSTANT, value = 255)    #untuk buat padding supaya find contour bisa jalan
        # strar=str(area)
        # plt.imsave('Hasil/'+strar+'.jpg',individual)
        contours, hierarchy=cv2.findContours(individual,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)   #mencari kontur dari selada
        
        for j in range(len(hierarchy[0])):   #hasil dari hierarchy ini bisa beda-beda tergantung dari jenis RETR yang digunakan
            if hierarchy[0,j,3]==0:
                x, y, w, h = cv2.boundingRect(contours[j])   #untuk buat kotak di sekitar selada untuk nantinya bisa diubah warnanya
                if individual[y:y+h, x:x+w][individual[y:y+h, x:x+w]==0].size>5000: #5000 merupakan batas pixel noise, dibawah itu akan diabaikan, nilai bisa disesuaikan
        #             cv2.rectangle(imcop, (x,y),(x+w,y+h), (0, 0, 255), 1)
                    cv2.fillPoly(individual, pts =[contours[j]], color=(0))   #untuk mengisi lubang-lubang yang kosong pada selada

                    if area in save:        #jika pada bidang 1 sudah ada kontur yang terdeteksi dan terdeteksi ada kontur lain, maka akan dibandingkan
                        if individual[y:y+h, x:x+w][individual[y:y+h, x:x+w]==0].size*0.00276>save[area]['size']:    #kontur yang paling besar yang akan disimpan
                            save[area]={}
                            save[area]['size']=individual[y:y+h, x:x+w][individual[y:y+h, x:x+w]==0].size*0.00276   #*0.00276 adalah koefisien pengali
                            save[area]['x']=x+x0-1                                                                  #didapatkan dari kalibrasi 
                            save[area]['y']=y+y0-1
                            save[area]['w']=w
                            save[area]['h']=h
                    else:
                        save[area]={}
                        save[area]['size']=individual[y:y+h, x:x+w][individual[y:y+h, x:x+w]==0].size*0.00276       #jika belum ada kontur terdeteksi 
                        save[area]['x']=x+x0-1                                                                      #maka akan langsung disimpan
                        save[area]['y']=y+y0-1
                        save[area]['w']=w
                        save[area]['h']=h
        area=areal[0+areai]   #ini berhubungan dengan penamaan sebuah bidang karena ingin bisa mengambil selada bagian kiri duluan, normalnya bisa liat 
        areai=areai+1           #file seladacv.py 
            
for area in save:
    if BnW_image[save[area]['y']:save[area]['y']+save[area]['h'], save[area]['x']:save[area]['x']+save[area]['w']][BnW_image[save[area]['y']:save[area]['y']+save[area]['h'], save[area]['x']:save[area]['x']+save[area]['w']]==0].size <5000:      #untuk menentukan kategori ukuran selada, ukuran minimum bisa disesuaikan
        small.append(area)
    elif BnW_image[save[area]['y']:save[area]['y']+save[area]['h'], save[area]['x']:save[area]['x']+save[area]['w']][BnW_image[save[area]['y']:save[area]['y']+save[area]['h'], save[area]['x']:save[area]['x']+save[area]['w']]==0].size <8000:
        med.append(area)
    elif BnW_image[save[area]['y']:save[area]['y']+save[area]['h'], save[area]['x']:save[area]['x']+save[area]['w']][BnW_image[save[area]['y']:save[area]['y']+save[area]['h'], save[area]['x']:save[area]['x']+save[area]['w']]==0].size >8000:
        big.append(area)
            
for k in big:
#     imcop[save[k]['y']:save[k]['y']+save[k]['h'],save[k]['x']:save[k]['x']+save[k]['w']][BnW_image[save[k]['y']:save[k]['y']+save[k]['h'],save[k]['x']:save[k]['x']+save[k]['w']] == 0] = [0, 255, 0]
    layer=np.ones(image[save[k]['y']:save[k]['y']+save[k]['h'],save[k]['x']:save[k]['x']+save[k]['w']].shape,dtype=np.uint8)*255   #untuk ubah warna selada supaya bisa transparan
    layer[BnW_image[save[k]['y']:save[k]['y']+save[k]['h'],save[k]['x']:save[k]['x']+save[k]['w']]==0]=(0,225,0)
    mask=~BnW_image[save[k]['y']:save[k]['y']+save[k]['h'],save[k]['x']:save[k]['x']+save[k]['w']]
    fg=cv2.bitwise_or(layer,layer,mask=mask)
    final=cv2.bitwise_or(imcop[save[k]['y']:save[k]['y']+save[k]['h'],save[k]['x']:save[k]['x']+save[k]['w']],fg)
    imcop[save[k]['y']:save[k]['y']+save[k]['h'],save[k]['x']:save[k]['x']+save[k]['w']]=final
    
    #Penentuan koordinat selada
    outcode.append(k)
    
    
for m in med:
#     imcop[save[m]['y']:save[m]['y']+save[m]['h'],save[m]['x']:save[m]['x']+save[m]['w']][BnW_image[save[m]['y']:save[m]['y']+save[m]['h'],save[m]['x']:save[m]['x']+save[m]['w']] == 0] = [0, 0, 255]
    layer=np.ones(image[save[m]['y']:save[m]['y']+save[m]['h'],save[m]['x']:save[m]['x']+save[m]['w']].shape,dtype=np.uint8)*255
    layer[BnW_image[save[m]['y']:save[m]['y']+save[m]['h'],save[m]['x']:save[m]['x']+save[m]['w']]==0]=(200,150,0)
    mask=~BnW_image[save[m]['y']:save[m]['y']+save[m]['h'],save[m]['x']:save[m]['x']+save[m]['w']]
    fg=cv2.bitwise_or(layer,layer,mask=mask)
    final=cv2.bitwise_or(imcop[save[m]['y']:save[m]['y']+save[m]['h'],save[m]['x']:save[m]['x']+save[m]['w']],fg)
    imcop[save[m]['y']:save[m]['y']+save[m]['h'],save[m]['x']:save[m]['x']+save[m]['w']]=final
    
for l in small:
#     imcop[save[l]['y']:save[l]['y']+save[l]['h'],save[l]['x']:save[l]['x']+save[l]['w']][BnW_image[save[l]['y']:save[l]['y']+save[l]['h'],save[l]['x']:save[l]['x']+save[l]['w']] == 0] = [255, 0, 0]
    layer=np.ones(image[save[l]['y']:save[l]['y']+save[l]['h'],save[l]['x']:save[l]['x']+save[l]['w']].shape,dtype=np.uint8)*255
    layer[BnW_image[save[l]['y']:save[l]['y']+save[l]['h'],save[l]['x']:save[l]['x']+save[l]['w']]==0]=(255,0,0)
    mask=~BnW_image[save[l]['y']:save[l]['y']+save[l]['h'],save[l]['x']:save[l]['x']+save[l]['w']]
    fg=cv2.bitwise_or(layer,layer,mask=mask)
    final=cv2.bitwise_or(imcop[save[l]['y']:save[l]['y']+save[l]['h'],save[l]['x']:save[l]['x']+save[l]['w']],fg)
    imcop[save[l]['y']:save[l]['y']+save[l]['h'],save[l]['x']:save[l]['x']+save[l]['w']]=final
    

save=pd.DataFrame(save)   #membuat dictionary save jadi dataframe
save=save.transpose()     #melakukan transpose pada dataframe
tempsave=save[['size']].copy()

for ada in (1,2,3,4):
    if ada not in tempsave.index:
        tempsave.loc[ada]=0  #jika suatu bidang tidak memiliki kontur yang terdektesi akan diberi nilai 0 supaya program tetap bisa jalan
tesna='pameran'
        
# record[date.today().strftime("%d/%m/%y")]=tempsave.sort_index()['size'].values        
record[tesna]=tempsave.sort_index()['size'].values            #menyimpan ukuran selada pada dataframe record

record.to_csv('record.csv')                               #simpan dataframe dengan format csv
# plt.imsave('Hasil/'+date.today().strftime("%y%m%d")+'.jpg',imcop)
plt.imsave('Hasil/'+tesna+'.jpg',imcop)                   #simpan hasil gambar dari program ini, format bisa diganti tidak harus jpg

print(outcode)
print(save)
print(record)
outcode.sort()             #outcode di sort supaya lengan robot mengambil sesuai urutan yang di mau

for ambil in outcode:
    if ambil==1:
        home()     
        pos1()
        tutup()
        home()
        buka()
    elif ambil==2:
        home()
        pos2()
        tutup()
        home()
        buka()
    elif ambil==3:
        home()
        pos3()
        tutup()
        home()
        buka()
    elif ambil==4:
        home()
        pos4()
        tutup()
        home()
        buka()   
home()
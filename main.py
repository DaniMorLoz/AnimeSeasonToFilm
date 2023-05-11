import cv2
import numpy as np
import os
import moviepy_method
import premiere_method

def comparison(img1,img2):
    h, w, _ = img1.shape
    errorL2 = cv2.norm( img1, img2, cv2.NORM_L2 )
    return 1 - errorL2 / ( h * w )

def ordenarLista(lista):
    primerCapitulo = int(lista[0].split("_")[1].split(".")[0])
    ultimoCapitulo = primerCapitulo
    for elemento in lista:
        numero = int(elemento.split("_")[1].split(".")[0])
        if numero < primerCapitulo:
            primerCapitulo = numero
        elif numero > ultimoCapitulo:
            ultimoCapitulo = numero
    return [primerCapitulo, ultimoCapitulo]

def getFrame(videoname,reference,startPercentage):
    cap = cv2.VideoCapture("Episodios/"+videoname)
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    startframe = frames * startPercentage
    if startframe == 0:
        lastframe = frames * 0.5
    else:
        lastframe = frames
    cap.set(cv2.CAP_PROP_POS_FRAMES,startframe)
    high = 0
    currentframe = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    while (cap.isOpened() or cap.get(cv2.CAP_PROP_POS_FRAMES) < lastframe):
        ret, frame = cap.read()
        if not ret:
            break
        dif = comparison(reference,frame)
        if (dif > 0.98):
            currentframe = str(cap.get(cv2.CAP_PROP_POS_FRAMES))
            break
        elif dif > high:
            high = dif
            currentframe = str(cap.get(cv2.CAP_PROP_POS_FRAMES))
    cap.release()
    cv2.destroyAllWindows() 
    return [currentframe,fps]

def getFrameList(videolist, Openingreference, Endingreference):
    print("Buscando openings y endings...")
    framelist = []
    for i, video in enumerate(videolist):
        print("Capitulo "+video.split("_")[1].split(".")[0]+":",end=" ")

        OpeningFrame, fps = getFrame(video,Openingreference,0)
        s = float(OpeningFrame)/fps
        mins = str(int(int(s)/60))
        segs = str(int(s) - int(mins)*60)
        print(mins+":"+segs,end=" ")

        EndingFrame, _ = getFrame(video,Endingreference,0.8)
        s = float(EndingFrame)/fps
        mins = str(int(int(s)/60))
        segs = str(int(s) - int(mins)*60)
        print(mins+":"+segs)

        framelist.append([OpeningFrame,EndingFrame])
    return framelist

def initFiles(OpeningFileReference,EndingFileReference):
    Openingreference = cv2.imread('Referencias/'+OpeningFileReference)
    Openingreference = cv2.resize(Openingreference,(1280,720))
    Endingreference = cv2.imread('Referencias/'+EndingFileReference)
    Endingreference = cv2.resize(Endingreference,(1280,720))
    videolist = os.listdir(path="Episodios/")
    primero, ultimo = ordenarLista(videolist)
    index = 0
    temporada = videolist[0].split("_")[0]
    for numero in range(primero,ultimo+1):
        videolist[index] = temporada+"_"+str(numero)+".mp4"
        index += 1
    return [videolist, Openingreference, Endingreference]

if __name__ == '__main__':
    ORCorrect = False
    ERCorrect = False
    while not ORCorrect or not ERCorrect:
        ORCorrect = False
        ERCorrect = False
        print("Los archivos disponibles en la carpeta de referencias son:")
        print(os.listdir("Referencias/"))
        OpeningFileReference = input("Cual se va a usar como referencia para el opening?:")
        for archivo in os.listdir("Referencias/"):
            if archivo == OpeningFileReference:
                ORCorrect = True
                break
        EndingFileReference = input("Cual se va a usar como referencia para el ending?:")
        for archivo in os.listdir("Referencias/"):
            if archivo == EndingFileReference:
                ERCorrect = True
                break
    principio = input("La referencia es del principio del opening?(si/no): ")
    if principio == "si":
        openingDuration = input("Cuanto dura el opening en segundos?: ")
    else:
        openingDuration = "0"
    openingDuration = float(openingDuration)
    methodCorrect = False
    while not methodCorrect:
        method = input("Seleccione el metodo a usar para generar el video final (moviepy/premiere): ")
        if method in ['moviepy','premiere']:
            methodCorrect = True

    videolist, Openingreference, Endingreference = initFiles(OpeningFileReference,EndingFileReference)
    frameList = getFrameList(videolist, Openingreference, Endingreference)
    if method == 'moviepy':
        moviepy_method.createVideo(videolist,frameList,openingDuration,cv2.CAP_PROP_FPS)
    else:
        premiere_method.colocarycortar(videolist,frameList,openingDuration)
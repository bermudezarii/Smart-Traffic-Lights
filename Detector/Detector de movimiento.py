import numpy as np
import cv2
 
cap = cv2.VideoCapture('videoplayback.mp4')
# parametros para detección de esquinas ShiTomasi
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
 
# Parámetros para el flujo óptico de Lucas Kanade
lk_params = dict( winSize = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
 
# Crea algunos colores aleatorios
color = np.random.randint(0,255,(100,3))
# Toma el primer cuadro y encuentra esquinas en él
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
 
# Crear una máscara de imagen para dibujar
mask = np.zeros_like(old_frame)
 
while(1):
  ret,frame = cap.read()
  frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
  # calcula optical flow
  p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
 
  # Select good points
  good_new = p1[st==1]
  good_old = p0[st==1]
 
  # dibuja las lineas
  for i,(new,old) in enumerate(zip(good_new,good_old)):
    a,b = new.ravel()
    c,d = old.ravel()
    mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
    frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
  img = cv2.add(frame,mask)
 
  cv2.imshow('frame',img)
  k = cv2.waitKey(30) & 0xff
  if k == 27:
    break
 
  # Ahora actualiza el marco anterior y los puntos anteriores
  old_gray = frame_gray.copy()
  p0 = good_new.reshape(-1,1,2)
 
cv2.destroyAllWindows()
cap.release()
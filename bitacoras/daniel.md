# Bitácora de Daniel

### Sábado 29 de abril

Se comienza investigación para encontrear un clasificador de emociones.

Se revisan varios repositorios de github, se intenta hechar a andar varios sin exito

### Lunes 1 de mayo

Se continua buscando clasificadores ya echos e intentar correrlos, se logra correr uno pero es bastante impreciso.

### Miercoles 3 de mayo

Se continua intentando correr un repo de un clasificador de emocioens que tiene errores en código de python, se cambia librería imgresize de scipy por resize de imageio. Se tiene otros errores.

Se elimina un error causado por un doble llamado a cv2.VideoCapture(0), con esto se logra correr el archivo de python del clasificador `emotions.py`. Se añade en archivo de bash `emociones_requerimientos.sh` los pip de las dependecias.

El clasificador parece ser bastante decente para identificar las emociones, y rapido en mi compu, aunque aunque quien sabe si es eficiente o es mi compu que tiene un i7 :v

Se suben archivos necesarios unicamente para correr el modelo al repositorio. Direcotrio Emociones. 

### Viernes 5 de amyo

Hablar con Rachel sobre como convertir el modelo con tensorflow lite

### Sábado 6 de mayo
Convertir el modelo a tensorflow lite e intentar correr el modelo recortado.
Archivos de converter_2.py para tomar el archivo .hdf5 orginial del modelo para convertilro a un .tflite 

Se hace copia del código orignial emotion.py -> emotions_tflite.py en donde se intenta utilizar en vez del modelo original el modelo recortado con tensorflow lite.

Referencias: bingchat

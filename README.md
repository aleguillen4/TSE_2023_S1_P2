# TSE_2023_S1_P2

Integrantes: 
Daniel González Vargas
Reichel Morales Sánchez
Alejandro Guillén


Se cuenta con los siguientes archivos requeridos en la rasberry pi para correr el sistema, estos se encuentran acomodados en la carpeta raspi_2/:

```
- emotions_pi.py
- model.tflite
- inference.py
- haarcascade_frontalface_default.xml
- config.txt
- output.cvs
``` 

El programa principal es `emotions_pi.py` cuando se corre, una carpeta llamada `capturas/` se creara y va ir guardando todas las capturas, en output.csv se guarda todo el historia de capturas junto con la fecha y tiempo y emoción.

Según el paper del modelo, cuenta con una precisión de 66%, [paper](https://github.com/oarriaga/face_classification/blob/master/report.pdf).



Archivos para correr en el computador remoto: 

- GUI.py
- config.txt
- capturas/

capturas sería un directorio vacío (`mkdir capturas`)
El programa GUI.py es el programa principal con la interfaz gráfica cuenta con las siguientes opciónes:

- Run Script -> Va correr el programa principal en la rasberry pi(emotion_pi.py)
- Update photo -> Va a copiar de la rasberry pi la ultima imagen que se haya tomado y mostrala en la aplicación
- Stop program -> Va a cortar la ejecución del programa
- Enter value es una cajita donde podemos ingresar cualquiera de los 3 valores de configuración para actualizarlos en la rasberry: update sample time, update maximun execution time, y cantidad maxima de capturas que se guardan en la rasberry, o que la rasberry guarda de forma local. Para actualizar cada valor se ingresa en enter value y de ahí se presiona el boton según se quiera.

Se muestra una imagen de la app:

![app](Emociones/app.png)


## Paquetes que importa los archivos de python para corre en la rasberry pi:

```
import datetime
import csv
import cv2
import numpy as np
import os
import time
import tensorflow.lite as tflite
import glob

import cv2
import matplotlib.pyplot as plt
import numpy as np

h5py
pandas
scipy

```

## Repositorios que clonar para dependencias

Se utilizan los siguientes comandos para clonar los repositorios:
```
git clone -b langdale https://github.com/openembedded/meta-openembedded.git
git clone -b langdale https://github.com/openembedded/openembedded-core.git
git clones -b langdale https://github.com/NobuoTsukamoto/meta-tensorflow-lite
git clone -b langdale git://git.yoctoproject.org/meta-raspberrypi
```

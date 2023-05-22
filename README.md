# TSE_2023_S1_P2

Integrantes: 
Daniel González Vargas
Rachel
Alejandro

## Descarga las dependencias para correr `emotions.py`

`bash emociones_requerimientos.sh`

Luego correr el archivo de python 

`python Emociones/emotions.py`


De momento se cuenta con los siguientes archivos requeridos en la rasberry pi para correr el sistema:

- emotions_pi.py
- model.tflite
- utils/inference.py
- models/haarcascade_frontalface_default.xml


Archivos para correr en el computador remoto: 

- GUI.py
- config.txt
- capturas/

capturas sería un directorio vacío (`mkdir capturas`)

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

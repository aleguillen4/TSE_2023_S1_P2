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

Se muestran los cambios exactos hechos al código original para que pudiera utilizar el modelo guradado en formato .tflite
```
(emotion-det) daniel@daniel-Latitude-7420:~/s1-2023/embebidos/p2/Emociones$ diff emotions.py emotions_tflite.py 
16c16
< emotion_model_path = './models/emotion_model.hdf5'
---
> emotion_model_path = 'model.tflite'
25c25,28
< emotion_classifier = load_model(emotion_model_path)
---
> #emotion_classifier = load_model(emotion_model_path)
> import tensorflow as tf
> interpreter = tf.lite.Interpreter(model_path="model.tflite")
> interpreter.allocate_tensors()
27,28c30,33
< # getting input model shapes for inference
< emotion_target_size = emotion_classifier.input_shape[1:3]
---
> input_details = interpreter.get_input_details()
> output_details = interpreter.get_output_details()
> 
> input_shape = input_details[0]['shape']
29a35,38
> 
> # getting input model shapes for inference
> #emotion_target_size = emotion_classifier.input_shape[1:3]
> emotion_target_size = input_details[0]['shape'][1:3]
68c77,86
<         emotion_prediction = emotion_classifier.predict(gray_face)
---
>         #emotion_prediction = emotion_classifier.predict(gray_face)
> 
>         input_data = gray_face.astype(np.float32)
>         interpreter.set_tensor(input_details[0]['index'], input_data)
> 
>         interpreter.invoke()
> 
>         output_data = interpreter.get_tensor(output_details[0]['index'])
>         
>         emotion_prediction = output_data
```

### Domingo 15 de mayo

Se realiza el archivo emotions_pi.py que será el programa principal encargado de correr en la rasberry pi, se empieza del programa emotions_tflite.py y se editan varias cosas como:

- Tomar fotos y realizar inferencias basado en un tiempo tomado de config.txt
- Limitar la duración maximo del programa basado en un tiempo tomado de config.txt
- Almacenar cada imagen en la carpte caputars con stampa de tiempo y emoción
- Almacenar en un archivo `output.csv` datos de las imagenes tomadas y emoción registrada

Se realiza el archivo gui.py que hace con TKinter una cajita con 3 botones de mommento, connect, run scrip, y disconnect, permite conectarse a un dispositov por ssh con su correspondiente clave publica lista, y corre el script the emociones.

# Jueves 18 de mayo

Se hace limpia de varias cosas del código para inferencia, para eliminar tantas dependecias de librerías como se pueda.

- Se elimina la dependencia de keras
- Se eliminan dependecias de algunos archivos de "util"

De momento se cuenta con los siguientes archivos requeridos en la rasberry pi para correr el sistema:

- emotions_pi.py
- model.tflite
- utils/inference.py
- models/haarcascade_frontalface_default.xml
 

# Sábado 20 de mayo

Se buscan otras opciones además de tkinter para realizar la gui del sistema "servidor"
Se prueba sin exito kviv, pyQT entre otros

Se empieza a utilizar con buenos resultados pysimpleimage.

Se basa en el siguiente (código base)[https://realpython.com/pysimplegui-python/#creating-a-pysimplegui-image-viewer] para desarrollar la aplicación con botones y visualización.

Se comienza a desarrollar varias funcionalidades:

- Corre programa
- Detener programa
- Actualizar la ultima foto
- Actualizar carpeta con todas las fotos
- Actualizar los valores configuracion: sample time, max time, max photos

Finalmente se tiene parametros de alta importancia para la implementación en la rasbery pi, al inicio del código `GUI.py`

```
# Set parameters
username = 'daniel'
ip = '192.168.100.113'
public_key = '/home/daniel/.ssh/embe'
remote_dir = '/home/daniel/s1-2023/embebidos/p2/Emociones/'

```
Se tiene también el archivo de pruebas de daniel gui_2.py (que es practicamente el mismo pero con unas lineas extras para correr el ambiente de anaconda)

## Martes 23 de mayo

Rachel se deja la rasberr PI para intentar usar el router de la casa para conectarse por ssh.
Le aydo por whatsapp

La conexipon funciona, pero hay problemas con la app, se van arreglando varios problemas como el `head -1` y la calve publica.

## Miercoles 24 de mayo 

Daniel lleva el extensor NETGEAR para intentar crear el punto de acceso y no depender de la red de electro. No funciona, se configura pero no se logra hacer funcionar.

Se utiliza la red de electro en un aula del segundo piso,  se logra conectarse correctamente. 


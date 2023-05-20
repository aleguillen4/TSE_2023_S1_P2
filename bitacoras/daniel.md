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



Referencias: bingchat

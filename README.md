# WhatsApp Web Automatization

## Descripción

Este proyecto permite enviar mensajes e imágenes a través de WhatsApp Web utilizando un script de Python. El script utiliza Selenium para automatizar la interacción con la interfaz web de WhatsApp.

## Archivos Necesarios

- configuration.exe:

Permite configurar el archivo config.txt que contiene información de rutas para el programa.

- config.txt:

Contiene las rutas de archivos para el uso del programa. Un excel para extraer los números de teléfono. Un archivo de texto con el mensaje a Enviar. Una carpeta de imágenes a enviar.

- numbers.xlsx:

Debe contener la primera columna con los números de teléfono a los que se enviarán los mensajes y las imágenes.
Ejemplo de estructura:

+51978456123
+51987654321
+51987656548

Ubicación: En la raíz del directorio del script.

- message.txt:

Contiene el texto que se enviará junto con las imágenes.
Ejemplo de contenido:

Copiar código
Hola, aquí está la imagen
Ubicación: En la raíz del directorio del script.

- Imágenes:

Coloca todas las imágenes que deseas enviar en una carpeta específica. Las imágenes deben estar en formatos compatibles (por ejemplo, .png, .jpg, .jpeg, .gif).
Ubicación: En la carpeta img dentro del directorio del script.

## Ejecución del Script

El script abrirá WhatsApp Web en tu navegador predeterminado. Escanea el código QR para iniciar sesión.
Espera a que el script complete:

El script leerá los números de teléfono desde el archivo Excel, el texto desde el archivo TXT y enviará las imágenes desde la carpeta especificada.
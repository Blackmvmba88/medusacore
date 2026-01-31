# Herramientas Asistente

Este repositorio contiene una colección de scripts y herramientas que hemos construido juntos para automatizar y mejorar nuestro flujo de trabajo.

## Aplicación Web de Control

Hemos construido una interfaz web para controlar nuestros scripts de una forma más visual y amigable.

### Cómo usarla

1.  **Instalar dependencias:**
    Primero, necesitas instalar Flask. Desde la carpeta `herramientas_asistente`, ejecuta:
    ```sh
    pip install -r requirements.txt
    ```

2.  **Iniciar la aplicación:**
    Una vez instaladas las dependencias, inicia el servidor web con:
    ```sh
    python3 nuestro_universo_app.py
    ```

3.  **Abrir en el navegador:**
    Abre tu navegador web y ve a la siguiente dirección: [http://127.0.0.1:5000](http://127.0.0.1:5000)

    Verás el panel de control desde donde podrás ejecutar los scripts.

## Scripts Base

### `limpiar_apps.sh`

Este es el script base que la aplicación web utiliza para cerrar las aplicaciones. Puedes modificar la lista de aplicaciones a cerrar editando este archivo directamente.

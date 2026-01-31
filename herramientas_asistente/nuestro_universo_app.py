import subprocess
import os
from flask import Flask, render_template, flash, redirect, url_for

app = Flask(__name__)
# Necesario para que los mensajes flash funcionen
app.secret_key = 'nuestro_universo_secreto'

@app.route('/')
def index():
    """Página principal que muestra el panel de control."""
    return render_template('index.html')

@app.route('/run-cleanup', methods=['POST'])
def run_cleanup():
    """Ejecuta el script de limpieza cuando se presiona el botón."""
    script_path = os.path.join(os.path.dirname(__file__), 'limpiar_apps.sh')
    
    try:
        # Ejecutamos el script. No es necesario capturar la salida si solo queremos que se ejecute.
        subprocess.run(['bash', script_path], check=True)
        flash('¡Las aplicaciones se han cerrado con éxito!')
    except FileNotFoundError:
        flash(f"Error: No se encontró el script en {script_path}")
    except subprocess.CalledProcessError as e:
        flash(f"Error durante la ejecución del script.")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Abrirá en http://127.0.0.1:5000
    app.run(debug=True)

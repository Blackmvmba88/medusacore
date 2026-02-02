"""MedusaCore Flask Web UI - Sistema de control y monitoreo

Esta aplicación web proporciona:
- Panel de control para gestión de scripts
- Monitoreo de rendimiento en tiempo real
- Integración con HermeticCore y Optimizer
- Visualización de métricas y logs
"""
import subprocess
import os
import sys
import time
from flask import Flask, render_template, flash, redirect, url_for, jsonify
from pathlib import Path

# Add parent directory to path to import core modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.seed import PrimordialSeed, HermeticCore, run_genesis_dry_run
from core.optimizer import Optimizer, PerformanceMonitor

app = Flask(__name__)
app.secret_key = 'medusacore_hermetic_secret_2024'

# Initialize core components
monitor = PerformanceMonitor(log_file="logs/performance.jsonl")
optimizer = Optimizer(monitor=monitor)
hermetic_core = HermeticCore()


@app.route('/')
def index():
    """Página principal con panel de control."""
    return render_template('index.html')


@app.route('/run-cleanup', methods=['POST'])
def run_cleanup():
    """Ejecuta el script de limpieza cuando se presiona el botón."""
    script_path = os.path.join(os.path.dirname(__file__), '..', 'limpiar_apps.sh')
    
    try:
        # Medir el rendimiento de la operación
        start_time = time.time()
        
        # Ejecutamos el script
        subprocess.run(['bash', script_path], check=True)
        
        duration = time.time() - start_time
        monitor.record_operation("cleanup_apps", duration, True)
        
        flash('¡Las aplicaciones se han cerrado con éxito!')
    except FileNotFoundError:
        monitor.record_operation("cleanup_apps", 0, False, metadata={"error": "script not found"})
        flash(f"Error: No se encontró el script en {script_path}")
    except subprocess.CalledProcessError as e:
        monitor.record_operation("cleanup_apps", 0, False, metadata={"error": str(e)})
        flash(f"Error durante la ejecución del script.")
    
    return redirect(url_for('index'))


@app.route('/api/genesis')
def api_genesis():
    """API endpoint para obtener información de Genesis."""
    result = run_genesis_dry_run()
    return jsonify({
        "success": True,
        "data": {
            "axiom_zero": result["axiom_zero"]["statement"],
            "principle_count": result["principle_count"],
            "principles": result["initial_principles"]
        }
    })


@app.route('/api/principles')
def api_principles():
    """API endpoint para obtener todos los principios."""
    principles = {
        name: hermetic_core.get_principle(name) 
        for name in hermetic_core.list_principles()
    }
    return jsonify({
        "success": True,
        "data": {
            "principles": principles,
            "count": len(principles)
        }
    })


@app.route('/api/performance')
def api_performance():
    """API endpoint para obtener métricas de rendimiento."""
    summary = monitor.get_summary()
    return jsonify({
        "success": True,
        "data": summary
    })


@app.route('/api/analysis')
def api_analysis():
    """API endpoint para obtener análisis de rendimiento."""
    analysis = optimizer.analyze_performance()
    return jsonify({
        "success": True,
        "data": analysis
    })


@app.route('/api/optimize', methods=['POST'])
def api_optimize():
    """API endpoint para ejecutar ciclo de optimización."""
    from core.optimizer import run_optimization_cycle
    
    result = run_optimization_cycle(optimizer, auto_adjust=True)
    return jsonify({
        "success": True,
        "data": result
    })


@app.route('/dashboard')
def dashboard():
    """Dashboard con visualización de métricas."""
    return render_template('dashboard.html')


if __name__ == '__main__':
    # Crear directorio de logs si no existe
    Path("logs").mkdir(exist_ok=True)
    
    print("\n" + "="*60)
    print("🌌 MedusaCore Flask WebUI")
    print("="*60)
    print(f"📍 Server: http://127.0.0.1:5000")
    print(f"📊 Dashboard: http://127.0.0.1:5000/dashboard")
    print(f"🔌 API Genesis: http://127.0.0.1:5000/api/genesis")
    print(f"📈 API Performance: http://127.0.0.1:5000/api/performance")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

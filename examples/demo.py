#!/usr/bin/env python3
"""
MedusaCore Demo - Complete example of the framework's capabilities

This script demonstrates:
1. Initializing AXIOM_ZERO and HermeticCore
2. Creating and using the Optimizer
3. Measuring operations
4. Running optimization cycles
5. Evolving principles based on evidence
"""
import time
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.seed import PrimordialSeed, HermeticCore, GenesisCommand, run_genesis_dry_run
from core.optimizer import Optimizer, PerformanceMonitor, run_optimization_cycle


def demo_axiom_zero():
    """Demonstrate AXIOM_ZERO initialization."""
    print("\n" + "="*60)
    print("🌌 AXIOM_ZERO - La Semilla Primordial")
    print("="*60)
    
    seed = PrimordialSeed.initialize()
    print(f"\n📜 Statement: {seed['statement']}")
    print(f"\n🔮 Essence:\n{seed['essence']}")
    print(f"\n💡 Meta-instruction:\n{seed['meta_instruction']}")


def demo_hermetic_core():
    """Demonstrate HermeticCore functionality."""
    print("\n" + "="*60)
    print("🔑 HermeticCore - Núcleo Hermético")
    print("="*60)
    
    core = HermeticCore()
    
    print(f"\n✨ Principios inicializados: {len(core.principles)}")
    print("\n📋 Lista de principios:")
    for i, principle in enumerate(core.list_principles(), 1):
        print(f"  {i}. {principle}")
    
    # Demonstrate principle evolution
    print("\n🔄 Evolucionando un principio...")
    entry = core.evolve_principle(
        principle_name="recursion",
        new_variant="La recursión es el camino hacia la comprensión profunda y la emergencia",
        conditions="ejemplo de demostración",
        evidence={"context": "demo script", "success": True}
    )
    print(f"  ✓ Evolución registrada: {entry['principle']}")
    print(f"  ✓ Timestamp: {entry['timestamp']['timestamp']}")
    print(f"  ✓ Nueva variante creada: recursion_v1")


def demo_genesis_command():
    """Demonstrate Genesis Command."""
    print("\n" + "="*60)
    print("🚀 Genesis Command - Primer Aliento")
    print("="*60)
    
    print(GenesisCommand.summary())


def demo_performance_monitoring():
    """Demonstrate performance monitoring."""
    print("\n" + "="*60)
    print("📊 Performance Monitoring")
    print("="*60)
    
    monitor = PerformanceMonitor()
    
    # Simulate some operations
    print("\n⚙️  Simulando operaciones...")
    operations = [
        ("initialization", 0.5, True),
        ("data_processing", 1.2, True),
        ("validation", 0.3, True),
        ("optimization", 2.1, True),
        ("error_handling", 0.8, False),
    ]
    
    for op_name, duration, success in operations:
        monitor.record_operation(op_name, duration, success)
        status = "✓" if success else "✗"
        print(f"  {status} {op_name}: {duration}s")
    
    # Get summary
    summary = monitor.get_summary()
    print(f"\n📈 Resumen:")
    print(f"  Total operaciones: {summary['total_operations']}")
    print(f"  Tasa de éxito: {summary['overall_success_rate']:.1f}%")
    print(f"  Duración promedio: {summary['overall_avg_duration']:.3f}s")
    
    return monitor


def demo_optimizer(monitor):
    """Demonstrate optimizer functionality."""
    print("\n" + "="*60)
    print("🎯 Optimizer - Auto-optimización")
    print("="*60)
    
    optimizer = Optimizer(monitor=monitor)
    
    # Analyze performance
    print("\n🔍 Analizando rendimiento...")
    analysis = optimizer.analyze_performance()
    
    print(f"\n🎨 Recomendaciones:")
    for i, rec in enumerate(analysis['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    if analysis['bottlenecks']:
        print(f"\n⚠️  Cuellos de botella detectados: {len(analysis['bottlenecks'])}")
        for bottleneck in analysis['bottlenecks']:
            print(f"  - {bottleneck['operation']}: {bottleneck['avg_duration']:.3f}s")
    
    if analysis['failing_operations']:
        print(f"\n❌ Operaciones fallidas: {len(analysis['failing_operations'])}")
        for failing in analysis['failing_operations']:
            print(f"  - {failing['operation']}: {failing['success_rate']:.1f}% éxito")
    
    # Run optimization
    print("\n🔧 Ejecutando ciclo de optimización...")
    result = run_optimization_cycle(optimizer, auto_adjust=True)
    
    if result['optimization'] and result['optimization']['changes']:
        print("\n✅ Parámetros optimizados:")
        for param, change in result['optimization']['changes'].items():
            print(f"  - {param}: {change['old']} → {change['new']}")
            print(f"    Razón: {change['reason']}")
    else:
        print("\n✅ No se requieren cambios en los parámetros actuales")


def demo_decorator():
    """Demonstrate the @measure_operation decorator."""
    print("\n" + "="*60)
    print("🎭 Decorator - Medición automática")
    print("="*60)
    
    optimizer = Optimizer()
    
    @optimizer.measure_operation("complex_calculation")
    def complex_calculation(n):
        """Simulate a complex calculation."""
        time.sleep(0.1)  # Simulate work
        return sum(i**2 for i in range(n))
    
    @optimizer.measure_operation("quick_operation")
    def quick_operation():
        """Simulate a quick operation."""
        time.sleep(0.01)
        return "done"
    
    print("\n⚙️  Ejecutando funciones decoradas...")
    result1 = complex_calculation(1000)
    print(f"  ✓ complex_calculation(1000) = {result1}")
    
    result2 = quick_operation()
    print(f"  ✓ quick_operation() = {result2}")
    
    # Show metrics
    summary = optimizer.monitor.get_summary()
    print(f"\n📊 Métricas capturadas:")
    for op, stats in summary['by_operation'].items():
        print(f"  - {op}:")
        print(f"    Duración: {stats['avg_duration']:.3f}s")
        print(f"    Éxito: {stats['success_rate']:.1f}%")


def main():
    """Run all demonstrations."""
    print("\n" + "🌌"*30)
    print(" "*20 + "MEDUSACORE DEMO")
    print("🌌"*30)
    
    try:
        # Run all demos
        demo_axiom_zero()
        demo_hermetic_core()
        demo_genesis_command()
        monitor = demo_performance_monitoring()
        demo_optimizer(monitor)
        demo_decorator()
        
        # Final message
        print("\n" + "="*60)
        print("✅ Demo completado exitosamente")
        print("="*60)
        print("\n💡 Próximos pasos:")
        print("  1. Ejecuta los tests: pytest tests/ -v")
        print("  2. Inicia el Flask UI: cd herramientas_asistente/Flask_webUI && python app.py")
        print("  3. Explora el dashboard: http://127.0.0.1:5000/dashboard")
        print("  4. Lee la documentación: README.md")
        print("\n🌌 MedusaCore - La evolución continúa...\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error durante el demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

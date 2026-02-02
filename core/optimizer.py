"""Optimizer module: Auto-optimization and performance monitoring for MedusaCore.

This module provides self-optimization capabilities including:
- Performance monitoring and metrics collection
- Automatic parameter adjustment based on performance
- Log analysis and pattern detection
- Dynamic resource allocation
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
import logging
import time
import json
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Container for performance metrics."""
    
    timestamp: str
    operation: str
    duration: float
    success: bool
    resource_usage: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "timestamp": self.timestamp,
            "operation": self.operation,
            "duration": self.duration,
            "success": self.success,
            "resource_usage": self.resource_usage,
            "metadata": self.metadata
        }


class PerformanceMonitor:
    """Monitors and tracks performance metrics for operations.
    
    This class provides real-time monitoring of system operations,
    collecting metrics that can be used for optimization decisions.
    """
    
    def __init__(self, log_file: Optional[str] = None):
        """Initialize the performance monitor.
        
        Args:
            log_file: Optional path to file for persisting metrics
        """
        self.metrics: List[PerformanceMetrics] = []
        self.log_file = Path(log_file) if log_file else None
        logger.info(f"PerformanceMonitor initialized (log_file: {self.log_file})")
    
    def record_operation(
        self,
        operation: str,
        duration: float,
        success: bool,
        resource_usage: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> PerformanceMetrics:
        """Record a completed operation with its metrics.
        
        Args:
            operation: Name/description of the operation
            duration: Time taken in seconds
            success: Whether the operation succeeded
            resource_usage: Optional resource usage data
            metadata: Optional additional metadata
            
        Returns:
            The recorded performance metrics
        """
        metrics = PerformanceMetrics(
            timestamp=datetime.utcnow().isoformat() + "Z",
            operation=operation,
            duration=duration,
            success=success,
            resource_usage=resource_usage or {},
            metadata=metadata or {}
        )
        
        self.metrics.append(metrics)
        logger.info(f"Recorded: {operation} - duration: {duration:.3f}s - success: {success}")
        
        if self.log_file:
            self._persist_metric(metrics)
        
        return metrics
    
    def _persist_metric(self, metric: PerformanceMetrics):
        """Persist a metric to the log file."""
        try:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(metric.to_dict()) + "\n")
        except Exception as e:
            logger.error(f"Failed to persist metric: {e}")
    
    def get_average_duration(self, operation: Optional[str] = None) -> float:
        """Get average duration for operations.
        
        Args:
            operation: Optional operation name to filter by
            
        Returns:
            Average duration in seconds
        """
        filtered = [m for m in self.metrics if operation is None or m.operation == operation]
        if not filtered:
            return 0.0
        return sum(m.duration for m in filtered) / len(filtered)
    
    def get_success_rate(self, operation: Optional[str] = None) -> float:
        """Get success rate for operations.
        
        Args:
            operation: Optional operation name to filter by
            
        Returns:
            Success rate as a percentage (0-100)
        """
        filtered = [m for m in self.metrics if operation is None or m.operation == operation]
        if not filtered:
            return 0.0
        successes = sum(1 for m in filtered if m.success)
        return (successes / len(filtered)) * 100
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all collected metrics."""
        operations = set(m.operation for m in self.metrics)
        
        return {
            "total_operations": len(self.metrics),
            "unique_operations": len(operations),
            "overall_success_rate": self.get_success_rate(),
            "overall_avg_duration": self.get_average_duration(),
            "by_operation": {
                op: {
                    "count": sum(1 for m in self.metrics if m.operation == op),
                    "avg_duration": self.get_average_duration(op),
                    "success_rate": self.get_success_rate(op)
                }
                for op in operations
            }
        }


class Optimizer:
    """Auto-optimization engine for MedusaCore.
    
    This class implements self-optimization capabilities:
    - Analyzes performance metrics
    - Identifies bottlenecks
    - Suggests and applies optimizations
    - Learns from past performance
    """
    
    def __init__(self, monitor: Optional[PerformanceMonitor] = None, bottleneck_threshold: float = 1.0):
        """Initialize the optimizer.
        
        Args:
            monitor: Optional performance monitor to use
            bottleneck_threshold: Duration threshold in seconds for identifying bottlenecks (default: 1.0)
        """
        self.monitor = monitor or PerformanceMonitor()
        self.optimization_log: List[Dict[str, Any]] = []
        self.parameters: Dict[str, Any] = self._initialize_parameters()
        self.bottleneck_threshold = bottleneck_threshold
        logger.info("Optimizer initialized")
    
    def _initialize_parameters(self) -> Dict[str, Any]:
        """Initialize default optimization parameters."""
        return {
            "max_retries": 3,
            "timeout_seconds": 30,
            "batch_size": 10,
            "learning_rate": 0.1,
            "optimization_threshold": 0.8  # 80% success rate threshold
        }
    
    def measure_operation(self, operation_name: str) -> Callable:
        """Decorator to measure and record operation performance.
        
        Args:
            operation_name: Name of the operation being measured
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                start_time = time.time()
                success = False
                result = None
                error = None
                
                try:
                    result = func(*args, **kwargs)
                    success = True
                except Exception as e:
                    error = str(e)
                    logger.error(f"Operation '{operation_name}' failed: {e}")
                    raise
                finally:
                    duration = time.time() - start_time
                    metadata = {"error": error} if error else {}
                    self.monitor.record_operation(
                        operation=operation_name,
                        duration=duration,
                        success=success,
                        metadata=metadata
                    )
                
                return result
            return wrapper
        return decorator
    
    def analyze_performance(self) -> Dict[str, Any]:
        """Analyze collected performance data and identify optimization opportunities.
        
        Returns:
            Analysis results with recommendations
        """
        logger.info("Analyzing performance data...")
        summary = self.monitor.get_summary()
        
        # Identify bottlenecks (operations with high duration)
        bottlenecks = []
        if summary.get("by_operation"):
            for op, stats in summary["by_operation"].items():
                if stats["avg_duration"] > self.bottleneck_threshold:
                    bottlenecks.append({
                        "operation": op,
                        "avg_duration": stats["avg_duration"],
                        "count": stats["count"]
                    })
        
        # Identify failing operations
        failing = []
        if summary.get("by_operation"):
            for op, stats in summary["by_operation"].items():
                if stats["success_rate"] < self.parameters["optimization_threshold"] * 100:
                    failing.append({
                        "operation": op,
                        "success_rate": stats["success_rate"],
                        "count": stats["count"]
                    })
        
        analysis = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "summary": summary,
            "bottlenecks": bottlenecks,
            "failing_operations": failing,
            "recommendations": self._generate_recommendations(bottlenecks, failing)
        }
        
        logger.info(f"Analysis complete - {len(bottlenecks)} bottlenecks, {len(failing)} failing operations")
        return analysis
    
    def _generate_recommendations(
        self, 
        bottlenecks: List[Dict[str, Any]], 
        failing: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate optimization recommendations based on analysis.
        
        Args:
            bottlenecks: List of identified bottlenecks
            failing: List of failing operations
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if bottlenecks:
            recommendations.append(
                f"Consider optimizing {len(bottlenecks)} slow operation(s): "
                f"{', '.join(b['operation'] for b in bottlenecks[:3])}"
            )
        
        if failing:
            recommendations.append(
                f"Investigate {len(failing)} operation(s) with low success rate: "
                f"{', '.join(f['operation'] for f in failing[:3])}"
            )
        
        if not bottlenecks and not failing:
            recommendations.append("System performance is within acceptable parameters")
        
        return recommendations
    
    def optimize_parameters(self, analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Automatically adjust optimization parameters based on performance.
        
        Args:
            analysis: Optional analysis results, will be generated if not provided
            
        Returns:
            Updated parameters and changes made
        """
        if analysis is None:
            analysis = self.analyze_performance()
        
        logger.info("Optimizing parameters...")
        changes = {}
        
        # Adjust max_retries based on failure rate
        overall_success = analysis["summary"].get("overall_success_rate", 100)
        if overall_success < 80 and self.parameters["max_retries"] < 5:
            old_value = self.parameters["max_retries"]
            self.parameters["max_retries"] = min(5, old_value + 1)
            changes["max_retries"] = {
                "old": old_value,
                "new": self.parameters["max_retries"],
                "reason": "Low success rate detected"
            }
        
        # Adjust batch_size based on performance
        avg_duration = analysis["summary"].get("overall_avg_duration", 0)
        if avg_duration > 2.0 and self.parameters["batch_size"] > 5:
            old_value = self.parameters["batch_size"]
            self.parameters["batch_size"] = max(5, int(old_value * 0.8))
            changes["batch_size"] = {
                "old": old_value,
                "new": self.parameters["batch_size"],
                "reason": "High average duration detected"
            }
        
        optimization_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "changes": changes,
            "new_parameters": self.parameters.copy()
        }
        
        self.optimization_log.append(optimization_entry)
        logger.info(f"Parameter optimization complete - {len(changes)} changes made")
        
        return optimization_entry
    
    def get_optimization_history(self) -> List[Dict[str, Any]]:
        """Get the history of optimization adjustments."""
        return self.optimization_log
    
    def reset_parameters(self):
        """Reset parameters to default values."""
        logger.info("Resetting parameters to defaults")
        self.parameters = self._initialize_parameters()


def run_optimization_cycle(
    optimizer: Optional[Optimizer] = None,
    auto_adjust: bool = True
) -> Dict[str, Any]:
    """Run a complete optimization cycle.
    
    Args:
        optimizer: Optional optimizer instance to use
        auto_adjust: Whether to automatically adjust parameters
        
    Returns:
        Results of the optimization cycle
    """
    if optimizer is None:
        optimizer = Optimizer()
    
    logger.info("Starting optimization cycle")
    
    # Analyze performance
    analysis = optimizer.analyze_performance()
    
    # Optionally optimize parameters
    optimization = None
    if auto_adjust:
        optimization = optimizer.optimize_parameters(analysis)
    
    result = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "analysis": analysis,
        "optimization": optimization,
        "current_parameters": optimizer.parameters.copy()
    }
    
    logger.info("Optimization cycle complete")
    return result


if __name__ == "__main__":
    # Demonstration of optimizer capabilities
    print("\n=== MedusaCore Optimizer Demo ===\n")
    
    # Create optimizer with monitor
    monitor = PerformanceMonitor(log_file="logs/performance.jsonl")
    optimizer = Optimizer(monitor=monitor)
    
    # Simulate some operations
    print("Simulating operations...")
    monitor.record_operation("initialization", 0.5, True)
    monitor.record_operation("processing", 1.2, True)
    monitor.record_operation("processing", 1.5, True)
    monitor.record_operation("validation", 0.3, False)
    monitor.record_operation("optimization", 2.1, True)
    
    # Run optimization cycle
    print("\nRunning optimization cycle...")
    result = run_optimization_cycle(optimizer, auto_adjust=True)
    
    # Display results
    print("\n=== Analysis Summary ===")
    summary = result["analysis"]["summary"]
    print(f"Total operations: {summary['total_operations']}")
    print(f"Success rate: {summary['overall_success_rate']:.1f}%")
    print(f"Average duration: {summary['overall_avg_duration']:.3f}s")
    
    print("\n=== Recommendations ===")
    for rec in result["analysis"]["recommendations"]:
        print(f"- {rec}")
    
    if result["optimization"] and result["optimization"]["changes"]:
        print("\n=== Parameter Changes ===")
        for param, change in result["optimization"]["changes"].items():
            print(f"- {param}: {change['old']} → {change['new']} ({change['reason']})")

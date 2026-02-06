"""Unit tests for optimizer module."""
import pytest
import time
from core.optimizer import (
    PerformanceMetrics,
    PerformanceMonitor,
    Optimizer,
    run_optimization_cycle
)


def test_performance_metrics_creation():
    """Test creating a PerformanceMetrics instance."""
    metrics = PerformanceMetrics(
        timestamp="2024-01-01T00:00:00Z",
        operation="test_op",
        duration=1.5,
        success=True,
        resource_usage={"cpu": 50},
        metadata={"version": "1.0"}
    )
    
    assert metrics.operation == "test_op"
    assert metrics.duration == 1.5
    assert metrics.success is True
    assert metrics.resource_usage["cpu"] == 50
    assert metrics.metadata["version"] == "1.0"


def test_performance_metrics_to_dict():
    """Test converting metrics to dictionary."""
    metrics = PerformanceMetrics(
        timestamp="2024-01-01T00:00:00Z",
        operation="test_op",
        duration=1.5,
        success=True
    )
    
    d = metrics.to_dict()
    assert d["operation"] == "test_op"
    assert d["duration"] == 1.5
    assert d["success"] is True
    assert "timestamp" in d


def test_performance_monitor_initialization():
    """Test PerformanceMonitor initialization."""
    monitor = PerformanceMonitor()
    assert len(monitor.metrics) == 0
    assert monitor.log_file is None


def test_performance_monitor_record_operation():
    """Test recording an operation."""
    monitor = PerformanceMonitor()
    
    metrics = monitor.record_operation(
        operation="test_operation",
        duration=0.5,
        success=True,
        resource_usage={"memory": 100},
        metadata={"test": True}
    )
    
    assert len(monitor.metrics) == 1
    assert metrics.operation == "test_operation"
    assert metrics.duration == 0.5
    assert metrics.success is True


def test_get_average_duration():
    """Test calculating average duration."""
    monitor = PerformanceMonitor()
    
    monitor.record_operation("op1", 1.0, True)
    monitor.record_operation("op1", 2.0, True)
    monitor.record_operation("op2", 3.0, True)
    
    # Average of all operations
    assert monitor.get_average_duration() == 2.0
    
    # Average for specific operation
    assert monitor.get_average_duration("op1") == 1.5
    assert monitor.get_average_duration("op2") == 3.0


def test_get_success_rate():
    """Test calculating success rate."""
    monitor = PerformanceMonitor()
    
    monitor.record_operation("op1", 1.0, True)
    monitor.record_operation("op1", 1.0, True)
    monitor.record_operation("op1", 1.0, False)
    monitor.record_operation("op2", 1.0, True)
    
    # Overall success rate: 3/4 = 75%
    assert monitor.get_success_rate() == 75.0
    
    # Success rate for op1: 2/3 = 66.67%
    assert abs(monitor.get_success_rate("op1") - 66.67) < 0.1
    
    # Success rate for op2: 1/1 = 100%
    assert monitor.get_success_rate("op2") == 100.0


def test_get_summary():
    """Test getting performance summary."""
    monitor = PerformanceMonitor()
    
    monitor.record_operation("op1", 1.0, True)
    monitor.record_operation("op1", 2.0, False)
    monitor.record_operation("op2", 0.5, True)
    
    summary = monitor.get_summary()
    
    assert summary["total_operations"] == 3
    assert summary["unique_operations"] == 2
    assert "overall_success_rate" in summary
    assert "by_operation" in summary
    assert "op1" in summary["by_operation"]
    assert "op2" in summary["by_operation"]


def test_optimizer_initialization():
    """Test Optimizer initialization."""
    optimizer = Optimizer()
    assert optimizer.monitor is not None
    assert len(optimizer.optimization_log) == 0
    assert "max_retries" in optimizer.parameters
    assert "timeout_seconds" in optimizer.parameters


def test_optimizer_with_custom_monitor():
    """Test Optimizer with custom monitor."""
    monitor = PerformanceMonitor()
    optimizer = Optimizer(monitor=monitor)
    assert optimizer.monitor is monitor


def test_initialize_parameters():
    """Test default parameters initialization."""
    optimizer = Optimizer()
    params = optimizer.parameters
    
    assert params["max_retries"] == 3
    assert params["timeout_seconds"] == 30
    assert params["batch_size"] == 10
    assert params["learning_rate"] == 0.1
    assert params["optimization_threshold"] == 0.8


def test_measure_operation_decorator_success():
    """Test the measure_operation decorator with successful operation."""
    optimizer = Optimizer()
    
    @optimizer.measure_operation("test_func")
    def test_function(x):
        time.sleep(0.01)  # Small delay
        return x * 2
    
    result = test_function(5)
    assert result == 10
    
    # Check that operation was recorded
    assert len(optimizer.monitor.metrics) == 1
    metric = optimizer.monitor.metrics[0]
    assert metric.operation == "test_func"
    assert metric.success is True
    assert metric.duration >= 0.01


def test_measure_operation_decorator_failure():
    """Test the measure_operation decorator with failing operation."""
    optimizer = Optimizer()
    
    @optimizer.measure_operation("failing_func")
    def failing_function():
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        failing_function()
    
    # Check that operation was recorded as failure
    assert len(optimizer.monitor.metrics) == 1
    metric = optimizer.monitor.metrics[0]
    assert metric.operation == "failing_func"
    assert metric.success is False
    assert "Test error" in metric.metadata.get("error", "")


def test_analyze_performance():
    """Test performance analysis."""
    optimizer = Optimizer()
    
    # Add some test data
    optimizer.monitor.record_operation("fast_op", 0.1, True)
    optimizer.monitor.record_operation("slow_op", 2.5, True)
    optimizer.monitor.record_operation("failing_op", 0.5, False)
    
    analysis = optimizer.analyze_performance()
    
    assert "timestamp" in analysis
    assert "summary" in analysis
    assert "bottlenecks" in analysis
    assert "failing_operations" in analysis
    assert "recommendations" in analysis


def test_generate_recommendations_with_bottlenecks():
    """Test recommendation generation with bottlenecks."""
    optimizer = Optimizer()
    
    # Simulate slow operations
    optimizer.monitor.record_operation("slow_op", 2.5, True)
    optimizer.monitor.record_operation("slow_op", 3.0, True)
    
    analysis = optimizer.analyze_performance()
    recommendations = analysis["recommendations"]
    
    assert len(recommendations) > 0
    assert any("slow" in rec.lower() or "optim" in rec.lower() for rec in recommendations)


def test_generate_recommendations_with_failures():
    """Test recommendation generation with failures."""
    optimizer = Optimizer()
    
    # Simulate failing operations
    optimizer.monitor.record_operation("failing_op", 0.5, False)
    optimizer.monitor.record_operation("failing_op", 0.5, False)
    optimizer.monitor.record_operation("failing_op", 0.5, False)
    
    analysis = optimizer.analyze_performance()
    recommendations = analysis["recommendations"]
    
    assert len(recommendations) > 0
    assert any("success rate" in rec.lower() or "investigat" in rec.lower() for rec in recommendations)


def test_optimize_parameters():
    """Test automatic parameter optimization."""
    optimizer = Optimizer()
    
    # Simulate poor performance
    for _ in range(10):
        optimizer.monitor.record_operation("test_op", 3.0, False)
    
    optimization = optimizer.optimize_parameters()
    
    assert "timestamp" in optimization
    assert "changes" in optimization
    assert "new_parameters" in optimization
    assert len(optimizer.optimization_log) == 1


def test_optimize_parameters_no_changes():
    """Test optimization when no changes are needed."""
    optimizer = Optimizer()
    
    # Simulate good performance
    optimizer.monitor.record_operation("test_op", 0.1, True)
    optimizer.monitor.record_operation("test_op", 0.1, True)
    
    optimization = optimizer.optimize_parameters()
    
    # Should have no changes or minimal changes
    assert "changes" in optimization


def test_get_optimization_history():
    """Test getting optimization history."""
    optimizer = Optimizer()
    
    # Run multiple optimization cycles
    optimizer.monitor.record_operation("op", 1.0, False)
    optimizer.optimize_parameters()
    
    optimizer.monitor.record_operation("op", 1.0, False)
    optimizer.optimize_parameters()
    
    history = optimizer.get_optimization_history()
    assert len(history) == 2


def test_reset_parameters():
    """Test resetting parameters to defaults."""
    optimizer = Optimizer()
    
    # Modify parameters
    optimizer.parameters["max_retries"] = 10
    optimizer.parameters["batch_size"] = 50
    
    # Reset
    optimizer.reset_parameters()
    
    # Should be back to defaults
    assert optimizer.parameters["max_retries"] == 3
    assert optimizer.parameters["batch_size"] == 10


def test_run_optimization_cycle():
    """Test running a complete optimization cycle."""
    monitor = PerformanceMonitor()
    optimizer = Optimizer(monitor=monitor)
    
    # Add some data
    monitor.record_operation("op1", 1.0, True)
    monitor.record_operation("op2", 2.0, False)
    
    result = run_optimization_cycle(optimizer, auto_adjust=True)
    
    assert "timestamp" in result
    assert "analysis" in result
    assert "optimization" in result
    assert "current_parameters" in result


def test_run_optimization_cycle_no_adjust():
    """Test running optimization cycle without auto-adjustment."""
    monitor = PerformanceMonitor()
    optimizer = Optimizer(monitor=monitor)
    
    monitor.record_operation("op1", 1.0, True)
    
    result = run_optimization_cycle(optimizer, auto_adjust=False)
    
    assert "analysis" in result
    assert result["optimization"] is None


def test_run_optimization_cycle_default_optimizer():
    """Test running optimization cycle with default optimizer."""
    result = run_optimization_cycle(optimizer=None, auto_adjust=True)
    
    assert "timestamp" in result
    assert "analysis" in result
    assert "current_parameters" in result

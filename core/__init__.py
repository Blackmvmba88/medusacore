"""MedusaCore - Core package for hermetic seed and optimization.

This package provides the fundamental building blocks for MedusaCore:
- PrimordialSeed (AXIOM_ZERO): The foundational seed for knowledge generation
- HermeticCore: Core system that derives principles and evolves
- Optimizer: Auto-optimization and performance monitoring
"""
from .seed import PrimordialSeed, HermeticCore, GenesisCommand
from .optimizer import Optimizer, PerformanceMonitor

__all__ = [
    "PrimordialSeed",
    "HermeticCore", 
    "GenesisCommand",
    "Optimizer",
    "PerformanceMonitor"
]
__version__ = "0.1.0"

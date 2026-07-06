"""
Logging utility for ai-kernel.

This module provides a centralized logging configuration.
"""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (typically __name__ or module path)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers and not logger.parent.handlers:
        logger.setLevel(logging.INFO)
        
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
    return logger


# Default module loggers
memory_logger = get_logger("ai_kernel.memory")
kernel_logger = get_logger("ai_kernel.kernel")
manager_logger = get_logger("ai_kernel.managers")
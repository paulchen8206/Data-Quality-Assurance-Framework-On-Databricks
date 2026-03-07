"""
Utility functions for the QA framework
"""
import logging
import yaml
from typing import Dict, Any
from pathlib import Path


def setup_logger(name: str = "qa_framework", level: int = logging.INFO) -> logging.Logger:
    """
    Setup and configure logger
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create console handler with formatting
    handler = logging.StreamHandler()
    handler.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


def read_config(config_path: str) -> Dict[str, Any]:
    """
    Read YAML configuration file
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid YAML
    """
    path = Path(config_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def format_validation_report(validation_summary: Dict[str, Any]) -> str:
    """
    Format validation summary into a readable report
    
    Args:
        validation_summary: Validation summary dictionary
        
    Returns:
        Formatted report string
    """
    report_lines = [
        "=" * 60,
        "DATA VALIDATION REPORT",
        "=" * 60,
        f"Total Checks: {validation_summary['total_checks']}",
        f"Passed: {validation_summary['passed_checks']}",
        f"Failed: {validation_summary['failed_checks']}",
        f"Pass Rate: {validation_summary['pass_rate']:.2%}",
        "=" * 60,
        ""
    ]
    
    for result in validation_summary["results"]:
        status = "✓ PASSED" if result["passed"] else "✗ FAILED"
        report_lines.append(f"{status} - {result['check']}: {result}")
    
    report_lines.append("=" * 60)
    
    return "\n".join(report_lines)

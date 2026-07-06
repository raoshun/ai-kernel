"""
Validation Helper - Shared validation utilities for reviewers and auditors.

Provides common patterns for:
- Error detection in execution output
- Task validation
- Result status classification
"""
from typing import Dict, Any, List, Literal
from src.models.core_entities import ExecutionStep

from ai_kernel._logging import manager_logger


# Error patterns to detect in output
ERROR_KEYWORDS = ["error", "failed", "exception", "traceback", "fatal", "critical"]
WARNING_KEYWORDS = ["warning", "warn", "deprecated", "timeout"]


class ExecutionValidator:
    """
    Validates execution steps and provides status classification.
    Centralizes error detection and output analysis.
    """
    
    @staticmethod
    def detect_errors_in_output(output: str) -> Dict[str, Any]:
        """
        Analyzes output for error/warning indicators.
        
        Returns:
            {
                'has_errors': bool,
                'has_warnings': bool,
                'error_keywords': List[str],
                'warning_keywords': List[str]
            }
        """
        if not output:
            return {
                'has_errors': False,
                'has_warnings': False,
                'error_keywords': [],
                'warning_keywords': []
            }
        
        output_lower = output.lower()
        found_errors = [kw for kw in ERROR_KEYWORDS if kw in output_lower]
        found_warnings = [kw for kw in WARNING_KEYWORDS if kw in output_lower]
        
        return {
            'has_errors': len(found_errors) > 0,
            'has_warnings': len(found_warnings) > 0,
            'error_keywords': found_errors,
            'warning_keywords': found_warnings
        }
    
    @staticmethod
    def validate_execution_steps(
        steps: List[ExecutionStep]
    ) -> Dict[str, Any]:
        """
        Validates a list of execution steps.
        
        Returns:
            {
                'total_steps': int,
                'successful_steps': int,
                'error_steps': int,
                'warning_steps': int,
                'issues': List[str],
                'step_details': List[Dict]
            }
        """
        result = {
            'total_steps': len(steps),
            'successful_steps': 0,
            'error_steps': 0,
            'warning_steps': 0,
            'issues': [],
            'step_details': []
        }
        
        for i, step in enumerate(steps):
            step_analysis = ExecutionValidator.detect_errors_in_output(step.actual_output)
            step_detail = {
                'index': i,
                'tool_name': step.tool_name,
                'has_output': bool(step.actual_output),
                'analysis': step_analysis
            }
            
            if not step.actual_output:
                result['warning_steps'] += 1
                result['issues'].append(f"Step {i}: Tool '{step.tool_name}' produced no output")
            elif step_analysis['has_errors']:
                result['error_steps'] += 1
                result['issues'].append(
                    f"Step {i}: Tool '{step.tool_name}' reported errors: {step_analysis['error_keywords']}"
                )
            elif step_analysis['has_warnings']:
                result['warning_steps'] += 1
                result['issues'].append(
                    f"Step {i}: Tool '{step.tool_name}' reported warnings: {step_analysis['warning_keywords']}"
                )
            else:
                result['successful_steps'] += 1
            
            step_detail['classification'] = ExecutionValidator._classify_step_status(step_analysis)
            result['step_details'].append(step_detail)
        
        return result
    
    @staticmethod
    def _classify_step_status(analysis: Dict[str, Any]) -> Literal["SUCCESS", "WARNING", "ERROR"]:
        """Classify step status based on analysis."""
        if analysis['has_errors']:
            return "ERROR"
        elif analysis['has_warnings']:
            return "WARNING"
        return "SUCCESS"
    
    @staticmethod
    def classify_overall_status(
        error_count: int,
        warning_count: int,
        success_count: int
    ) -> Literal["SUCCESS", "PARTIAL", "FAILED"]:
        """
        Classify overall execution status.
        
        Args:
            error_count: Number of failed steps
            warning_count: Number of steps with warnings
            success_count: Number of successful steps
            
        Returns:
            Overall status classification
        """
        if error_count > 0:
            return "FAILED"
        elif warning_count > 0:
            return "PARTIAL"
        return "SUCCESS"

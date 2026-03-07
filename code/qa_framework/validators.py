"""
Data validation module for quality checks
"""
from typing import List, Dict, Any, Optional
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, when, isnan, isnull


class DataValidator:
    """
    Validates data quality for DataFrames
    """
    
    def __init__(self, df: DataFrame):
        """
        Initialize validator with a DataFrame
        
        Args:
            df: PySpark DataFrame to validate
        """
        self.df = df
        self.validation_results = []
    
    def check_null_values(self, columns: Optional[List[str]] = None) -> Dict[str, int]:
        """
        Check for null values in specified columns
        
        Args:
            columns: List of column names to check. If None, checks all columns.
            
        Returns:
            Dictionary mapping column names to null counts
        """
        if columns is None:
            columns = self.df.columns
        
        null_counts = {}
        for column in columns:
            null_count = self.df.filter(
                col(column).isNull() | isnan(col(column))
            ).count()
            null_counts[column] = null_count
            
            self.validation_results.append({
                "check": "null_values",
                "column": column,
                "null_count": null_count,
                "passed": null_count == 0
            })
        
        return null_counts
    
    def check_duplicates(self, subset: Optional[List[str]] = None) -> int:
        """
        Check for duplicate rows
        
        Args:
            subset: List of columns to consider for duplicates. If None, uses all columns.
            
        Returns:
            Number of duplicate rows
        """
        total_count = self.df.count()
        distinct_count = self.df.dropDuplicates(subset=subset).count()
        duplicate_count = total_count - distinct_count
        
        self.validation_results.append({
            "check": "duplicates",
            "duplicate_count": duplicate_count,
            "passed": duplicate_count == 0
        })
        
        return duplicate_count
    
    def check_column_exists(self, column_name: str) -> bool:
        """
        Check if a column exists in the DataFrame
        
        Args:
            column_name: Name of the column to check
            
        Returns:
            True if column exists, False otherwise
        """
        exists = column_name in self.df.columns
        
        self.validation_results.append({
            "check": "column_exists",
            "column": column_name,
            "passed": exists
        })
        
        return exists
    
    def check_value_range(
        self, 
        column: str, 
        min_value: Optional[float] = None, 
        max_value: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Check if values in a column are within specified range
        
        Args:
            column: Column name to check
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            
        Returns:
            Dictionary with validation results
        """
        result = {"column": column, "violations": 0}
        
        if min_value is not None:
            violations = self.df.filter(col(column) < min_value).count()
            result["min_violations"] = violations
            result["violations"] += violations
        
        if max_value is not None:
            violations = self.df.filter(col(column) > max_value).count()
            result["max_violations"] = violations
            result["violations"] += violations
        
        self.validation_results.append({
            "check": "value_range",
            "column": column,
            "min_value": min_value,
            "max_value": max_value,
            "violations": result["violations"],
            "passed": result["violations"] == 0
        })
        
        return result
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get summary of all validation results
        
        Returns:
            Dictionary containing validation summary
        """
        total_checks = len(self.validation_results)
        passed_checks = sum(1 for r in self.validation_results if r["passed"])
        
        return {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": total_checks - passed_checks,
            "pass_rate": passed_checks / total_checks if total_checks > 0 else 0,
            "results": self.validation_results
        }

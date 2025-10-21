"""
Team Flex Credits Analytics Module
Parallel processing for large teams with model-level insights.
"""

from .team_daily_flex_credits import (
    fetch_parallel,
    aggregate_by_date,
    save_results
)

from .flex_credits_by_model import (
    aggregate_by_date_and_model,
    save_results as save_model_results
)

__all__ = [
    'fetch_parallel',
    'aggregate_by_date',
    'aggregate_by_date_and_model',
    'save_results',
    'save_model_results'
]

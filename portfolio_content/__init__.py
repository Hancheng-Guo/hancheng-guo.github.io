"""Offline content builder for the static portfolio."""
from .builder import Portfolio, ProjectPage
from .validators import ValidationReport, validate_document

__all__ = ["Portfolio", "ProjectPage", "ValidationReport", "validate_document"]

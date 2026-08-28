"""
Copyright (c) 2026 MongoDB Inc.

DISCLAIMER: THESE CODE SAMPLES ARE PROVIDED FOR EDUCATIONAL AND ILLUSTRATIVE PURPOSES ONLY,
TO DEMONSTRATE THE FUNCTIONALITY OF SPECIFIC MONGODB FEATURES.
THEY ARE NOT PRODUCTION-READY AND MAY LACK THE SECURITY HARDENING, ERROR HANDLING, AND TESTING REQUIRED FOR A LIVE ENVIRONMENT.
YOU ARE RESPONSIBLE FOR TESTING, VALIDATING, AND SECURING THIS CODE WITHIN YOUR OWN ENVIRONMENT BEFORE IMPLEMENTATION.
THIS MATERIAL IS PROVIDED "AS IS" WITHOUT WARRANTY OR LIABILITY.

Base class for FTDC analysis items.
"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path


class BaseItem(ABC):
    """Analyze FTDC files and render one section of the report."""

    def __init__(self, output_folder: str, config: dict, **_kwargs) -> None:
        self.config = config
        self.output_folder = Path(output_folder)
        self._logger = logging.getLogger(__name__)

    @property
    def name(self) -> str:
        """Human-readable item name."""
        return self.__class__.__name__

    @abstractmethod
    def analyze(self, file_path: Path) -> None:
        """Ingest one FTDC file."""
        raise NotImplementedError

    def finalize_analysis(self) -> None:
        """Finish analysis after all input files have been ingested."""

    @abstractmethod
    def review_results_markdown(self, output, section_number: int = 1) -> None:
        """Write this item's report section as Markdown."""
        raise NotImplementedError

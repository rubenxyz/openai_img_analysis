"""OpenAI Image Analyzer - Analyzes images from URLs using OpenAI Vision API."""

__version__ = "1.0.0"

from .analyzer import main, analyze_image

__all__ = ["main", "analyze_image"]
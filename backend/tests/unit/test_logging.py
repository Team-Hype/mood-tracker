# backend/tests/unit/test_logging.py
import pytest
import logging
import os
import tempfile
from datetime import datetime


class TestLogging:
    """Tests for logging configuration."""
    
    def test_logging_settings_have_required_attributes(self):
        """Test that logging settings have required attributes."""
        # Проверяем базовые настройки логгирования
        assert hasattr(logging, "DEBUG")
        assert hasattr(logging, "INFO")
        assert hasattr(logging, "WARNING")
        assert hasattr(logging, "ERROR")
    
    def test_logger_creation(self):
        """Test creating a logger."""
        logger = logging.getLogger("test_logger")
        assert logger is not None
        assert isinstance(logger, logging.Logger)
    
    def test_logger_set_level(self):
        """Test setting log level."""
        logger = logging.getLogger("test_logger_level")
        logger.setLevel(logging.DEBUG)
        assert logger.level == logging.DEBUG
        
        logger.setLevel(logging.ERROR)
        assert logger.level == logging.ERROR
    
    def test_logger_handlers(self):
        """Test adding handlers to logger."""
        logger = logging.getLogger("test_logger_handlers")
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        assert len(logger.handlers) > 0
    
    def test_log_file_creation(self, tmp_path):
        """Test that log file can be created."""
        log_file = tmp_path / "test.log"
        handler = logging.FileHandler(log_file)
        logger = logging.getLogger("test_file_logger")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        logger.info("Test message")
        handler.flush()
        
        assert log_file.exists()
        content = log_file.read_text()
        assert "Test message" in content
    
    def test_log_format(self):
        """Test log message formatting."""
        logger = logging.getLogger("test_format")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        # Проверяем, что формат установлен
        assert handler.formatter is not None
    
    def test_multiple_log_levels(self):
        """Test different log levels."""
        logger = logging.getLogger("test_levels")
        logger.setLevel(logging.DEBUG)
        
        assert logger.isEnabledFor(logging.DEBUG)
        assert logger.isEnabledFor(logging.INFO)
        assert logger.isEnabledFor(logging.WARNING)
        assert logger.isEnabledFor(logging.ERROR)
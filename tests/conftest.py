# pytest configuration file
import pytest
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

@pytest.fixture
def sample_topic():
    """Sample topic for testing"""
    return "Artificial Intelligence in Healthcare"

@pytest.fixture
def sample_research_points():
    """Sample research points for testing"""
    return [
        "AI applications in medical diagnosis",
        "Machine learning in drug discovery",
        "Robotic surgery and AI assistance",
        "Patient data analysis and prediction"
    ]

@pytest.fixture
def sample_article():
    """Sample article content for testing"""
    return """
    Artificial Intelligence in Healthcare
    
    Artificial Intelligence (AI) has revolutionized the healthcare industry in numerous ways. 
    From diagnostic tools to treatment planning, AI applications are becoming increasingly 
    prevalent in modern medical practice.
    
    Key applications include:
    • Medical imaging analysis
    • Drug discovery and development
    • Patient data management
    • Predictive analytics for disease prevention
    """ 
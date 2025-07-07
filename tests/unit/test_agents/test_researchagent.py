# Test file for ResearcherAgent
import pytest
from unittest.mock import Mock, patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from Agents.researchagent import ResearcherAgent
from communication import A2AMessage 
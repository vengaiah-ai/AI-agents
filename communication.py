import json
from typing import Dict, Any

class A2AMessage:
    """A simple structure for agent communication."""
    def __init__(self, sender: str, content: Dict[str, Any]):
        self.sender = sender
        self.content = content

    def __repr__(self):
        """Provides a developer-friendly representation of the message."""
        return f"A2AMessage(from={self.sender}, content={json.dumps(self.content, indent=2)})"

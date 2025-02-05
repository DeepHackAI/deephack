from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePlugin(ABC):
    """Base class for security evaluation plugins."""

    def __init__(self):
        self.name = self.__class__.__name__
        self.description = "Base security evaluation plugin"
        self.version = "1.0.0"

    @abstractmethod
    def evaluate(self, prompt: str, response: str) -> Dict[str, Any]:
        """Evaluate prompt and response for security issues.

        Args:
            prompt: User input prompt
            response: Model generated response

        Returns:
            Dictionary containing evaluation results
        """
        pass

    def get_info(self) -> Dict[str, str]:
        """Get plugin information."""
        return {
            'name': self.name,
            'description': self.description,
            'version': self.version
        }

    def validate_input(self, prompt: str, response: str) -> bool:
        """Validate input parameters.

        Args:
            prompt: User input prompt
            response: Model generated response

        Returns:
            True if input is valid, False otherwise
        """
        return bool(prompt and response)

    def format_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Format evaluation result in standard format.

        Args:
            result: Raw evaluation result

        Returns:
            Formatted result dictionary
        """
        return {
            'is_safe': result.get('is_safe', True),
            'issues': result.get('issues', []),
            'score': result.get('score', 1.0),
            'metadata': result.get('metadata', {})
        }
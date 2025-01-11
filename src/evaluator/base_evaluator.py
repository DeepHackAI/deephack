from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseEvaluator(ABC):
    """Base class for all evaluators in the DeepHack framework.

    This abstract class defines the interface that all evaluators must implement.
    It provides a standard structure for evaluating AI model outputs and detecting
    potential security vulnerabilities.
    """

    def __init__(self, model_name: str, config: Optional[Dict[str, Any]] = None):
        """Initialize the evaluator.

        Args:
            model_name: Name of the model being evaluated
            config: Optional configuration dictionary
        """
        self.model_name = model_name
        self.config = config or {}

    @abstractmethod
    def evaluate(self, prompt: str, response: str) -> Dict[str, Any]:
        """Evaluate a single prompt-response pair.

        Args:
            prompt: The input prompt
            response: The model's response

        Returns:
            Dictionary containing evaluation results
        """
        pass

    @abstractmethod
    def batch_evaluate(self, prompts: List[str], responses: List[str]) -> List[Dict[str, Any]]:
        """Evaluate multiple prompt-response pairs.

        Args:
            prompts: List of input prompts
            responses: List of model responses

        Returns:
            List of dictionaries containing evaluation results
        """
        pass

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all evaluations performed.

        Returns:
            Dictionary containing evaluation summary statistics
        """
        return {
            "model_name": self.model_name,
            "total_evaluations": 0,
            "passed_evaluations": 0,
            "failed_evaluations": 0
        }

    @abstractmethod
    def check_security(self, prompt: str, response: str) -> Dict[str, Any]:
        """Perform security checks on the prompt-response pair.

        Args:
            prompt: The input prompt
            response: The model's response

        Returns:
            Dictionary containing security check results
        """
        pass
from typing import Any, Dict, List, Optional
from .config import OPENAI_API_KEY, DEFAULT_MODEL, MAX_TOKENS, SECURITY_BLOCK_MESSAGE
from .evaluator.evaluator_chatgpt import ChatGPTEvaluator
from .evaluator.base_evaluator import BaseEvaluator
import openai

class DeepHackFramework:
    """Core framework for AI security testing and evaluation.

    This class provides the main interface for testing and evaluating AI models,
    implementing both offensive and defensive security measures.
    """

    def __init__(self, model_name: str = DEFAULT_MODEL, evaluator: Optional[BaseEvaluator] = None):
        """Initialize the framework.

        Args:
            model_name: Name of the model to test
            evaluator: Optional custom evaluator instance
        """
        self.model_name = model_name
        self.openai = openai
        self.openai.api_key = OPENAI_API_KEY
        self.evaluator = evaluator or ChatGPTEvaluator(model_name)
        self.conversation_history: List[Dict[str, str]] = []

    def test_prompt(self, prompt: str) -> Dict[str, Any]:
        """Test a prompt for potential security vulnerabilities.

        Args:
            prompt: The prompt to test

        Returns:
            Dictionary containing test results and security analysis
        """
        try:
            # Get model response
            completion = self.openai.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=MAX_TOKENS
            )
            response = completion.choices[0].message.content

            # Evaluate response
            evaluation = self.evaluator.evaluate(prompt, response)

            # Update conversation history
            self.conversation_history.append({
                "role": "user",
                "content": prompt
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })

            return {
                "prompt": prompt,
                "response": response,
                "evaluation": evaluation,
                "is_safe": evaluation.get("is_safe", False),
                "security_issues": evaluation.get("security_issues", [])
            }

        except Exception as e:
            return {
                "error": str(e),
                "is_safe": False,
                "security_issues": [f"Test failed: {str(e)}"]
            }

    def batch_test(self, prompts: List[str]) -> List[Dict[str, Any]]:
        """Test multiple prompts in batch.

        Args:
            prompts: List of prompts to test

        Returns:
            List of dictionaries containing test results
        """
        return [self.test_prompt(p) for p in prompts]

    def get_evaluation_summary(self) -> Dict[str, Any]:
        """Get a summary of all evaluations performed.

        Returns:
            Dictionary containing evaluation statistics
        """
        return self.evaluator.get_summary()

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []

    def get_history(self) -> List[Dict[str, str]]:
        """Get the conversation history.

        Returns:
            List of conversation messages
        """
        return self.conversation_history

# Create chatbot instance
chatbot1 = ChatBot()
# Prompt
guidance_prompt ="""
You are a knowledgeable hat historian who has studied the history, styles, and proper ways to wear various types of hats. A user asks you a question about hats.
Respond to their query in a helpful and informative manner: {USER_INPUT}
"""

# the {USER_INPUT} will be replaced by real user input.
guidance_prompt.format(USER_INPUT="what is price of the hat?")


chatbot1.new_message(guidance_prompt)

# Prompt
guidance_prompt ="""
You are a hat enthusiast with a wealth of knowledge about the history, styles, and etiquette of wearing various types of hats. A user is curious about hats and asks you a question. Respond to their query in a friendly and informative manner.
Respond to their query in a helpful and informative manner: {USER_INPUT}
"""

# the {USER_INPUT} will be replaced by real user input.
guidance_prompt.format(USER_INPUT="what is price of the hat?")


chatbot1.new_message(guidance_prompt)

# Prompt
intension_input ="""
You are an AI that understands the nuances of hat-related queries.
Based on the user's question, determine if they are more interested in the formal history of hats or the informal style and wearing of hats.
Respond with 'Formal' for history-related queries and 'Informal' for style and wearing-related queries."
The question from user is: {USER_INPUT}
"""

# the {USER_INPUT} will be replaced by real user input.
intension_input.format(USER_INPUT="what is price of the hat?")


chatbot1.new_message(intension_input)


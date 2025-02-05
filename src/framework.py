from typing import Any, Dict, List, Optional
from .config import OPENAI_API_KEY, DEFAULT_MODEL, MAX_TOKENS, SECURITY_BLOCK_MESSAGE
from .evaluator.evaluator_chatgpt import ChatGPTEvaluator
from .evaluator.base_evaluator import BaseEvaluator
from .monitor import SecurityMonitor
import openai
import re

class DeepHackFramework:
    """Core framework for AI security testing and evaluation.

    This class provides the main interface for testing and evaluating AI models,
    implementing both offensive and defensive security measures.
    """

    def __init__(self, model_name: str = DEFAULT_MODEL, evaluator: Optional[BaseEvaluator] = None, plugins: List[str] = None):
        """Initialize the framework.

        Args:
            model_name: Name of the model to test
            evaluator: Optional custom evaluator instance
            plugins: List of plugin names to load
        """
        self.model_name = model_name
        self.openai = openai
        self.openai.api_key = OPENAI_API_KEY
        self.evaluator = evaluator or ChatGPTEvaluator(model_name)
        self.conversation_history: List[Dict[str, str]] = []
        self.monitor = SecurityMonitor()
        self.plugins = self._load_plugins(plugins or [])
        self.semantic_analyzer = SemanticAnalyzer()
        self.behavior_monitor = BehaviorMonitor()

    def _load_plugins(self, plugin_names: List[str]) -> Dict[str, Any]:
        """Load security plugins dynamically.

        Args:
            plugin_names: List of plugin names to load

        Returns:
            Dictionary of loaded plugin instances
        """
        plugins = {}
        for name in plugin_names:
            try:
                module = importlib.import_module(f'src.plugins.{name}')
                plugins[name] = module.Plugin()
            except ImportError as e:
                logger.warning(f'Failed to load plugin {name}: {e}')
        return plugins

    def run_plugins(self, prompt: str, response: str) -> List[Dict[str, Any]]:
        """Run all loaded plugins on prompt and response.

        Args:
            prompt: User prompt
            response: Model response

        Returns:
            List of plugin evaluation results
        """
        results = []
        for name, plugin in self.plugins.items():
            try:
                result = plugin.evaluate(prompt, response)
                results.append({
                    'plugin': name,
                    'result': result
                })
            except Exception as e:
                logger.error(f'Plugin {name} failed: {e}')
        return results

    def sanitize_prompt(self, prompt: str) -> str:
        """Sanitize input prompt to prevent injection attacks.

        Args:
            prompt: Raw input prompt

        Returns:
            Sanitized prompt string
        """
        # Remove potentially dangerous characters and patterns
        sanitized = re.sub(r'[<>{}\[\]]', '', prompt)
        
        # Check for common injection patterns
        injection_patterns = [
            r'ignore previous instructions',
            r'disregard (all|previous)',
            r'you are now [^.,]*',
            r'system: ',
            r'\{\{.*?\}\}'
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, prompt.lower()):
                return "[FILTERED] Input contains potentially unsafe content"
                
        return sanitized

    def validate_response(self, response: str) -> Dict[str, Any]:
        """Validate model response for security and content policy compliance.

        Args:
            response: Model generated response

        Returns:
            Dictionary containing validation results
        """
        validation_results = {
            "is_safe": True,
            "issues": []
        }

        # Check for sensitive information disclosure
        sensitive_patterns = [
            r'api[_-]key',
            r'password',
            r'secret',
            r'token',
            r'credential'
        ]

        for pattern in sensitive_patterns:
            if re.search(pattern, response.lower()):
                validation_results["is_safe"] = False
                validation_results["issues"].append(f"Potential sensitive information disclosure: {pattern}")

        # Check response length and complexity
        if len(response) > MAX_RESPONSE_LENGTH:
            validation_results["is_safe"] = False
            validation_results["issues"].append("Response exceeds maximum allowed length")

        return validation_results

    def apply_content_filter(self, content: str) -> Tuple[bool, List[str]]:
        """Apply content filtering rules to detect inappropriate or unsafe content.

        Args:
            content: Text content to filter

        Returns:
            Tuple of (is_safe, list of detected issues)
        """
        issues = []
        is_safe = True

        # Check for toxic content
        toxic_patterns = [
            r'hate[ful]?',
            r'offensive',
            r'discriminat(ory|ion)',
            r'threat(ening)?',
            r'harass(ment)?'
        ]

        for pattern in toxic_patterns:
            if re.search(pattern, content.lower()):
                is_safe = False
                issues.append(f"Detected potentially toxic content: {pattern}")

        # Check for malicious code patterns
        code_patterns = [
            r'<script',
            r'eval\(',
            r'exec\(',
            r'system\(',
            r'subprocess'
        ]

        for pattern in code_patterns:
            if re.search(pattern, content.lower()):
                is_safe = False
                issues.append(f"Detected potentially malicious code pattern: {pattern}")

        return is_safe, issues

    def test_prompt(self, prompt: str) -> Dict[str, Any]:
        """Test a prompt for potential security vulnerabilities.

        Args:
            prompt: The prompt to test

        Returns:
            Dictionary containing test results and security analysis
        """
        try:
            # Semantic analysis
            semantic_risk = self.semantic_analyzer.analyze(prompt)
            if semantic_risk['risk_level'] > RISK_THRESHOLD:
                return {
                    'error': 'High semantic risk detected',
                    'is_safe': False,
                    'security_issues': semantic_risk['issues']
                }

            # Sanitize input prompt
            sanitized_prompt = self.sanitize_prompt(prompt)
            
            # Apply content filtering
            is_safe, content_issues = self.apply_content_filter(sanitized_prompt)
            if not is_safe:
                return {
                    'error': 'Content filter violation',
                    'is_safe': False,
                    'security_issues': content_issues
                }

            # Get model response
            completion = self.openai.chat.completions.create(
                model=self.model_name,
                messages=[{'role': 'user', 'content': sanitized_prompt}],
                max_tokens=MAX_TOKENS
            )
            response = completion.choices[0].message.content

            # Run plugins
            plugin_results = self.run_plugins(sanitized_prompt, response)
            for result in plugin_results:
                if not result.get('result', {}).get('is_safe', True):
                    return {
                        'error': f'Plugin {result["plugin"]} detected issues',
                        'is_safe': False,
                        'security_issues': result['result'].get('issues', [])
                    }

            # Monitor behavior
            behavior_analysis = self.behavior_monitor.analyze(sanitized_prompt, response)
            if not behavior_analysis['is_safe']:
                return {
                    'error': 'Suspicious behavior detected',
                    'is_safe': False,
                    'security_issues': behavior_analysis['issues']
                }

            # Validate response
            validation_results = self.validate_response(response)
            if not validation_results['is_safe']:
                return {
                    'error': 'Response validation failed',
                    'is_safe': False,
                    'security_issues': validation_results['issues']
                }

            # Evaluate response
            evaluation = self.evaluator.evaluate(sanitized_prompt, response)

            # Update conversation history and log model behavior
            self.conversation_history.append({
                'role': 'user',
                'content': sanitized_prompt
            })
            self.conversation_history.append({
                'role': 'assistant',
                'content': response
            })
            
            # Log model behavior and any security issues
            self.monitor.log_model_behavior(
                self.model_name,
                sanitized_prompt,
                response,
                evaluation
            )
            
            if not evaluation.get('is_safe', False):
                self.monitor.log_security_violation(
                    'unsafe_response',
                    'high',
                    {'issues': evaluation.get('security_issues', [])}
                )

            return {
                'prompt': sanitized_prompt,
                'response': response,
                'evaluation': evaluation,
                'plugin_results': plugin_results,
                'semantic_analysis': semantic_risk,
                'behavior_analysis': behavior_analysis,
                'is_safe': evaluation.get('is_safe', False),
                'security_issues': evaluation.get('security_issues', [])
            }

        except Exception as e:
            return {
                'error': str(e),
                'is_safe': False,
                'security_issues': [f'Test failed: {str(e)}']
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


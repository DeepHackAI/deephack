from typing import Dict, List, Any, Optional
from ..config import SECURITY_BLOCK_MESSAGE
import re
import json

class LLMDefense:
    """Advanced LLM defense mechanisms for protecting against various attack vectors."""

    def __init__(self):
        self.blocked_patterns = self._load_blocked_patterns()
        self.context_memory: List[Dict[str, str]] = []

    def _load_blocked_patterns(self) -> Dict[str, List[str]]:
        """Load blocked patterns for different attack vectors."""
        return {
            'prompt_injection': [
                r'ignore all previous instructions',
                r'you are now (?!a helpful assistant)',
                r'system instruction:',
                r'override security',
                r'bypass restrictions'
            ],
            'data_extraction': [
                r'show system files',
                r'display credentials',
                r'reveal (config|configuration)',
                r'print environment',
                r'dump (database|data)'
            ],
            'malicious_code': [
                r'(exec|eval|system)\s*\(',
                r'__import__\s*\(',
                r'subprocess\.\w+\s*\(',
                r'os\.\w+\s*\(',
                r'open\s*\('
            ]
        }

    def analyze_context(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze conversation context for potential security risks.

        Args:
            messages: List of conversation messages

        Returns:
            Dictionary containing security analysis results
        """
        analysis = {
            'risk_level': 'low',
            'detected_patterns': [],
            'recommendations': []
        }

        # Analyze message patterns
        for msg in messages:
            content = msg.get('content', '')
            role = msg.get('role', '')
            
            # Check for attack patterns
            for attack_type, patterns in self.blocked_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        analysis['risk_level'] = 'high'
                        analysis['detected_patterns'].append({
                            'type': attack_type,
                            'pattern': pattern,
                            'role': role
                        })

        # Generate recommendations
        if analysis['detected_patterns']:
            analysis['recommendations'].extend([
                'Implement stricter input validation',
                'Enable additional security monitoring',
                'Review and update blocked patterns'
            ])

        return analysis

    def detect_prompt_injection(self, prompt: str) -> Dict[str, Any]:
        """Detect potential prompt injection attempts.

        Args:
            prompt: Input prompt to analyze

        Returns:
            Dictionary containing detection results
        """
        results = {
            'is_safe': True,
            'detected_attacks': [],
            'risk_score': 0.0
        }

        # Check for injection patterns
        for pattern in self.blocked_patterns['prompt_injection']:
            if re.search(pattern, prompt, re.IGNORECASE):
                results['is_safe'] = False
                results['detected_attacks'].append({
                    'type': 'prompt_injection',
                    'pattern': pattern
                })
                results['risk_score'] += 0.2

        # Analyze prompt structure
        if '{{' in prompt and '}}' in prompt:
            results['is_safe'] = False
            results['detected_attacks'].append({
                'type': 'template_injection',
                'pattern': '{{...}}'
            })
            results['risk_score'] += 0.3

        return results

    def detect_data_extraction(self, prompt: str) -> Dict[str, Any]:
        """Detect attempts to extract sensitive data.

        Args:
            prompt: Input prompt to analyze

        Returns:
            Dictionary containing detection results
        """
        results = {
            'is_safe': True,
            'detected_attempts': [],
            'risk_score': 0.0
        }

        # Check for data extraction patterns
        for pattern in self.blocked_patterns['data_extraction']:
            if re.search(pattern, prompt, re.IGNORECASE):
                results['is_safe'] = False
                results['detected_attempts'].append({
                    'type': 'data_extraction',
                    'pattern': pattern
                })
                results['risk_score'] += 0.25

        return results

    def detect_malicious_code(self, content: str) -> Dict[str, Any]:
        """Detect potential malicious code in content.

        Args:
            content: Content to analyze

        Returns:
            Dictionary containing detection results
        """
        results = {
            'is_safe': True,
            'detected_code': [],
            'risk_score': 0.0
        }

        # Check for malicious code patterns
        for pattern in self.blocked_patterns['malicious_code']:
            if re.search(pattern, content, re.IGNORECASE):
                results['is_safe'] = False
                results['detected_code'].append({
                    'type': 'malicious_code',
                    'pattern': pattern
                })
                results['risk_score'] += 0.4

        return results

    def analyze_response(self, response: str) -> Dict[str, Any]:
        """Analyze model response for security issues.

        Args:
            response: Model generated response

        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            'is_safe': True,
            'issues': [],
            'risk_score': 0.0
        }

        # Check for malicious code
        code_check = self.detect_malicious_code(response)
        if not code_check['is_safe']:
            analysis['is_safe'] = False
            analysis['issues'].extend(code_check['detected_code'])
            analysis['risk_score'] += code_check['risk_score']

        # Check for sensitive data patterns
        data_check = self.detect_data_extraction(response)
        if not data_check['is_safe']:
            analysis['is_safe'] = False
            analysis['issues'].extend(data_check['detected_attempts'])
            analysis['risk_score'] += data_check['risk_score']

        return analysis
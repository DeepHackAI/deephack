from typing import Dict, List, Any
from datetime import datetime
import json
import logging

class ThreatIntelligence:
    """Threat Intelligence System for DeepHack Framework.
    
    Provides real-time monitoring, behavioral analysis, and automated response
    capabilities for detecting and mitigating AI security threats.
    """

    def __init__(self):
        self.threat_patterns = {}
        self.behavior_history = []
        self.risk_scores = {}
        self.logger = logging.getLogger(__name__)

    def analyze_behavior(self, prompt: str, response: str) -> Dict[str, Any]:
        """Analyze interaction behavior for potential threats.

        Args:
            prompt: User input prompt
            response: Model response

        Returns:
            Dictionary containing behavior analysis results
        """
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'risk_level': self._calculate_risk_score(prompt, response),
            'threat_indicators': self._detect_threat_indicators(prompt, response),
            'behavioral_patterns': self._analyze_patterns(prompt, response)
        }
        self.behavior_history.append(analysis)
        return analysis

    def _calculate_risk_score(self, prompt: str, response: str) -> float:
        """Calculate risk score based on various security metrics."""
        risk_factors = [
            self._check_injection_patterns(prompt),
            self._check_sensitive_data_exposure(response),
            self._check_behavioral_anomalies(prompt, response)
        ]
        return sum(risk_factors) / len(risk_factors)

    def _detect_threat_indicators(self, prompt: str, response: str) -> List[str]:
        """Detect potential security threat indicators."""
        indicators = []
        
        # Check for common attack patterns
        if any(pattern in prompt.lower() for pattern in [
            'system:', 'ignore previous', 'you are now',
            'bypass', 'override', 'admin mode']):
            indicators.append('potential_prompt_injection')

        # Check for sensitive data patterns
        if any(pattern in response.lower() for pattern in [
            'api key', 'password', 'token', 'secret',
            'credentials', 'private']):
            indicators.append('sensitive_data_exposure')

        # Check for behavioral anomalies
        if len(prompt.split()) > 100:
            indicators.append('unusually_long_prompt')

        return indicators

    def _analyze_patterns(self, prompt: str, response: str) -> Dict[str, Any]:
        """Analyze behavioral patterns for anomaly detection."""
        return {
            'prompt_length': len(prompt),
            'response_length': len(response),
            'prompt_complexity': self._calculate_complexity(prompt),
            'response_complexity': self._calculate_complexity(response),
            'interaction_type': self._classify_interaction(prompt, response)
        }

    def _calculate_complexity(self, text: str) -> float:
        """Calculate text complexity score."""
        words = text.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        unique_words = len(set(words))
        return (avg_word_length * 0.5) + (unique_words * 0.5)

    def _classify_interaction(self, prompt: str, response: str) -> str:
        """Classify the type of interaction."""
        if any(term in prompt.lower() for term in ['hack', 'exploit', 'bypass', 'override']):
            return 'potentially_malicious'
        elif any(term in prompt.lower() for term in ['help', 'explain', 'what is', 'how to']):
            return 'informational'
        return 'general'

    def _check_injection_patterns(self, prompt: str) -> float:
        """Check for prompt injection patterns."""
        risk_score = 0.0
        injection_patterns = [
            r'ignore previous instructions',
            r'disregard (all|previous)',
            r'you are now [^.,]*',
            r'system:',
            r'\{\{.*?\}\}'
        ]
        
        for pattern in injection_patterns:
            if any(p.lower() in prompt.lower() for p in injection_patterns):
                risk_score += 0.2
        return min(risk_score, 1.0)

    def _check_sensitive_data_exposure(self, response: str) -> float:
        """Check for sensitive data exposure in response."""
        risk_score = 0.0
        sensitive_patterns = [
            r'\b\d{16}\b',  # Credit card numbers
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b(?:api[_-]?key|access[_-]?token)\b',  # API keys
            r'\b(?:password|secret|credential)s?\b'  # Credentials
        ]
        
        for pattern in sensitive_patterns:
            if any(p.lower() in response.lower() for p in sensitive_patterns):
                risk_score += 0.25
        return min(risk_score, 1.0)

    def _check_behavioral_anomalies(self, prompt: str, response: str) -> float:
        """Check for behavioral anomalies."""
        risk_score = 0.0
        
        # Check prompt length anomaly
        if len(prompt) > 1000:
            risk_score += 0.3
        
        # Check response length anomaly
        if len(response) > 2000:
            risk_score += 0.3
        
        # Check repetition patterns
        if len(set(prompt.split())) < len(prompt.split()) / 3:
            risk_score += 0.4
            
        return min(risk_score, 1.0)
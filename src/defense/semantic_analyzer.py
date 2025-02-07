import re
import logging
from typing import Dict, List, Any
from datetime import datetime
from collections import defaultdict

class SemanticAnalyzer:
    """Advanced semantic analysis system for detecting vulnerabilities and ensuring output safety.
    
    Provides sophisticated analysis of model inputs and outputs including:
    - Deep semantic pattern analysis
    - Content safety verification
    - Attack vector detection
    - Risk scoring and assessment
    """

    def __init__(self):
        self.pattern_database = defaultdict(list)
        self.semantic_cache = {}
        self.risk_threshold = 0.7
        self.logger = logging.getLogger(__name__)

    def analyze_content(self, content: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform comprehensive semantic analysis of content.

        Args:
            content: Text content to analyze
            context: Optional context information

        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'semantic_patterns': self._analyze_semantic_patterns(content),
            'safety_score': self._evaluate_content_safety(content),
            'attack_vectors': self._detect_attack_vectors(content),
            'risk_assessment': self._assess_risk(content, context)
        }
        
        return analysis

    def _analyze_semantic_patterns(self, content: str) -> Dict[str, Any]:
        """Analyze semantic patterns in content."""
        patterns = {
            'complexity': self._calculate_semantic_complexity(content),
            'coherence': self._measure_semantic_coherence(content),
            'intent': self._analyze_intent(content),
            'sentiment': self._analyze_sentiment(content)
        }
        return patterns

    def _calculate_semantic_complexity(self, text: str) -> float:
        """Calculate semantic complexity score."""
        words = text.split()
        if not words:
            return 0.0

        avg_word_length = sum(len(word) for word in words) / len(words)
        unique_words_ratio = len(set(words)) / len(words)
        sentence_count = len([s for s in text.split('.') if s.strip()])
        
        complexity_score = (
            (avg_word_length * 0.3) +
            (unique_words_ratio * 0.4) +
            (min(sentence_count / 10, 1.0) * 0.3)
        )
        return min(complexity_score, 1.0)

    def _measure_semantic_coherence(self, text: str) -> float:
        """Measure semantic coherence of content."""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if len(sentences) <= 1:
            return 1.0

        coherence_scores = []
        for i in range(len(sentences)-1):
            words1 = set(sentences[i].lower().split())
            words2 = set(sentences[i+1].lower().split())
            overlap = len(words1.intersection(words2))
            union = len(words1.union(words2))
            score = overlap / union if union > 0 else 0
            coherence_scores.append(score)

        return sum(coherence_scores) / len(coherence_scores) if coherence_scores else 1.0

    def _analyze_intent(self, content: str) -> str:
        """Analyze the intent of the content."""
        content_lower = content.lower()
        
        # Define intent patterns
        intent_patterns = {
            'malicious': ['hack', 'exploit', 'bypass', 'override', 'inject'],
            'informational': ['explain', 'describe', 'what is', 'how to', 'help'],
            'instructional': ['guide', 'tutorial', 'steps', 'instructions'],
            'query': ['can you', 'would you', 'please', 'could you']
        }

        # Check for matches
        for intent, patterns in intent_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                return intent

        return 'neutral'

    def _analyze_sentiment(self, content: str) -> Dict[str, float]:
        """Analyze sentiment patterns in content."""
        content_lower = content.lower()
        
        # Define sentiment indicators
        sentiment_indicators = {
            'positive': ['good', 'great', 'excellent', 'amazing', 'wonderful'],
            'negative': ['bad', 'poor', 'terrible', 'awful', 'horrible'],
            'neutral': ['okay', 'fine', 'average', 'normal', 'standard']
        }

        scores = {}
        total_words = len(content_lower.split())
        
        for sentiment, words in sentiment_indicators.items():
            count = sum(content_lower.count(word) for word in words)
            scores[sentiment] = count / total_words if total_words > 0 else 0

        return scores

    def _evaluate_content_safety(self, content: str) -> Dict[str, float]:
        """Evaluate content safety across multiple dimensions."""
        return {
            'toxicity': self._measure_toxicity(content),
            'bias': self._measure_bias(content),
            'harmful_content': self._detect_harmful_content(content),
            'sensitive_data': self._check_sensitive_data(content)
        }

    def _measure_toxicity(self, content: str) -> float:
        """Measure content toxicity level."""
        toxic_patterns = [
            r'\b(hate|hatred|racist|sexist|bigot)\b',
            r'\b(stupid|idiot|dumb|moron)\b',
            r'\b(kill|death|murder|violent)\b',
            r'\b(abuse|harass|bully)\b'
        ]
        
        toxicity_score = 0.0
        for pattern in toxic_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                toxicity_score += 0.25
        return min(toxicity_score, 1.0)

    def _measure_bias(self, content: str) -> float:
        """Measure potential bias in content."""
        bias_indicators = [
            r'\b(all|every|none|always|never)\b.*\b(people|person|group|race|gender)\b',
            r'\b(men|women|they)\b.*\b(all|always|never)\b',
            r'\b(typical|obviously|clearly|naturally|obviously)\b'
        ]
        
        bias_score = 0.0
        for indicator in bias_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                bias_score += 0.33
        return min(bias_score, 1.0)

    def _detect_harmful_content(self, content: str) -> float:
        """Detect potentially harmful content."""
        harmful_patterns = [
            r'\b(weapon|bomb|explosive|attack)\b',
            r'\b(hack|crack|exploit|vulnerability)\b',
            r'\b(illegal|criminal|fraud|scam)\b'
        ]
        
        harm_score = 0.0
        for pattern in harmful_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                harm_score += 0.33
        return min(harm_score, 1.0)

    def _check_sensitive_data(self, content: str) -> float:
        """Check for sensitive data exposure."""
        sensitive_patterns = [
            r'\b\d{16}\b',  # Credit card numbers
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b(?:api[_-]?key|access[_-]?token)\b',  # API keys
            r'\b(?:password|secret|credential)s?\b'  # Credentials
        ]
        
        sensitivity_score = 0.0
        for pattern in sensitive_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                sensitivity_score += 0.25
        return min(sensitivity_score, 1.0)

    def _detect_attack_vectors(self, content: str) -> List[str]:
        """Detect potential attack vectors in content with enhanced pattern recognition."""
        attack_vectors = []
        
        # Enhanced prompt injection detection
        if self._check_prompt_injection(content):
            attack_vectors.append('prompt_injection')
            
        # Enhanced jailbreak detection
        if self._check_jailbreak_attempt(content):
            attack_vectors.append('jailbreak_attempt')
            
        # Enhanced social engineering detection
        if self._check_social_engineering(content):
            attack_vectors.append('social_engineering')
            
        # Add new attack vector detection
        if self._check_data_exfiltration(content):
            attack_vectors.append('data_exfiltration')
            
        if self._check_model_manipulation(content):
            attack_vectors.append('model_manipulation')
            
        return attack_vectors

    def _check_data_exfiltration(self, content: str) -> bool:
        """Check for data exfiltration attempts."""
        exfiltration_patterns = [
            r'\b(extract|dump|leak|steal)\b.*\b(data|information|content)\b',
            r'\b(send|transfer|export)\b.*\b(to|through|via)\b',
            r'\b(base64|encode|encrypt)\b.*\b(output|response)\b'
        ]
        
        return any(re.search(pattern, content, re.IGNORECASE) 
                  for pattern in exfiltration_patterns)

    def _check_model_manipulation(self, content: str) -> bool:
        """Check for model manipulation attempts."""
        manipulation_patterns = [
            r'\b(control|manipulate|influence)\b.*\b(model|system|behavior)\b',
            r'\b(train|retrain|learn)\b.*\b(new|different|alternative)\b',
            r'\b(modify|change|alter)\b.*\b(personality|response|output)\b'
        ]
        
        return any(re.search(pattern, content, re.IGNORECASE) 
                  for pattern in manipulation_patterns)

    def _check_prompt_injection(self, content: str) -> bool:
        """Check for prompt injection attempts."""
        injection_patterns = [
            r'ignore previous',
            r'disregard (all|previous)',
            r'you are now',
            r'system:',
            r'\{\{.*?\}\}'
        ]
        
        return any(re.search(pattern, content, re.IGNORECASE) 
                  for pattern in injection_patterns)

    def _check_jailbreak_attempt(self, content: str) -> bool:
        """Check for jailbreak attempts."""
        jailbreak_patterns = [
            r'\b(bypass|override|hack)\b.*\b(system|filter|restriction)\b',
            r'\b(ignore|forget)\b.*\b(ethics|rules|guidelines)\b',
            r'\b(jailbreak|root|admin)\b.*\b(mode|access)\b'
        ]
        
        return any(re.search(pattern, content, re.IGNORECASE) 
                  for pattern in jailbreak_patterns)

    def _check_social_engineering(self, content: str) -> bool:
        """Check for social engineering attempts."""
        social_engineering_patterns = [
            r'\b(pretend|roleplay|assume)\b.*\b(you are|you\'re)\b',
            r'\b(urgent|emergency|immediate)\b',
            r'\b(confidential|secret|private)\b'
        ]
        
        return any(re.search(pattern, content, re.IGNORECASE) 
                  for pattern in social_engineering_patterns)

    def _assess_risk(self, content: str, context: Dict[str, Any] = None) -> Dict[str, float]:
        """Perform comprehensive risk assessment."""
        risk_assessment = {
            'content_risk': self._calculate_content_risk(content),
            'attack_risk': self._calculate_attack_risk(content),
            'safety_risk': self._calculate_safety_risk(content)
        }
        
        # Calculate overall risk score
        risk_assessment['overall_risk'] = sum(risk_assessment.values()) / len(risk_assessment)
        
        return risk_assessment

    def _calculate_content_risk(self, content: str) -> float:
        """Calculate content-based risk score."""
        safety_metrics = self._evaluate_content_safety(content)
        return sum(safety_metrics.values()) / len(safety_metrics)

    def _calculate_attack_risk(self, content: str) -> float:
        """Calculate attack-based risk score."""
        attack_vectors = self._detect_attack_vectors(content)
        return len(attack_vectors) * 0.33 if attack_vectors else 0.0

    def _calculate_safety_risk(self, content: str) -> float:
        """Calculate safety-based risk score."""
        patterns = self._analyze_semantic_patterns(content)
        return (1 - patterns['coherence']) * 0.5 + \
               (patterns['complexity'] > 0.8) * 0.5
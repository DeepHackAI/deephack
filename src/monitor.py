from typing import Dict, List, Any
from datetime import datetime
import json
import logging

class SecurityMonitor:
    """Monitor system for tracking security events and model behaviors.

    This class provides comprehensive monitoring capabilities for tracking
    security-related events, model behaviors, and system performance metrics.
    """

    def __init__(self, log_file: str = "security_events.log"):
        """Initialize the security monitor.

        Args:
            log_file: Path to the log file for security events
        """
        self.events: List[Dict[str, Any]] = []
        self.setup_logging(log_file)

    def setup_logging(self, log_file: str) -> None:
        """Set up logging configuration.

        Args:
            log_file: Path to the log file
        """
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def log_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """Log a security event.

        Args:
            event_type: Type of security event
            details: Additional event details
        """
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'details': details
        }
        self.events.append(event)
        logging.info(f"Security event: {json.dumps(event)}")

    def log_model_behavior(self, model_name: str, prompt: str, 
                          response: str, evaluation: Dict[str, Any]) -> None:
        """Log model behavior and response.

        Args:
            model_name: Name of the AI model
            prompt: Input prompt
            response: Model response
            evaluation: Security evaluation results
        """
        self.log_event('model_behavior', {
            'model_name': model_name,
            'prompt': prompt,
            'response': response,
            'evaluation': evaluation
        })

    def log_security_violation(self, violation_type: str, severity: str, 
                             details: Dict[str, Any]) -> None:
        """Log a security violation.

        Args:
            violation_type: Type of security violation
            severity: Severity level (low, medium, high, critical)
            details: Additional violation details
        """
        self.log_event('security_violation', {
            'violation_type': violation_type,
            'severity': severity,
            'details': details
        })

    def get_events(self, event_type: str = None, 
                   start_time: str = None, end_time: str = None) -> List[Dict[str, Any]]:
        """Get filtered security events.

        Args:
            event_type: Optional filter by event type
            start_time: Optional filter by start time (ISO format)
            end_time: Optional filter by end time (ISO format)

        Returns:
            List of filtered security events
        """
        filtered_events = self.events

        if event_type:
            filtered_events = [e for e in filtered_events if e['type'] == event_type]

        if start_time:
            filtered_events = [e for e in filtered_events 
                             if e['timestamp'] >= start_time]

        if end_time:
            filtered_events = [e for e in filtered_events 
                             if e['timestamp'] <= end_time]

        return filtered_events

    def get_security_metrics(self) -> Dict[str, Any]:
        """Get security monitoring metrics.

        Returns:
            Dictionary containing security metrics and statistics
        """
        total_events = len(self.events)
        event_types = {}
        violations_by_severity = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}

        for event in self.events:
            event_type = event['type']
            event_types[event_type] = event_types.get(event_type, 0) + 1

            if event_type == 'security_violation':
                severity = event['details']['severity']
                violations_by_severity[severity] += 1

        return {
            'total_events': total_events,
            'event_types': event_types,
            'violations_by_severity': violations_by_severity
        }

    def analyze_behavior_pattern(self, model_name: str, timeframe: str = '1h') -> Dict[str, Any]:
        """Analyze model behavior patterns over a specified timeframe.

        Args:
            model_name: Name of the AI model
            timeframe: Time period for analysis (e.g., '1h', '24h', '7d')

        Returns:
            Dictionary containing behavior analysis results
        """
        relevant_events = [e for e in self.events 
                         if e['type'] == 'model_behavior' 
                         and e['details']['model_name'] == model_name]
        
        # Analyze response patterns
        response_patterns = {
            'potentially_harmful': 0,
            'safety_violations': 0,
            'ethical_concerns': 0,
            'instruction_adherence': 0
        }
        
        for event in relevant_events:
            eval_results = event['details']['evaluation']
            if not eval_results.get('is_aligned', True):
                if 'value_issues' in eval_results.get('issues', {}):
                    response_patterns['potentially_harmful'] += 1
                if 'safety_issues' in eval_results.get('issues', {}):
                    response_patterns['safety_violations'] += 1
                if 'ethical_issues' in eval_results.get('issues', {}):
                    response_patterns['ethical_concerns'] += 1
                if 'instruction_issues' in eval_results.get('issues', {}):
                    response_patterns['instruction_adherence'] += 1
        
        return {
            'model_name': model_name,
            'timeframe': timeframe,
            'total_interactions': len(relevant_events),
            'response_patterns': response_patterns,
            'risk_level': self._calculate_risk_level(response_patterns)
        }
    
    def _calculate_risk_level(self, patterns: Dict[str, int]) -> str:
        """Calculate overall risk level based on behavior patterns.

        Args:
            patterns: Dictionary of behavior pattern counts

        Returns:
            Risk level assessment (low, medium, high, critical)
        """
        total_issues = sum(patterns.values())
        if total_issues == 0:
            return 'low'
        elif total_issues < 5:
            return 'medium'
        elif total_issues < 10:
            return 'high'
        return 'critical'

    def get_threat_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive threat summary.

        Returns:
            Dictionary containing threat analysis summary
        """
        violations = [e for e in self.events if e['type'] == 'security_violation']
        threat_levels = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
        
        for violation in violations:
            severity = violation['details']['severity']
            threat_levels[severity] = threat_levels.get(severity, 0) + 1
        
        return {
            'total_violations': len(violations),
            'threat_levels': threat_levels,
            'recent_critical_events': [
                v for v in violations 
                if v['details']['severity'] == 'critical'
            ][-5:]
        }
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
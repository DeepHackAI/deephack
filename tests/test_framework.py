import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from src.framework import DeepHackFramework

class TestDeepHackFramework(unittest.TestCase):
    def setUp(self):
        self.framework = DeepHackFramework()

    def test_validate_prompt(self):
        """Test prompt validation functionality"""
        # Test valid prompt
        self.assertTrue(self.framework.validate_prompt("Valid prompt"))
        
        # Test invalid prompts
        self.assertFalse(self.framework.validate_prompt(""))
        self.assertFalse(self.framework.validate_prompt(None))
        self.assertFalse(self.framework.validate_prompt("   "))

    @patch('src.framework.openai')
    def test_test_prompt(self, mock_openai):
        """Test the main prompt testing functionality"""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test response"))]
        mock_openai.chat.completions.create.return_value = mock_response

        # Test with valid prompt
        result = self.framework.test_prompt("Test prompt")
        self.assertIn("response", result)
        self.assertIn("evaluation", result)

        # Test with invalid prompt
        result = self.framework.test_prompt("")
        self.assertIn("error", result)
        self.assertFalse(result["is_safe"])

    def test_batch_test(self):
        """Test batch testing functionality"""
        prompts = ["Test 1", "Test 2", ""]
        results = self.framework.batch_test(prompts)
        self.assertEqual(len(results), len(prompts))

    def test_conversation_history(self):
        """Test conversation history management"""
        self.framework.test_prompt("Test prompt")
        history = self.framework.get_history()
        self.assertTrue(len(history) > 0)

        self.framework.clear_history()
        self.assertEqual(len(self.framework.get_history()), 0)

    def test_security_stats(self):
        """Test security statistics tracking"""
        stats = self.framework.get_security_stats()
        self.assertIn("total_requests", stats)
        self.assertIn("last_request_time", stats)
        self.assertIn("conversation_length", stats)

if __name__ == '__main__':
    unittest.main()
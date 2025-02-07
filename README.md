# DeepHackAI

## Mission
DeepHack is a framework for Adversarial Hacking by crowdsourcing AI Hacks through collaborative hacking techniques. It aims to build a decentralized network to safeguard AI by enabling a community of AI Hackers to protect humanity.

## Overview
DeepHack provides a comprehensive suite of tools and methodologies for testing, evaluating, and securing AI systems, particularly Large Language Models (LLMs). The framework supports both offensive (Red Team) and defensive (Blue Team) security measures.

## Key Components

### Red Team Testing
- **Prompt Injection Testing**: Tools for testing LLM vulnerabilities through various prompt injection techniques
- **Jailbreak Detection**: Mechanisms to identify and test jailbreak attempts
- **Bias and Toxicity Analysis**: Tools to evaluate model responses for bias and inappropriate content

### Defensive Measures
- **Input Filtering**: Implementation of word exclusion lists and content filtering
- **Instruction Defense**: Multiple defensive techniques against prompt manipulation
- **Separate LLM Evaluation**: Secondary AI system for evaluating input safety

### Evaluation Tools
- ChatGLM Evaluation
- Garak Evaluator
- MindGuard Integration
- Inspect Evaluator
- Deepseek Evaluator: Specialized security metrics and vulnerability detection for Deepseek models

### Security Components
- AI Firewall
- LLamaGuard Integration
- Agent Smith Defense System
- Semantic Analysis System

### Deepseek-Specific Features
- **Advanced Pattern Detection**: Sophisticated detection of vulnerability patterns specific to Deepseek models
- **Behavioral Analysis**: Real-time monitoring of model behavior and response patterns
- **Security Metrics**: Specialized metrics for evaluating Deepseek model outputs
  - Vulnerability pattern detection
  - Injection attempt identification
  - Semantic attack analysis
  - Risk scoring and assessment
- **Safety Verification**: Comprehensive content safety evaluation system

## Project Structure
```
├── src/
│   ├── agent/         # Agent-based defense systems
│   ├── attack/        # Attack vectors and testing
│   ├── dataset/       # Test datasets and injection prompts
│   ├── evaluator/     # Evaluation tools
│   ├── prompt/        # Prompt templates and testing
│   └── framework.py   # Core framework implementation
└── docs/
    ├── attack.md      # Attack documentation
    ├── basic.md       # Basic concepts
    ├── blueteam.md    # Defense strategies
    └── redteam.md     # Red team testing guide
```

## Features
- Scalable red team testing framework
- Comprehensive prompt injection testing
- Multiple defensive measure implementations
- Automated evaluation systems
- Extensive documentation and testing datasets
- Deepseek model security analysis and protection

## Getting Started

### Prerequisites
- Python 3.x
- OpenAI API key
- Required Python packages (see requirements.txt)

### Installation
1. Clone the repository
```bash
git clone https://github.com/deephackai/deephack.git
cd deephack
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key
```python
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

### Red Team Testing
```python
from src.readteam import ChatBot

# Initialize chatbot for testing
chatbot = ChatBot()

# Run red team evaluation
chatbot.new_message(your_test_prompt)
```

### Defensive Measures
```python
from src.defensive_measure import ChatBot

# Initialize protected chatbot
chatbot = ChatBot()

# Test with defensive measures
chatbot.new_message(user_input)
```

### Deepseek Model Evaluation
```python
from src.evaluator.evaluator_deepseek import DeepseekEvaluator

# Initialize Deepseek evaluator
evaluator = DeepseekEvaluator()

# Evaluate prompt safety
result = evaluator.evaluate_prompt("Your prompt here")

# Analyze response
safety_analysis = evaluator.evaluate_response("Model response here")
```
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- OpenAI for API access
- Contributors to the various evaluation tools
- AI security research community

## Disclaimer
This tool is for research and defensive purposes only. Users are responsible for complying with applicable laws and terms of service.



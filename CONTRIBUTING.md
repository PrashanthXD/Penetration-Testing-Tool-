# Contributing to Penetration Testing Tool

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We expect all contributors to:
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Your environment details (Python version, OS, etc.)

### Suggesting Features

For feature requests, please include:
- A clear description of the feature
- Use cases and benefits
- Any implementation suggestions

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Write or update tests for your changes
5. Ensure all tests pass (`python -m unittest discover -s tests -v`)
6. Commit your changes with a clear message
7. Push to your fork and submit a pull request

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Penetration-Testing-Tool-.git
cd Penetration-Testing-Tool-
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install python-nmap  # For Nmap scanner
```

## Writing Tests

### Test Requirements

- All new code must have corresponding unit tests
- Tests should cover edge cases and error handling
- Use Python's `unittest` framework (already used in the project)
- Mock external dependencies (network calls, file I/O) to ensure tests are reliable

### Test Structure

Tests are located in the `tests/` directory. Each module has its own test file:

```
tests/
├── __init__.py
├── test_tcpserver.py
├── test_tcpclient.py
├── test_portscanner.py
├── test_bannergrabber.py
└── test_scanner.py
```

### Writing a New Test

Example of a well-structured test:

```python
#!/usr/bin/env python3
"""Unit tests for YourModule."""

import unittest
from unittest.mock import Mock, patch

from PenetrationTesting.YourModule.yourmodule import your_function


class TestYourFunction(unittest.TestCase):
    """Tests for the your_function function."""
    
    def test_your_function_normal_case(self):
        """Test your_function with normal input."""
        result = your_function('normal_input')
        self.assertEqual(result, 'expected_output')
    
    def test_your_function_edge_case(self):
        """Test your_function with edge case input."""
        result = your_function('')
        self.assertIsNone(result)
    
    @patch('PenetrationTesting.YourModule.yourmodule.external_call')
    def test_your_function_with_mock(self, mock_external):
        """Test your_function with mocked external dependency."""
        mock_external.return_value = 'mocked_value'
        result = your_function('input')
        mock_external.assert_called_once_with('input')


if __name__ == '__main__':
    unittest.main()
```

### Running Tests

```bash
# Run all tests
python -m unittest discover -s tests -v

# Run a specific test file
python -m unittest tests.test_tcpserver -v

# Run a specific test class
python -m unittest tests.test_tcpserver.TestTranslateCommand -v

# Run a specific test method
python -m unittest tests.test_tcpserver.TestTranslateCommand.test_translate_ls_on_windows -v
```

## Code Style Guidelines

- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Docstring Format

```python
def function_name(param1, param2):
    """Brief description of the function.
    
    More detailed description if needed.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
        
    Returns:
        Description of the return value.
        
    Raises:
        ExceptionType: When this exception is raised.
    """
    pass
```

## Module Structure

When adding new modules, follow this structure:

```
PenetrationTesting/
└── NewModule/
    ├── __init__.py
    └── newmodule.py
```

And add corresponding tests:

```
tests/
└── test_newmodule.py
```

## Security Considerations

Since this is a security tool:
- Never commit actual credentials or sensitive data
- Be mindful of the implications of security testing tools
- Document any security-related functionality clearly
- Consider the potential for misuse when implementing features

## Questions?

If you have questions about contributing, feel free to open an issue for discussion.

Thank you for contributing to making this project better!

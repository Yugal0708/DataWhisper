# Contributing to DataWhisper

Thank you for your interest in contributing to DataWhisper! We welcome contributions from the community. This guide will help you understand our development workflow, coding standards, and submission process.

## Table of Contents

- [Project Setup Instructions](#project-setup-instructions)
- [Branch Naming Rules](#branch-naming-rules)
- [PR Submission Workflow](#pr-submission-workflow)
- [Code Formatting & Style Expectations](#code-formatting--style-expectations)
- [Testing and Validation Steps](#testing-and-validation-steps)
- [Contribution Best Practices](#contribution-best-practices)

---

## Project Setup Instructions

### Prerequisites

- **Python 3.8+** installed on your system
- **Git** for version control
- A **Groq API key** (required for LLM features)

### Local Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/DataWhisper.git
   cd DataWhisper
   ```

2. **Create a Virtual Environment**
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Or using conda
   conda create -n datawhisper python=3.10
   conda activate datawhisper
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your credentials
   # Required variables:
   # - GROQ_API_KEY: Your Groq API key
   # - STREAMLIT_AUTH_PASSWORD: Password for Streamlit authentication
   ```

5. **Verify Installation**
   ```bash
   # Run the application in test mode
   streamlit run app.py
   
   # Visit http://localhost:8501 in your browser
   ```

---

## Branch Naming Rules

Follow these naming conventions for branches to maintain clarity and organization:

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<feature-name>` | `feature/add-export-pdf` |
| Bug Fix | `bugfix/<issue-name>` | `bugfix/fix-missing-values-display` |
| Refactor | `refactor/<component>` | `refactor/streamline-eda-module` |
| Documentation | `docs/<section>` | `docs/update-contributing-guide` |
| Testing | `test/<feature>` | `test/add-csv-parser-tests` |
| Hotfix | `hotfix/<critical-issue>` | `hotfix/auth-token-expiry` |

### Best Practices

- Use lowercase letters and hyphens (no underscores or spaces)
- Be descriptive but concise (keep under 50 characters after the prefix)
- Reference issue numbers when applicable: `feature/add-export-pdf-#42`

---

## PR Submission Workflow

### 1. Create Your Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Keep commits atomic and focused on a single change
- Write clear, descriptive commit messages
- Reference related issues: `Fixes #123` or `Related to #456`

### 3. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 4. Create a Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your branch as the source
4. Fill in the PR title and description using this template:

```markdown
## Description
Brief description of your changes and why they're needed.

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Performance improvement
- [ ] Documentation update
- [ ] Refactoring

## Related Issues
Fixes #123

## Testing Performed
Describe the testing you've done.

## Screenshots (if applicable)
Add any relevant screenshots or GIFs.

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No breaking changes (or documented if necessary)
- [ ] Tests added/updated
- [ ] All tests pass locally
```

### 5. Code Review Process

- Maintainers will review your PR within 2-3 business days
- Address requested changes promptly
- Push additional commits to the same branch (don't force push after review starts)
- Once approved, maintainers will merge your PR

---

## Code Formatting & Style Expectations

### Python Style Guide

We follow **PEP 8** conventions with the following specifics:

#### Naming Conventions

```python
# ✅ Good
def load_csv_data(file_path):
    """Load data from CSV file."""
    pass

class DataProcessor:
    """Process and transform data."""
    pass

MAXIMUM_ROWS = 1000000
config_value = "example"

# ❌ Avoid
def loadCSVData(file_path):
    pass

class data_processor:
    pass

max_Rows = 1000000
```

#### Line Length & Formatting

- Maximum line length: **100 characters**
- Use 4 spaces for indentation (no tabs)
- Use consistent quotes (prefer double quotes for strings)

#### Documentation & Comments

```python
def generate_eda_report(data, output_format="html"):
    """
    Generate an exploratory data analysis report.
    
    Args:
        data (pd.DataFrame): The input dataset.
        output_format (str): Format of the report ('html' or 'pdf'). Defaults to 'html'.
    
    Returns:
        str: Path to the generated report file.
    
    Raises:
        ValueError: If data is empty or output_format is invalid.
    """
    if data.empty:
        raise ValueError("Input data cannot be empty")
    
    # Generate visualizations
    visualizations = create_visualizations(data)
    
    return save_report(visualizations, output_format)
```

#### Imports

- Organize imports into three groups (stdlib, third-party, local) separated by blank lines
- One import per line (except for `from X import a, b, c`)

```python
import os
import sys
from pathlib import Path

import pandas as pd
import numpy as np
import streamlit as st

from src.eda import generate_plots
from src.llm_insights import get_insights
```

### File Organization

- Keep modules focused on a single responsibility
- Maximum file size: ~500 lines of code (consider splitting larger files)
- Use type hints where possible

```python
from typing import Optional, Dict, List
import pandas as pd

def process_missing_values(
    data: pd.DataFrame,
    strategy: str = "mean"
) -> pd.DataFrame:
    """Process missing values in the dataset."""
    pass
```

### Git Commit Messages

- Use imperative mood: "Add feature" not "Added feature"
- First line ≤ 50 characters
- Blank line between subject and body
- Wrap body at 72 characters

```
Add CSV import with validation

- Support for multiple encoding formats
- Automatic type inference
- Comprehensive error messages

Fixes #42
```

---

## Testing and Validation Steps

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_data_loader.py

# Run tests matching a pattern
pytest -k "test_csv"
```

### Manual Testing

1. **Data Loading**
   - Upload various CSV formats (different encodings, delimiters)
   - Test with sample_data/titanic.csv
   - Verify error handling for corrupted files

2. **EDA Functionality**
   - Check all visualizations render correctly
   - Verify statistics calculations
   - Test with datasets of varying sizes

3. **LLM Integration**
   - Verify Groq API connectivity
   - Test insight generation
   - Check error handling for API failures

4. **Chat Interface**
   - Test various natural language queries
   - Verify conversation context is maintained
   - Check response accuracy

5. **Report Generation**
   - Generate and export reports
   - Verify HTML formatting
   - Check all visualizations are included

### Validation Checklist

Before submitting a PR, ensure:

- [ ] Code runs without errors
- [ ] No debug prints or console logs left in code
- [ ] All new features have corresponding documentation
- [ ] Error handling is implemented for edge cases
- [ ] Performance is acceptable for typical datasets
- [ ] No hardcoded credentials or sensitive data
- [ ] Environment variables are properly documented

### Testing Best Practices

```python
# tests/test_eda.py
import pytest
import pandas as pd
from src.eda import generate_summary_stats

class TestEDA:
    """Test suite for EDA module."""
    
    @pytest.fixture
    def sample_data(self):
        """Fixture providing sample data for tests."""
        return pd.DataFrame({
            'age': [25, 30, 35, None],
            'salary': [50000, 60000, 75000, 80000]
        })
    
    def test_summary_stats_calculation(self, sample_data):
        """Test that summary stats are calculated correctly."""
        stats = generate_summary_stats(sample_data)
        assert stats['age']['mean'] == 30.0
        assert stats['age']['missing'] == 1
    
    def test_summary_stats_with_empty_dataframe(self):
        """Test error handling for empty dataframe."""
        with pytest.raises(ValueError):
            generate_summary_stats(pd.DataFrame())
```

---

## Contribution Best Practices

### 1. Start Small

- Begin with small, focused contributions
- This helps you understand the workflow and get familiar with the codebase
- Good starting points: documentation fixes, bug reports with proposed solutions

### 2. Communicate Before Major Changes

- Open an issue to discuss significant features or refactoring
- Get feedback early to avoid wasted effort
- Coordinate with maintainers on complex architectural decisions

### 3. Code Review Tips

- Be open to feedback—code review improves code quality for everyone
- Explain your reasoning in comments for non-obvious code
- Ask questions if you don't understand review comments

### 4. Documentation Matters

- Update README.md if you add new features
- Add docstrings to all functions and classes
- Update this CONTRIBUTING.md if you change workflows

### 5. Keep Commits Clean

```bash
# Before pushing, check your commits
git log --oneline -5

# If needed, squash or rebase commits
git rebase -i HEAD~3

# Force push only if absolutely necessary and with caution
git push --force-with-lease origin feature/your-feature
```

### 6. Handle Dependencies Carefully

- Update requirements.txt with exact version pins
- Document any new library additions in the PR description
- Consider compatibility with Python 3.8+
- Test with different versions of key dependencies (pandas, streamlit)

### 7. Performance Considerations

- Test with larger datasets (100k+ rows)
- Profile code for bottlenecks
- Document any known performance limitations

### 8. Security Best Practices

- Never commit API keys, passwords, or tokens
- Use environment variables for sensitive data
- Validate and sanitize user inputs
- Be cautious with file operations (path traversal attacks)

---

## Reporting Bugs and Requesting Features

### Bug Reports

Include the following information:

- Clear title describing the bug
- Detailed steps to reproduce
- Expected vs actual behavior
- Environment (Python version, OS, browser)
- Screenshots/error logs if applicable
- Sample data that reproduces the issue (if possible)

### Feature Requests

Include:

- Clear description of the desired feature
- Use case and why it's needed
- Proposed implementation approach (optional)
- Mockups or examples (if applicable)

---

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and professional in all interactions
- Welcome diverse perspectives and experiences
- Provide constructive feedback
- Report any harassment or inappropriate behavior

---

## Questions?

- 📧 Open an issue for discussions
- 💬 Check existing issues before opening a new one
- 📖 Review the README.md for general project information

Thank you for contributing to DataWhisper! 🎉

---

**Last Updated:** May 2026

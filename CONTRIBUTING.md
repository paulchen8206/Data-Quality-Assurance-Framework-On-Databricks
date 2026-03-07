# Contributing to QA Framework

Thank you for your interest in contributing to the QA Framework! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Qa-Framework-On-Databricks.git
   cd Qa-Framework-On-Databricks
   ```
3. **Set up the development environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   pip install -e ".[dev]"
   ```
4. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/paulchen8206/Qa-Framework-On-Databricks.git
   ```

## How to Contribute

### Reporting Bugs

- Check if the issue already exists in [GitHub Issues](https://github.com/paulchen8206/Qa-Framework-On-Databricks/issues)
- Use the bug report template
- Include:
  - Clear description of the problem
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment details (Python version, OS, etc.)

### Suggesting Enhancements

- Open an issue with the enhancement label
- Describe the feature and its benefits
- Provide examples of how it would be used

### Documentation Improvements

- Fix typos, clarify instructions
- Add examples and use cases
- Improve API documentation

## Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests locally**:
   ```bash
   pytest tests/test_utils.py -v
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: Add new validation method"
   ```
   
   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `test:` Test changes
   - `refactor:` Code refactoring
   - `chore:` Maintenance tasks

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

## Coding Standards

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use type hints where appropriate
- Write docstrings for all public functions/classes
- Keep functions focused and modular

### Code Examples

```python
def check_validation(self, column: str, threshold: float = 0.95) -> bool:
    """
    Check if validation passes for a column.
    
    Args:
        column: Name of the column to validate
        threshold: Minimum acceptable pass rate (default: 0.95)
        
    Returns:
        True if validation passes, False otherwise
        
    Raises:
        ValueError: If column doesn't exist in DataFrame
    """
    # Implementation here
    pass
```

### Documentation

- Use clear, concise language
- Include code examples
- Update README.md for major changes
- Add docstrings with proper formatting

## Testing Guidelines

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test names: `test_check_null_values_with_nulls_present()`
- Include both positive and negative test cases

### Test Structure

```python
def test_feature_name():
    # Arrange - Set up test data
    df = create_test_dataframe()
    validator = DataValidator(df)
    
    # Act - Execute the test
    result = validator.check_null_values()
    
    # Assert - Verify the result
    assert result['column1'] == 0
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_validators.py -v

# Run with coverage
pytest --cov=qa_framework --cov-report=html
```

## Submitting Changes

### Pull Request Process

1. **Update documentation** for any changed functionality
2. **Add tests** for new features
3. **Ensure all tests pass** locally
4. **Update CHANGELOG** (if applicable)
5. **Create Pull Request** with:
   - Clear title describing the change
   - Detailed description of what and why
   - Reference any related issues
   - Screenshots (if UI changes)

### PR Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged

### After Your PR is Merged

- Delete your feature branch
- Update your local repository:
  ```bash
  git checkout main
  git pull upstream main
  ```

## Development Tips

### Virtual Environment

Always activate the virtual environment before working:
```bash
source .venv/bin/activate
```

### Keeping Your Fork Updated

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### Code Quality Tools

Consider using:
- **black** for code formatting
- **flake8** for linting
- **mypy** for type checking
- **pytest-cov** for test coverage

## Questions?

- Open an issue with the "question" label
- Check existing documentation
- Review closed issues and PRs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to QA Framework! 🎉

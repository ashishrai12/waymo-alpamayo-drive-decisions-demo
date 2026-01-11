# Contributing to Alpamayo R1 Demo

Thank you for your interest in contributing! We follow standard professional engineering practices.

## Development Workflow

1. **Fork and Clone**: Create your own fork and clone it locally.
2. **Environment**: Use a virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Branching**: Create a feature branch (`git checkout -b feature/your-feature`).
4. **Code Quality**:
   - Run tests: `pytest tests/`
   - Run linting: `flake8 src/ tests/`
   - Use `black` and `isort` for formatting.
5. **Commit**: Write descriptive commit messages.

## Testing

All new features should include unit tests in the `tests/` directory. We aim for high coverage of the decision-making logic.

## Code Style

- Follow PEP 8.
- Use type hints wherever possible.
- Document classes and functions using NumPy or Google style docstrings.

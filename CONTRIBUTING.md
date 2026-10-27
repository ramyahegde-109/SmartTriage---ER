# Contributing to Smart ER Triage & Risk Management System

Thank you for your interest in contributing to this project!
Contributions that improve reliability, usability, documentation,
testing, and scheduling correctness are welcome.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-FORK.git
   cd YOUR-FORK
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
4. Activate it.

   Windows (Git Bash):
   ```bash
   source .venv/Scripts/activate
   ```

   Linux or macOS:
   ```bash
   source .venv/bin/activate
   ```
5. Install the project's dependencies using its existing
   requirements file or setup instructions.

## Good First Contributions

You can contribute by:

- Adding tests for the scheduling algorithm.
- Improving CSV input validation and error messages.
- Testing duplicate or malformed patient records.
- Improving Streamlit dashboard usability.
- Handling JSON export errors safely.
- Improving documentation and setup instructions.
- Fixing bugs while preserving existing behavior.

Before starting a large change, check existing issues and
discuss your proposed approach with the maintainers.

## Development Guidelines

- Follow the coding conventions already used in the project.
- Keep changes focused and easy to review.
- Use descriptive variable and function names.
- Handle invalid inputs explicitly.
- Avoid introducing unnecessary dependencies.
- Update documentation when behavior or setup instructions change.
- Add regression tests for bug fixes whenever practical.

## Testing

Run the existing tests before and after making changes.

If the project uses pytest, run:

```bash
python -m pytest -q
```

If no tests are present, consider adding tests for the behavior
you change. Do not claim tests pass unless you have run them.

## Scheduling Algorithm

The project uses Smith's Rule (Weighted Shortest Processing Time)
as its scheduling approach.

When changing scheduling logic:

- Verify the existing priority and risk-score definitions.
- Add tests for scheduling order and tie-breaking.
- Check empty queues and invalid treatment durations.
- Preserve the output format required by the project.
- Do not assume algorithmic priority alone represents clinical
  triage guidance.

Changes affecting patient prioritization should be clearly
documented and reviewed carefully.

## CSV and JSON Data

- Preserve the existing CSV column names and expected formats.
- Handle malformed rows with understandable error messages.
- Avoid silently discarding patient records.
- Preserve the expected submission.json schema.
- Do not commit real patient records or confidential information.
- Use synthetic data in tests and examples.

## Pull Request Process

1. Create a feature branch:
   ```bash
   git switch -c type/short-description
   ```
2. Make your changes.
3. Run relevant tests and inspect your changes:
   ```bash
   python -m pytest -q
   git diff --check
   git status
   ```
4. Commit with a descriptive message:
   ```bash
   git add <changed-files>
   git commit -m "Describe your changes"
   ```
5. Push your branch:
   ```bash
   git push -u origin type/short-description
   ```
6. Open a pull request against the upstream repository's
   default branch.
7. Explain the problem, summarize the changes, and report the
   tests you ran.

Keep pull requests focused on one improvement and respond
constructively to review feedback.

## Commit Message Examples

- `docs: improve project setup instructions`
- `test: add scheduling algorithm tests`
- `fix: validate patient treatment duration`
- `feat: improve queue visibility`

Use these prefixes as suggestions unless the project defines
a different commit message convention.

## Reporting Bugs

When reporting a bug, include:

- A clear description of the problem.
- Steps to reproduce it.
- Expected and actual behavior.
- Relevant error messages.
- A minimal example using synthetic data.

Never include real patient information, credentials, or secrets.

## Questions and Discussions

Check the repository's README, existing issues, and contribution
guidelines before opening a new issue. Follow the maintainers'
instructions and code of conduct, if one is provided.

Thank you for helping improve this project!

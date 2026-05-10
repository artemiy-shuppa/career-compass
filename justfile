default:
  @just --list

# First-time setup: venv, deps, pre-commit hooks and their environments.
onboard:
  @echo "Host tools:"
  @printf "  python:     "; python --version
  @printf "  pre-commit: "; pre-commit --version
  @printf "  direnv:     "; direnv --version
  test -d .venv || python -m venv .venv
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install -r requirements-dev.txt
  pre-commit install-hooks
  @echo "✓ Project initialized: host tools and .venv are ready."

# Compile requirements*.txt from requirements*.in files via pip-tools.
sync:
  .venv/bin/pip-compile --strip-extras requirements.in
  .venv/bin/pip-compile --strip-extras requirements-dev.in

# Bump locked deps to latest versions compatible with requirements*.in.
upgrade:
  .venv/bin/pip-compile --strip-extras --upgrade requirements.in
  .venv/bin/pip-compile --strip-extras --upgrade requirements-dev.in

# Bump pre-commit hook revisions in .pre-commit-config.yaml to latest.
upgrade-hooks:
  pre-commit autoupdate

# Run linters and formatters via pre-commit on all files.
lint:
  pre-commit run --all-files

# Run the pipeline.
run:
  .venv/bin/python main.py

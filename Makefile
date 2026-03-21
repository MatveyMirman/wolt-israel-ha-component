.PHONY: ha-start ha-restart ha-logs ha-logs-follow ha-test ha-lint

ha-start:
	cd .devcontainer && docker compose up -d homeassistant

ha-restart:
	cd .devcontainer && docker compose restart homeassistant

ha-logs:
	cd .devcontainer && docker compose logs --tail=50 homeassistant

ha-logs-follow:
	cd .devcontainer && docker compose logs -f homeassistant

ha-stop:
	cd .devcontainer && docker compose down

ha-test:
	venv/bin/python -m pytest tests/ -v --cov=custom_components.wolt

ha-lint:
	venv/bin/ruff check custom_components/wolt/
	venv/bin/ruff format --check custom_components/wolt/

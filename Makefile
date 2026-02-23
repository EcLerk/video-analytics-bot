.PHONY: load-data

load-data:
	docker compose exec bot python -m scripts.load_data
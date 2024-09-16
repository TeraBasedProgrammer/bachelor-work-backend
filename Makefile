run:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigr:
	python manage.py makemigrations

clean_pycache: ## Removes the __pycaches__
	sudo find . -type f -name "*.pyc" -delete
	sudo find . -type d -name "__pycache__" -exec rm -r {} +

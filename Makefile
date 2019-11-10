runserver:
	FLASK_ENV=development flask run --host 0.0.0.0

install:
	pip install -r requirements.txt

format:
	black .


test:
	rm -f test.db
	pytest -s
	rm test.db

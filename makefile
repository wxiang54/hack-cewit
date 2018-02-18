install:
	pip install -r requirements.txt

setup: install
	python utils/dbUtils.py

run: app.py
	python app.py

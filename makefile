install:
	pip install -r requirements.txt

setup: install
	sudo chgrp www-data ghostwallet/data
	sudo chmod g+w ghostwallet/data	
	sudo python ghostwallet/utils/dbUtils.py
	sudo chgrp www-data ghostwallet/data/db.db
	sudo chmod g+w ghostwallet/data/db.db

run: __init__.py
	python __init__.py

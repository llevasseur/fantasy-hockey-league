setup:
	pip install -r requirements.txt
run:
	python3 src/beta-nhl/fetch-player-data.py
	python3 src/beta-nhl/data-to-md.py
	python3 src/beta-nhl/parse-standings.py
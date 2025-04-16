create-venv:
	python3 -m venv venv
activate-venv:
	source venv/bin/activate
deactivate-venv:
	deactivate
install:
	pip3 install -r requirements.txt
force_install:
	python3 -m pip3 install -r requirements.txt
run:
	python3 -m uvicorn app:app --port 3000 --reload
create-db:
	psql -f ./postgreSQL/shcema.sql -d management_db
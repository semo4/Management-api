run:
	pip3 install -r requirements.txt
	python3 -m uvicorn app:app --port 3000 --reload 
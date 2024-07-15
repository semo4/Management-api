install:
	pip3 install -r requirements.txt
run:
	python3 -m uvicorn app:app --port 3000 --reload 
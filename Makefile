requirements:
	python -m pip install --upgrade pip
	pip install -r ./mockserver/testapp/requirements.txt
runserver:
	python ./mockserver/manage.py runserver 127.0.0.1:8000
actual-client-testing:
	python ./mockserver/check_client.py
run-tests:
	pytest mockserver/testapp/tests.py

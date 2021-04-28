test:
	coverage run -m pytest -s

update-requirements:
	pip freeze > etc/requirements.txt
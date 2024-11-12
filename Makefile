install-packages:
	pip3 install -U -r requirements-dev.txt

venv: venv/touchfile

venv/touchfile: requirements-dev.txt
	test -d venv || python3.12 -m venv venv --prompt="siads699-py312"
	. venv/bin/activate && pip install -Ur requirements-dev.txt
	touch venv/touchfile

test: venv
	. venv/bin/activate; nosetests project/test

clean:
	rm -rf venv
	find -iname "*.pyc" -delete

update-makefile:
	git add Makefile && git commit -m "updated makefile" && git push

update-requirements:
	git add services/web/requirements.txt && git add requirements-dev.txt && git commit -m "updated reqs" && git push


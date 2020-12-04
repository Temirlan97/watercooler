.PHONY: clean
clean:
	rm -rf venv/

.PHONY: blackify
blackify: venv
	venv/bin/black ./ --exclude venv/

venv:
	virtualenv --python python3.7 venv
	. venv/bin/activate; pip install -r requirements-minimal.txt

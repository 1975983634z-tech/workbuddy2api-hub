.PHONY: test check compile docker-build clean

test:
	python3 -m unittest discover -s tests -v

check:
	python3 scripts/check_release.py

compile:
	python3 -m py_compile wb_*.py migrate_usage.py

docker-build:
	docker build -t workbuddy2api-hub:local .

clean:
	rm -rf __pycache__ tests/__pycache__ scripts/__pycache__

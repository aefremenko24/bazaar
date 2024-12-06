.PHONY: setup clean

PIP := pip3.9
REQ_FILE := requirements.txt

setup: $(REQ_FILE)
	@echo "Setting up the Python environment..."
	$(PIP) install -r $(REQ_FILE) --user

	rm -rf __pycache__ *.pyc
clean:
	@echo "Cleaning up...
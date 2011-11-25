PROJECT_NAME=advideo
PROJECT_PACKAGE=advideo
PROJECT_TESTS=tests
PORT=8888
URL=http://localhost:$(PORT)
DATABASE_NAME=videoadx

ifndef LANG_PO
	LANG_PO=pt_BR
endif

# Color strings
NO_COLOR=\x1b[0m
OK_COLOR=\x1b[32;01m
OK_STRING=$(OK_COLOR)[OK]$(NO_COLOR)

clean:
	@echo "Cleaning up build and *.pyc files...\c"
	@find . -name '*.pyc' -exec rm -rf {} \;
	@rm -rf build
	@echo " $(OK_STRING)"

start:
	@echo "Running $(PROJECT_NAME) on $(OK_COLOR)$(URL)$(NO_COLOR)..."
	@cd $(PROJECT_PACKAGE) && python application.py

test: clean
	@echo "Running $(PROJECT_NAME) unit tests..."
	@export PYTHONPATH=$PYTHONPATH:`pwd`/$(PROJECT_PACKAGE) && \
	    nosetests -s --verbose --with-coverage --cover-package=$(PROJECT_PACKAGE) $(PROJECT_TESTS)/* --cover-html --cover-html-dir=build/coverage
	@echo " $(OK_STRING)"

unit: clean
	@echo "Running $(PROJECT_NAME) unit tests..."
	@export PYTHONPATH=$PYTHONPATH:`pwd`/$(PROJECT_PACKAGE) && \
	    nosetests -s --verbose --with-coverage --cover-package=$(PROJECT_PACKAGE) $(PROJECT_TESTS)/unit/*
	@echo " $(OK_STRING)"

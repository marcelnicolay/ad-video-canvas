unit: clean
	@echo "Running $(PROJECT_NAME) unit tests..."
	@export PYTHONPATH=$PYTHONPATH:`pwd`/$(PROJECT_PACKAGE) && \
	    nosetests -s --verbose --with-coverage --cover-package=$(PROJECT_PACKAGE) $(PROJECT_TESTS)/unit/*
	@echo " $(OK_STRING)"

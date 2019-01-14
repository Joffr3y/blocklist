DESTDIR       =
PYTHON        = python3
RECORDTXT     = ./record.txt
RM            = rm -rf

build:
	@$(PYTHON) ./setup.py build

install:
	@echo > $(RECORDTXT)
ifdef DESTDIR
	@$(PYTHON) ./setup.py install \
	    --root=$(DESTDIR) \
	    --record=$(RECORDTXT)
	    --optimize=1
else
	@$(PYTHON) ./setup.py install \
	    --record=$(RECORDTXT) \
	    --optimize=1
endif

pypi:
	$(PYTHON) ./setup.py sdist upload

clean:
	$(RM) ./{build,MANIFEST.in,*.egg-info,dist}
	$(RM) ./blocklist/__pycache__

uninstall: clean
	$(RM) $(shell cat $(RECORDTXT))

.PHONY: build install pypi clean uninstall

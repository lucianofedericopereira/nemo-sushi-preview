PACKAGE  = nemo-sushi-preview
VERSION  = 1.0
ARCH     = all
DEB      = $(PACKAGE)_$(VERSION)_$(ARCH).deb
STAGING  = .build/$(PACKAGE)_$(VERSION)_$(ARCH)

ACTIONS_DST    = $(STAGING)/usr/share/nemo/actions
EXTENSIONS_DST = $(STAGING)/usr/share/nemo-python/extensions

.PHONY: all deb install uninstall clean

all: deb

deb:
	mkdir -p $(ACTIONS_DST) $(EXTENSIONS_DST) $(STAGING)/DEBIAN
	cp debian/control             $(STAGING)/DEBIAN/control
	cp src/actions/*.nemo_action  $(ACTIONS_DST)/
	cp src/extensions/*.py        $(EXTENSIONS_DST)/
	dpkg-deb --root-owner-group --build $(STAGING) $(DEB)
	@echo "Built: $(DEB)"

install:
	sudo dpkg -i $(DEB)

uninstall:
	sudo dpkg -r $(PACKAGE)

clean:
	rm -rf .build $(DEB)

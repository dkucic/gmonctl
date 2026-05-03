build:
	mkdir -p _build
	cp -r gmonctl _build/
	python3 -m zipapp _build \
		-m "gmonctl.cli:main" \
		-p "/usr/bin/env python3" \
		-o gmonctl.pyz
	rm -rf _build
	chmod +x gmonctl.pyz

clean:
	rm -f gmonctl.pyz

.PHONY: build clean

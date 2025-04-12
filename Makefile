
cwd = ${shell pwd}

.PHONY: docs build


build:
	-rm -rf build
	-rm -rf dist
	python3 -m build

test_upload:
	python3 -m twine upload -u __token__ --repository testpypi dist/*

upload:
	python3 -m twine upload -u __token__ --repository pypi dist/*

JEKYLL_VERSION=3.8
SITE=${shell pwd}/docs
jstart:
	docker run --rm --name aicex_docs --volume="${SITE}:/srv/jekyll" -p 3002:4000 -it jekyll/jekyll:${JEKYLL_VERSION} jekyll serve --watch --drafts

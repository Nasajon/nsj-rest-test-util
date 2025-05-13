install_to_pkg:
	pip install build==1.2.2.post1
	pip install twine==4.0.0

build_pkg:
	python3 -m build

upload_pkg:
	python3 -m twine upload --skip-existing dist/*
	
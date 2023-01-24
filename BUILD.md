
pip install build twine

python -m build
twine upload -r testpypi dist/*
twine upload dist/*
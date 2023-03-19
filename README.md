# ShorthandAI Open Source

This repository implements language-specific SDKs for ShorthandAI 


### Testing
```
$ python setup.py sdist bdist_wheel && python -m twine upload --repository testpypi dist/*
$ pip install -i https://test.pypi.org/simple/ shorthandai
```

### Deploy
```
$ python -m twine upload dist/*
```
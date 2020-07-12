# DDD on Python

Trial and error of DDD on Python.

## Domain model 

![model](packages.png)

```
$ pyreverse -o png --ignore=__init___test.py domain/
```

## Set up 

In the Dev Container.

```
$ export PIPENV_VENV_IN_PROJECT=1
$ pipenv --python 3.8 
$ pipenv install
```

## Run

In the Dev Container.

```
$ pipenv shell
$ uvicorn main:app --reload --host 0.0.0.0 --port 8000 
```

The same as appPort in [devcontainer.json](.devcontainer/devcontainer.json).


## Swagger UI

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)



## Test

In the Dev Container.

```
$ pipenv shell
$ pytest usecase/
```

## Reference

- [FastAPI](https://fastapi.tiangolo.com/)
- [Swagger](https://swagger.io/)
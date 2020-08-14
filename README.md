# DDD on Python

Trial and error of DDD on Python.

## Domain model 

![model](packages.png)


```
$ code ./ 
$ pipenv shell
$ pyreverse -o png --ignore=__init___test.py domain/
```

## Set up 

1. [Build the container in advance.](https://github.com/usabarashi/ddd-on-python-composer)
1. [Editing the path of docker-compose.](https://github.com/usabarashi/ddd-on-python/blob/master/.devcontainer/devcontainer.json)
1. Set up the environment inside the container. Using VSCode's Remote Container.

```
$ code ./ 
$ export PIPENV_VENV_IN_PROJECT=1
$ pipenv --python 3.8 
$ pipenv install
```

## Run

```
$ code ./ 
$ pipenv shell
$ python main.py 
```

## Open API

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Test

```
$ code ./ 
$ pipenv shell
$ pytest domain/ command/
```

## Reference

- [docker-compose](https://github.com/usabarashi/ddd-on-python-composer)
- [Developing inside a Container](https://code.visualstudio.com/docs/remote/containers)
- [docker](https://www.docker.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Swagger](https://swagger.io/)
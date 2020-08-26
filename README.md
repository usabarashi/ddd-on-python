# DDD on Python

Trial and error of DDD on Python.

## Domain model 

![model](packages.png)


## Setting up a development environment 

1. [Build the container in advance.](https://github.com/usabarashi/ddd-on-python-composer)
1. [Editing the path of docker-compose.](https://github.com/usabarashi/ddd-on-python/blob/master/.devcontainer/devcontainer.json)
1. Set up the environment inside the container. Using VSCode's Remote Container.

```
$ pipenv install
$ pipenv install --dev
```

## Run

```
$ pipenv run start 
```

## Open API

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Test

```
$ pipenv run test 
```

## Reference

- [docker-compose](https://github.com/usabarashi/ddd-on-python-composer)
- [Developing inside a Container](https://code.visualstudio.com/docs/remote/containers)
- [docker](https://www.docker.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Swagger](https://swagger.io/)
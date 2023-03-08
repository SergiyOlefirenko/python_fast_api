# Python Fast-api tutorial - https://youtu.be/0sOvCWFmrtA

Command to start server in dev mode:

```sh
uvicorn app.main:app --reload
```

## Required environment variables

All env variables can be specified in the ```.env``` file in the root directory of the project.

- ```POSTGRES_URL``` - postgresql connection url. Example: ```postgresql://postgres@localhost/fastapi```.

- ```SERCRET_KEY``` JWT token secret key. Example: ```cdecb314b87b6e3c8424538f1fbf6067aac90e9357dd8c7b70a9e67716b28f4f```. Secret key can be generated using the following command:
```sh
openssl rand -hex 32 
```

- ```ALGORITHM``` - encoding algorithm. Example: ```HS256```.

- ```ACCESS_TOKEN_EXPIRE_MINS``` - expiration time for the access token. Example: ```60```.

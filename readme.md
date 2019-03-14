# What did I learn today?
## About
Is a multiplatform app for introspective private microblogging. It allows you to write down something you have learn that day to take a look at it again in the future.

## Deployment

### RESTful API
In order to deploy the REST API you need python (tested only in 3.4) and the following dependencies:

```bash
pip install flask flask_restful flask_cors  flask_sqlalchemy configparser mysql-connector-python-rf pyjwt
```

Proceed uploading the api_wdilt.py found in the API folder to your Flask server, and the configuration config.ini file where you should change the defaults to your database URI.

Once the API is uploaded and the config changed, set a enviroment variable for your secret key to encode the Json Web Tokens (JWT), used for authentification.

```bash
(env)$ export JWT_KEY="super secret key here"
```

Now we can deploy the API as any other flask application.

### ANDROID app
In development...

### ANGULAR web app
In development...


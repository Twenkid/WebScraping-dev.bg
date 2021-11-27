# WebScraping-dev.bg

A lesson in Flask, web scraping, sqlalchemy, beautifulsoup by Marko, presented during a Dev.bg event.

Twenkid: An exercise, trying it out without the video of the lecture and no prior experience with Flask; on Windows. Figuring out how to set up the DB, adding a batch file for setting the environment variables etc.

## Install WAMP or XAMPP.

![image](https://user-images.githubusercontent.com/23367640/143671396-c543d3f8-e10d-4f7d-b552-945136d661c3.png)

Config it: you may need to change the port 80, 81 to 8080, 8081 of the Apache (Skype conflicts). Left click on Config:

httpd.conf

#Listen 12.34.56.78:80
Listen 8080

ServerName localhost:8080

httpd-ssl.conf

Listen 8081

## Main config (top right button)

Set the call to phpmyadmin etc. :8080 ...

## Read the code: apis/models.py and recreate the Database:

(I changed some names to flask, pass: flask123 ...)

flask.sql

## Set the env file:

```
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_APP=app.py

SQL_SERVER=localhost:8080
SQL_DATABASE=flask
SQL_UID=root
SQL_PWD=flask123
```



## For running in Windows in the app folder:

```
cmd /v /c "set SQL_SERVER=localhost&&set SQL_UID=root&&set SQL_PWD=flask123&&set SQL_DATABASE=flask&& python app.py
```

...

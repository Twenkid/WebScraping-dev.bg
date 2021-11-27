# WebScraping-dev.bg

A lesson in Flask, web scraping, sqlalchemy, beautifulsoup by Marko, presented during a Dev.bg event.

Twenkid: An exercise, trying it out without the video of the lecture and no prior experience with Flask; on Windows. Figuring out how to set up the DB, adding a batch file for setting the environment variables etc. Reminding/practice of SQL commands etc.

## Install WAMP or XAMPP

WAMP now seems to have nasty requirements of 1000 VS redistributables to install and is bigger, XAMPP is smaller and is OK:

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

```
CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `website_id` int(11) DEFAULT NULL,
  `category_name` text NOT NULL,
  `category_url` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `website_id` (`website_id`);
```  
etc.

## phpmyadmin

SET PASSWORD = 'flask123';


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



##

## However/or override it with the command in Windows, while cwd = app folder:

```
cmd /v /c "set SQL_SERVER=localhost&&set SQL_UID=root&&set SQL_PWD=flask123&&set SQL_DATABASE=flask&& python app.py
```

...

## The more interesting part ...

...

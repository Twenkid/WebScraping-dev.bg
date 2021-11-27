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

## Study the code, ```__init__.py``` etc. Finding apis/models.py - SQL model, recreate the Database:

![image](https://user-images.githubusercontent.com/23367640/143672249-c5310df8-dabd-4126-a6a0-21c61f8b48e3.png)

![image](https://user-images.githubusercontent.com/23367640/143672285-f0b6d106-9c98-4376-8488-afcbbd97f64b.png)


I changed some names to flask, pass: flask123 ...

See **flask.sql**

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

Find out how to change passowrd, to edit types, add foreign key etc.

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

## However/or override it with the command in Windows, while cwd = app folder:
(Study the code and figure it out)
```
cmd /v /c "set SQL_SERVER=localhost&&set SQL_UID=root&&set SQL_PWD=flask123&&set SQL_DATABASE=flask&& python app.py
```

![image](https://user-images.githubusercontent.com/23367640/143672318-1ae3cc9e-76d6-4466-a3e7-6296661b86d9.png)

...

## The more interesting part ...

...

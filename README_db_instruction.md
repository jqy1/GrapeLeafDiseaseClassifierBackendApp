## 1. Set up db via flask-migrate (for first time user)

### 1.1 Gather all the necessary info first
```
Refer to email "Test databases for COSC680" on the 2022-12-19 3:00 PM

Locate these info from the email:
  usercode
  password
  host
  db
```
### 1.2 Update .env
```
In the .env file, replace usercode:password@host/db with the info gathered above, and save the file.
```
### 1.3 Delete
```
Delete these first:
  "migrations" folder under cosc680-backend
  "alembic_version" table in the phpMyAdmin cosc680-2022 db
```
### 1.4 Run these commands in terminal with this order
```
$ export FLASK_APP=run.py
$ flask db init
$ flask db migrate -m "message for this update."
$ flask db upgrade
```


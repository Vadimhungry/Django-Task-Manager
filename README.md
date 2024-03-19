# The Task Manager application.
___
[![Actions Status](https://github.com/Vadimhungry/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Vadimhungry/python-project-52/actions)[![Maintainability](https://api.codeclimate.com/v1/badges/d8910e1e0b24d5145a42/maintainability)](https://codeclimate.com/github/Vadimhungry/python-project-52/maintainability)[![Test Coverage](https://api.codeclimate.com/v1/badges/d8910e1e0b24d5145a42/test_coverage)](https://codeclimate.com/github/Vadimhungry/python-project-52/test_coverage)

This is a simple task manager built on Django. It features user registration, authentication, creation, modification, and deletion of statuses, labels, and tasks. Check working app here: [Task manager app](https://python-project-52-production-9e9a.up.railway.app/)

## Installation 
1. `git clone git@github.com:Vadimhungry/Django-Task-Manager.git`
2. `poetry install`
3. `make migrations`

## Environment variables
You should set three env variables.
The simplest way to set variables is to rename the project file ".env.example" to ".env"

### Variables
The ".env.example" file contains three variables:

DJANGO_DEBUG=True/False

SECRET_KEY="your_secret_key"

ROLLBAR="your_rollbar_key"

Additionally, you can connect your database by setting variable:
DATABASE_URL="your_database_url"

## Language

In `task_manager/settings.py` set LANGUAGE_CODE.
For English language, replace "your_language" with "en", and for Russian - with "ru".

LANGUAGE_CODE = "your_language"

## Run the app

Use `make start` to run the app.
Application will be availible at http://127.0.0.1:8000/

## The functionality of the application
### Hompage
![Homepage](https://i.postimg.cc/q74mHrxh/Screenshot-2024-02-27-at-15-58-15.png)
To use the application, you need to register and log in. To proceed to registration, click **Sign Up**.

### Sign Up page
![Sign up page](https://i.postimg.cc/Vk6QQjsP/Screenshot-2024-02-27-at-16-09-35.png)
To register, fill out the form and click Register.

### Login page
In case of successful registration, you will be redirected to the login page. 
Enter your username and password here to authenticate.
![Sign up page](https://i.postimg.cc/02vw90B3/Screenshot-2024-02-27-at-16-12-48.png)

### Hompage after login
If the username and password are correct, you will be redirected to the main page and see a flash message about successful login. Now you have access to all the functionalities of the application.

![Succsessfull login page](https://i.postimg.cc/k5PrHD4x/Screenshot-2024-02-27-at-16-16-26.png)

### Users page
On the Users page, you can view the list of users, as well as edit or delete your profile.
![Users page](https://i.postimg.cc/GpvjMm8T/Screenshot-2024-02-27-at-16-23-43.png)

### Statuses page
Here you can create, update and delete statuses for tasks.
![Statuses page](https://i.postimg.cc/B6nfskGp/Screenshot-2024-02-27-at-16-26-55.png)

### Labels page
Here you can create, update and delete labels for tasks.
![Labels page](https://i.postimg.cc/vBxFc9cx/Screenshot-2024-02-27-at-16-30-52.png)

### Tasks page
Here you can create, update and delete tasks.
Also you can use filter to find tasks of certain categories.
![Tasks page](https://i.postimg.cc/R054KgxQ/Screenshot-2024-02-27-at-16-45-46.png)
Click "Create task" to proceed on task creation page.

### Task creation page
To create a task, fill out the form. The 'Name' and 'Description' fields can be filled with any text. 'Status', 'Executor', and 'Labels' can only be selected from the dropdown list. 'Status', 'Executor', and 'Labels' need to be created beforehand in the respective sections of the website.
![Task creation page](https://i.postimg.cc/zX2nzgY1/Screenshot-2024-02-27-at-16-51-34.png)

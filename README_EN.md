# Yamdb API
## Project description
YaMDb is a project where people can leave reviews of books, films, music and other works. The works are divided into categories and can be assigned a genre. Administrators can add new works, categories and genres. Users can leave their reviews and rate works and comment on reviews of other users.
## Launch of the project
- Clone the repository and go to it on the command line:
```
git clone https://github.com/Belyanski/api_yamdb
```
```
cd api_yamdb
```
- Create and activate a virtual environment
```
python -m venv venv # For Windows
python3 -m venv venv # For Linux and macOS
```
```
source venv/Scripts/activate # For Windows
source venv/bin/activate # For Linux and macOS
```
- Install dependencies from requirements.txt file
```
pip install -r requirements.txt
```
- Go to the folder with the management script and perform migrations
```
cd api_yamdb
```
```
python manage.py migrate
```

- Launch the project
```
python manage.py runserver
```
## Creating a superuser
- In the directory with the manage.py file, run the command
```
python manage.py createsuperuser
```
- Fill in the fields in the terminal
```
Username: <your_name>
Email address: <your_email>
Password: <your_password>
Password (again): <your_password>
```
## New User Registration
- Send ```127.0.0.1:8000/api/v1/auth/signup/``` **username** and **email** to the endpoint
- Receive a confirmation code to the transmitted **email**. Access rights: Available without a token. The use of 'me' as **username** is prohibited. The **email** and **username** fields must be unique.

## Obtaining a JWT token
- Transfer to the endpoint ```127.0.0.1:8000/api/v1/auth/token/``` **username** and **confirmation** code from the letter. Access rights: Available without a token.

## Query examples

- Send a POST request to the address ```http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/``` and pass the ``text`` field ` <br>
An example of a request to create a comment on a review:
```
{
"text": "Cool review!"
}
```
Sample answer:
```
{
"id": 0,
"text": "Cool review!",
"author": "string",
"pub_date": "2019-08-24T14:15:22Z"
}
```

## Complete documentation for the project API:

The list of requests to the resource can be found in the API description

```
http://127.0.0.1:8000/redoc/
```

### Importing data from test CSV files into the database:
To import data, use the ```importdata``` command.
```
python3 manage.py importdata
```

The command imports data from CSV files into database tables with appropriate names.
CSV files must be placed in a folder designated ```STATICFILES_DIRS``` in the data subfolder.
The data will be imported into the default database specified in the project settings as ```DATABASE['default']```.



### Technologies:

REST API, Viewsets, routers, JWT, serializers, permissions, limits, pagination, sorting, CSV, Django.

## The project was made by
* [Ekaterina Dodonova](https://github.com/dodonova)</br>
* [Alexey Kotko](https://github.com/Zaphod999)</br>
* [Anton Ilyichev](https://github.com/Antochino)</br>

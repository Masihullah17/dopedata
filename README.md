# DopeData

## SOAD Course Project

## Team Members
* Shaik Masihullah | S20180010159
* Shikhar Arya | S20180010162
* Rishimanudeep | S20180010062
* Kavya Nemmoju | S20180010078

## To run the django application
```
Create env :
	python -m venv env

Activate env :
	For Windows :
		.\env\Scripts\activate
	For Linux :
		./env/Scripts/activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py makemigrations data
python manage.py migrate
python manage.py createsuperuser

python manage.py loaddata db.json

python manage.py runserver
```

## Project Structure
* **dopedata** - Main Django application name
* **data** - App containing the models and database work
* **data/api** - Contains the API
* **webapp** - App containing the web application
* **templates** - Contains all the html pages of webapp
* **static** - Contains all the static files (css, js, images, etc) for webapp
* **templatetags** - Contains filters to be used in html pages to render better
* **media** - Contains all images, videos and audios we collect as part of data collection

## Resources
* [**Firebase Authentication API**](http://www.lib4dev.in/info/thisbejim/Pyrebase/36919582)
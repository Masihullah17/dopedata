# DopeData

## Service Oriented Application Development (SOAD) Course Project

### Team Members - Group 2

-   Shaik Masihullah | S20180010159
-   Shikhar Arya | S20180010162
-   Brinda S | S20180010031
-   Rishimanudeep | S20180010062
-   Kavya Nemmoju | S20180010078

### Problem

In the world of Big Data, there might exist a situation where there is shortage of a particular dataset.
This maybe data which has to be more fresh or more closely related to daily life of people.

To understand this in a better way, let’s consider an example where a person has a bright idea of making a machine learning model which will be of great help to the society, but he doesn’t have enough data to train his model or a survey is to be taken at a large scale and it is almost impossible to create it from scratch.

Having the solution of an unsolved real world problem, but no data available to implement it, is a modern nightmare.

Real world problems like fraud & spam detection, surveillance systems (CCTV & UAV), navigation system, etc can be leveraged to another level if sufficient & accurate data is available.

### Introduction

DopeData is an open data community platform (blend of Kaggle and GitHub). Open data is based on the idea that some data should be freely available to everyone to use and republish as they wish, without restrictions from copyright, patents or other mechanisms of control.

Building a community platform where researchers, organizations, contributors, consumers, etc can come together and help each other in piling up non existing datasets for crafting new revolutionary products.

Aim is to not let any competent and out of the box idea go in vain for just the sake of data unavailability.

### Data Formats available

-   Image
-   Video
-   Audio
-   Choose an option
-   Multi choice - Multi correct
-   Short texts
-   Paragraph

### Services Consumed

-   **Firebase Authentication**
    -   To allow customers authenticate our application using different platforms like email, gmail, github, linkedin, etc.
    -   To enable cross platform authentication, so as if we extend our application for different platforms, we will have a centralized authentication system.
-   **Google Drive**
    -   To allow customers to store the data they have requested to be stored directly on their google drives itself.
    -   It also ensures the customers not to worry about the data safety.

<br/><br/><br/><br/>

### Services Exposed

-   **Search**
    -   To enable searching across the community for publicly available datasets
-   **Request**
    -   To raise a request for a new data requirement
-   **Contribute**
    -   For contributing to a data request raised
-   **User profile and Data Insights**
    -   To showcase the user’s competitive profile in our community on their portfolio or company websites.
-   **Download collected data**
    -   Once the required data volume is collected, download all the data with a single download request.

### Potential Marketplace

-   **Business to Business (B2B)**
    -   Organizations, startups, research labs, etc can raise a request for a dataset, use a dataset or manage their datasets.
    -   With premium feature, they can also create a local network of who can contribute to or access the dataset.
-   **Business to Customers (B2C)**
    -   Data scientists, researchers, analyst, developers, students or any individual in search of a dataset to give shape to their creative ideas.
    -   Any lettered individual can contribute, request or use the dataset.

### Creating python virtual environment

```
Create env :
	python -m venv env

Activate env :
	For Windows :
		.\env\Scripts\activate
	For Linux :
		./env/Scripts/activate
```

### API Keys

-   Firebase : Plugin your firebase config data in dopedata/settings.py file
-   Google Drive API : Create a file named client_secrets.json with your credentails and keep it in the same folder as README.md file

### To run the django application

```
pip install -r requirements.txt

python manage.py makemigrations
python manage.py makemigrations data
python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
```

### To run the django unit and integration tests

```
python manage.py test
```

### To run the django mock application using services

```
cd mockapplication
python manage.py runserver 127.0.0.1:8080
```

<br/><br/><br/><br/>

### Project Files Structure

-   **dopedata** - Main Django application name
-   **data** - App containing the models and database work
-   **data/api** - Contains the API
-   **webapp** - App containing the web application
-   **templates** - Contains all the html pages of webapp
-   **static** - Contains all the static files (css, js, images, etc) for webapp
-   **templatetags** - Contains filters to be used in html pages to render better
-   **data/tests & webapp/tests** - Folder containing all the django tests created to test the application
-   **media** - Contains all images, videos and audios we collect as part of data collection

The development branch is maintained seperately for development pushes. Code is merged to main branch whenever a submodule and it's testing is completed.

### Review Videos Link

-   [**Google Drive Link**](https://drive.google.com/drive/folders/1_jsIHaLgilVkxZ67JS9u8vjdDyQ0DRXB?usp=sharing)

### Resources Used

-   [**Firebase Authentication API**](http://www.lib4dev.in/info/thisbejim/Pyrebase/36919582)
-   [**Google Drive API**](https://googleworkspace.github.io/PyDrive/docs/build/html/index.html)
-   [**Django Testing**](https://www.valentinog.com/blog/testing-django/)

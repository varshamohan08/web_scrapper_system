# Web Scrapper System
This Django project is designed to save and retrieve details of entities from a specified webpage. It uses Django REST framework to create API endpoints and Selenium WebDriver to scrape the webpage for data.
### Features
- Save Entity: `/api/save-entity/` accepts a URL as a parameter, uses Selenium to pull down the page, extracts entities from the page, and stores the extracted data in the `EntitiesMaster` table in a MySQL database.
- Get Entity: `/api/get-entity/` reads the entities from the EntitiesMaster table.
### How to Run
#### Prerequisites
- Python 3.x
- Django
- Django REST framework
- Selenium
- ChromeDriver
#### Installation / Setup
Clone the repository:
```
git clone https://github.com/varshamohan08/web_scrapper_system.git
```
Navigate to the project directory:
```
cd web_scrapper_system
```
Install the required packages:
```
pip install -r requirements.txt
```
Setup the database:
```
python manage.py makemigrations
python manage.py migrate
```
Run the development server:
```
python manage.py runserver
```




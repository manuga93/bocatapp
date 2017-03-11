# Bocatapp Core

## Project structure (IMPORTANT to read before make changes)
If you have some question you could contact to @garridev directly. This is project structure:
```
\bocatapp
  \bocatapp (General views, templates and urls. f.e. login, legal advice, home, contact, etc.)
  |--\templates
  |--|--\auth
  |--|--\forms
  |--|--\includes
  |--|--|--footer.html
  |--|--|--header.html
  |--|--base.html (Parent template)
  |--|--home.html (Home page)
  |--decorators.py
  |--settings.py (Main configuration file of project)
  |--urls.py
  |--views.py
  \customer (Views, templates and url related to Customers. f.e. checkout, my orders, my account, etc.)
  |--\forms (Forms)
  |--\templates (Templates for customers .html)
  |--\models.py  (Models related to Customer model)
  |--\views.py (Views related to Customer entity)
  |--\urls.py (Urls only for customers)
  \seller (Similar to customer folder but for sellers)
  \administration (Similar to customer folder but for administration)
  \media (Users images uploads, f.e, profile pics)
  \static (All statics of app)
  |--\fonts  (.woff, .ttf, etc.)
  |--\images  (logos, icons, etc.)
  |--\scripts (.js)
  |--\styles (.css)
```

**IMPORTANT ADVICE!**
Django's models are the same as Spring's models.
**BUT**
Django's views are Spring's controllers in Django projects.
Django's templates are Spring's views in Django projects.

## Start project

Run this project typing in Terminal:
```
./manage.py runserver
```
Open in your navigator http://127.0.0.1:8000/

## Updating models

Run after udpating models:
```
./manage.py makemigrations
./manage.py migrate
```

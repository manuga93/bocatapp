# Bocatapp Core

## Dependencies
**IMPORTANT!** bootstrap3 dependency is required! Please install it:
```
pip install django-bootstrap3
```
Now you keep using Django forms easily like in this example:
```
{# Load the tag library #}
{% load bootstrap3 %}

{# Display django.contrib.messages as Bootstrap alerts #}
{% bootstrap_messages %}

<form action="/url/to/submit/" method="post" class="form">
  {% csrf_token %}
  {% bootstrap_form form %} <!-- old form.as_p -->
  {% buttons %}
    <button type="submit" class="btn btn-primary">
      {% bootstrap_icon "star" %} Submit
    </button>
  {% endbuttons %}
</form>

{# Read the documentation for more information #}
```
Read his documentation [here](https://django-bootstrap3.readthedocs.io/en/latest/quickstart.html)

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
## Populate DB

To populate the database you must type in Terminal:
```
python manage.py populatedb
```

## Users and Roles
To force a user to be logged in you must type this in the url file
```
from .decorators import anonymous_required
url(r'^customer/register/$', anonymous_required(RegistrationCustomerView.as_view(),
                                               message='You`ve already sign in!'), name='user_register'),
```
you can check the permission in the view typing this just before the controller
```
from bocatapp.decorators import permission_required
@permission_required('bocatapp.customer', message='you cant enter')
```

And at the template you can use this to show whatever you want
```
{% if perms.bocatapp.customer %}
    <li><a href='seller/local'>Listado</a></li>
{% endif %}

{% if perms.bocatapp.seller %}
    <li><a href='seller/local/new'>Insertar</a></li>
{% endif %}
```

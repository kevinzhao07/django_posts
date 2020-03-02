## Quick Python Commands  
**Run our program**: `python manage.py runserver`  
**Create new app**: `python manage.py startapp [APPNAME]`  
**Create a user to log into `/admin`**: `python manage.py createsuperuser`  
> make sure a database has already been created, so migrations will allow us to make changes.  

**Run migrations on database**: `python manage.py makemigrations`
> will either display `No changes detected` or show which new models were made. (if database was previous created)  

**Apply migrations onto database**: `python manage.py migrate`  
> will also work if no database was created, and will create a simple database structure to start with. in our project, our `authuser` table exists.

**See SQL code represented from out database**: `python manage.py sqlmigrate [APPNAME] [MIGRATION NUMBER]`   
**Run python-django shell**: `python manage.py shell`  
**Query all users from a model**: `[MODEL NAME].objects.all()` 
> `objects` supports `.first()`, `.filter([ATTRIBUTE = 'SOMETHING'])`, `.get(id=[ID])`, etc to bring out specific entries in a model. each objects has their own unique `id` and `pk` (primary key)




## To add new pages/links to our site
In order to create new links for our website, like `localhost:8000/blog` into our new website:  
- we have to create a function inside `blog/views.py` and link it to the urlpatterns inside `blog/urls.py`.
- we also have to update our urlpatterns inside our `/urls.py` in our main project directory in order for it to be passed onto our `blog/urls.py`.
- to set homepage, set the first argument of the `path` to `''`, and a corresponding function will automatically be executed to be the homepage.
- **blog/view.py** (function) --> **blog/urls.py** (update urlpatterns) -> **/urls.py** (update urlpatterns) 

**<ins>How it works</ins>:**  
1. when the computer reads any `string` after the `localhost:8000`, it passes this argument using `HttpResponse` from `django.http` to `/urls.py` in the main project directory.
2. it then scans the `urlpatterns` variable and tries to find a match with any of the links provided. if no match is found, a `404 ERROR` will be returned.
> if `/blog/about` was read in, it would scan for blog only, and advance from there. if `/` is found, the empty string is looked for (usually our main/homepage).
3. if there is a match, the rest of the `string` will be passed onto the corresponding function or a function will be executed. 
> if `/blog/about` was read in and `blog` was matched, the rest of the string (`/about`) would be passed onto the `/urls.py` in the `/blog` directory.  

## Usage of Templates  

`django` automatically looks for a sub-directory of `/templates` in each installed app (in our case `blog`).
> convention to create another folder with same app name (`/blog`) inside `/templates` as to not confuse reader. the templates will go **inside** that folder. our structure is `django_posts` (overarching directory) > `/blog` (our app) > `/templates` > `/blog` > our .html files.

**<ins>Adding each app to list of installed apps</ins>**  
we must add our app of 'blog' to our list of installed app, so django knows where to look for a `/templates` directory. within our blog application, we can find a file called `apps.py`, which has a `AppName-Config` function. Open up project's `settings.py` file to add path to this `AppName-Config` for our list of installed app, so django knows where to look. 
> get used to adding applications to this list whenever we create one so django can look for databases/templates.

**<ins>Loading in Templates</ins>**  
in order for a page to use a template, we must load it in through `HttpResponse`, or return a `render(request, directory/template.html)`. this must be added to our `views.py`. 

**<ins>Displaying already made posts in templates</ins>**  
we can add dummy data in our `views.py` in our `/blog` directory. we can have a "list of dictionaries" that we will render in our templates soon. 
> these are in a static repeating form of `author:`, `title:`, etc. for now, we can imitate this as having just gotten data back from a database (haven't talked about those yet).
to display anything (gotten from database or not) to homepage, we can pass in templates as a dictionary. `render()` takes a third optional argument, which is for content or extra data needed to be passed in. our dictionary that we created can simply be passed in here.  

**<ins>Using template rendering to pull in data</ins>**  
from there, we have to modify our `home.html` file to reflect changes and posts that are being made. django uses a templating engine similar to jinja2, and we can write loops/functions using code blocks (`{% %}` and `{% [end statement] %}`). we can access variables using `{{ }}`.
> we have `{% for post in posts %}`. `post` is our locally defined variable and can be anything (post just seems related to posts). however, `posts` refers to the key of the dictionary `context` that we passed in earlier from our `views.py` file. though the same name, it is not the object inside `views.py` (that we declared outside of scope), it is referring to it because we passed it in as `'posts': posts`.

since we passed in some context (appropriately named `posts`), we can then loop through that dictionary and for each entry (or `post` in our case), we can access the variables inside (`title`, `author`, etc.) we used `{{ }}` to access variables and `{% %}` for logic. 

**Adding more context (passing into templates)**  
we can add multiple pieces of data into our templates and can name then whatever. to refer to that data from our templates, we can use the same name but with `{{ }}`. we added `title` to our templates in order to see how an `{% if %}` and `{% else %}` works. if we were to pass in a `title`, `{% if title %}` would check if one existed, and if it did, we could do with it accordingly. after both `if` and `else` statements, an `{% endif %}` is needed to end the `if` statements.

**What to do for repeated `html` between template files**  
when we look at our files for now, there are a lot of repeated `html` segments that we don't want to keeo writing over again. we then created a `base.html` template with all the repeated code that can be inherited by the other files. we can create a `{% block content %}` and `{% endblock %}` for the text that needs to be changed from file to file. 
> now we have to remove all the duplicated code from both `home.html` and `about.html`. for code specific to each file, we will wrap in a `{% block content %}` and `{% endblock content %}` and have `{% extends "folder/template.html" %}` where `template.html` is the file that contains all the duplicated code. 

**Adding bootstrap/css files (popular with designing webpages)**  
we will add it __locally__ since it's easier than downloading all of bootstrap and hosting it at the same time as our website. for css/js files that are `static`, we must add it into a `static` folder within our app. we can create a `static` folder within our root `blog` folder (our app folder), and again, inside the `static` folder (as we did with our `templates` folder) create a `blog` folder so we tell the machine where our `.css` and for what website they are being used for. 
> wherever a `.css` files needs to be included, a `{% load static %}` must be put at the top of the page to indicate that we want to load a static file from our `static` directory. also, the `href=" "` tag is unique in that we must access the name of the file using `{% static 'nameOfApp/nameOfCssFile.css' %}`

## Urls and Links  
because we don't want to keep chaging our html whenever we change the names of our urls, especially in our template file (`base.html`). what we can do is instead of hardcoding the route, we can add `href="{% url 'nameOfRoute-in-urls.py-in-/blog' %}` in our case, our name was `blog-home`. 

## Creating Databases with Models  
we can create models for whatever type of data we want, and in our case, we will create a model for differenty types of `posts` and `users`. each of these `models` will be a class, and will have different attributes that you specify. 
> we can access each field by `models.[type]Field()`.
**note on databases**: a lot of fields have required/optional/no arguments, and those can be found at this documentation: https://docs.djangoproject.com/en/3.0/topics/db/models/. this contains every type of field that can be used within a django model.

**Adding User Table and Foreign Keys**  
since the user table was already created by django, in order to user it to fill our `author` attribute in our `Post` model, we can import it from `django.contrib.auth.models` and `import User`. this was pre-created by django. we will also make use of Foreign Keys, a one-to-one or many-to-one relationship to links posts and authors together, which is demonstrated by `models.ForeignKey`. there are two required arguments, first, another models table (which we will be linking to) and `on_delete`, which asks what to do when, in our case, the `User` gets deleted (only one way).  

`migration` is useful because it allows us to make changes to a database even after it's been created without using or learning sql. always use `makemigrations` then `migrate`

**Querying objects from previously created Models**  
to see what is in our database and make sure everything's in order, we can use the python shell to display all our previously created `models` and what's inside. we will be using the commands `[MODEL NAME].objects.all()` to show a dictionary of previously created entries inside each `model`. these can be set to a variable, and they all have specific `id` and `pk` to filter them. 

**Creating a [NAME OF MODEL] object**  
we are able to create model objects in our shell command line as if it were a constructor. creating a post would entail: `var = Post(title='', content='', author=user)`, where `user` was our variable that came from filtering the `User` model. in order for that change to be reflected into our database, we have to `.save()` it.
> to show how you want to display each model that's being printed in the shell, we can create a "dunder" function, in our case, `__str__(self)` to specify what we want to display when it is printed. 

**What can we do with these created Models and objects?**  
each of these newly crated objects can be set to a variable, and it's attributes can be accessed with `.` because we had a foreign key, we were able to access any `User` object inside of our `Post` object, which makes it easy to grab information about a user based on a `Post`. also, we are able to see all `Post` objects made by one `User` by running the command `[USER VARIABLE].[NAME OF MODEL].set.all()`. within this `set` command, we are also able to create more `Post` objects by adding onto the end `.create()` and fill in attribute fields.
> creating it this way does not require any `.save()` or `author` attribute. 

**Importing Models into `views.py` to be used with generating webpages**  
in the `.py` file, we have to import our Model to use as context to pass onto our template `.html` files. our old `context` passed in dummy data from our `posts` that we created, but now since we imported our Models, there is no need for hardcoding data. we can do this by `from .models import [NAME OF MODEL]`, and now we are able to use this model as we please in this file.

**Register our Models onto `admin` site**  
we want to have specific models of our choosing show up on the admin page, so we are able to edit/add/and delete them from the `admin` GUI. it's really easy: we just have to run `admin.site.register([NAME OF MODEL])` in that `admin` GUI, we are able to edit users/content, etc. 

## Quick Boostrap Classes  
`<div class="container">`: gives nice padding to whatever content is placed inside the div. for styling and spacing purposes. 
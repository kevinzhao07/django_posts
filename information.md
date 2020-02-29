## Quick Python Commands  
**Run our program**: `python manage.py runserver`  
**Create new app**: `python manage.py startapp [APPNAME]`  
**Create a user to log into `/admin`**: `python manage.py createsuperuser`  
> make sure a database has already been created, so migrations will allow us to make changes.
**Run migrations on database**: `python manage.py makemigrations`
> will either display `No changes detected` or show that there were changes (if database was previous created)  
**Apply migrations onto database**: `python manage.py migrate`
> will also work if no database was created, and will create a simple database structure to start with. in our project, our `authuser` table exists.


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

## Quick Boostrap Classes  
`<div class="container">`: gives nice padding to whatever content is placed inside the div. for styling and spacing purposes. 
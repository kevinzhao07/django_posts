## Run our program:  
`python manage.py runserver`  

## To add new pages/links to our site
In order to create new links for our website, like `localhost:8000/blog` into our new website:  
- we have to create a function inside `blog/views.py` and link it to the urlpatterns inside `blog/urls.py`.
- we also have to update our urlpatterns inside our `/urls.py` in our main project directory in order for it to be passed onto our `blog/urls.py`.
- to set homepage, set the first argument of the `path` to `''`, and a corresponding function will automatically be executed to be the homepage.
- **blog/view.py** (function) --> **blog/urls.py** (update urlpatterns) -> **/urls.py** (update urlpatterns) 

**!How it works!:**  
1. when the computer reads any `string` after the `localhost:8000`, it passes this argument using `HttpResponse` from `django.http` to `/urls.py` in the main project directory.
2. it then scans the `urlpatterns` variable and tries to find a match with any of the links provided. if no match is found, a `404 ERROR` will be returned.
> if `/blog/about` was read in, it would scan for blog only, and advance from there. if `/` is found, the empty string is looked for (usually our main/homepage).
3. if there is a match, the rest of the `string` will be passed onto the corresponding function or a function will be executed. 
> if `/blog/about` was read in and `blog` was matched, the rest of the string (`/about`) would be passed onto the `/urls.py` in the `/blog` directory.  

## Usage of Templates  

`django` automatically looks for a sub-directory of `/templates` in each installed app (in our case `blog`).
> convention to create another folder with same app name (`/blog`) inside `/templates` as to not confuse reader. the templates will go **inside** that folder. our structure is `django_posts` (overarching directory) > `/blog` (our app) > `/templates` > `/blog` > our .html files.

**!Adding each app to list of installed apps!**  
we must add our app of 'blog' to our list of installed app, so django knows where to look for a `/templates` directory. within our blog application, we can find a file called `apps.py`, which has a `AppName-Config` function. Open up project's `settings.py` file to add path to this `AppName-Config` for our list of installed app, so django knows where to look. 
> get used to adding applications to this list whenever we create one so django can look for databases/templates.

**!Loading in Templates!**  
in order for a page to use a template, we must load it in through `HttpResponse`, or return a `render(request, directory/template.html)`. this must be added to our `views.py`. 

**!Displaying already made posts in templates!**  
we can add dummy data in our `views.py` in our `/blog` directory. we can have a "list of dictionaries" that we will render in our templates soon. 
> these are in a static repeating form of `author:`, `title:`, etc. for now, we can imitate this as having just gotten data back from a database (haven't talked about those yet).
to display anything (gotten from database or not) to homepage, we can pass in templates as a dictionary. `render()` takes a third optional argument, which is for content or extra data needed to be passed in. our dictionary that we created can simply be passed in here.  

**!Using template rendering to pull in data!**  
from there, we have to modify our `home.html` file to reflect changes and posts that are being made. django uses a templating engine similar to jinja2, and we can write loops/functions using code blocks (`{% %}` and `{% [end statement] %}`). we can access variables using `{{ }}`.
> we have `{% for post in posts %}`. `post` is our locally defined variable and can be anything (post just seems related to posts). however, `posts` refers to the key of the dictionary `context` that we passed in earlier from our `views.py` file. though the same name, it is not the object inside `views.py` (that we declared outside of scope), it is referring to it because we passed it in as `'posts': posts`.

since we passed in some context (appropriately named `posts`), we can then loop through that dictionary and for each entry (or `post` in our case), we can access the variables inside (`title`, `author`, etc.) we used `{{ }}` to access variables and `{% %}` for logic. 
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
> convention to create another directory with same app name (`/blog`) inside `/templates` as to not confuse reader. the templates will go **inside** that directory. our structure is `django_posts` (overarching directory) > `/blog` (our app) > `/templates` > `/blog` > our .html files.

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

**<ins>Adding more context (passing into templates)</ins>**  
we can add multiple pieces of data into our templates and can name then whatever. to refer to that data from our templates, we can use the same name but with `{{ }}`. we added `title` to our templates in order to see how an `{% if %}` and `{% else %}` works. if we were to pass in a `title`, `{% if title %}` would check if one existed, and if it did, we could do with it accordingly. after both `if` and `else` statements, an `{% endif %}` is needed to end the `if` statements.

**<ins>What to do for repeated `html` between template files</ins>**  
when we look at our files for now, there are a lot of repeated `html` segments that we don't want to keeo writing over again. we then created a `base.html` template with all the repeated code that can be inherited by the other files. we can create a `{% block content %}` and `{% endblock %}` for the text that needs to be changed from file to file. 
> now we have to remove all the duplicated code from both `home.html` and `about.html`. for code specific to each file, we will wrap in a `{% block content %}` and `{% endblock content %}` and have `{% extends "directory/template.html" %}` where `template.html` is the file that contains all the duplicated code. 

**<ins>Adding bootstrap/css files (popular with designing webpages)</ins>**  
we will add it __locally__ since it's easier than downloading all of bootstrap and hosting it at the same time as our website. for css/js files that are `static`, we must add it into a `static` directory within our app. we can create a `static` directory within our root `blog` directory (our app directory), and again, inside the `static` directory (as we did with our `templates` directory) create a `blog` directory so we tell the machine where our `.css` and for what website they are being used for. 
> wherever a `.css` files needs to be included, a `{% load static %}` must be put at the top of the page to indicate that we want to load a static file from our `static` directory. also, the `href=" "` tag is unique in that we must access the name of the file using `{% static 'nameOfApp/nameOfCssFile.css' %}`

## Urls and Links  
because we don't want to keep chaging our html whenever we change the names of our urls, especially in our template file (`base.html`). what we can do is instead of hardcoding the route, we can add `href="{% url 'nameOfRoute-in-urls.py-in-/blog' %}` in our case, our name was `blog-home`. 

## Creating Databases with Models  
we can create models for whatever type of data we want, and in our case, we will create a model for differenty types of `posts` and `users`. each of these `models` will be a class, and will have different attributes that you specify. 
> we can access each field by `models.[type]Field()`.
**<ins>note on databases</ins>**: a lot of fields have required/optional/no arguments, and those can be found at this documentation: https://docs.djangoproject.com/en/3.0/topics/db/models/. this contains every type of field that can be used within a django model.

**<ins>Adding User Table and Foreign Keys</ins>**  
since the user table was already created by django, in order to user it to fill our `author` attribute in our `Post` model, we can import it from `django.contrib.auth.models` and `import User`. this was pre-created by django. we will also make use of Foreign Keys, a one-to-one or many-to-one relationship to links posts and authors together, which is demonstrated by `models.ForeignKey`. there are two required arguments, first, another models table (which we will be linking to) and `on_delete`, which asks what to do when, in our case, the `User` gets deleted (only one way).  

`migration` is useful because it allows us to make changes to a database even after it's been created without using or learning sql. 
when making changes to any model, always use `makemigrations` then `migrate`.

**<ins>Querying objects from previously created Models</ins>**  
to see what is in our database and make sure everything's in order, we can use the python shell to display all our previously created `models` and what's inside. we will be using the commands `[MODEL NAME].objects.all()` to show a dictionary of previously created entries inside each `model`. these can be set to a variable, and they all have specific `id` and `pk` to filter them. 

**<ins>Creating a [NAME OF MODEL] object</ins>**  
we are able to create model objects in our shell command line as if it were a constructor. creating a post would entail: `var = Post(title='', content='', author=user)`, where `user` was our variable that came from filtering the `User` model. in order for that change to be reflected into our database, we have to `.save()` it.
> to show how you want to display each model that's being printed in the shell, we can create a "dunder" function, in our case, `__str__(self)` to specify what we want to display when it is printed. 

**<ins>What can we do with these created Models and objects?</ins>**  
each of these newly created objects can be set to a variable, and it's attributes can be accessed with `.` because we had a foreign key, we were able to access any `User` object inside of our `Post` object, which makes it easy to grab information about a user based on a `Post`. also, we are able to see all `Post` objects made by one `User` by running the command `[USER VARIABLE].[NAME OF MODEL].set.all()`. within this `set` command, we are also able to create more `Post` objects by adding onto the end `.create()` and fill in attribute fields.
> creating it this way does not require any `.save()` or `author` attribute. 

**<ins>Importing Models into `views.py` to be used with generating webpages</ins>**  
in the `.py` file, we have to import our Model to use as context to pass onto our template `.html` files. our old `context` passed in dummy data from our `posts` that we created, but now since we imported our Models, there is no need for hardcoding data. we can do this by `from .models import [NAME OF MODEL]`, and now we are able to use this model as we please in this file.

**<ins>Register our Models onto `admin` site</ins>**  
we want to have specific models of our choosing show up on the admin page, so we are able to edit/add/and delete them from the `admin` GUI. it's really easy: we just have to run `admin.site.register([NAME OF MODEL])` in our app's `admin.py`, and we are able to edit users/content, etc. 
> make sure to import the model from our `models.py`  

## Authenticating Users with Login/Password  
we start off with creating a new app called `users`, since it will have it's own template,`views.py`, etc. this will be in the same directory as our `blog` app. 
> make sure to add the newly created app in our `settings.py` in the project `.py` file.  

**<ins>Accessing Django's built in Authentification System</ins>**  
in our site, we would want the ability for new users to join and post, as well as existing users to be able to log in and edit their own posts, so we would have to use an user authentication form. since this process is very common, django has a lot of built in tools in place to help with authentication. 
> we have to import `from django.contrib.auth.forms import UserCreationForms` in order to get access to these shortcuts.  

**<ins>How to get `.html` files from other apps/directories</ins>**  
since we have a new `.html` file in our new app, we still want to extend our `base.html` found in the `templates/blog` directory. however, we are still able to access the file in another app because it's in the `templates` directory. our heading can stay as `{% extends "blog/base.html" %}`.  

**<ins>CSRF Token for Security</ins>**  
in order for our form to work, we must add `{% csrf_token %}`. this protects against hacking and makes our website more secure. the form can be put anywhere using {{ form }}. the username entry, password, and password confirmation has already been set for us, so there's nothing to do but to drop the `form` somewhere.   
> we can include `{{ form.as_p }}` to show our form in paragraph text.  

**<ins>Adding Path to new App without `urls.py`</ins>**  
in our new app, we are able to add it to our path in `urls.py` in our main project directory without creating a `[APPNAME].urls.py` by simply importing our `views.py` model in our newly created app (this works either way). in our main project directory, we can import `from [APPNAME] import views as [APPNAME]_views` directly.
> this assumes that we have created a function in that `views.py` file. that function would take the form of: (as reference)
```python 
def register(request): # always have the request as an argument
  form = UserCreationForm() # passing in optional context 
  return render(request, 'users/register.html', {'form':form}) # request, template, context, etc.
```  
we will proceed to add a new path variable, specifying it's link, our register function and give it a name for now.  

**<ins>Submitting the Form</ins>**  
if we submit our form (with data) using `'POST'`, our app will create a `UserCreationForm` with that new data, but if the form was submitted without data, it simply redirects to an emtpy `UserCreationForm`. we still have to make sure the form that we submitted is valid, so we can run the command `form.is_valid()`. 
> the `username` or `password` field from our form is stored in `.cleaned_data`, which we have to use `.get()` to get. we can also print a message (one-time) of success to display to the user that their account was successful from `messages.success(request, [STRING])` by importing it from `django.contrib`.    

after the user successfully creates an account, we would want to redirect them to another page. to do this, we can make use of `redirect` from `django.shortcuts`. 
> this takes an argument of a url, or the name of a previously created url (in your other apps)

**<ins>Displaying Messages</ins>**  
messages in django are important because sometimes you need to tell the user something, and a small, one time pop-up is required. if the `messages.[NAME OF TAG]` is used in any `views.py` file, it should also be displayed in the base `base.html` file. to do this, a conditional to check for messages is needed and a loop through all messages is needed. the messages can be given a class of `alert-{{ message.tags }}`, which can be grabbed like so. 

**<ins>Saving Users from Forms into Database</ins>**  
after filling out our form and seeing that it's valid, we can save our User into our model database. this is as easy as `form.save()` since this form was originally generated from `django.contrib.auth.forms`, which had the `User` model in it already.   

**<ins>Adding other inputs onto `UserCreationForm`</ins>**  
we may want to have other inputs (email, birthday, etc), and to do this, we have to start with a `forms.py` file in our directory. this `forms.py` would import the `User` model from our `django.contrib.auth.models` as well as the `UserCreationForm` from `.forms`. we then have to create a class to pass our `UserCreationForm` as a parameter to use for modification. 
> we can add as many extra fields as we would like, and in our case, we added an `EmailField()`.   

we also have to add a class `Meta` to specify more options. we can set a model to be used when `form.save()` is called, as well as how fields will show up in an `array`.  
> `fields = ['STRING', 'STRING', 'STRING']`  

now, instead of using the old `UserCreationForm`, we can replace that with our `UserRegisterForm` that we just made in `forms.py`.
> make sure to import that file on the top!  

**<ins>Crispy Forms</ins>**  
a third-party application that allows easy styling of forms. make sure to add it into installed apps in our project's `settings.py` after pip installing it. also, change the `CRISPY_TEMPLATE_PACK` to bootstrap4. 
> to use this, we must `{% load crispy_forms_tags %}` into our template and use it as a filter on `{{ form }}`.

## Login Page for Users with Accounts
django aleady takes care of login and logout forms for us, so all we must do it import the views from `django.contrib.auth` in our `urls.py` file. we must add them to our `urlpatterns`, but django already takes care of all the logic, authentification of forms/usernames/passwords. 
> note that we still must create templates for these new urls as django doesn't create templates for us.  

**<ins>Connect LoginView and LogoutView to our own templates</ins>**  
because django doesn't create templates for us, we need to specify a route to our own template or our `/login` and `/logout` page will result in an error. we can pass an argument into our `.as_view()` file, `template_name="[directory NAME]/[HTML.html]`. 

**<ins>Changing Link on Successful Login/Logout</ins>**  
when using django's `Login` and `Logout` View, on successful login, it automatically redirects to `accounts/profile`. because we don't have that, we have to modify that automatic redirection into our project's `settings.py`. we have to add a setting called `LOGIN_REDIRECT_URL`, setting it equal to whatever page we want, in our case the `blog-home` page. 
> we have to do this for logout as well, because the default logout page links us to the django administration pages.  

**<ins>Navigation Bar Conditional</ins>**
it would make sense to display login and register only if the user wasn't logged in, so we can place a conditional `if` inside `base.html`. django makes this easy by having a `user.is_authenticated` that tells us if anyone is logged in at the moment. 
> it's good to have additional feedback for the user to see if they're logged in or logged out.  

**<ins>Getting User in Templates</ins>**:   
the user is automatically passed in by django, and doesn't need to be passed in as context into a template. we are able to access these users using `{{ }}`. 

**<ins>Login_Required</ins>**:  
for some pages, we don't want any user who is not logged in to view a page (such as a profile page since it would make no sense). for these pages, we can import a decorator, specifically `login_required` from `django.contrib.auth.decorators`, and add it to whatever page that requires a login to view beforehand. however, since django still defaults to `accounts/profile`, we have to go into our `settings.py` file as before, and add a `LOGIN-URL`.

our code becomes:
```python 
# in django_blogs/settings.py
LOGIN_URL = 'login' # or name of login (you specified)

# in users/views.py
@login_required # requires user login before viewing profile
def profile(request):
  return render(request, 'users/profile.html') # links to profile.html
```

## User Profile and Uploading Pictures
becuase the `User` model that django provides for us is pretty limited, we want to add the choice of a profile picture or other things to modify a user's profile. we can do this in our own `models.py` file, with the help of `OneToOneField` relationships (same as `ForeignKey`).

**<ins>Creating and Inheriting other Models</ins>**  
since we want to branch off of the `User` model that django gives us, we can create a new model to inherit a `OneToOne` relationship with it. our new model is profile, which means each `User` will have one profile and vice versa. we can also add as many other fields as we want (`CharField`, `ImageField`, etc). 
> for our `ImageField()`, we can set a default .jpg photo, as well as an `upload_to` argument which states the directory that photos will be uploaded to.   

**f strings**: f strings, or `f'{}`, are strings where you can embed expressions inside string literals. for example, if you want to print someone's username, we can do `f'{user.username}'s profile`, which will print a string of the user's username and combine this with other string literals. 

we are able to access our profile from a `User` model by doing `user.profile`, since it is a one to one relationship, and vice versa because the profile model inherits from `User`. 

**<ins>Image Saving</ins>**  
since we don't have the ability to create profiles yet, we can manually create them in our `/admin` site. after doing that, we see that a new directory called `profile_pics` has been created (same directory as our entire project directory), where all the images that have been uploaded as profile pictures have been stored. 

this is not good for the following reasons:
1. if we have multiple models that want to save an image/file upload, then these new directories will clutter up our main project directory with extra directorys. 
2. we want to store files and uploaded images not in our database because that would slow our site down. there is no need to hold an image for every user. 
3. we want to edit our `settings.py` file and add a `MEDIA_ROOT` AND `MEDIA_URL`, where `MEDIA_ROOT` is the full path of where uploaded images will be saved and 

**<ins>`MEDIA_ROOT` and `MEDIA_URL`</ins>**  
we have to use `MEDIA_ROOT` and `MEDIA_URL` in order to save our photos in another directory. we want to set our `MEDIA_ROOT = os.path.join(BASE_DIR, 'media')` and `MEDIA_URL = '/media/`
- `os.path.join` means no matter what OS we are using, a path will be generated correctly (let this be abstracted away)
- `BASE_DIR` was a django created variable that specifies where our project's base directory directory is
- `media` is the name of our directory to where our directory of uploaded photos will be stored (2 directories deep) 
- `/media/` tells django where to look to find our directory of uploaded photos 
now, when an image is uploaded into a new profile, a directory called `media/` appears in our project's directory (same directory as `manage.py`), and inside, a directory named `profile_pics` has appeared. inside that are our uploaded photos. 
> `django_posts/` -> `media/` (as well as `django_posts/`) -> `profile_pics/` -> `img.jpg`  

**<ins>Setting up Profile Template to work</ins>**  
after image upload and creation is done, we can set up each user's profile. images will not work yet unless we add a snippet of code to our `urlpatterns` in our project directory's `url.py`. from the django documentation, https://docs.djangoproject.com/en/3.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development, we can add:  
```python
# ... the rest of your imports goes here ...
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] 

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # making it more readable
```

**<ins>Default Profile for Every User</ins>**  
right now, the only way to create profiles is through the `/admin` settings, but we don't want to do that every time a new user is made. we need to make use of `django signals`, which would require us creating a `signals.py` file inside of our `users` app. we have to write `from django.db.models.signals import post_save` in order to have an action that happens post_save of a `user` being created (or saved).  
> this only works when we have a signal and receiver. our `User` model from `django.contrib.auth.models` will be the signal (when it is saved), and our `Profile` model from `.models` will be the receiver.

**function needed**: this simply creates and saves a profile, and imports signal
```python
# when our sender (User) is saved, (post_save), create_profile is called (as the receiver)
@receiver(post_save, sender=User)

""" arguments that receiver passed in:
  - instance: is an instance of the model, User
  - created: bool, was the User just created or not?
  - sender: the User model
  - kwargs: any extra keyword arguments (don't need to know)
"""
def create_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)

# when our sender (User) is saved, (post_save), save_profile is called (as the receiver)
@receiver(post_save, sender=User)

# we have no need for created. after our profile was created, we can just do instance(our User).profile.save()
def save_profile(sender, instance, **kwargs):
  instance.profile.save()
```
also, in our `apps.py` file in our `users` app, we have to include a function called `ready(self)`, which simply imports `[APPNAME].signals`. this allows for a `Profile` to be created as soon as a `User` is created. importing signals will take in the code from the directory's `signals.py`.

## Updating User (Model) Profile
we want to have a way for users to update their username and email (for now), and the way to go about that is through using a `UserUpdateForm`, inheriting from `forms.ModelForm)` [is built in].
> if we want to edit our image, we have to do that through our `Profile` model, not our `User` model.

```python 
# to update the User form, inherit from forms.ModelForm
class UserUpdateForm(forms.ModelForm):
  email = forms.EmailField() # the extra form added from before

    class Meta:
      model = User # which Model are we targeting?
      fields = ['username', 'email'] # which can we change?

# to update the Profile form, same inherit as before
class ProfileUpdateForm(forms.ModelForm):
  # no additional fields added
  class Meta:
    model = Profile # affecting the Profile model
    fields = ['image'] # we are only looking to change image
```
we can only allow users to update their email, username, and image _inside_ their profile, so where we `return render(request...)`, we can pass in context of the two `UserUpdateForm()` and `ProfileUpdateForm()`
> since these are forms we are passing in as context, we can display them as `forms|crispy` in our template.

**have forms already filled in with current info**: when we make a form, we sometimes would want the form to be filled in with the current user's information. this is easy to do and requires passing in an argument to that form (only passing in a model it expects). for example, in our `UserUpdateForm`, it can take an `instance` argument of another existing `User`. we want it to be our currently logged in user, we can give it an `instance = request.user`, which is the current user. the same goes for `Profile`, giving it `instance = instance.user.profile`.

**forms and images**: when using forms to update an image/store an image, make sure to add `enctype="multipart/form-data"` so the site knows to save the picture in the background. 

**<ins>Get Forms to Save Updated Content</ins>**  
because now our profile template has a form, we can make it work by setting the same conditional as the register template, having a `request.method == "POST"`. this is only called when the form is submitted, where new files and new data will be stored. this will have to be passed in as additional arguments into the `UserUpdateForm` and `ProfileUpdateForm`. 

**<ins>Resizing Images</ins>**  
when large images are uploaded, we want to resize them to a point where they don't take up too much room because on the website, there's no need for a super big photo. we can use this by accessing the `Pillow` extension that we installed from django. (`from PIL import Image`) we have to override the save method in our `models.py`, with a simple `def save(self):` function.  
this overwrites the existing save function:
```python 
# save function is already defined, we are overwriting it
def save(self, *args, **kwargs):
    super().save(*args, **kwargs ) # calls the first parent save function

    img = Image.open(self.image.path) # sets var img to the uploaded img

    if img.height > 300 or img.width > 300: # if too big, change to max 300 pixels
      output_size = (300, 300)
      img.thumbnail(output_size) # resizes the image to 300x300
      img.save(self.image.path) # resave and overwrite the large photo

```
## Class Based Views
there are two types of views, function based (what we've worked with so far) and class based views. class based views allows for more functionality as it is built inside django already:
1. `ListViews`: in YouTube, there's a link to see a _<ins>list</ins>_ of all your subscriptions to channels, which has the same functionality as a `ListView.
2. `DetailedViews`: if you click on any video in YouTube, you'll be brought to a page with more _<ins>detail</ins>_, with comments, a video description, etc.
3. `UpdateViews` and `DeleteViews`: same as _<ins>updating</ins>_ a video/blog or _<ins>deleting</ins>_ a video/blog. 

**<ins>Rewriting Home Template with Class Based Views</ins>**  
right now, our home template has a function based view where we are _<ins>listing</ins>_ posts. we can instead change it to a `ListView`, using the functionality and logic of django. we only have to specify a model, and in our case, we specify the `Post` model. 
> we have to import all the `Views` using `from django.views.generic import ListView`, etc.

because of django's name convention, it tries to search for a file in the form of: `[APP NAME].[MODEL NAME]_[TYPE OF VIEW].html`. currently, we link to `home.html`. also, we need to give our own variable name to the `Posts` being passed into the template, since django automatically gives it a name of `ObjectList`.  
total fixes:
- change `template_name` to whatever name our template was before, in our case, `blog/home.html`. 
- change `context_object_name = 'posts'`, which was the name of our passed in context from before
- set `ordering = ['-date_posted']`, to have our post order reverse chronologically. 
- when we change our urlpatterns to use `PostListView`, we have to set an `as_view` attribute to change the class based view into an actual view template. 

**<ins>Linking to each Post</ins>**  
we also want a detailed view, which means we can create a class for that as well. this is simple, as it only takes the `model` argument and everything else with django standard. after we import this to our `urls.py`, we will try to link to every available post. django has this available already, as we can give variables to path links. to do this, we can write our path variable like so:   `path('post/<int:pk>', PostDetailView.as_view(), name='post-detail')`
- since we want to display all of our `Posts`, we can have a `/post` to distinguish it from other links.
- we can visit posts using their primary key, or `pk`, and we specify to django that we expect an integer there. (make sure it is in `<>`)
- again, we must convert `PostDetailView` and add an `as_view()`.
- alter `context_object_name = 'post'`, going against django convention (orignally named `object`).

in our home page, we want to link every post to a "detailed view". to do this, we have to modify our href to include the `post-detail` and a `post-id` (which was our `pk` parameter that was passed in). 

**<ins>Creating New Posts</ins>**  
as with the other class views, we have to import `CreateView` to help us create new posts. there's an attribute we must give it, which specifies which elements of Post we want to modify, in our case, the title and content. when we add it to our `urlpatterns`, it follows the same rules as the other three. the template that is django default looks at is `post_form.html`. when we create that, we can still use `crispy_forms` to display the contents of our `Post` model.
> note: the creation of posts, validating of posts, and all the logic exhibited inside `views.py` (as in the user app), is all abstracted away by the class views we used. 

**overwrite save method**: the current save method, when saving a post, has no author attribute attached to it, so we must override the given `form_valid()` function. code is below: 
```python 
# override django's given form_valid()
def form_valid(self, form): # given paramters of itself (logged in user) and form (of creating new Post)
    form.instance.author = self.request.user # the new post's author is the user that's currently logged in
    return super().form_valid(form) # still, call django's given form_valid()
```
**linking after creating new posts**: after a post is created, we want to go to the detail page of a post. to link back we have to use a `reverse()` function, which returns the absolute url. we have to do this modification in our `models.py`, because that is where django looks when a new model gets created. we must add a function `get_absolute_url(self)` using the `reverse()` function. the parameters passed in are the name of the route (in our case `'post-detail'`, and arguments, `kwargs={'pk': self.pk})` 
> this is because `'post-detail'` expects an argument (named `pk`), and each `Post` entry has their own primary key value. 

**login required**: as seen before, we used `@login_required` in our `users/views.py` to make sure if we wanted to modify a profile we had to be logged in first. however, we can't apply decorators to class based views, but we can use a mixin that django provides for us. it's as simple as `from django.contrib.auth.mixins import LoginRequiredMixin` and adding it as an additional argument. 

**<ins>Updating Posts</ins>**  
same as before, we have to import the `UpdateView` class view. it will have almost the exact same functionality as the `PostCreateView()` function we had before, as we want affec the model `Post`, have the same fields able to be altered, and have the same `form_valid()` function (with the logged in user as the author). 

we have to update our `urlpatterns` to reflect this extra link, and it will have the same link as the `PostDetailView`, with an extra `/update/` after it. 
> note that we still need the `pk` because we want to know which post is being updated. 

**check for same author/user**: we only want the user that wrote a post to update it, so we have to use another mixin to check if the user is the actual author. this mixin is called `UserPassesTestMixin` and is passed as an extra parameter to `PostUpdateView()`. this allows us to have a `test_func()` that only grants user access if it returns `True`. 
```python
# test function must return true becuase of UserPassesTextMixin to work
def test_func(self):
    post = self.get_object() # built in django function that returns what object is currently being worked on (which post model)
    return self.request.user == post.author # is the author == the logged in user?
```
> `PostUpdateView` doesn't require a template because it uses the same one as `PostCreateView`.  

**<ins>Delete Post</ins>**  
our delete post will also be a class view from django, which we will inerit (`DeleteView`). we will also require a user to be logged in and pass a test, so we can use the same `Mixins` from `PostUpdateView()`. the test will be same and can be copied too. when adding to our `urlpatterns`, it has the same form as `PostUpdateView()`, and instead of `update`, it will be `delete`.

we do require a template asking for confirmation of deleting a post, which will be named `post_confirm_delete.html`.
> we will have a cancel button, linking back to the detail page if the user changes their mind. the href will be set to: `href="{% url 'post-detail' post.id %}`, since we want to go back to the `'post-detail'` page that takes in a `pk` paramter, (or our post's id since we have access to the object).

after deletion, django still needs to know where to redirect us afterwards. just like when creating a new post, we had to specify an absolute url, or in our case, a `success_url`. this can be added as a variable inside `PostDeleteView()` inside `views.py`.

**<ins>Putting it All Together</ins>**  
we are now able to create new posts, update, delete, and see details about our posts. now, we have to link everything together. because we only want logged in users to create posts, we have to add that to the part of our nav bar in `base.html` where the user is authenticated. also, we only want the user who created the post to update or delete it, and must write a conditional in `post_detail.html`.

## Quick Boostrap Classes  
`<div class="container">`: gives nice padding to whatever content is placed inside the div. for styling and spacing purposes. 
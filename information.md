## Tutorial to add new pages/links to our site
In order to create new links for our website, like `localhost:8000/blog` into our new website:  
- we have to create a function inside `blog/views.py` and link it to the urlpatterns inside `blog/urls.py`.
- we also have to update our urlpatterns inside our `/urls.py` in our main project directory in order for it to be passed onto our `blog/urls.py`.
- to set homepage, set the first argument of the `path` to `''`, and a corresponding function will automatically be executed to be the homepage.
- **blog/view.py** (function) --> **blog/urls.py** (update urlpatterns) --> **/urls.py** (update urlpatterns) 

**How it works:**  
1. when the computer reads any `string` after the `localhost:8000`, it passes this argument using `HttpResponse` from `django.http` to `/urls.py` in the main project directory.
2. it then scans the `urlpatterns` variable and tries to find a match with any of the links provided. if no match is found, a `404 ERROR` will be returned.
> if `/blog/about` was read in, it would scan for blog only, and advance from there. if `/` is found, the empty string is looked for (usually our main/homepage).
3. if there is a match, the rest of the `string` will be passed onto the corresponding function or a function will be executed. 
> if `/blog/about` was read in and `blog` was matched, the rest of the string (`/about`) would be passed onto the `/urls.py` in the `/blog` directory.
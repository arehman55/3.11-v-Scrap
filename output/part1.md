## Part 1: Django Notes

**Summary:** Let’s learn by example.

---

```python
$ python -m django --version
```

```python
$ django-admin startproject mysite djangotutorial
```

```python
$ python manage.py runserver
```

```python
$ python manage.py startapp polls
```

```python
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
```

```python
$ python manage.py runserver
```


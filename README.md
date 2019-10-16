# habr_proxy
Proxy server for habr.com that extends words of 6 length with symbol ™.

Can be used with any site, just change TARGET_SITE inside habr_proxy/settings.py

---

How to make everything work
1. Clone repository
2. Install dependencies (highly recomended to install them inside the virtual environment)
```
pip install -r requirements.txt
```
3. Run django server or use your own production config (uwsgi, nginx, gunicorn etc.)
```
python manage.py runserver
```

---

What it's currently doing?
* Replaces URLs to stay on your host while browsing target site.
* Adds symbol ™ after all words of 6 length on the page.

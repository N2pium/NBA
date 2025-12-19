# How to Deploy Your NBA Website

Your project is now fully configured for production deployment!

## 1. Prerequisites
- **GitHub Account**: Your code should be pushed to a GitHub repository.
- **Hosting Account**: We recommend **Railway** or **Render** for easiest deployment.

## 2. Deploying to Railway (Recommended)
1.  Go to [railway.app](https://railway.app/).
2.  Log in with GitHub.
3.  Click **"New Project"** -> **"Deploy from GitHub repo"**.
4.  Select your NBA repository.
5.  Railway will automatically detect the `Procfile` and `requirements.txt`.
6.  **Environment Variables**:
    - Go to the **Variables** tab.
    - Add the following:
        - `SECRET_KEY`: (Generate a long random string)
        - `DEBUG`: `False`
        - `ALLOWED_HOSTS`: `*` (or your specific domain)
        - `SECURE_SSL`: `True`
7.  Railway automatically provides a database (PostgreSQL) if you add it as a service, or you can use the built-in SQLite (not persistent across re-deploys, but easier). *Note: For persistent data, add a PostgreSQL plugin in Railway.*

## 3. Deploying to Render
1.  Go to [render.com](https://render.com/).
2.  Click **"New"** -> **"Web Service"**.
3.  Connect your GitHub repo.
4.  **Runtime**: Python 3.
5.  **Build Command**: `pip install -r requirements.txt && python website/manage.py collectstatic --noinput`
6.  **Start Command**: `gunicorn --chdir website website.wsgi:application`
7.  **Environment Variables**:
    - `PYTHON_VERSION`: `3.12.0`
    - `SECRET_KEY`: (Generate a long random string)
    - `WEB_CONCURRENCY`: `4`

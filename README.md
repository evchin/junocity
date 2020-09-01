# JunoCity
[See website.](http://junocity.com/)

## Overview
JunoCity was born as a platform where younger generations could ask questions, and seniors could tell their own stories and life lessons. The idea took root during the beginnings of COVID-19 in 2020, where JunoCity was intended to be utilized as a resource for people to ground themselves, and take in advice from the most experienced members of society, in one of the most tumultous times of the 21st century.

I developed the website using the Django Python framework, Postgres databases served through Amazon AWS, Git for damage control (lol), and Heroku for final deployment connected to GitHub. Languages used include HTML, CSS, SCSS/SASS, JavaScript, and Python.

## Features / How to use JunoCity
1. **What can I do here?**
JunoCity is a website where seniors and younger generations are encouraged to interact with each other, allowing those with more experience to share the lessons they have learned, and give advice to those with less experience. People of all ages are welcome to post questions or stories in communities called blocks, where each block represents a distinct aspect of life. Anyone can answer or comment on posts, and are also welcome to develop even deeper relationships through a private messaging inbox. We wish to give our senior citizens the ability to share the lessons and stories they have gained throughout the years, while providing value to those who need it.

2. **What are blocks?**
Blocks are forums that focus on distinct aspects of life (i.e. Financial Block, Relationships Block). Anyone is welcome to post in a particular block, but you can also choose to join a block, which will bring posts from that particular block directly to your homepage. Block populations are simply the number of people in that block. Junocity has 6 official blocks so far: Financial, Retirement, Health, Career, Life Lessons & Stories, and Relationships. We are planning to allow users to add their own blocks as our community grows.

3. **What are posts?**
Everyone with an account is permitted to post on Junocity. You are welcome to post questions, ask for advice, and tell stories through posts.

4. **What are neighbors?**
Neighbors can be your friends and/or people you enjoy seeing posts from. You and your neighbors put together are considered Your Block. This personal block of yours is your very own personally built community, and you'll be able to see all of your neighbors' posts on your homepage.

5. **What are bookmarks?**
Bookmark icons look like bookmarks. For each post, you can click on this icon and it will bookmark/save the post to your bookmarks list. Your Bookmarks can be found in your profile page, right beside the settings icon. There, you will be able to see all the posts you have saved.

## Running the Project
Running this project locally requires access to an AWS secret key. The settings.py file that is essential to any Django project is therefore not commited to the public repository due to the security of confidential information. Please contact me at evchin2@gmail.com for direct access to the settings.py file to run this project locally. Once given the settings.py file, add the file under the jc_project folder.

1. Install the [Anaconda CLI](https://www.anaconda.com/products/individual).
2. Clone this project locally.
3. Navigate to the junocity project folder on your machine.
4. Open the Anaconda CLI, and install Pipenv using `pip install pipenv`.
5. Install necessary dependencies using `pipenv install -r requirements.txt`.
6. Activate your environment by using `pipenv shell`.
7. Run the server by using `python manage.py runserver`.
7. Navgiate to given url of localhost.

## Dependencies
Comprehensive list with specified versions found in requirements.txt
* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* [Django](https://www.djangoproject.com/)
* [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
* [django-extensions](https://github.com/django-extensions/django-extensions)
* [django-notifications-hq](https://pypi.org/project/django-notifications-hq/)
* [django-postman](https://pypi.org/project/django-postman/)
* [django-recaptcha](https://pypi.org/project/django-recaptcha/)
* [django-sass-processor](https://pypi.org/project/django-sass-processor/0.2.6/)
* [django-storages](https://django-storages.readthedocs.io/en/latest/)
* [django-taggit](https://django-taggit.readthedocs.io/en/latest/)
* [gunicorn](https://docs.gunicorn.org/en/stable/)
* [libsass](https://sass-lang.com/libsass)
* [Pillow](https://pillow.readthedocs.io/en/stable/)
* [psycopg2](https://pypi.org/project/psycopg2/)
* [pusher](https://pypi.org/project/pusher/)
* [rcssmin](https://pypi.org/project/rcssmin/)
* [requests](https://requests.readthedocs.io/en/master/)
* [s3transfer](https://pypi.org/project/s3transfer/)
* [scss](https://sass-lang.com/)
* [sendgrid](https://github.com/sendgrid/sendgrid-python)
* [virtualenv](https://virtualenv.pypa.io/en/latest/)
* [whitenoise](http://whitenoise.evans.io/en/stable/)

# Project Title

Classimax webapp is completely based on python django framework. This is an initial release of the webapp. For further enhancement or feature addition please fork a branch and follow the instruction given below to test and add the feature.

## Getting Started

Please set up a dedicated python virtual environment for this django based prjoect.

Follow the instructions to set up the environment.
	
	1. Please install and set up python virtual-environment.
	2. Activate the env and install requirement.txt into it.

		 pip install -r requirements.txt

	3. Start the django server
		3.1 GO to the project directory
		3.2 Type commond

		    python manage.py runserver

	    For running on local server in DEBUG=False mode run command
 			
 			python manage.py runserver --insecure


		3.3 Make migrations to install all djnago apps.

			django-admin makemigrations/ python manage.p makemigrations

		3.4 Migrate all apps

			django-admin migrate/ python manage.py migrate

		3.5 Again start the server using command in 3.2


## Setting up django-stripe payment gateway

	1. Register on www.stripe.com 
	2. Go to doc for all setup
	3. Get STRIPE-SECRET-KEY and STRIPE-PUBLIC-KEY for both test and production.
	4. Place the keys in settings.py at appropriate lines in django root project folder


## Setting SMTP server
    
    **Go to settings.py and fill smtp details**

	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	EMAIL_HOST = '' # mail service smtp..for gmail use `smtp.gmail.com`
	EMAIL_HOST_USER = '' # email id or userId
	EMAIL_HOST_PASSWORD = '' #password
	EMAIL_PORT = 587
	EMAIL_USE_TLS = True
	DEFAULT_FROM_EMAIL = 'testing@example.com' # Sender email

### Prerequisites

	1. Python 3.6 or above.
	2. Django 3.0 or above.


 


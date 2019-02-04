# Collectly quick python backend challenge

# Challenge description

We are running the web application which stores and exposes Patients and their Payments.
The application must stay in sync with external users's system data and provide
some additional analytics on top of the data.

## Models

As a sample, basic SQLAlchemy models are provided in models.py file.
Feel free to extend and modify them, but do not delete existing fields.

**external_id** field must contain id of an object in external system, and is
unique in the external source. It is the only field guaranteed not to change.
All other fields in external source ***can change***, including payment amount!

#### Fameworks/ORMs

You can use flask/django or other framework of choice, just convert the models
by yourself.


## Required functionality

1. Implement web service which exposes methods
    * GET /patients?payment_min=10&payments_max=20
      - Returns list of patients with total amount of payments in supplied range (in
      this example between $10 and $20)
      - filters are optional

    * GET /payments?external_id=
      - Returns the list of payments, probably filtered by patient's external_id
      - filters are optional

2. Implement data sync
    Just for the sake of simplicity we assume all the data comes in one piece, which
    should be replicated in the database. If something is missing in the upload,
    it means object has been deleted in external system.

    * Option 1. POST /patients and POST /payments methods
    * Option 2. Import json files from the command line

3. Keep track of `created` and `updated` model fields.


## Sample data

Sample data is provided in patients.json and payments.json files.


## Evaluation criteria

* Code as you will code for a production use. You can omit some of the boring stuff
 if you leave the comment that it should be there.
 Make performance/reliability decisions as for production with 1000x more data/load.
* Challenge completion time is important, build the working version as fast as you can

## How to submit
* Clone the repo or start a new one. Do not fork it!
* Upload in public or private repository on github. In case of private, please share the access.
* Keep your commit history.


---

## Requirements

The basic system requirements are:

 - Python 3.x
 - Django>=2.1.5
 - database (see the django supported database engines here https://docs.djangoproject.com/en/2.1/ref/databases/)

## Local deployment for development

Clone the project:

```
$ git clone git@github.com:AndrewBurdyug/collectly-tz.git
```

Create a new virtual environment:

```
$ sudo apt-get install python python-dev python-virtualenv git
# mkdir ~/envs
$ virtualenv ~/envs/collectly-tz
```

Enable virtual env:

```
[buran@buran-pc collectly-tz] $ . ~/envs/collectly-tz/bin/activate
(collectly-tz) [buran@buran-pc collectly-tz]$ pip install -U setuptools pip

```

Install python requirements:

```
(collectly-tz) [buran@buran-pc collectly-tz]$ pip install -r requrements.txt
```

Run migrations:

```
(collectly-tz) [buran@buran-pc collectly-tz]$ cd paymentagg
(collectly-tz) [buran@buran-pc paymentagg]$ ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, payments, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying payments.0001_initial... OK
  Applying payments.0002_auto_20190202_1505... OK
  Applying sessions.0001_initial... OK
(collectly-tz) [buran@buran-pc paymentagg]$
```

Create superuser account (optional) if you want to use the back-office (/admin):

```
(collectly-tz) [buran@buran-pc paymentagg]$ ./manage.py createsuperuser
Username (leave blank to use 'buran'): admin
Email address: admin@ex.com
Password:
Password (again):
Superuser created successfully.
(collectly-tz) [buran@buran-pc paymentagg]$
```

Run local development server:

```
(collectly-tz) [buran@buran-pc paymentagg]$ ./manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
February 03, 2019 - 09:18:25
Django version 2.1.5, using settings 'paymentagg.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Extra validation rules

Currently we add just one extra rules: date of birth patient cannot be less or equal 1900 year and cannot be from future.

## Production deployment

For production deployment I suggest to use uWSGI + Nginx and manage the application service
by systemD. You can see config examples here: https://github.com/AndrewBurdyug/django-folder

## Console data loading

To load data from json file you can use this command:

```
(collectly-tz) [buran@buran-pc paymentagg]$ ./manage.py load_data --help
usage: manage.py load_data [-h] --input-file INPUT_FILE --model-name
                           {patient,payment} [--version] [-v {0,1,2,3}]
                           [--settings SETTINGS] [--pythonpath PYTHONPATH]
                           [--traceback] [--no-color]

Load data from json file.

optional arguments:
  -h, --help            show this help message and exit
  --input-file INPUT_FILE
  --model-name {patient,payment}
                        choose the model (available: patient, payment)
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
(collectly-tz) [buran@buran-pc paymentagg]$
```

Examples:

```
(collectly-tz) [buran@buran-pc paymentagg]$ ./manage.py load_data --input-file ../patients.json --model-name patient
Failed load: {'first_name': 'Rick', 'last_name': 'Deckard', 'middle_name': None, 'date_of_birth': datetime.date(2094, 2, 1)}, errors: {'external_id':
['Patient with this External id already exists.']}
Failed load: {'first_name': 'Pris', 'last_name': 'Stratton', 'middle_name': None, 'date_of_birth': datetime.date(2093, 12, 20)}, errors: {'external_id':
['Patient with this External id already exists.']}
Successfully load: {'first_name': 'Roy', 'last_name': 'Batti', 'middle_name': None, 'date_of_birth': datetime.date(2093, 6, 12), 'external_id': '8'}
Failed load: {'first_name': 'Eldon', 'last_name': 'Tyrell', 'middle_name': None, 'date_of_birth': datetime.date(2056, 4, 1)}, errors: {'external_id':
['Patient with this External id already exists.']}
(collectly-tz) [buran@buran-pc paymentagg]$ ./manage.py load_data --input-file ../payments.json --model-name payment
Failed load: {'amount': Decimal('4.46'), 'patient': <Patient: Rick Deckard <extID:5>>}, errors: {'external_id': ['Payment with this External id already exists.']}
Failed load: {'amount': Decimal('5.66'), 'patient': <Patient: Rick Deckard <extID:5>>}, errors: {'external_id': ['Payment with this External id already exists.']}
Failed load: {'amount': Decimal('7.1'), 'patient': <Patient: Rick Deckard <extID:5>>}, errors: {'external_id': ['Payment with this External id already exists.']}
Failed load: {'amount': Decimal('23.32'), 'external_id': '601'}, errors: {'patient': ['Select a valid choice. That choice is not one of the available choices.']}
Failed load: {'amount': Decimal('2.29'), 'external_id': '602'}, errors: {'patient': ['Select a valid choice. That choice is not one of the available choices.']}
Successfully load: {'amount': Decimal('9.29'), 'patient': <Patient: Roy Batti <extID:8>>, 'external_id': '602'}
(collectly-tz) [buran@buran-pc paymentagg]$
```

## API errors reporting

For example this sample set for the "POST /patients" endpoint:

```
[{
  "firstName": "Aaron",
  "lastName": "Achard",
  "dateOfBirth": "2083-02-01",
  "externalId": "52"
}, {
  "firstName": "Rick",
  "lastName": "Deckard",
  "dateOfBirth": "1983-02-01",
  "externalId": "52"
}, {
  "firstName": "Pris",
  "lastName": "Stratton",
  "dateOfBirth": "1993-12-20",
  "externalId": "4"
}, {
  "firstName": "Roy",
  "lastName": "Batti",
  "dateOfBirth": "1993-06-12",
  "externalId": "8"
}, {
  "firstName": "Eldon",
  "lastName": "Tyrell",
  "dateOfBirth": "1956-04-01",
  "externalId": "15"
}]
```

will cause such response with errors:

```
[
    {
        "status": "fail",
        "data": {
            "first_name": "Aaron",
            "last_name": "Achard",
            "middle_name": null,
            "external_id": "52"
        },
        "errors": {
            "date_of_birth": [
                "Date of birth cannot be in future"
            ]
        }
    },
    {
        "status": "success",
        "data": {
            "first_name": "Rick",
            "last_name": "Deckard",
            "middle_name": null,
            "date_of_birth": "1983-02-01",
            "external_id": "52"
        }
    },
    {
        "status": "success",
        "data": {
            "first_name": "Pris",
            "last_name": "Stratton",
            "middle_name": null,
            "date_of_birth": "1993-12-20",
            "external_id": "4"
        }
    },
    {
        "status": "success",
        "data": {
            "first_name": "Roy",
            "last_name": "Batti",
            "middle_name": null,
            "date_of_birth": "1993-06-12",
            "external_id": "8"
        }
    },
    {
        "status": "success",
        "data": {
            "first_name": "Eldon",
            "last_name": "Tyrell",
            "middle_name": null,
            "date_of_birth": "1956-04-01",
            "external_id": "15"
        }
    }
]
```

And this one for "POST /payments":

```
[{
  "amount": 4.46,
  "patientId": "5",
  "externalId": "501"
}, {
  "amount": 5.66,
  "patientId": "5",
  "externalId": "502"
}, {
  "amount": 7.10,
  "patientId": "5",
  "externalId": "503"
},{
  "amount": 23.32,
  "patientId": "6",
  "externalId": "601"
}, {
  "amount": 2.29,
  "patientId": "6",
  "externalId": "602"
}, {
  "amount": 9.29,
  "patientId": "8",
  "externalId": "602"
}]
```

will cause such response with errors (only 1 item has been saved successfully):

```
[
    {
        "status": "fail",
        "data": {
            "amount": "4.46",
            "external_id": "501"
        },
        "errors": {
            "patient": [
                "Select a valid choice. That choice is not one of the available choices."
            ]
        }
    },
    {
        "status": "fail",
        "data": {
            "amount": "5.66",
            "external_id": "502"
        },
        "errors": {
            "patient": [
                "Select a valid choice. That choice is not one of the available choices."
            ]
        }
    },
    {
        "status": "fail",
        "data": {
            "amount": "7.1",
            "external_id": "503"
        },
        "errors": {
            "patient": [
                "Select a valid choice. That choice is not one of the available choices."
            ]
        }
    },
    {
        "status": "fail",
        "data": {
            "amount": "23.32",
            "external_id": "601"
        },
        "errors": {
            "patient": [
                "Select a valid choice. That choice is not one of the available choices."
            ]
        }
    },
    {
        "status": "fail",
        "data": {
            "amount": "2.29",
            "external_id": "602"
        },
        "errors": {
            "patient": [
                "Select a valid choice. That choice is not one of the available choices."
            ]
        }
    },
    {
        "status": "success",
        "data": {
            "amount": "9.29",
            "patient": {
                "id": 3,
                "lastName": "Batti",
                "firstName": "Roy",
                "dateOfBirth": "1993-06-12",
                "externalId": "8"
            },
            "external_id": "602"
        }
    }
]
```

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

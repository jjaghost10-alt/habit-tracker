## Setup (for graders / professor)

After cloning the repository, please run:

```bash
python3 manage.py migrate
python3 manage.py loaddata books/fixtures/books.json
python3 manage.py runserver

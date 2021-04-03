populate:
	python manage.py populate

clean:
	find project/ todo/ | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf

clean_db:
	python -c "import os; os.remove('db.sqlite3')"

clean_all:
	make clean
	make clean_db
	python -c "import shutil; shutil.rmtree('todo/migrations')"

all_migrations:
	python manage.py makemigrations
	python manage.py makemigrations todo
	python manage.py migrate

reset_migrations:
	make clean_all
	make all_migrations
	make populate

install_dependencies:
	pipenv --python 3.9
	pipenv install --dev
	pipenv shell

run:
	python manage.py runserver 0.0.0.0:9000

reset_run:
	make reset_migrations
	make run
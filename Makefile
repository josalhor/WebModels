create_superuser:
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@g.com', 'TodoPassword')" | python manage.py shell

clean:
	find project/ todo/ | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf

clean_db:
	rm -f db.sqlite3

clean_all:
	make clean
	make clean_db
	rm -rf todo/migrations

all_migrations:
	python manage.py makemigrations
	python manage.py makemigrations todo
	python manage.py migrate

reset_migrations:
	make clean_all
	make all_migrations
	make create_superuser

install_dependencies:
	pipenv --python 3.9
	pipenv install --dev
	pipenv shell

run:
	python manage.py runserver 0.0.0.0:9000
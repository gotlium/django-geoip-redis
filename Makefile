test:
	django-admin.py test --settings=geoip.test_settings geoip
coverage:
	export DJANGO_SETTINGS_MODULE=geoip.test_settings && \
	coverage run --branch --source=geoip `which django-admin.py` test geoip && \
	coverage report --omit="geoip/test*,geoip/migrations/*,geoip/management/*"
sphinx:
	cd docs && sphinx-build -b html -d .build/doctrees . .build/html
pep8:
	flake8 --exclude=migrations geoip
open_docs:
	open docs/.build/html/index.html
run:
	cd demo && ./manage.py syncdb && ./manage.py migrate && ./manage.py runserver_plus --print-sql --threaded

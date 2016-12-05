# gtfs-server
Our restful gtfs server based on django

# setup instructions
Assuming an installation of Ubuntu 16.04

sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade

1.  Install core softwate: python, postgres, postgis, nginx, git

    - sudo apt-get install -y binutils libproj-dev gdal-bin python-dev python-virtualenv python-pip postgresql postgresql-server-dev-all postgresql-client postgis postgresql-9.5-postgis-2.2 postgresql-9.5-postgis-scripts libncurses5-dev nginx-full git

2.  Install the gtfs application under /srv/projects/gtfs

    - mkdir -p /srv/projects/gtfs
    - cd /srv/projects/gtfs
    - git clone <url> .
    - virtualenv env
    - source ./env/bin/activate

    - pip install -r requirements.txt
    - deactivate

3. Create the gtsf database in postgres

    - sudo su - postgres
    - psql -c "CREATE USER gtfs WITH PASSWORD 'gtfs'"
    - psql -c "CREATE DATABASE gtfs"
    - psql -c "GRANT ALL PRIVILEGES ON DATABASE gtfs TO gtfs"

    - exit

4. Set up UWSGI

    - sudo mkdir -p /etc/uwsgi/sites
    - sudo cp config/uwsgi/uwsgi.ini /etc/uwsgi/sites

5. Set up Upstart
    - sudo cp config/upstart/uwsgi.conf /etc/init

6. Set up nginx
    - sudo service nginx stop
    - sudo rm /etc/nginx/sites-enabled/default
    - sudo cp config/nginx/nginx.conf /etc/nginx/sites-available
    - sudo ln -s /etc/nginx/sites-available/nginx.conf /etc/sites-enabled

    - sudo service uwsgi restart
    - sudo service nginx restart

7. Initialize the database and set up an admin user
    - python gtfsserver/manage.py collectstatic
    - python gtfsserver/manage.py syncdb --noinput
    - python gtfsserver/manage.py migrate
    - python gtfsserver/manage.py createsuperuser




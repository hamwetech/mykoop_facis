# FTF

FTF API (A MyKoop variant)

## Developer guide

Local enviroment setup

- Use (Python 2.7)[https://www.python.org/download/releases/2.7/] and Mysql 5.6

### local develop

Run `git clone https://github.com/hamweorg/ftf.git`

### How to run the app locally

- Run `virtualenv --python=C:\Python27\python.exe venv` (point to your python27 executable accordingly)
- Run `venv\Scripts\activate` if on windows (activate the virtual environment accordingly otherwise)
- Run `pip install mysqlclient`. If that fails, download an unofficial binary (here)[https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient] then run `pip install <path-to-whl-file>`. Windows may ask you to install Microsoft Visual C++ 9.0, try (this)[https://web.archive.org/web/20190720195601/http://www.microsoft.com/en-us/download/confirmation.aspx?id=44266]
- Or run(this)[https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04] for Linux and `pip install pymysql`.
- Run `pip install -r requirements.txt`
- Run `mysql -u root -p`
- Run `create database ftf;`
- Run `python manage.py makemigrations`
- Run `python manage.py migrate`
- Run `python manage.py createsuperuser`
- Run `python manage.py help` to view available commands
- Run `python manage.py runserver` to start the app

### Contributing

- Create your feature branch: git checkout -b `my-new-feature`
- Commit your changes: git commit -am `Add some feature`
- Push to the branch: git push origin `my-new-feature`
- Submit a pull request

### Extra

You could run `find . | grep -E "(\__pycache__|\migrations|\.pytest_cache)" | xargs rm -rf` to remove unnecessary files (BUT EXCLUDE MIGRATIONS).
Or replace `find` with `bash`.
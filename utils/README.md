# Utils
### How to add anime + fake-users to the db:
#### 1. Use a virtual environment
Ensure you are in a virutal environment. If not:
* Create a virtual environment in Windows:
```sh
python -m venv venv_name
```
* Activate virtual environment\
```.  /venv_name/bin/activate ``` (Linux) \
``` ./venv_name/Scripts/activate ``` (Windows)

#### 2. In root directory(*project-himawari*) run:
```sh
pip install -e .
```
#### 3. Run populate-db.py with argparse settings

Arguments:
```sh
  -a, --anime           Number of anime rows to add to DB
  -u, --user            Number of fake user-rows to add to DB
  -d, --db              Will delete current DB and create new one
```

Example of how to run from /utils:
```sh
python populate-db.py -a 500 -u 100 -d
```

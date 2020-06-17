# Project-Himawari

### How to run kaguya:
```sh
python run.py
```

### How to initialize database migrations:

 **If 'migrations' directory doesn't exist...**

1. Initialize environment variable in project directory:

    WINDOWS:
    ```sh
    $ set FLASK_APP=run.py
    ```
    
    LINUX:
    ```sh
    $ export FLASK_APP=run.py
    ```

2.  Run the following to create `/migrations` directory:
```sh
$ flask db init
```

### How to use database migrations:
1. Initialize environment variable like above.

2. Generate migration script. (Records database transformations).
    ```sh
    $ flask db migrate -m "[OPTIONAL_MIGRATION_MESSAGE]"
    ```

3. Apply new changes to database:
    ```sh
    $ flask db upgrade
    ```
   
4. Undo the last migration:
    ```sh
    $ flask db downgrade
    ```
    After downgrading, **DELETE** the migration script if the newest migration isn't as expected.
   
#### When to use database migrations:
When there are structural changes to the database schema (e.g. added/removed columns or tables or relationships).

### How to use setup.py
Will add instructions later

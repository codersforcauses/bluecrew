# django-vue-template

Django + Vue Template: Standardised CFC Tech Stack

## Get started

### Using the dev container (Recommended)

0. Activate the dev container in VSCode
1. In the `client` folder, run `npm run dev` to start the frontend on port at `localhost:3000`
2. In the `server` folder, run `python manage.py runserver` to start the server at `localhost:8000`

> Note:
> For manual setup see end of README

## Server

### Create and run migrations

If the models are updated, be sure to create a migration:

```bash
python manage.py makemigrations # create migration
python manage.py migrate # apply migrations
```

### Nuke the DB

If you run into migration conflicts that you can't be bothered to fix, run `nuke.sh` to clear your database. Then, run migrations again.

## Other

### Update Dependencies

You can run `npm install` and `poetry install` in the respective `client` and `server` folders to install the newest dependencies.

### Editing Docker stuff

If you modify anything in the `docker` folder, you need to add the `--build` flag or Docker won't give you the latest changes.

### Changing env vars

Edit the `.env` file in the respective directory (client or server).

### Manual Setup (for if you aren't using the devcontainer)

Setup environment variables:
1. In the `client` folder, copy the content from `.env.example` into a new file called `.env`
2. In the `server` folder, copy the content from `.env.example` into a new file called `.env`

Run the client:
1. In the `client` folder, run `npm i`
2. Run `npm run dev`

Run the database:
1. In the project root, run `docker compose up`

Run the server:
1. In the `server` folder, run `poetry install`.
2. Start the poetry shell by running `poetry shell`
3. Run migrations using `python manage.py migrate`
4. Start the server using `python manage.py runserver`
Note: To exit the poetry shell after stopping the server, use the command `exit`

# ASAP Demo App

## Architecture

I kept it pretty simple. Decoupled routes, domain logic, and database logic.
Tests only cover the domain logic, with mocks for the database layer. Caching is
implemented in the database layer; domain doesn't have to know a thing about it.

Suggested read order:

* `members.py` and `test_members.py`: to see the core domain logic
* `routes.py`: to see how the domain logic is used
* `db.py`: to see the underpinnings of the domain logic
* `templates/*.html`: ...honestly not very interesting at all

## Running

Standard Docker Compose setup. Check out the code, then:

```
docker compose up --build
```
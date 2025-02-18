# src/main.py - Main Application Script

[Linked Table of Contents](#linked-table-of-contents)

## Linked Table of Contents

* [1. Overview](#1-overview)
* [2. Module Imports](#2-module-imports)
* [3. `main()` Function](#3-main-function)
    * [3.1 Database Initialization](#31-database-initialization)
    * [3.2 Server Startup](#32-server-startup)


## 1. Overview

This script serves as the entry point for the application.  It initializes the database and then starts the Uvicorn ASGI server to run the FastAPI application.

## 2. Module Imports

The script begins by importing necessary modules:

| Module             | Path             | Description                                      |
|----------------------|-------------------|--------------------------------------------------|
| `uvicorn`           | standard library | ASGI server for running the application.        |
| `app`               | `src.api.api`    | FastAPI application instance (relative import). |
| `init_db`           | `src.database.database` | Function to initialize the database (relative import). |


## 3. `main()` Function

The `main()` function orchestrates the application startup.

```python
def main():
    # Inizializza il database
    init_db()

    # Avvia il server
    uvicorn.run(
        app,  # percorso relativo al modulo
        host="0.0.0.0",
        port=8000,
        reload=True  # abilita hot reload in development
    )
```

### 3.1 Database Initialization

The line `init_db()` calls a function (located in `src/database/database.py`) responsible for setting up the database connection and potentially performing other initialization tasks such as creating tables or loading initial data.  The implementation details of `init_db()` are documented separately in `src/database/database.py`.


### 3.2 Server Startup

The `uvicorn.run()` function starts the Uvicorn server.  The arguments passed are:

* `app`:  The FastAPI application instance to be served.
* `host="0.0.0.0"`:  The host IP address to bind to.  `0.0.0.0` means all available interfaces.
* `port=8000`: The port number the server will listen on.
* `reload=True`: Enables hot reloading during development.  Changes to the code will automatically restart the server without manual intervention. This is useful for rapid development and testing.


The `main()` function is only executed when the script is run directly (not imported as a module):

```python
if __name__ == "__main__":
    main()
```

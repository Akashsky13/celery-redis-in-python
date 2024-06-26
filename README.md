# Celery with Redis in Python

## Setup Instructions

1. **Edit Configuration:**

    - Open `tasks.py`.
    - Replace the email and password placeholders with your own email and password.

    ```python
    # tasks.py
    YOUR EMAIL ID = 'exapmle@gmail.com'
    PASSWORD = 'your_password'
    ```

    - Open `library.db` and update the email there as well to match your email for testing purposes.

2. **Run Docker:**

    Ensure you have Docker installed on your laptop. If not, download and install Docker from [here](https://www.docker.com/products/docker-desktop).

    - Build and start the Docker containers:

    ```sh
    docker-compose up --build
    ```

## Screenshot

![Celery Redis Setup](https://github.com/Akashsky13/celery-redis-in-python/blob/main/Screenshot%202024-06-26%20125615.png)

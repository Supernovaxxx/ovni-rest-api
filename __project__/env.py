"""
Project environment management.
Configure application expected env variables' type and default values,
intermediating their consumption and improving this handling.
See https://django-environ.readthedocs.io/en/latest/index.html.
"""

import environ


# Define expected env variables, its casting and default value
# See https://django-environ.readthedocs.io/en/latest/tips.html.
env = environ.Env(
    ENV_FILE=(str, ".env.example"),
    HOST=(str, "0.0.0.0"),
    PORT=(int, 8000),
    WORKERS=(int, None),
    THREADS=(int, None),
    RELOAD=(bool, False),
    SECRET_KEY=(str, None),
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["*"]),
    CSRF_TRUSTED_ORIGINS=(list, ["http://*", "https://*"]),
    CORS_ALLOWED_ORIGINS=(
        list,
        [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
    ),
    STATIC_DIR=(str, "static"),
)

# Manage chosen .env file consumption.
env.read_env(
    env("ENV_FILE"),
    # overwrite=True,
)

# Extra options
# env.prefix = 'DJANGO_'
# env.escape_proxy = True

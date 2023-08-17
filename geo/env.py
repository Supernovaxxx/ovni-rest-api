"""
App environment management.
Configure application expected env variables' type and default values,
intermediating their consumption and improving this handling.
See https://django-environ.readthedocs.io/en/latest/index.html.
"""

import environ
from environ import ImproperlyConfigured


# Define expected env variables, its casting and default value
# See https://django-environ.readthedocs.io/en/latest/tips.html.
env = environ.Env(
    ENV_FILE=(str, ".env.example"),
    GOOGLE_MAPS_API_KEY=(str, None),
)

# Manage chosen .env file consumption.
env.read_env(
    env("ENV_FILE"),
    # overwrite=True,
)

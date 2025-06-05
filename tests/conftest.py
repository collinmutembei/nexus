import os
import django
import pytest
from django.conf import settings
from django.core.management import call_command


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nexus.settings")
    # Set mock OIDC and SECRET_KEY values for tests
    os.environ.setdefault("OIDC_CLIENT_ID", "test-client-id")
    os.environ.setdefault("OIDC_CLIENT_SECRET", "test-client-secret")
    os.environ.setdefault(
        "OIDC_PROVIDER_DISCOVERY_URI",
        "http://localhost/realms/testing/.well-known/openid-configuration",
    )
    os.environ.setdefault("SECRET_KEY", "test-secret-key")
    os.environ.setdefault("AFRICASTALKING_USERNAME", "testuser")
    os.environ.setdefault("AFRICASTALKING_API_KEY", "testkey")
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
    # Add testserver to allowed hosts for test client
    settings.ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]
    django.setup()
    # Apply migrations and create cache table for tests
    call_command("migrate", run_syncdb=True, verbosity=0)
    call_command("createcachetable", verbosity=0)

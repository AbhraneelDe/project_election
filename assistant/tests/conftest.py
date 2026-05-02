import pytest
from django.conf import settings

@pytest.fixture(autouse=True)
def use_dummy_static_storage(settings):
    """Avoid WhiteNoise manifest errors during tests."""
    settings.STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    # Also ensure whitenoise middleware doesn't interfere with simple tests if not needed
    if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
        settings.MIDDLEWARE = [m for m in settings.MIDDLEWARE if m != 'whitenoise.middleware.WhiteNoiseMiddleware']

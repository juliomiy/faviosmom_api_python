# /instance/config.py

import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    WOOCOMMERCE_KEY = "ck_07255729fa6f3226ec93dbf0715f43c802679da9"
    WOOCOMMERCE_SECRET = "cs_ad44500a974ab6f3d268a0ac235f11193a352aa4"
    WOOCOMMERCE_URL = "http://faviosmom.com"
    WOOCOMMERCE_VERSION = "wc/v1"

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
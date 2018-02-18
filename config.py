class Config:
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = "ayyyyyy"
    STRIPE_SECRET_KEY = "tdwopadjwaodija"
    STRIPE_PUBLISHABLE_KEY = "adoiorsifjoijoaji"
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SESSION_PERMANENT = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

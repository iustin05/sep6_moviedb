import os
import urllib


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(Config):
    params = urllib.parse.quote_plus("Driver={ODBC Driver 18 for SQL Server};"
                                     "Server=tcp:sep6moviedb.database.windows.net,1433;"
                                     "Database=sep6_movie;"
                                     "Uid=sep6user;"
                                     "Pwd=rYvvuh-7gomki-tyxhot;"
                                     "Encrypt=yes;"
                                     "TrustServerCertificate=no;"
                                     "Connection Timeout=30;")

    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    AZURE_DATABASE_URI = os.environ.get('AZURE_DATABASE_URI')
    
HOSTNAME = "docker0:ip"
PORT = "3306"
DATABASE = "g13"
USERNAME = "username"
PASSWORD = "password"
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# sqlalchemy configure
SQLALCHEMY_DATABASE_URI = DB_URI

MAIL_SERVER = "server"
MAIL_PORT = 465
MAIL_USE_TSL = False
MAIL_USE_SSL = True
MAIL_DEBUG = False
MAIL_USERNAME = "username"
MAIL_PASSWORD = "password"
MAIL_DEFAULT_SENDER = "sender"


export FLASK_DEBUG=1
export FLASK_APP="application"
export FLASK_SQLALCHEMY_DATABASE_URI="postgresql://login:password@localhost:5432/kitchen_dev"
export FLASK_SQLALCHEMY_TRACK_MODIFICATIONS=0
# export FLASK_MAIL_SERVER = ""
# export FLASK_MAIL_PORT = ""
# export FLASK_MAIL_USERNAME = ""
# export FLASK_MAIL_DEFAULT_SENDER = ""
# export FLASK_MAIL_PASSWORD = ""

flask run -p 5201

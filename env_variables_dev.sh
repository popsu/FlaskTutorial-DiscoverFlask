# If using virtualenvwrapper add the lines below to $VIRTUAL_ENV/bin/postactivate file
export APP_SETTINGS='config.DevelopmentConfig'
export DATABASE_URL='postgresql:///discover_flask_dev'
export FLASK_APP="run.py"
export FLASK_DEBUG=1

# this file is executed first and its set using command -> $env:FLASK_APP = "run.py"
# change app to development server -> $env:FLASK_ENV = "development" 
# activate debugger -> set FLASK_DEBUG= 1 
# command to run the app -> python -m flask run
from gen_app.templates import app

if __name__ == "__main__":
  app.run()
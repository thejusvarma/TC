# this file is executed first and its set using command -> $env:FLASK_APP="run.py"
# change app to development server -> $env:FLASK_ENV="development" 
# activate debugger -> set FLASK_DEBUG=1 
# command to run the app -> python -m flask run
# bcrypt.generate_password_hash('password').decode('utf-8')
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt()
# user1 = User(username='thejus', email='thejusvarma11@gmail.com', password='$2b$12$8fE7qxlg03389WG5NBaQJeQYB3WmTtoB7Da6UW1D4nEWTdxWyoNBW')
from gen_app import app
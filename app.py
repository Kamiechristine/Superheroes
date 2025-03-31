from flask import Flask
from flask_migrate import Migrate
from routes import setup_routes  
from models import db  
from config import Config  

app = Flask(__name__)  
app.config.from_object(Config)  
db.init_app(app)  

# Set up migrations
migrate = Migrate(app, db)

# Set up routes  
setup_routes(app)  

if __name__ == '__main__':
    app.run(debug=True)

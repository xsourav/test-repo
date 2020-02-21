from test-repo.app import app
from test-repo.db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
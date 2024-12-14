from app import create_app, db
from app.models import users

app = create_app()

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

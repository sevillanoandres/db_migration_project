from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://apichallengeadmin:Oscar1984$@srvapichallenge.database.windows.net/API_Challenge_DB?driver=ODBC+Driver+18+for+SQL+Server'  # or any other SQL database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

from database import db

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(100), nullable=False)


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.Date, nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable= True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=True)


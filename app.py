from flask import Flask, request, jsonify
from sqlalchemy import func
from sqlalchemy.sql import case
from models import Department, Job, Employee
from database import db, init_db
import pandas as pd

app = Flask(__name__)
init_db(app)


@app.route('/metrics/above_mean_hired', methods=['GET'])
def above_mean_hired():
    total_hired = db.session.query(
        Employee.department_id, func.count(Employee.id).label('hired')
    ).filter(func.strftime('%Y', Employee.datetime) == '2021').group_by(Employee.department_id).subquery()

    mean_hired = db.session.query(func.avg(total_hired.c.hired)).scalar()

    results = db.session.query(
        Department.id, Department.name.label('department'), total_hired.c.hired
    ).join(total_hired, Department.id == total_hired.c.department_id).filter(total_hired.c.hired > mean_hired).order_by(total_hired.c.hired.desc()).all()

    data = [{"id": row.id, "department": row.department, "hired": row.hired} for row in results]

    return jsonify(data)

@app.route('/metrics/hired_per_quarter', methods=['GET'])
def hired_per_quarter():
    q1 = func.sum(case((func.strftime('%m', Employee.datetime).between('01', '03'), 1), else_=0)).label('Q1')
    q2 = func.sum(case((func.strftime('%m', Employee.datetime).between('04', '06'), 1), else_=0)).label('Q2')
    q3 = func.sum(case((func.strftime('%m', Employee.datetime).between('07', '09'), 1), else_=0)).label('Q3')
    q4 = func.sum(case((func.strftime('%m', Employee.datetime).between('10', '12'), 1), else_=0)).label('Q4')

    results = db.session.query(
        Department.name.label('department'),
        Job.job.label('job'),
        q1,
        q2,
        q3,
        q4
    ).join(Department, Employee.department_id == Department.id).join(Job, Employee.job_id == Job.id).filter(
        func.strftime('%Y', Employee.datetime) == '2021'
    ).group_by(Department.name, Job.job).order_by(Department.name, Job.job).all()

    data = [{"department": row.department, "job": row.job, "Q1": row.Q1, "Q2": row.Q2, "Q3": row.Q3, "Q4": row.Q4} for row in results]

    return jsonify(data)

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        df = pd.read_csv(file)
        table_name = request.args.get('table')
        if table_name == 'departments':
            df.to_sql('departments', con=db.engine, if_exists='replace', index=False)
        elif table_name == 'jobs':
            df.to_sql('jobs', con=db.engine, if_exists='replace', index=False)
        elif table_name == 'employees':
            df.to_sql('employees', con=db.engine, if_exists='replace', index=False)
        else:
            return 'Invalid table name', 400

        return 'File successfully uploaded', 200

@app.route('/insert_batch', methods=['POST'])
def insert_batch():
    data = request.json
    table_name = request.args.get('table')
    if len(data) > 1000:
        return 'Batch size limit exceeded', 400

    if table_name == 'departments':
        db.session.bulk_insert_mappings(Department, data)
    elif table_name == 'jobs':
        db.session.bulk_insert_mappings(Job, data)
    elif table_name == 'employees':
        db.session.bulk_insert_mappings(Employee, data)
    else:
        return 'Invalid table name', 400

    db.session.commit()
    return 'Batch successfully inserted', 200

if __name__ == '__main__':
    app.run(debug=True)


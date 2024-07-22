from flask import Flask, request, jsonify
from models import Department, Job, Employee
from database import db, init_db
import pandas as pd

app = Flask(__name__)
init_db(app)

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
            df.to_sql('departments', con=db.engine, if_exists='append', index=False)
        elif table_name == 'jobs':
            df.to_sql('jobs', con=db.engine, if_exists='append', index=False)
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


# a vibe coding
# python 3.8.0
# version 1.0

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import pandas as pd
import json
import sqlite3
import numpy as np
from io import StringIO
import analysis_ as an

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
CORS(app)
# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'json', 'sql'}
data_= None
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    global data_
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    print(file.filename)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the file based on its extension
        file_extension = filename.rsplit('.', 1)[1].lower()
        try:
            if file_extension == 'csv':
                df = pd.read_csv(file_path)
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(file_path)
            elif file_extension == 'json':
                df = pd.read_json(file_path)
            elif file_extension == 'sql':
                # For SQL files, we'll just return the content
                with open(file_path, 'r') as f:
                    sql_content = f.read()
                return jsonify({
                    'message': 'SQL file uploaded successfully',
                    'content': sql_content
                })
            #print(df.head())
            # Check if the DataFrame is empty
            data_ = df

            if len(df) > 200:  
                df = df.head(200)
            

            
            # Convert DataFrame to JSON
            result = {
                'columns': df.columns.tolist(),
                'data': df.to_dict(orient='records'),
                'row_count': len(df)
            }
            
            
            return jsonify(result)
            
        except Exception as e:
            
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404
@app.route('/execute-python', methods=['POST'])
def execute_python():
    global data_
    try:
        data = request.json
        code = data.get('code')
        input_data = data_
        
        if not code or not input_data:
            return jsonify({'error': 'Missing code or data'}), 400

        # Convert input data to DataFrame
        df = pd.DataFrame(input_data['data'])
        
        # Create a safe execution environment
        local_vars = {
            'df': df,
            'pd': pd,
            'np': np,
            'result': None
        }
        
        # Execute the code in a controlled environment
        exec(code, {'__builtins__': {}}, local_vars)
        
        # Get the result
        result_df = local_vars.get('result', df)
        
        # Convert result back to JSON format
        result = {
            'columns': result_df.columns.tolist(),
            'data': result_df.to_dict(orient='records'),
            'row_count': len(result_df)
        }
        
        return jsonify(result)
        
    except Exception as e:
        jsonify({'error': str(e)}), 500
@app.route('/analysis/<operation>', methods=['POST'])
def analysis(operation):
    global data_
    analysis_obj = None
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        if data_ is None:
            return jsonify({'error': 'No dataset loaded. Please upload a file first.'}), 400

        # Create analysis object with the correct data format
        analysis_obj = an.Analysis(data_)

        if operation == 'filter':
            filter_value = data.get('filterValue')
            column_name = data.get('columnName')
            
    
            if not filter_value or not column_name:
                return jsonify({'error': 'Missing filter value or column name'}), 400
                
            filtered_df = analysis_obj.filter_data(column_name, filter_value)
            
            if filtered_df is None or filtered_df.empty:
                return jsonify({'error': 'No data matches the filter criteria'}), 400
                
            if len(filtered_df) > 200:  
                filtered_df = filtered_df.head(200)
                
            return jsonify({
                'columns': filtered_df.columns.tolist(),
                'data': filtered_df.to_dict(orient='records'),
                'row_count': len(filtered_df)
            })
        
        elif operation == 'sort':
            column_name = data.get('columnName')
            direction = data.get('direction')
            if not column_name:
                return jsonify({'error': 'Missing column name'}), 400
            
            if direction not in ['asc', 'desc']:
                return jsonify({'error': 'Invalid sort direction. Use "asc" or "desc".'}), 400
            if direction == 'asc':
                sorted_df = analysis_obj.acending(column_name)
            else:
                sorted_df = analysis_obj.descending(column_name)
            
            if len(sorted_df) > 200:  
                sorted_df = sorted_df.head(200)
            return jsonify({
                'columns': sorted_df.columns.tolist(),
                'data': sorted_df.to_dict(orient='records'),
                'row_count': len(sorted_df)
            })
        
        elif operation == 'delete':
            column_name = data.get('columnName')
            if not column_name:
                return jsonify({'error': 'Missing column name'}), 400
            deleted_df = analysis_obj.drop_column(column_name)
            data_ = deleted_df
            if len(deleted_df) > 200:  
                deleted_df = deleted_df.head(200)
            return jsonify({
                'columns': deleted_df.columns.tolist(),
                'data': deleted_df.to_dict(orient='records'),
                'row_count': len(deleted_df)
            })
        
        
        elif operation == 'describe':
            column_name = data.get('columnName')
            if not column_name:
                return jsonify({'error': 'Missing column name'}), 400
            describe_ = analysis_obj.describe_column(column_name)
            
            return jsonify({
                'describe': describe_
            })
        


    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the analysis object
        if analysis_obj:
            analysis_obj.cleanup()



if __name__ == '__main__':
    app.run(debug=True, port=5000)

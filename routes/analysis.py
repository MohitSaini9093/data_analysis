from flask import Flask, request, jsonify, Blueprint,current_app, send_file
import os
from flask_cors import CORS
from utils import get_user_dataframe
import pandas as pd


analysis = Blueprint('analysis', __name__)

def fetch_data():
    df = get_user_dataframe()
    if df is None:
        return jsonify({'error': 'No dataset found. Please upload first.'}), 400

    try:
        # Example: send full summary statistics
        summary = df.describe(include='all').to_dict()
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        

@analysis.route('/advanced_analysis', methods=['POST'])
def advanced_analysis():
    pass

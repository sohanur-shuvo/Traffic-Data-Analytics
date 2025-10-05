from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_excel_data(data):
    """Process Excel data similar to the original Streamlit logic"""
    try:
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        if df.empty:
            return {"error": "Excel file appears to be empty"}
        
        # Debug: Print column info
        print(f"DataFrame shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"First few rows:")
        print(df.head())
        print(f"Data types:")
        print(df.dtypes)
        
        # Use column C (index 2) as the time column if available
        if len(df.columns) > 2:
            time_col = df.columns[2]
            # Convert to datetime with error handling
            try:
                df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
                
                # Extract date and time components
                df['Date'] = df[time_col].dt.date
                df['Time'] = df[time_col].dt.time
                df['Hour'] = df[time_col].dt.hour
            except:
                # If datetime conversion fails, try to find date/time columns
                date_cols = [col for col in df.columns if any(name in col.lower() for name in ['date', 'day'])]
                time_cols = [col for col in df.columns if any(name in col.lower() for name in ['time', 'hour'])]
                
                if date_cols and time_cols:
                    try:
                        df['Date'] = pd.to_datetime(df[date_cols[0]], errors='coerce').dt.date
                        df['Time'] = pd.to_datetime(df[time_cols[0]], errors='coerce').dt.time
                        df['Hour'] = pd.to_datetime(df[time_cols[0]], errors='coerce').dt.hour
                    except:
                        # Fallback: create dummy date/time columns
                        df['Date'] = '2024-01-01'
                        df['Time'] = '08:00:00'
                        df['Hour'] = 8
                else:
                    # Fallback: create dummy date/time columns
                    df['Date'] = '2024-01-01'
                    df['Time'] = '08:00:00'
                    df['Hour'] = 8
        else:
            # Try to find date/time columns with common names
            date_cols = [col for col in df.columns if any(name in col.lower() for name in ['date', 'day'])]
            time_cols = [col for col in df.columns if any(name in col.lower() for name in ['time', 'hour'])]
            
            if date_cols and time_cols:
                try:
                    df['Date'] = pd.to_datetime(df[date_cols[0]], errors='coerce').dt.date
                    df['Time'] = pd.to_datetime(df[time_cols[0]], errors='coerce').dt.time
                    df['Hour'] = pd.to_datetime(df[time_cols[0]], errors='coerce').dt.hour
                except:
                    # Fallback: create dummy date/time columns
                    df['Date'] = '2024-01-01'
                    df['Time'] = '08:00:00'
                    df['Hour'] = 8
            else:
                # Fallback: create dummy date/time columns
                df['Date'] = '2024-01-01'
                df['Time'] = '08:00:00'
                df['Hour'] = 8
        
        # Filter for business hours (8am to 8pm)
        df_filtered = df[(df['Hour'] >= 8) & (df['Hour'] < 20)]
        
        # Convert to JSON-serializable format
        processed_data = []
        for _, row in df_filtered.iterrows():
            processed_row = {}
            for col in df_filtered.columns:
                value = row[col]
                # Convert non-serializable types
                if isinstance(value, pd.Timestamp):
                    processed_row[col] = value.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(value, datetime):
                    processed_row[col] = value.strftime('%Y-%m-%d')
                elif isinstance(value, (np.integer, np.floating)):
                    processed_row[col] = int(float(value)) if np.isfinite(value) else None
                elif pd.isna(value):
                    processed_row[col] = None
                else:
                    processed_row[col] = str(value)
            processed_data.append(processed_row)
        
        # Extract available dates
        available_dates = [str(date) for date in df_filtered['Date'].unique() if pd.notna(date)]
        available_dates.sort()
        
        return {
            "success": True,
            "data": processed_data,
            "available_dates": available_dates,
            "total_records": len(processed_data),
            "filtered_records": len(processed_data),
            "original_records": len(df),
            "preview_data": processed_data[:10] if len(processed_data) > 10 else processed_data  # Show first 10 rows
        }
        
    except Exception as e:
        return {"error": f"Error processing data: {str(e)}"}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Traffic Analytics API is running"})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and process Excel file"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Read Excel file
            df = pd.read_excel(filepath, engine='openpyxl')
            
            # Convert to JSON for processing
            json_data = df.to_dict('records')
            
            # Process the data
            result = process_excel_data(json_data)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({"error": f"Error processing file: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file type. Please upload a .xlsx file"}), 400

@app.route('/api/compare', methods=['POST'])
def compare_dates():
    """Compare traffic data between two dates - simplified version"""
    try:
        data = request.json
        
        if not data or 'excel_data' not in data or 'date1' not in data or 'date2' not in data:
            return jsonify({"error": "Missing required data"}), 400

        # Get the original Excel data
        excel_data = data.get('excel_data', [])
        date1 = data['date1']
        date2 = data['date2']
        show_highlighted_only = data.get('show_highlighted_only', False)
        min_ratio_threshold = data.get('min_ratio_threshold', 4)
        
        print(f"Received min_ratio_threshold: {min_ratio_threshold} (type: {type(min_ratio_threshold)})")
        print(f"Received show_highlighted_only: {show_highlighted_only}")
        print(f"Full request data keys: {list(data.keys())}")
        
        if not excel_data:
            return jsonify({"error": "No Excel data provided"}), 400
        
        # Convert to DataFrame
        df = pd.DataFrame(excel_data)
        
        if df.empty:
            return jsonify({"error": "No data in Excel file"}), 400
        
        print(f"\n=== Comparing {date1} vs {date2} ===")
        print(f"Total rows in DataFrame: {len(df)}")
        print(f"Columns: {df.columns.tolist()}")
        
        # Filter data by date
        # Try different column name variations
        date_col = None
        for col in ['Date', 'date', 'DATE']:
            if col in df.columns:
                date_col = col
                break
        
        if date_col is None:
            return jsonify({"error": "No Date column found in data"}), 400
        
        # Convert date column to string for comparison
        df[date_col] = df[date_col].astype(str)
        
        # Filter for each date
        date1_data = df[df[date_col] == date1].copy()
        date2_data = df[df[date_col] == date2].copy()
        
        print(f"Rows for {date1}: {len(date1_data)}")
        print(f"Rows for {date2}: {len(date2_data)}")
        
        if len(date1_data) == 0:
            return jsonify({"error": f"No data found for date: {date1}"}), 400
        if len(date2_data) == 0:
            return jsonify({"error": f"No data found for date: {date2}"}), 400
        
        # Find Customer In/Out columns
        customer_in_col = None
        customer_out_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if 'customer' in col_lower and 'in' in col_lower:
                customer_in_col = col
            elif 'customer' in col_lower and 'out' in col_lower:
                customer_out_col = col
        
        if customer_in_col is None or customer_out_col is None:
            # Fallback to column indices if names not found
            try:
                customer_in_col = df.columns[4]  # Column E
                customer_out_col = df.columns[5]  # Column F
                print(f"Using column indices - In: {customer_in_col}, Out: {customer_out_col}")
            except:
                return jsonify({"error": "Cannot find Customer In/Out columns"}), 400
        else:
            print(f"Found columns - In: {customer_in_col}, Out: {customer_out_col}")
        
        # Find Time column
        time_col = None
        for col in ['Time', 'time', 'TIME', 'Time Slot']:
            if col in df.columns:
                time_col = col
                break
        
        if time_col is None:
            return jsonify({"error": "No Time column found in data"}), 400
        
        # Convert time to string for matching
        date1_data[time_col] = date1_data[time_col].astype(str)
        date2_data[time_col] = date2_data[time_col].astype(str)
        
        # Generate 15-minute time slots from 8:00 AM to 8:00 PM
        time_slots = []
        for hour in range(8, 20):  # 8 AM to 8 PM
            for minute in [0, 15, 30, 45]:
                time_str = f"{hour:02d}:{minute:02d}:00"
                time_slots.append(time_str)
        
        print(f"Generated {len(time_slots)} time slots")
        
        # Create comparison results
        comparison_results = []
        
        for time_str in time_slots:
            # Format time slot for display
            hour = int(time_str[:2])
            minute = int(time_str[3:5])
            end_minute = minute + 15
            end_hour = hour
            if end_minute >= 60:
                end_hour += 1
                end_minute -= 60
            
            ampm = "pm" if end_hour >= 12 else "am"
            display_time = f"{hour:02d}:{minute:02d}-{end_hour:02d}:{end_minute:02d}{ampm}"
            
            # Find matching rows for this time slot (match by hour:minute)
            time_pattern = time_str[:5]  # Just HH:MM part
            
            date1_rows = date1_data[date1_data[time_col].str.contains(time_pattern, na=False)]
            date2_rows = date2_data[date2_data[time_col].str.contains(time_pattern, na=False)]
            
            # Get values (use first match if multiple)
            if len(date1_rows) > 0:
                date1_in = int(float(date1_rows.iloc[0][customer_in_col]) if pd.notna(date1_rows.iloc[0][customer_in_col]) else 0)
                date1_out = int(float(date1_rows.iloc[0][customer_out_col]) if pd.notna(date1_rows.iloc[0][customer_out_col]) else 0)
            else:
                date1_in = date1_out = 0
            
            if len(date2_rows) > 0:
                date2_in = int(float(date2_rows.iloc[0][customer_in_col]) if pd.notna(date2_rows.iloc[0][customer_in_col]) else 0)
                date2_out = int(float(date2_rows.iloc[0][customer_out_col]) if pd.notna(date2_rows.iloc[0][customer_out_col]) else 0)
            else:
                date2_in = date2_out = 0
            
            diff_in = date2_in - date1_in
            diff_out = date2_out - date1_out
            
            # Calculate ratios exactly like app.py
            # Ratio = max(value1, value2) / min(value1, value2)
            ratio_in = max(date1_in, date2_in) / min(date1_in, date2_in) if min(date1_in, date2_in) > 0 else 999999
            ratio_out = max(date1_out, date2_out) / min(date1_out, date2_out) if min(date1_out, date2_out) > 0 else 999999
            
            # Determine if should be highlighted - exactly like app.py
            should_highlight = (date1_in == 0 or date2_in == 0 or 
                             date1_out == 0 or date2_out == 0 or
                             ratio_in >= min_ratio_threshold or ratio_out >= min_ratio_threshold)
            
            comparison_results.append({
                "timeSlot": display_time,
                "date1Value": date1_in,
                "date2Value": date2_in,
                "difference": diff_in,
                "date1OutValue": date1_out,
                "date2OutValue": date2_out,
                "differenceOut": diff_out,
                "ratioIn": ratio_in,
                "ratioOut": ratio_out,
                "should_highlight": should_highlight
            })
        
        # Filter for highlighted only if requested
        if show_highlighted_only:
            comparison_results = [r for r in comparison_results if r["should_highlight"]]
        
        # Calculate summary totals
        date1_total_in = sum(r["date1Value"] for r in comparison_results)
        date1_total_out = sum(r["date1OutValue"] for r in comparison_results)
        date2_total_in = sum(r["date2Value"] for r in comparison_results)
        date2_total_out = sum(r["date2OutValue"] for r in comparison_results)
        
        summary = {
            "date1": {
                "date": date1,
                "customerIn": date1_total_in,
                "customerOut": date1_total_out
            },
            "date2": {
                "date": date2,
                "customerIn": date2_total_in,
                "customerOut": date2_total_out
            },
            "differences": {
                "customerIn": date2_total_in - date1_total_in,
                "customerOut": date2_total_out - date1_total_out
            }
        }
        
        return jsonify({
            "success": True,
            "comparison_data": comparison_results,
            "summary": summary,
            "total_slots": len(comparison_results)
        })
        
    except Exception as e:
        return jsonify({"error": f"Error comparing dates: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

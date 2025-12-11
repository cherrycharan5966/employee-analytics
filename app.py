from flask import Flask, render_template, jsonify, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global dataframe to store employee data
df = None

# Load the employee data
def load_employee_data():
    """Load employee data from CSV file"""
    global df
    if os.path.exists('employee_analysis_output.csv'):
        df = pd.read_csv('employee_analysis_output.csv')
    elif os.path.exists('employees.csv'):
        # Fallback to original data if processed file doesn't exist
        df = pd.read_csv('employees.csv')
        # Add the computed columns if they don't exist
        if 'performance_level' not in df.columns:
            df['performance_level'] = pd.cut(df['performance_score'], 
                                           bins=[0, 69, 84, 100], 
                                           labels=['LOW', 'MEDIUM', 'HIGH'],
                                           include_lowest=True)
        if 'promotion_eligible' not in df.columns:
            df['promotion_eligible'] = df.apply(lambda row: 'YES' if row['years_exp'] >= 4 and row['performance_score'] >= 80 else 'NO', axis=1)
    else:
        # Create empty dataframe with required columns if no files exist
        df = pd.DataFrame(columns=['emp_id', 'name', 'department', 'salary', 'years_exp', 'performance_score'])

# Process uploaded file
def process_uploaded_data(file_path):
    """Process uploaded CSV file and add computed columns"""
    global df
    try:
        df = pd.read_csv(file_path)
        # Ensure numeric columns are properly typed
        numeric_columns = ['salary', 'years_exp', 'performance_score']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Add computed columns if they don't exist
        if 'performance_level' not in df.columns:
            df['performance_level'] = pd.cut(df['performance_score'], 
                                           bins=[0, 69, 84, 100], 
                                           labels=['LOW', 'MEDIUM', 'HIGH'],
                                           include_lowest=True)
        if 'promotion_eligible' not in df.columns:
            df['promotion_eligible'] = df.apply(lambda row: 'YES' if row['years_exp'] >= 4 and row['performance_score'] >= 80 else 'NO', axis=1)
        return True
    except Exception as e:
        print(f"Error processing uploaded file: {e}")
        return False

# Initialize data on startup
load_employee_data()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload"""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename.endswith('.csv'):
            try:
                # Save file temporarily
                filepath = os.path.join('uploads', file.filename)
                os.makedirs('uploads', exist_ok=True)
                file.save(filepath)
                
                # Process the file
                if process_uploaded_data(filepath):
                    # Remove temporary file
                    os.remove(filepath)
                    return jsonify({'success': 'File uploaded and processed successfully'}), 200
                else:
                    # Remove temporary file
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    return jsonify({'error': 'Error processing file'}), 500
            except Exception as e:
                # Clean up temporary file if it exists
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': f'Error saving file: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Invalid file format. Please upload a CSV file.'}), 400
    
    return render_template('upload.html')

@app.route('/api/employees')
def get_employees():
    """API endpoint to get all employees"""
    global df
    if df is not None and not df.empty:
        return jsonify(df.to_dict('records'))
    else:
        # Return empty list if no data
        return jsonify([])

@app.route('/api/salary-analytics')
def salary_analytics():
    """API endpoint for salary analytics"""
    global df
    if df is None or df.empty:
        return jsonify({})
    
    try:
        # Average salary by department
        avg_salary = df.groupby('department')['salary'].mean().round(2).to_dict()
        
        # Salary ranges by department
        salary_ranges = df.groupby('department')['salary'].agg(['min', 'max']).to_dict()
        
        return jsonify({
            'avg_salary': avg_salary,
            'salary_ranges': {
                'min': salary_ranges['min'],
                'max': salary_ranges['max']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance-analytics')
def performance_analytics():
    """API endpoint for performance analytics"""
    global df
    if df is None or df.empty:
        return jsonify({})
    
    try:
        # Performance level counts
        perf_counts = df['performance_level'].value_counts().to_dict()
        
        # Top 3 performers
        top_performers = df.nlargest(3, 'performance_score')[['name', 'department', 'performance_score']].to_dict('records')
        
        # Average performance by department
        avg_performance = df.groupby('department')['performance_score'].mean().round(2).to_dict()
        
        return jsonify({
            'performance_counts': perf_counts,
            'top_performers': top_performers,
            'avg_performance_by_dept': avg_performance
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/promotion-analytics')
def promotion_analytics():
    """API endpoint for promotion analytics"""
    global df
    if df is None or df.empty:
        return jsonify({})
    
    try:
        # Promotion eligible counts
        promo_counts = df['promotion_eligible'].value_counts().to_dict()
        
        # Eligible employees
        eligible_employees = df[df['promotion_eligible'] == 'YES'][['name', 'department', 'years_exp', 'performance_score']].to_dict('records')
        
        return jsonify({
            'promotion_counts': promo_counts,
            'eligible_employees': eligible_employees
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/summary')
def summary():
    """API endpoint for summary statistics"""
    global df
    if df is None or df.empty:
        return jsonify({})
    
    try:
        # Employee count by department
        emp_count_dept = df['department'].value_counts().to_dict()
        
        # Performance level counts
        perf_level_counts = df['performance_level'].value_counts().to_dict()
        
        # Total salary expense by department
        total_salary_dept = df.groupby('department')['salary'].sum().to_dict()
        
        # Correlation between salary and performance
        correlation = df['salary'].corr(df['performance_score'])
        
        return jsonify({
            'employee_count_by_dept': emp_count_dept,
            'performance_level_counts': perf_level_counts,
            'total_salary_by_dept': total_salary_dept,
            'salary_performance_correlation': round(correlation, 2) if not pd.isna(correlation) else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
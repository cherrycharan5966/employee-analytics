#!/usr/bin/env python3
"""
Standalone Employee Salary & Performance Analytics
--------------------------------------------------
This script demonstrates the same analytics as the PySpark version but using pure Python with pandas.
It's useful for understanding the logic before setting up the full PySpark environment.

Features:
1. Data Loading: Reads employee data from CSV file
2. Data Cleaning: Converts data types and handles missing values
3. Salary Analytics: Calculates average, highest, and lowest salaries by department
4. Performance Analytics: Categorizes employees by performance level and identifies top performers
5. Promotion Eligibility: Identifies employees eligible for promotion based on experience and performance
6. Insights: Analyzes correlation between salary and performance
7. Summary Reports: Generates counts and expenses by department and performance level
8. Output: Saves processed data to CSV format
"""

import pandas as pd
import numpy as np

def load_data():
    """Load employee data from CSV file"""
    # In a real scenario, we would read from employees.csv
    # For demonstration, we'll create the DataFrame directly
    data = {
        'emp_id': ['E101', 'E102', 'E103', 'E104', 'E105'],
        'name': ['Ramesh', 'Sneha', 'Amit', 'Leela', 'Karan'],
        'department': ['Sales', 'HR', 'IT', 'Sales', 'IT'],
        'salary': [45000, 52000, 62000, 39000, 58000],
        'years_exp': [3, 5, 7, 2, 4],
        'performance_score': [78, 85, 92, 70, 81]
    }
    return pd.DataFrame(data)

def clean_data(df):
    """Clean and convert data types"""
    df['salary'] = pd.to_numeric(df['salary'], errors='coerce')
    df['years_exp'] = pd.to_numeric(df['years_exp'], errors='coerce')
    df['performance_score'] = pd.to_numeric(df['performance_score'], errors='coerce')
    
    # Replace any missing values with 0
    df = df.fillna(0)
    
    return df

def salary_analytics(df):
    """Perform salary analytics by department"""
    print("\n=== Salary Analytics ===")
    
    # Calculate average salary per department
    avg_salary = df.groupby('department')['salary'].mean().reset_index()
    avg_salary.columns = ['department', 'avg_salary']
    print("Average salary per department:")
    print(avg_salary.to_string(index=False))
    
    # Calculate highest and lowest salary in each department
    salary_range = df.groupby('department')['salary'].agg(['max', 'min']).reset_index()
    salary_range.columns = ['department', 'highest_salary', 'lowest_salary']
    print("\nHighest and lowest salary in each department:")
    print(salary_range.to_string(index=False))
    
    return avg_salary, salary_range

def performance_analytics(df):
    """Perform performance analytics"""
    print("\n=== Performance Analytics ===")
    
    # Add performance level column
    df['performance_level'] = pd.cut(df['performance_score'], 
                                    bins=[0, 69, 84, 100], 
                                    labels=['LOW', 'MEDIUM', 'HIGH'],
                                    include_lowest=True)
    
    print("DataFrame with performance level:")
    print(df[['name', 'department', 'performance_score', 'performance_level']].to_string(index=False))
    
    # Find top 3 employees by performance score
    top_performers = df.nlargest(3, 'performance_score')[['name', 'department', 'performance_score']]
    print("\nTop 3 employees by performance score:")
    print(top_performers.to_string(index=False))
    
    return df

def promotion_eligibility(df):
    """Determine promotion eligibility"""
    print("\n=== Promotion Eligibility ===")
    
    # Add promotion eligibility column
    df['promotion_eligible'] = np.where((df['years_exp'] >= 4) & (df['performance_score'] >= 80), 'YES', 'NO')
    
    print("DataFrame with promotion eligibility:")
    print(df[['name', 'years_exp', 'performance_score', 'promotion_eligible']].to_string(index=False))
    
    # Display eligible employees
    eligible = df[df['promotion_eligible'] == 'YES'][['name', 'department', 'years_exp', 'performance_score']]
    print("\nEmployees eligible for promotion:")
    print(eligible.to_string(index=False))
    
    return df

def salary_vs_performance_insights(df):
    """Analyze salary vs performance correlation"""
    print("\n=== Salary vs Performance Insights ===")
    
    # Average performance score per department
    avg_performance = df.groupby('department')['performance_score'].mean().reset_index()
    avg_performance.columns = ['department', 'avg_performance_score']
    print("Average performance score per department:")
    print(avg_performance.to_string(index=False))
    
    # Correlation between salary and performance score
    correlation = df['salary'].corr(df['performance_score'])
    print(f"\nCorrelation between salary and performance score: {correlation:.2f}")
    
    return avg_performance, correlation

def summary_reports(df):
    """Generate summary reports"""
    print("\n=== Final Summary Outputs ===")
    
    # Count of employees per department
    emp_count_dept = df['department'].value_counts().reset_index()
    emp_count_dept.columns = ['department', 'employee_count']
    print("Count of employees per department:")
    print(emp_count_dept.to_string(index=False))
    
    # Count of employees in each performance level
    emp_count_perf = df['performance_level'].value_counts().reset_index()
    emp_count_perf.columns = ['performance_level', 'employee_count']
    print("\nCount of employees in each performance level:")
    print(emp_count_perf.to_string(index=False))
    
    # Total salary expense per department
    total_salary_dept = df.groupby('department')['salary'].sum().reset_index()
    total_salary_dept.columns = ['department', 'total_salary_expense']
    print("\nTotal salary expense per department:")
    print(total_salary_dept.to_string(index=False))
    
    return emp_count_dept, emp_count_perf, total_salary_dept

def save_results(df):
    """Save processed data to CSV"""
    print("\n=== Saving Processed Data ===")
    df.to_csv('employee_analysis_output.csv', index=False)
    print("Processed DataFrame saved as 'employee_analysis_output.csv'")

def main():
    """Main function to run all analytics"""
    print("Employee Salary & Performance Analytics")
    print("=" * 50)
    
    # 1. Load data
    print("\n1. Loading employee data...")
    df = load_data()
    print("\nOriginal DataFrame:")
    print(df.to_string(index=False))
    
    # 2. Clean data
    print("\n2. Cleaning data...")
    df = clean_data(df)
    print("\nCleaned DataFrame:")
    print(df.to_string(index=False))
    
    # 3. Salary analytics
    print("\n3. Performing salary analytics...")
    avg_salary, salary_range = salary_analytics(df)
    
    # 4. Performance analytics
    print("\n4. Performing performance analytics...")
    df = performance_analytics(df)
    
    # 5. Promotion eligibility
    print("\n5. Checking promotion eligibility...")
    df = promotion_eligibility(df)
    
    # 6. Salary vs performance insights
    print("\n6. Analyzing salary vs performance...")
    avg_performance, correlation = salary_vs_performance_insights(df)
    
    # 7. Summary reports
    print("\n7. Generating summary reports...")
    emp_count_dept, emp_count_perf, total_salary_dept = summary_reports(df)
    
    # 8. Save results
    print("\n8. Saving results...")
    save_results(df)
    
    # 9. Final output preview
    print("\n=== Final Processed DataFrame Preview ===")
    print(df.to_string(index=False))
    
    print("\nAnalytics completed successfully!")

if __name__ == "__main__":
    main()
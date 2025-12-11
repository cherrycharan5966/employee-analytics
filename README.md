# Employee Salary & Performance Analytics with PySpark and Flask

This project demonstrates how to perform employee analytics using Apache Spark (PySpark) and visualize the results with a Flask web application.

## Prerequisites

1. **Java 8 or higher** - Required for running Spark
2. **Python 3.6 or higher**
3. **Required Python packages** (see [requirements.txt](requirements.txt))

## Setup Instructions

### 1. Install Java
- Download and install Java JDK from [Oracle](https://www.oracle.com/java/technologies/downloads/) or [OpenJDK](https://openjdk.org/)
- Set the `JAVA_HOME` environment variable to point to your Java installation directory

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Analysis (Optional)
If you want to regenerate the analytics data:
```bash
python employee_analytics.py
```

Or for a standalone version without Spark:
```bash
python employee_analytics_standalone.py
```

### 4. Run the Flask Web Application
```bash
python app.py
```

Or simply double-click [run_app.bat](run_app.bat) on Windows.

The application will be available at http://localhost:5000

## Project Structure

- [employees.csv](employees.csv): Sample employee data
- [employee_analytics.py](employee_analytics.py): Main PySpark script implementing all analytics
- [employee_analytics_standalone.py](employee_analytics_standalone.py): Standalone Python version using pandas
- [employee_analysis_output.csv](employee_analysis_output.csv): Processed data with analytics results
- [app.py](app.py): Flask web application
- [templates/index.html](templates/index.html): Main dashboard UI
- [static/styles.css](static/styles.css): Custom CSS styles
- [requirements.txt](requirements.txt): Python dependencies
- [run_app.bat](run_app.bat): Windows batch file to start the application
- [README.md](README.md): This file

## Features

### Data Analytics
1. **Data Loading**: Reads employee data from CSV file
2. **Data Cleaning**: Converts data types and handles missing values
3. **Salary Analytics**: Calculates average, highest, and lowest salaries by department
4. **Performance Analytics**: Categorizes employees by performance level and identifies top performers
5. **Promotion Eligibility**: Identifies employees eligible for promotion based on experience and performance
6. **Insights**: Analyzes correlation between salary and performance
7. **Summary Reports**: Generates counts and expenses by department and performance level

### Web Dashboard
1. **Interactive Charts**: Visualize data with Chart.js
2. **Tabbed Interface**: Organize analytics into logical sections
3. **Responsive Design**: Works on desktop and mobile devices
4. **Real-time Data**: Fetches data through RESTful API endpoints

## API Endpoints

- `GET /` - Main dashboard page
- `GET /api/employees` - All employee data
- `GET /api/salary-analytics` - Salary analytics data
- `GET /api/performance-analytics` - Performance analytics data
- `GET /api/promotion-analytics` - Promotion analytics data
- `GET /api/summary` - Summary statistics

## Dataset

The project uses the following sample data in [employees.csv](employees.csv):

```
emp_id,name,department,salary,years_exp,performance_score
E101,Ramesh,Sales,45000,3,78
E102,Sneha,HR,52000,5,85
E103,Amit,IT,62000,7,92
E104,Leela,Sales,39000,2,70
E105,Karan,IT,58000,4,81
```

## Output

The application generates:
- Interactive web dashboard at http://localhost:5000
- Processed data in [employee_analysis_output.csv](employee_analysis_output.csv)

## Troubleshooting

1. **Java not found**: Ensure Java is installed and JAVA_HOME is set
2. **Port already in use**: Change the port in [app.py](app.py)
3. **Missing dependencies**: Run `pip install -r requirements.txt`

## License

This project is open source and available under the MIT License.
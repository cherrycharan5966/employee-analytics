# Employee Salary & Performance Analytics - Results

## Project Overview

This project demonstrates employee analytics using two approaches:
1. **PySpark version** (`employee_analytics.py`) - For big data processing
2. **Standalone Python version** (`employee_analytics_standalone.py`) - For learning and small datasets

## Dataset

We analyzed the following employee data:

| emp_id | name   | department | salary | years_exp | performance_score |
|--------|--------|------------|--------|-----------|-------------------|
| E101   | Ramesh | Sales      | 45000  | 3         | 78                |
| E102   | Sneha  | HR         | 52000  | 5         | 85                |
| E103   | Amit   | IT         | 62000  | 7         | 92                |
| E104   | Leela  | Sales      | 39000  | 2         | 70                |
| E105   | Karan  | IT         | 58000  | 4         | 81                |

## Key Analytics Results

### Salary Analytics
- **Average salary by department:**
  - HR: ₹52,000
  - IT: ₹60,000
  - Sales: ₹42,000
  
- **Salary ranges:**
  - HR: ₹52,000 (both highest and lowest)
  - IT: ₹62,000 (highest) to ₹58,000 (lowest)
  - Sales: ₹45,000 (highest) to ₹39,000 (lowest)

### Performance Analytics
- **Performance levels:**
  - HIGH (≥85): 2 employees (Sneha, Amit)
  - MEDIUM (70-84): 3 employees (Ramesh, Leela, Karan)
  - LOW (<70): 0 employees
  
- **Top 3 performers:**
  1. Amit (IT): 92
  2. Sneha (HR): 85
  3. Karan (IT): 81

### Promotion Eligibility
- **Eligibility criteria:** Years of experience ≥ 4 AND performance score ≥ 80
- **Eligible employees:**
  - Sneha (HR): 5 years, score 85
  - Amit (IT): 7 years, score 92
  - Karan (IT): 4 years, score 81

### Insights
- **Correlation:** Strong positive correlation (0.90) between salary and performance score
- **Department performance averages:**
  - IT: 86.5
  - HR: 85.0
  - Sales: 74.0
- **Employee distribution:**
  - Sales: 2 employees
  - IT: 2 employees
  - HR: 1 employee
- **Total salary expenses:**
  - IT: ₹120,000
  - Sales: ₹84,000
  - HR: ₹52,000

## Output Files

1. `employees.csv` - Original dataset
2. `employee_analysis_output.csv` - Processed data with added columns:
   - `performance_level` - Categorized performance scores
   - `promotion_eligible` - Promotion eligibility status

## How to Run

### For Learning/Small Datasets
```bash
python employee_analytics_standalone.py
```

### For Big Data Processing (Requires Java)
1. Install Java 8 or higher
2. Set JAVA_HOME environment variable
3. Install PySpark: `pip install pyspark`
4. Run: `python employee_analytics.py`

## Conclusion

The analysis reveals strong correlations between performance and compensation, with IT department showing both highest salaries and performance scores. Three employees are eligible for promotion based on experience and performance criteria.
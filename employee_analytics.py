#!/usr/bin/env python3
"""
Employee Salary & Performance Analytics with PySpark
--------------------------------------------------
This script demonstrates how to perform employee analytics using Apache Spark (PySpark).

Features:
1. Data Loading: Reads employee data from CSV file
2. Data Cleaning: Converts data types and handles missing values
3. Salary Analytics: Calculates average, highest, and lowest salaries by department
4. Performance Analytics: Categorizes employees by performance level and identifies top performers
5. Promotion Eligibility: Identifies employees eligible for promotion based on experience and performance
6. Insights: Analyzes correlation between salary and performance
7. Summary Reports: Generates counts and expenses by department and performance level
8. Output: Saves processed data to CSV format

Prerequisites:
- Java 8 or higher (required for Spark)
- Python 3.6+
- PySpark library

To install PySpark: pip install pyspark
"""

try:
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, when, avg, max, min, count, sum, corr
    from pyspark.sql.types import IntegerType
    
    # Check if Java is available
    import subprocess
    try:
        subprocess.run(["java", "-version"], check=True, capture_output=True)
        JAVA_AVAILABLE = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        JAVA_AVAILABLE = False
    
    if not JAVA_AVAILABLE:
        print("=" * 60)
        print("WARNING: Java is not installed or not in PATH")
        print("PySpark requires Java 8 or higher to run.")
        print("Please install Java and set JAVA_HOME environment variable.")
        print("Skipping PySpark execution...")
        print("=" * 60)
        
        # Show what the script would do
        print("\nThis script would perform the following analytics:")
        print("1. Load employee data from employees.csv")
        print("2. Clean and convert data types")
        print("3. Calculate salary statistics by department")
        print("4. Categorize employees by performance level")
        print("5. Identify top performers")
        print("6. Determine promotion eligibility")
        print("7. Analyze correlation between salary and performance")
        print("8. Generate summary reports")
        print("9. Save results to employee_analysis_output.csv")
        
        print("\nTo run this script:")
        print("1. Install Java 8 or higher")
        print("2. Set JAVA_HOME environment variable")
        print("3. Run: python employee_analytics.py")
        exit(0)
    
    # 1. Create SparkSession
    print("Creating SparkSession...")
    spark = SparkSession.builder \
        .appName("Employee Salary & Performance Analytics") \
        .getOrCreate()

    print("SparkSession created successfully!")

    # 2. Load data using PySpark
    # Read employees.csv into a DataFrame
    print("\nLoading employee data...")
    df = spark.read.option("header", "true").csv("employees.csv")

    print("\n=== Original DataFrame ===")
    df.show()

    # 3. Data Cleaning
    # Convert salary, years_exp, and performance_score to integer
    print("\nCleaning data...")
    df_cleaned = df.withColumn("salary", col("salary").cast(IntegerType())) \
                   .withColumn("years_exp", col("years_exp").cast(IntegerType())) \
                   .withColumn("performance_score", col("performance_score").cast(IntegerType()))

    # Replace any missing values with 0 (though our dataset doesn't have missing values)
    df_cleaned = df_cleaned.fillna(0, subset=["salary", "years_exp", "performance_score"])

    print("\n=== Cleaned DataFrame ===")
    df_cleaned.show()

    # 4. Salary Analytics
    print("\n=== Salary Analytics ===")
    # Calculate average salary per department
    avg_salary_dept = df_cleaned.groupBy("department").agg(avg("salary").alias("avg_salary"))
    print("Average salary per department:")
    avg_salary_dept.show()

    # Calculate highest and lowest salary in each department
    salary_range_dept = df_cleaned.groupBy("department").agg(
        max("salary").alias("highest_salary"),
        min("salary").alias("lowest_salary")
    )
    print("Highest and lowest salary in each department:")
    salary_range_dept.show()

    # 5. Performance Analytics
    print("\n=== Performance Analytics ===")
    # Add a new column "performance_level"
    df_with_performance = df_cleaned.withColumn(
        "performance_level",
        when(col("performance_score") >= 85, "HIGH")
        .when((col("performance_score") >= 70) & (col("performance_score") < 85), "MEDIUM")
        .otherwise("LOW")
    )

    print("DataFrame with performance level:")
    df_with_performance.show()

    # Find top 3 employees by performance score
    print("Top 3 employees by performance score:")
    top_performers = df_with_performance.orderBy(col("performance_score").desc()).limit(3)
    top_performers.show()

    # 6. Promotion Eligibility
    print("\n=== Promotion Eligibility ===")
    # Add a new column "promotion_eligible"
    df_with_promotion = df_with_performance.withColumn(
        "promotion_eligible",
        when((col("years_exp") >= 4) & (col("performance_score") >= 80), "YES")
        .otherwise("NO")
    )

    print("DataFrame with promotion eligibility:")
    df_with_promotion.show()

    # Display a list of all eligible employees
    print("Employees eligible for promotion:")
    eligible_employees = df_with_promotion.filter(col("promotion_eligible") == "YES")
    eligible_employees.show()

    # 7. Salary vs Performance Insights
    print("\n=== Salary vs Performance Insights ===")
    # Compute average performance score per department
    avg_performance_dept = df_with_promotion.groupBy("department").agg(avg("performance_score").alias("avg_performance_score"))
    print("Average performance score per department:")
    avg_performance_dept.show()

    # Check correlation between salary and performance score
    correlation = df_with_promotion.select(corr("salary", "performance_score")).collect()[0][0]
    print(f"\nCorrelation between salary and performance score: {correlation:.2f}")

    # 8. Final Summary Outputs
    print("\n=== Final Summary Outputs ===")
    # Count of employees per department
    emp_count_dept = df_with_promotion.groupBy("department").agg(count("*").alias("employee_count"))
    print("Count of employees per department:")
    emp_count_dept.show()

    # Count of employees in each performance_level
    emp_count_performance = df_with_promotion.groupBy("performance_level").agg(count("*").alias("employee_count"))
    print("Count of employees in each performance level:")
    emp_count_performance.show()

    # Total salary expense per department
    total_salary_dept = df_with_promotion.groupBy("department").agg(sum("salary").alias("total_salary_expense"))
    print("Total salary expense per department:")
    total_salary_dept.show()

    # 9. Save the final processed DataFrame
    print("\n=== Saving Processed Data ===")
    # Save as employee_analysis_output.csv
    df_with_promotion.coalesce(1).write.mode("overwrite").option("header", "true").csv("employee_analysis_output")

    print("Processed DataFrame saved as 'employee_analysis_output' directory")

    # 10. Final Output Preview
    print("\n=== Final Processed DataFrame Preview ===")
    df_with_promotion.show()

    # Stop the SparkSession
    spark.stop()
    print("\nSparkSession stopped.")
    
except ImportError as e:
    print("Error importing PySpark. Please install it using: pip install pyspark")
    print(f"Error details: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()
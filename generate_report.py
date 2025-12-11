import markdown
import pdfkit
import os

def convert_md_to_pdf():
    # Read the markdown file
    with open('EMPLOYEE_ANALYTICS_REPORT.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    html = markdown.markdown(markdown_content)
    
    # Add basic styling
    html_with_style = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Employee Salary & Performance Analytics Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1, h2, h3 {{
                color: #2c3e50;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            table, th, td {{
                border: 1px solid #ddd;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .executive-summary {{
                background-color: #e8f4f8;
                padding: 15px;
                border-left: 4px solid #3498db;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        {html}
    </body>
    </html>
    """
    
    # Write HTML to file
    with open('report.html', 'w', encoding='utf-8') as f:
        f.write(html_with_style)
    
    print("HTML report generated successfully!")
    
    # Convert HTML to PDF
    try:
        pdfkit.from_string(html_with_style, 'EMPLOYEE_ANALYTICS_REPORT.pdf')
        print("PDF report generated successfully!")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        print("Please install wkhtmltopdf: https://wkhtmltopdf.org/downloads.html")

if __name__ == "__main__":
    convert_md_to_pdf()
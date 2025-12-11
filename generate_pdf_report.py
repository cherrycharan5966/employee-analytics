import markdown
from weasyprint import HTML, CSS
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
            @page {{
                margin: 2cm;
            }}
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 100%;
                margin: 0 auto;
                padding: 0;
                font-size: 12px;
            }}
            h1, h2, h3 {{
                color: #2c3e50;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }}
            h1 {{
                font-size: 24px;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                font-size: 20px;
                border-bottom: 1px solid #ccc;
                padding-bottom: 5px;
            }}
            h3 {{
                font-size: 16px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                page-break-inside: avoid;
            }}
            table, th, td {{
                border: 1px solid #ddd;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            ul, ol {{
                margin-top: 0.5em;
                margin-bottom: 1em;
            }}
            li {{
                margin-bottom: 0.3em;
            }}
            .page-break {{
                page-break-before: always;
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
    
    # Convert HTML to PDF using WeasyPrint
    try:
        HTML(string=html_with_style).write_pdf('EMPLOYEE_ANALYTICS_REPORT.pdf')
        print("PDF report generated successfully!")
        print("Report saved as EMPLOYEE_ANALYTICS_REPORT.pdf")
    except Exception as e:
        print(f"Error generating PDF: {e}")

if __name__ == "__main__":
    convert_md_to_pdf()
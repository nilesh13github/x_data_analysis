from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Data
data = [
    ["S.NO.", "Country Code", "Count", "Country"],
    [1,"GB", 393, "United Kingdom (GBR)"],
    [2,"IR", 355, "Iran (IRN)"],
    [3,"PK", 339, "Pakistan (PAK)"],
    [4,"UA", 302, "Ukraine (UKR)"],
    [5,"NG", 278, "Nigeria (NGA)"],
]

# Create the PDF
pdf_file = "Top_Countries_Report.pdf"
pdf = SimpleDocTemplate(pdf_file, pagesize=letter)

# Create table
table = Table(data)

# Style it
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),

    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
])

table.setStyle(style)

# Build the PDF
pdf.build([table])

print(f"PDF generated: {pdf_file}")

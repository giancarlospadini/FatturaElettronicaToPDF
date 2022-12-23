# Fattura Elettronica To PDF

**Fattura Elettronica** is an italian standard to exchange invoices.

Print one or more Electronic Invoices into a single PDF.

This project is also a good example of how to print xml files formatted with a suitable stylesheet (xsl).


# Installation

Install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html.

Add pdfkit library to Python3: `pip3 install pdfkit`.


# Getting Started

Copy all your invoice files in folder `/fatture_xml`.

Run `python3 main.py` to create `MergedFE.pdf`.


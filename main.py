import lxml.etree as ET
import pdfkit
import pathlib
import os, glob

def printPDF(html_data):
    #Define path to wkhtmltopdf.exe
    #https://wkhtmltopdf.org/downloads.html
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    #Point pdfkit configuration to wkhtmltopdf.exe
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    #Convert Webpage to PDF
    html_data = html_data.replace('\\n', '\n').replace('\\t', '\t')
    pdfkit.from_string(html_data, output_path='MergedFE.pdf', configuration=config)


if __name__ == "__main__":
    xsl_filename = 'FoglioStileAssoSoftware.xsl'

    current_path = str(pathlib.Path().resolve())
    path_to_xml = current_path + r'\fatture_xml'

    html_data = ''
    new_page = '<div style = "display:block; clear:both; page-break-after:always;"></div>'
    for filename in glob.glob(os.path.join(path_to_xml, '*.xml')):
        xml_filename = filename
        dom = ET.parse(xml_filename)
        xslt = ET.parse(xsl_filename)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        html_data_current = ET.tostring(newdom, pretty_print=True).decode("utf-8")
        html_data = html_data + str(html_data_current) + new_page

    html_data = ''.join(html_data.rsplit(new_page, 1))
    printPDF(html_data)

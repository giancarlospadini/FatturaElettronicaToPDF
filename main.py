import lxml.etree as ET
import pdfkit
import pathlib
import os, glob

def savePDF(html_data):
    #Define path to wkhtmltopdf.exe
    #https://wkhtmltopdf.org/downloads.html
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    #Point pdfkit configuration to wkhtmltopdf.exe
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    #Convert HTML to PDF
    html_data = html_data.replace('\\n', '\n').replace('\\t', '\t')
    pdfkit.from_string(html_data, output_path='MergedFE.pdf', configuration=config)


def decodeXML(xml_filename):
    xsl_filename = 'FoglioStileAssoSoftware.xsl'

    dom = ET.parse(xml_filename)
    xslt = ET.parse(xsl_filename)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    html_data = ET.tostring(newdom, pretty_print=True).decode("utf-8")

    return html_data


def getInvoiceN(xml_filename):
    tree = ET.parse(xml_filename)
    FatturaElettronicaBody = tree.find('FatturaElettronicaBody')
    DatiGenerali = FatturaElettronicaBody.find('DatiGenerali')
    DatiGeneraliDocumento = DatiGenerali.find('DatiGeneraliDocumento')
    Numero = DatiGeneraliDocumento.find('Numero')

    return Numero.text


if __name__ == "__main__":
    new_page = '<div style = "display:block; clear:both; page-break-after:always;"></div>'
    html_data = ''

    current_path = str(pathlib.Path().resolve())
    path_to_xml = current_path + r'\fatture_xml'

    file_list = {}
    for filename in glob.glob(os.path.join(path_to_xml, '*.xml')):
        file_list[filename] = getInvoiceN(filename)
    file_list = sorted(
        file_list.items(), key=lambda kv: 
            (kv[1], kv[0])
    )
    for filename in file_list:
        html_data = html_data + decodeXML(filename[0]) + new_page

    html_data = ''.join(html_data.rsplit(new_page, 1))
    savePDF(html_data)
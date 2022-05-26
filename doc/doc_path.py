import pathlib
from pathlib import Path

doc_path = pathlib.Path.cwd()

json_file = Path(doc_path, 'doc', 'staff.json')
avans_ecxel_template = Path(doc_path, 'doc', "template_report.xlsx")
avans_ecxel_file = Path(doc_path, 'doc', "report.xlsx")
word_otpusk_file = Path(doc_path, 'doc', "template_otpusk.docx")
word_otpusk_new_file = Path(doc_path, 'doc', "otpusk.docx")
word_otgul_file = Path(doc_path, 'doc', "template_otgul.docx")
word_otgul_new_file = Path(doc_path, 'doc', "otgul.docx")


def avans_pdf(filename):
    avans_pdf_file = Path(doc_path, 'doc',filename)
    return avans_pdf_file

import os
import re
import openpyxl
import pdfminer.high_level
from doc import doc_path as dpath
import datetime


class PdfToExcell():
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', "августа", "сентября", "октября", "ноября",
              "декабря"]

    def pdf_pars(self, pdf):
        pdfpars = pdfminer.high_level.extract_text(pdf)
        dty_pars = re.findall(r'\d{2}\.\d{2}\.\d{4}', pdfpars)
        number_pars = re.findall(r'\d-\d-\d{3}-\d{3}-\d{3}', pdfpars)
        return dty_pars, number_pars

    def write_excell(self, pdf, fio, position):
        [f, n, ln] = fio.split(' ')
        data = self.pdf_pars(pdf)
        dty_list = data[0][0].split(".")
        m_now = int(dty_list[1])
        file = dpath.avans_ecxel_file
        wb = openpyxl.load_workbook(file)
        sheet = wb['стр1']
        sheet['F63'] = str(data[0][0])
        sheet['K63'] = str(data[1][0]).replace('-', '')
        sheet['AM16'] =str(datetime.datetime.now().strftime("%d"))
        sheet['AP16'] = str(self.months[int(datetime.datetime.now().strftime("%m"))-1])
        sheet['AZ16'] = str(datetime.datetime.now().strftime("%Y"))
        sheet['K20'] = (f'{f} {n[0]}.{ln[0]}.')
        sheet['N22'] = position
        sheet['AI72'] = (f'{f} {n[0]}.{ln[0]}.')
        wb.save(filename=file)
        return file

    def write_excell_template(self, fio, position):
        [f, n, ln] = fio.split(' ')
        file = dpath.avans_ecxel_template
        wb = openpyxl.load_workbook(file)
        sheet = wb['стр1']
        sheet['AM16'] = str(datetime.datetime.now().strftime("%d"))
        sheet['AP16'] = str(self.months[int(datetime.datetime.now().strftime("%m"))-1])
        sheet['AZ16'] = str(datetime.datetime.now().strftime("%Y"))
        sheet['K20'] = (f'{f} {n[0]}.{ln[0]}.')
        sheet['N22'] = position
        sheet['AI72'] = (f'{f} {n[0]}.{ln[0]}.')
        wb.save(filename=file)
        return file

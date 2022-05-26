from docxtpl import DocxTemplate
from doc import doc_path as dpath


def write_word_otgul(file_template, data_fio, data, date_otgul, date_report):

    doc = DocxTemplate(file_template)
    [f, n, ln] = data[0].split(' ')
    [frp, nrp, lnrp] = data_fio.split(' ')


    context = {'должность': str(data[3]), 'отдел': str(data[1]), "ФИО": (f'{f} {n[0]}.{ln[0]}.'), 'датаотгула': date_otgul,
               "датазаявления": date_report, "ФИО_РП": (f'{frp} {nrp[0]}.{lnrp[0]}.')}
    doc.render(context)
    doc.save(dpath.word_otgul_new_file)
    return dpath.word_otgul_new_file


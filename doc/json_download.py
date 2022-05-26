import json
class FioException(Exception):
    pass

def load_staff_data(json_data):
    staff = {}
    staff_happybirthday = {}
    with open(json_data, 'r', encoding='utf-8') as f:
        staff_load = json.load(f)

    for txt in staff_load:
        staff.update({txt['ФИО']: (txt['ФИО_РП'], txt['Отдел (Управление)'], txt["Должность"],
                                   txt["Должность_РП"])})
        staff_happybirthday.update({txt["Дата Рождения"]: txt['ФИО']})

    return staff, staff_happybirthday


def find_fio(begin_fio,staff):
    find_fio_list = []
    for stfk in staff.keys():
        if stfk.lower().startswith(begin_fio.lower()):
            find_fio_list.append(stfk)

    if len(find_fio_list) > 0:
        return find_fio_list
    else:
        raise FioException

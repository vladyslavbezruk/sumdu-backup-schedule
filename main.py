import os.path
import time
from datetime import datetime, timedelta

import requests

from src import config
from src import files
from src import jsons
from src import paths


def update_groups():
    try:
        global groups

        path = paths.groups_file_path

        files.save_file(jsons.download_json(config.site_groups), path)

        print('Оновлено групи')
    except:
        print('Не було оновлено групи')


def backup_schedules():
    groups = files.load_file(paths.groups_file_path)
    i = 0
    count_ok = 0
    count_error = 0
    count_all = 0

    for group_code in groups:
        i += 1

        day_amount = 59
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=day_amount)
        formatted_date = end_date.strftime('%d.%m.%Y')

        if group_code != "0":

            flag = False

            try:
                # json
                filename_json = 'schedule-' + group_code + '.json'

                path_json = os.path.join(paths.backups_file_path, 'json', str(datetime.now().date()))

                if not os.path.exists(path_json):
                    os.mkdir(path_json)

                path_json = os.path.join(path_json, filename_json)

                url_json = config.site_schedules + group_code + '&date_end=' + formatted_date

                schedule_json = jsons.download_json(url_json)

                files.save_file(schedule_json, path_json)

                # pdf

                filename_pdf = str(groups[group_code]).replace('/', '-') + '.pdf'

                path_pdf = os.path.join(paths.backups_file_path, 'pdf', str(datetime.now().date()))

                if not os.path.exists(path_pdf):
                    os.mkdir(path_pdf)

                path = os.path.join(path_pdf, filename_pdf)

                url_pdf = config.site_pdf_schedules + group_code + '&date_end=' + formatted_date

                schedule_pdf = requests.get(url_pdf)

                if schedule_pdf.status_code == 200:
                    with open(path, 'wb') as file:
                        file.write(schedule_pdf.content)
                else:
                    flag = True

            except:
                print('Не вдалося зробити бекап для групи ' + groups[group_code])

                flag = True

                count_error += 1

            if not flag:
                print('Успішно зроблено бекап для групи ' + groups[group_code])

                count_ok += 1

            print('Загальний прогрес ' + str(round(100.0 * i / len(groups), 3)) + '%')

            count_all += 1

    print('Операцію завершено')
    print('Всього груп ' + str(count_all))
    print('Успішно збережено ' + str(count_ok))
    print('Не збережено ' + str(count_error))
    input()


start_time = time.time()

update_groups()

backup_schedules()

end_time = time.time()

elapsed_time = end_time - start_time

print(f"Час виконання: {elapsed_time} секунд")

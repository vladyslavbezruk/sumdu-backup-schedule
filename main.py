import os.path
from datetime import datetime, timedelta

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

    for group_code in groups:
        i += 1

        day_amount = 59
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=day_amount)
        formatted_date = end_date.strftime('%d.%m.%Y')

        if group_code != "0":

            flag = False

            try:
                filename = 'schedule-' + group_code + '.json'

                path = os.path.join(paths.backups_file_path, str(datetime.now().date()))

                if not os.path.exists(path):
                    os.mkdir(path)

                path = os.path.join(path, filename)

                url = config.site_schedules + group_code + '&date_end=' + formatted_date

                schedule = jsons.download_json(url)

                files.save_file(schedule, path)

            except:
                print('Не вдалося зробити бекап для групи ' + groups[group_code])

                flag = True

            if not flag:
                print('Успішно зроблено бекап для групи ' + groups[group_code])

            print('Загальний прогрес ' + str(round(100.0 * i / len(groups), 3)) + '%')


update_groups()

backup_schedules()

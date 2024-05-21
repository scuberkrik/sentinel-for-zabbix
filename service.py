import os
import requests
import xml.etree.ElementTree as ET
import json
import schedule
import time

# Функция для выполнения задачи
def execute_task():
    # Веб-адрес XML
    url = 'http://127.0.0.1:61220/xml'

    # Директория для сохранения файлов
    output_dir = 'C:\\SentinelForZabbix\\disks'

    # Создание директории, если она не существует
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Получение данных XML
    response = requests.get(url)

    # Проверка успешного получения данных
    if response.status_code == 200:
        # Парсинг XML
        root = ET.fromstring(response.content)

        # Поиск всех секций Hard_Disk_Summary
        hard_disk_summaries = root.findall('.//Hard_Disk_Summary')

        # Обработка каждой секции Hard_Disk_Summary
        for idx, hard_disk_summary in enumerate(hard_disk_summaries):
            summary = {}
            summary['Hard_Disk_Summary'] = idx + 1
            for elem in hard_disk_summary:
                summary[elem.tag] = elem.text

            # Преобразование отдельного блока в JSON
            json_output = json.dumps(summary, indent=4, ensure_ascii=False)

            # Имя файла для сохранения блока
            file_name = os.path.join(output_dir, f'disk_{idx + 1}.json')

            # Сохранение JSON в файл
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(json_output)

        print("Все файлы были успешно созданы.")
    else:
        print(f'Не удалось получить данные. Код ответа: {response.status_code}')

# Запуск задачи каждую минуту
schedule.every(1).minutes.do(execute_task)

# Бесконечный цикл для выполнения задач по расписанию
while True:
    schedule.run_pending()
    time.sleep(1)
import os
import shutil

# Директория с JSON файлами
json_dir = 'C:\\SentinelForZabbix\\disks'
# Директория для скриптов PowerShell
psscripts_dir = 'C:\\SentinelForZabbix\\PSscripts'
# Имя конфигурационного файла
zabbix_conf_filename = 'zabbix_agentd.conf'
# Путь к конфигурационному файлу в текущей директории
current_conf_path = os.path.join(os.getcwd(), zabbix_conf_filename)
# Путь к целевому конфигурационному файлу в директорию C:\SentinelForZabbix
zabbix_conf_path = f'C:\\SentinelForZabbix\\{zabbix_conf_filename}'

# Копирование конфигурационного файла в директорию C:\SentinelForZabbix
shutil.copy(current_conf_path, zabbix_conf_path)

# Создание директории, если она не существует
if not os.path.exists(psscripts_dir):
    os.makedirs(psscripts_dir)

# Получение списка файлов в директории JSON
json_files = [f for f in os.listdir(json_dir) if f.startswith('disk_') and f.endswith('.json')]

# Список строк для добавления в конфигурационный файл
zabbix_conf_lines = []

# Создание PowerShell скриптов
for json_file in json_files:
    # Извлечение номера из имени файла
    file_number = json_file.split('_')[1].replace('.json', '')
    # Имя нового скрипта
    ps_script_name = f'get_health_{file_number}.ps1'
    ps_script_path = os.path.join(psscripts_dir, ps_script_name)

    # Путь к JSON файлу
    json_file_path = os.path.join(json_dir, json_file)

    # Содержимое скрипта PowerShell
    ps_script_content = f"""$FilePath = "{json_file_path}"
$json = Get-Content $FilePath | ConvertFrom-Json
$health = $json.Health -replace '%', ''
[int]$intHealth = [int]$health
$intHealth"""

    # Запись содержимого в файл PowerShell
    with open(ps_script_path, 'w', encoding='utf-8') as ps_script_file:
        ps_script_file.write(ps_script_content)

    # Формирование строки для конфигурационного файла Zabbix
    zabbix_conf_lines.append(
        f'UserParameter=custom.json{file_number}.health,powershell -NoProfile -ExecutionPolicy Bypass -File "C:\\SentinelForZabbix\\PSscripts\\{ps_script_name}"'
    )

# Добавление строк в конфигурационный файл Zabbix
with open(zabbix_conf_path, 'a', encoding='utf-8') as zabbix_conf_file:
    for line in zabbix_conf_lines:
        zabbix_conf_file.write(line + '\n')

print("Все PowerShell скрипты и строки конфигурации для Zabbix были успешно созданы и добавлены.")

# Пути к файлам
original_conf_path = 'C:\\Program Files\\Zabbix Agent\\zabbix_agentd.conf'
new_conf_path = 'C:\\SentinelForZabbix\\zabbix_agentd.conf'
destination_dir = 'C:\\Program Files\\Zabbix Agent\\'

# Удаление старого конфигурационного файла, если он существует
if os.path.exists(original_conf_path):
    os.remove(original_conf_path)
    print(f'Удалён файл: {original_conf_path}')

# Копирование нового конфигурационного файла в директорию назначения
shutil.copy(new_conf_path, destination_dir)
print(f'Скопирован файл из {new_conf_path} в {destination_dir}')

# Пути к исходному и целевому файлам pars_xml.py
source_file = os.path.join(os.getcwd(), 'service.py')
destination_dir = 'C:\\SentinelForZabbix'

# Копирование файла pars_xml.py в целевую директорию
shutil.copy(source_file, destination_dir)
print(f'Скопирован файл {source_file} в {destination_dir}')

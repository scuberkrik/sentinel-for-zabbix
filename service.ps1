# Создание директорий, если они не существуют
if (-Not (Test-Path "C:\nssm")) {
    New-Item -Path "C:\nssm" -ItemType Directory
}

# Путь к вашему Python скрипту
$scriptPath = "C:\SentinelForZabbix\service.py"

# Путь к python.exe
$pythonPath = "C:\Program Files\Python312\python.exe"

# Имя службы
$serviceName = "SentinelService"

# Скачивание и установка NSSM (при необходимости)
$downloadUrl = "https://nssm.cc/release/nssm-2.24.zip"
$nssmPath = "C:\nssm"
$zipPath = "$nssmPath\nssm.zip"

# Проверка наличия NSSM
if (-Not (Test-Path "$nssmPath\nssm.exe")) {
    Write-Output "Скачиваю NSSM..."
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath

    # Убедитесь, что архив скачан успешно
    if (Test-Path $zipPath) {
        Expand-Archive -Path $zipPath -DestinationPath $nssmPath
        Move-Item "$nssmPath\nssm-2.24\win64\nssm.exe" "$nssmPath\nssm.exe"
        Remove-Item -Recurse -Force "$nssmPath\nssm-2.24"

        # Установка службы с помощью NSSM
        & "C:\nssm\nssm.exe" install $serviceName "$pythonPath" "$scriptPath"

        # Запуск службы
        Start-Service $serviceName
        Write-Output "$serviceName is installed and running."
    } else {
        Write-Error "Не удалось скачать NSSM."
        exit
    }
} else {
    Write-Output "NSSM already installed."

    # Установка службы с помощью NSSM
    & "C:\nssm\nssm.exe" install $serviceName "$pythonPath" "$scriptPath"

    # Запуск службы
    Start-Service $serviceName
    Write-Output "$serviceName is running."
}
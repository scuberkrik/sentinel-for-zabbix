$serviceName = "Zabbix Agent"
$service = Get-Service $serviceName -ErrorAction SilentlyContinue

# Если служба отключена, включаем её, иначе останавливаем и запускаем
if ($service -eq $null) {
    Start-Service -Name $serviceName
    Write-Output "Служба $serviceName запущена"
}
else {
    if ($service.Status -eq "Running" -or $service.Status -eq "StopPending") {
        Stop-Service -Name $serviceName
        Write-Output "Служба $serviceName остановлена"
        Start-Sleep -Seconds 5  # Небольшая задержка для обеспечения корректного останова службы
    }

    Start-Service -Name $serviceName
    Write-Output "Служба $serviceName запущена"
}
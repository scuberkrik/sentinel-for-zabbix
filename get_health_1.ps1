$FilePath = "C:\Users\admin\PycharmProjects\pythonProject\disk_1.json"
$json = Get-Content $FilePath | ConvertFrom-Json
$health = $json.Health -replace '%', ''
[int]$intHealth = [int]$health
$intHealth
$Request = Invoke-WebRequest -Uri "https://api.openai.com/v1/models" -Headers @{Authorization="Bearer $env:OPENAI_API_KEY"} -UseBasicParsing

$Content = $Request.Content | ConvertFrom-Json

$Models = $Content.data

$Models | Format-Table id, object, created, owned_by -AutoSize
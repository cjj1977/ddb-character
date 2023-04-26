$Content = Get-Content ./ddb_character/.env
foreach($Line in $Content){
    $Key = $Line.split("=")[0]
    $Value = $Line.split("=")[1]

    Write-Verbose "Setting $Key"

    try {
        New-Item -Path Env:\$Key -Value $Value -Force | Out-Null
    }
    catch {
    }
}
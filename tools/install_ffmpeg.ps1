# PowerShell script to download and install ffmpeg on Windows

$ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$zipPath = "$env:TEMP\ffmpeg.zip"
$installPath = "$env:USERPROFILE\ffmpeg"

Write-Host "Downloading ffmpeg..."
Invoke-WebRequest -Uri $ffmpegUrl -OutFile $zipPath

Write-Host "Extracting ffmpeg..."
Expand-Archive -Path $zipPath -DestinationPath $installPath -Force

# The extracted folder name may vary, find the folder with ffmpeg.exe
$ffmpegBinPath = Get-ChildItem -Path $installPath -Directory | Where-Object { Test-Path "$($_.FullName)\bin\ffmpeg.exe" } | Select-Object -First 1

if ($ffmpegBinPath) {
    $ffmpegBin = "$($ffmpegBinPath.FullName)\bin"
    Write-Host "Adding ffmpeg to PATH..."
    [Environment]::SetEnvironmentVariable("Path", $env:Path + ";" + $ffmpegBin, [EnvironmentVariableTarget]::User)
    Write-Host "ffmpeg installed successfully. Please restart your terminal or IDE to apply PATH changes."
} else {
    Write-Host "ffmpeg binary not found after extraction."
}

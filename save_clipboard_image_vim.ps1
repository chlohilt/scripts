$outputPath = "C:\Users\chloehi\Pictures\Screenshots"
$fileName = "screenshot_$(Get-Date -Format 'yyyyMMdd_HHmmss').png"
$fullPath = Join-Path $outputPath $fileName

Add-Type -AssemblyName System.Windows.Forms
$clipboard = [System.Windows.Forms.Clipboard]::GetImage()

if ($clipboard -ne $null) {
    $clipboard.Save($fullPath)
    Write-Output $fileName
} else {
    Write-Error "No image found in clipboard."
}

$sourcePath = "C:\pim3\MicroMikeGit\MicroMike\src\theme.css"
$destPath = "C:\pim3\newtekgit\.obsidian\themes\Art Deco CSS\theme.css"
$destPath2 = "C:\pim3\MicroMikeGit\MicroMike\theme.css"
$destPath3 = "C:\pim3\MMpure\.obsidian\themes\micro mike 2\theme.css"
# Copy to first destination
Copy-Item -Path $sourcePath -Destination $destPath -Force
Write-Host "File copied to $destPath"

# Copy to second destination
Copy-Item -Path $sourcePath -Destination $destPath2 -Force
Write-Host "File copied to $destPath2"

# Copy to second destination
Copy-Item -Path $sourcePath -Destination $destPath3 -Force
Write-Host "File copied to $destPath3"
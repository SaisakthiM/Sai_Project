# Ensure you are in your Sai_Project repo folder before running this script

# Get all .zip files
$zipFiles = Get-ChildItem -Filter *.zip

foreach ($zip in $zipFiles) {
    $folderName = [System.IO.Path]::GetFileNameWithoutExtension($zip.Name)
    $targetPath = Join-Path -Path (Get-Location) -ChildPath $folderName

    # Create folder if it doesn't exist
    if (-Not (Test-Path $targetPath)) {
        New-Item -ItemType Directory -Path $targetPath | Out-Null
    }

    # Unzip into folder
    Expand-Archive -Path $zip.FullName -DestinationPath $targetPath -Force

    # Remove original zip
    Remove-Item $zip.FullName -Force

    # Stage the folder and removal
    git add $folderName
    git rm --cached $zip.Name 2>$null  # remove zip from Git if tracked
    git commit -m "Unzipped and replaced: $folderName"
}

# Finally push all commits
git push origin main

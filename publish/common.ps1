#!/usr/bin/env pwsh

function require_file ($filepath) {
    $exists = (Test-Path $filepath)
    if (!$exists) {
        Write-Error "'${version_fiepath}' not found"
        exit
    }
}

function grep ($finding, $filepath) {
    $result = ( `
        (Get-Content $setuppy_filepath) | `
        ForEach-Object {$i++; "L$($i-1):$_"} | `
        Select-String $finding `
        )
    if ($result -eq $null) {
        Write-Output "not found: '$finding'"
        return 1 | Out-Null
    } else {
        Write-Output "found:"
        Write-Output "$result"
        return 0 | Out-Null
    }
}

function update_version($measure) {
    # 1. Conduct pytest (exit on error)
    Clear-Host
    python -m pytest
    if (! $?) {
        Write-Error "Failed on pytest."
        return $result
    }

    # 2. Check uncommitted files (exit if exist)
    if ("$(git status --porcelain)" -ne "") {
        Write-Error (
            "Uncommited files exist. " +
            "Commit all files before an update."
        )
        git status --porcelain
        return 1 | Out-Null
    }

    # 3. Check old version is consistent to setup.py (exit on error)
    $old_version = (Get-Content $version_filepath | Select-Object -First 1)
    grep "version='${old_version}'" $setuppy_filepath
    if (!$?) {
        return 1 | Out-Null
    }
    
    # 4. Calculate new version by incrementing revision verison
    $ver_list = $old_version.Split(".")
    $ver_list[$measure] = [int]$ver_list[$measure] + 1
    $new_version = ($ver_list -join ".")

    # 5. Update version and setup.py, and git push
    Write-Output $new_version | Set-Content $version_filepath -NoNewline
    (Get-Content $setuppy_filepath) | `
        %{ "$_`n" -replace "version='${old_version}'", "version='${new_version}'" } | `
        Set-Content $setuppy_filepath -NoNewline
    git add -A | Out-Null
    git commit -m "Release v$new_version." | Out-Null
    git tag "v$new_version"
    git push | Out-Null
    Write-Host "Updated: v$old_version to v$new_version."
}

$major = 0
$minor = 1
$revision = 2
$test = 3

# Check the existence of files.
$version_filepath = "publish/version"
$setuppy_filepath = "setup.py"
require_file $version_filepath
require_file $setuppy_filepath


# Function to check if a command exists
function Test-CommandExists {
    param (
        [string]$command
    )
    $exists = $false
    try {
        if (Get-Command $command -ErrorAction Stop) {
            $exists = $true
        }
    }
    catch {
        $exists = $false
    }
    return $exists
}

# Check for Python 3 installation
$pythonInstalled = Test-CommandExists "python3"
if (-not $pythonInstalled) {
    # Some systems may have Python 3 accessible as 'python'
    $pythonInstalled = Test-CommandExists "python"
}

# Check for pip installation
$pipInstalled = Test-CommandExists "pip"

if ($pythonInstalled -and $pipInstalled) {
    Write-Host "Installing Dependencies..." -ForegroundColor Cyan
    # Dependencies to install
    $dependencies = @("bs4", "python-csv", "requests")

    foreach ($dep in $dependencies) {
        try {
            Start-Process python -ArgumentList " -m pip install $dep" -NoNewWindow -Wait -ErrorAction Stop
            Write-Host "$dep installed successfully." -ForegroundColor Green
        }
        catch {
            Write-Host "$dep could not be installed. Please check for errors and try again." -ForegroundColor Red
        }
    }
    Write-Host "Dependency installation process completed." -ForegroundColor Green
}
else {
    Write-Host "Dependency Installation Failed" -ForegroundColor Red
    # Provide instructions for installing Python 3 and pip
    if (-not $pythonInstalled) {
        Write-Host "Python 3 is not installed. Please install Python 3." -ForegroundColor Yellow
    }
    if (-not $pipInstalled) {
        Write-Host "pip is not installed. Please ensure Python 3 and pip are correctly installed." -ForegroundColor Yellow
    }
}
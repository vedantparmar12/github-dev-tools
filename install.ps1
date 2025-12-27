# GitHub Dev Tools Skill - Installation Script for Windows

param(
    [string]$InstallDir = ""
)

Write-Host "Installing GitHub Dev Tools Skill for Codex CLI..." -ForegroundColor Green
Write-Host ""

# Determine installation location
if ($InstallDir -eq "") {
    $codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { "$env:USERPROFILE\.codex" }
    $InstallDir = "$codexHome\skills"
}

# Create skills directory if it doesn't exist
if (!(Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}

# Get the directory where this script is located
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Copy skill files
$targetDir = "$InstallDir\github-dev-tools"
Write-Host "Installing to: $targetDir"

if (Test-Path $targetDir) {
    Remove-Item -Path $targetDir -Recurse -Force
}

Copy-Item -Path $scriptDir -Destination $targetDir -Recurse -Force

# Install Python dependencies
Write-Host ""
Write-Host "Installing Python dependencies..."

$pipCommand = Get-Command pip -ErrorAction SilentlyContinue
if (!$pipCommand) {
    $pipCommand = Get-Command pip3 -ErrorAction SilentlyContinue
}

if ($pipCommand) {
    & $pipCommand.Source install -r "$targetDir\scripts\requirements.txt"
} else {
    Write-Host "Warning: pip not found. Please install Python dependencies manually:" -ForegroundColor Yellow
    Write-Host "  pip install -r $targetDir\scripts\requirements.txt"
}

Write-Host ""
Write-Host "✓ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Set your GitHub Personal Access Token:"
Write-Host "   `$env:GITHUB_PERSONAL_ACCESS_TOKEN = 'ghp_your_token_here'"
Write-Host ""
Write-Host "2. Add to your PowerShell profile:"
Write-Host "   Add-Content `$PROFILE '`$env:GITHUB_PERSONAL_ACCESS_TOKEN = `"ghp_your_token_here`"'"
Write-Host ""
Write-Host "3. Start using the skill in Codex:"
Write-Host "   - Just describe GitHub tasks naturally"
Write-Host "   - Or use: `$github-dev-tools <description>"
Write-Host ""
Write-Host "For more information, see: $targetDir\README.md"

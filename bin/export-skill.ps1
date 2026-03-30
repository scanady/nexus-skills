#!/usr/bin/env pwsh
# export-skill.ps1 — Packages a skill into a zip file for import into Claude and other platforms.
#
# Usage:
#   .\export-skill.ps1 <skill-name>
#   .\export-skill.ps1 research-deep-reading-analyst
#
# Output: ./output/<skill-name>.zip
#
# Zip structure (as required by Claude):
#   <skill-name>.zip
#   └── <skill-name>/
#       ├── SKILL.md
#       └── (any other files/folders in the skill directory)

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$SkillName
)

$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$SkillsDir   = Join-Path $ProjectRoot "skills"
$OutputDir   = Join-Path $ProjectRoot "output"

function Get-AvailableSkills {
    Get-ChildItem -Path $SkillsDir -Directory |
        Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") } |
        Select-Object -ExpandProperty Name |
        Sort-Object
}

function Show-Usage {
    Write-Host ""
    Write-Host "Usage: export-skill.ps1 <skill-name>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Available skills:"
    Get-AvailableSkills | ForEach-Object { Write-Host "  * $_" }
    Write-Host ""
}

# Show usage when no skill name is provided
if (-not $SkillName) {
    Show-Usage
    exit 1
}

# Validate skill directory exists
$SkillPath = Join-Path $SkillsDir $SkillName
if (-not (Test-Path $SkillPath -PathType Container)) {
    Write-Host ""
    Write-Host "ERROR: Skill '$SkillName' not found in $SkillsDir" -ForegroundColor Red
    Write-Host ""
    Write-Host "Available skills:"
    Get-AvailableSkills | ForEach-Object { Write-Host "  * $_" }
    Write-Host ""
    exit 1
}

# Validate SKILL.md exists
if (-not (Test-Path (Join-Path $SkillPath "SKILL.md"))) {
    Write-Host ""
    Write-Host "ERROR: '$SkillName' is missing a SKILL.md file." -ForegroundColor Red
    Write-Host ""
    exit 1
}

# Ensure output directory exists
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

$ZipPath = Join-Path $OutputDir "$SkillName.zip"

# Remove any existing zip with the same name
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}

# Compress-Archive with a folder path includes the folder itself as the zip root.
# Result: <skill-name>.zip → <skill-name>/ → SKILL.md, ...
Compress-Archive -Path $SkillPath -DestinationPath $ZipPath

# Print summary
Write-Host ""
Write-Host "Exported '$SkillName'" -ForegroundColor Green
Write-Host "  $ZipPath"
Write-Host ""
Write-Host "Zip contents:"
Write-Host "  $SkillName.zip"
Write-Host "  +-- $SkillName/"
Get-ChildItem -Path $SkillPath | ForEach-Object {
    Write-Host "      +-- $($_.Name)"
}
Write-Host ""

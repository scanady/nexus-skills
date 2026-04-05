#!/usr/bin/env pwsh
# export-skill.ps1 — Packages a skill directory into a zip file for manual import.
#
# The archive layout follows the Agent Skills convention:
#   <skill-name>.zip
#   └── <skill-name>/
#       ├── SKILL.md
#       └── optional files/directories (scripts/, references/, assets/, ...)
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

function Get-FrontmatterValue {
    param(
        [string]$Path,
        [string]$FieldName
    )

    $lines = Get-Content -LiteralPath $Path
    $inFrontmatter = $false

    foreach ($line in $lines) {
        if ($line.Trim() -eq '---') {
            if ($inFrontmatter) {
                break
            }

            $inFrontmatter = $true
            continue
        }

        if (-not $inFrontmatter) {
            continue
        }

        if ($line -match "^$FieldName:\s*(.*)$") {
            return $matches[1].Trim().Trim('"').Trim("'")
        }
    }

    return ''
}

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

if (($SkillName.Length -gt 64) -or ($SkillName -notmatch '^[a-z0-9]+(?:-[a-z0-9]+)*$')) {
    Write-Host ""
    Write-Host "ERROR: '$SkillName' does not satisfy the Agent Skills naming rules." -ForegroundColor Red
    Write-Host ""
    exit 1
}

$SkillFile = Join-Path $SkillPath "SKILL.md"
$FrontmatterName = Get-FrontmatterValue -Path $SkillFile -FieldName "name"
$FrontmatterDescription = Get-FrontmatterValue -Path $SkillFile -FieldName "description"

if (-not $FrontmatterName) {
    Write-Host ""
    Write-Host "ERROR: '$SkillName/SKILL.md' is missing the required frontmatter name field." -ForegroundColor Red
    Write-Host ""
    exit 1
}

if ($FrontmatterName -ne $SkillName) {
    Write-Host ""
    Write-Host "ERROR: Frontmatter name '$FrontmatterName' must match the folder name '$SkillName'." -ForegroundColor Red
    Write-Host ""
    exit 1
}

if (-not $FrontmatterDescription) {
    Write-Host ""
    Write-Host "ERROR: '$SkillName/SKILL.md' is missing the required frontmatter description field." -ForegroundColor Red
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
Compress-Archive -LiteralPath $SkillPath -DestinationPath $ZipPath -Force

# Print summary
Write-Host ""
Write-Host "Exported '$SkillName'" -ForegroundColor Green
Write-Host "  $ZipPath"
Write-Host "  Standard: Agent Skills directory layout"
Write-Host ""
Write-Host "Zip contents:"
Write-Host "  $SkillName.zip"
Write-Host "  +-- $SkillName/"
Get-ChildItem -Path $SkillPath | Sort-Object Name | ForEach-Object {
    Write-Host "      +-- $($_.Name)"
}
Write-Host ""

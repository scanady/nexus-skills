<#
.SYNOPSIS
    Scaffold the starter shell for a new repository.
.PARAMETER TargetPath
    Target directory. Default: current working directory.
.PARAMETER ProjectName
    Project name used in file stubs. Default: target directory name.
.PARAMETER DryRun
    Show what would be created without writing files.
.PARAMETER Force
    Overwrite files that already exist.
.PARAMETER UpdateExisting
    Update existing scaffold artifacts and common skills. Equivalent to Force.
.PARAMETER SkipCommonSkills
    Do not install common skills into .agents/skills.
.PARAMETER SkillsSourceUrl
    Git repository for common skills.
.PARAMETER SkillsSourceRef
    Git branch, tag, or commit for common skills.
.PARAMETER SkipSharedStandards
    Do not apply the shared engineering standards (.github/instructions files and AGENTS.md).
.PARAMETER StandardsSourceUrl
    Git repository holding the shared standards and the sync script.
.PARAMETER StandardsSourceRef
    Git branch, tag, or commit for the shared standards.
.EXAMPLE
    .\repo-scaffold.ps1 -TargetPath C:\new-repo -ProjectName "my-project"
.EXAMPLE
    .\repo-scaffold.ps1 -DryRun
#>
param(
    [string]$TargetPath  = (Get-Location).Path,
    [string]$ProjectName = '',
    [switch]$DryRun,
    [switch]$Force,
    [switch]$UpdateExisting,
    [switch]$SkipCommonSkills,
    [string]$SkillsSourceUrl = 'https://github.com/scanady/nexus-skills.git',
    [string]$SkillsSourceRef = 'main',
    [switch]$SkipSharedStandards,
    [string]$StandardsSourceUrl = 'https://github.com/scanady/ifoundry-development.git',
    [string]$StandardsSourceRef = 'main'
)

$scriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent
$templateRoot = Join-Path $scriptDir '..\assets\starter'
$commonSkillsFile = Join-Path $scriptDir '..\assets\common-skills.txt'
. (Join-Path $scriptDir '_lib\validators.ps1')

$rulesPath = Join-Path $scriptDir '..\references\path-rules.json'
$rules     = Get-PathRules -RulesPath $rulesPath

if (-not $ProjectName) {
    if (Test-Path $TargetPath -PathType Container) {
        $ProjectName = Split-Path (Resolve-Path -LiteralPath $TargetPath).Path -Leaf
    } else {
        $ProjectName = Split-Path $TargetPath -Leaf
    }
}

$overwriteExisting = $Force -or $UpdateExisting

Write-Host 'Repository Scaffold' -ForegroundColor Cyan
Write-Host '===================' -ForegroundColor Cyan
Write-Host ("Target  : {0}" -f $TargetPath)
Write-Host ("Project : {0}" -f $ProjectName)
if ($DryRun) { Write-Host '[DRY RUN]' -ForegroundColor Yellow }
Write-Host ''

# ── Create files ──────────────────────────────────────────────────────────────
$created = 0
$skipped = 0
$errors  = 0
$warnings = 0

function Get-CommonSkills {
    param([string]$Path)

    if (-not (Test-Path $Path -PathType Leaf)) {
        return @()
    }

    return Get-Content -Path $Path |
        ForEach-Object { ($_ -replace '#.*$', '').Trim() } |
        Where-Object { $_ }
}

function Install-CommonSkills {
    param(
        [string]$TargetPath,
        [string]$SourceUrl,
        [string]$SourceRef,
        [string]$SkillsFile,
        [switch]$DryRun,
        [switch]$Force,
        [switch]$Skip
    )

    if ($Skip) {
        Write-Host '  -- Skip common skills' -ForegroundColor Gray
        return @{ created = 0; skipped = 0; warnings = 0 }
    }

    if (-not (Test-Path $SkillsFile -PathType Leaf)) {
        Write-Host ('  !! Common skills list missing: {0}' -f $SkillsFile) -ForegroundColor Yellow
        return @{ created = 0; skipped = 0; warnings = 1 }
    }

    $skills = @(Get-CommonSkills -Path $SkillsFile)
    if ($skills.Count -eq 0) {
        Write-Host '  -- No common skills configured' -ForegroundColor Gray
        return @{ created = 0; skipped = 0; warnings = 0 }
    }

    if ($DryRun) {
        Write-Host ('  >> Install common skills from {0}#{1}' -f $SourceUrl, $SourceRef) -ForegroundColor Cyan
        foreach ($skill in $skills) {
            Write-Host ('     - .agents/skills/{0}' -f $skill) -ForegroundColor Cyan
        }
        return @{ created = 0; skipped = 0; warnings = 0 }
    }

    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host '  !! git is required to install common skills' -ForegroundColor Yellow
        return @{ created = 0; skipped = 0; warnings = 1 }
    }

    $tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())
    $result = @{ created = 0; skipped = 0; warnings = 0 }

    try {
        & git clone --depth 1 --branch $SourceRef $SourceUrl $tempRoot *> $null
        if ($LASTEXITCODE -ne 0) {
            Write-Host ('  !! Failed to clone common skills source: {0}#{1}' -f $SourceUrl, $SourceRef) -ForegroundColor Yellow
            $result.warnings++
            return $result
        }

        $targetSkillsDir = Join-Path $TargetPath '.agents\skills'
        New-Item -ItemType Directory -Path $targetSkillsDir -Force | Out-Null

        foreach ($skill in $skills) {
            $sourceDir = Join-Path $tempRoot ('skills\{0}' -f $skill)
            if (-not (Test-Path $sourceDir -PathType Container)) {
                $sourceDir = Join-Path $tempRoot ('.agents\skills\{0}' -f $skill)
            }

            if (-not (Test-Path $sourceDir -PathType Container)) {
                Write-Host ('  !! Missing common skill in source: {0}' -f $skill) -ForegroundColor Yellow
                $result.warnings++
                continue
            }

            $destination = Join-Path $targetSkillsDir $skill
            if ((Test-Path $destination) -and (-not $Force)) {
                Write-Host ('  -- Skip (exists) : .agents/skills/{0}' -f $skill) -ForegroundColor Gray
                $result.skipped++
                continue
            }

            if (Test-Path $destination) {
                Remove-Item -Path $destination -Recurse -Force
            }

            Copy-Item -Path $sourceDir -Destination $destination -Recurse
            Write-Host ('  OK Installed     : .agents/skills/{0}' -f $skill) -ForegroundColor Green
            $result.created++
        }
    } finally {
        if (Test-Path $tempRoot) {
            Remove-Item -Path $tempRoot -Recurse -Force
        }
    }

    return $result
}

function Install-ClaudeSkillsLink {
    param(
        [string]$TargetPath,
        [switch]$DryRun,
        [switch]$Force
    )

    # Path Claude Code discovers; created as a link to the reusable-skills folder.
    $linkPath   = Join-Path $TargetPath '.claude\skills'
    $linkParent = Join-Path $TargetPath '.claude'
    $targetRel  = '..\.agents\skills'
    $display    = '.claude/skills'
    $result     = @{ created = 0; skipped = 0; warnings = 0 }

    $existingItem = Get-Item -LiteralPath $linkPath -Force -ErrorAction SilentlyContinue
    $isReparse    = $false
    $currentTarget = $null
    if ($existingItem) {
        $isReparse = ($existingItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0
        if ($isReparse) {
            $currentTarget = $existingItem.Target
            if ($currentTarget -is [array]) { $currentTarget = $currentTarget[0] }
        }
    }

    if ($DryRun) {
        if ($isReparse) {
            Write-Host ('  -- Link exists   : {0} -> {1}' -f $display, $currentTarget) -ForegroundColor Gray
        } else {
            Write-Host ('  >> Junction      : {0} -> {1}' -f $display, $targetRel) -ForegroundColor Cyan
        }
        return $result
    }

    if (-not (Test-Path $linkParent)) {
        New-Item -ItemType Directory -Path $linkParent -Force | Out-Null
    }

    if ($existingItem) {
        if ($isReparse) {
            $matches = $false
            if ($currentTarget) {
                $normalized = ($currentTarget -replace '/', '\').TrimEnd('\')
                $expected   = $targetRel.TrimEnd('\')
                # Compare either the relative form we set, or the absolute path Windows may report.
                if ($normalized -eq $expected -or $normalized -like "*\.agents\skills") { $matches = $true }
            }
            if ($matches) {
                Write-Host ('  -- Skip (link)   : {0} -> {1}' -f $display, $targetRel) -ForegroundColor Gray
                $result.skipped++
                return $result
            }
            if ($Force) {
                Remove-Item -LiteralPath $linkPath -Force -Recurse
            } else {
                Write-Host ('  !! Existing link : {0} -> {1} (expected {2}); pass -Force to replace' -f $display, $currentTarget, $targetRel) -ForegroundColor Yellow
                $result.warnings++
                return $result
            }
        } else {
            if ($Force) {
                Remove-Item -LiteralPath $linkPath -Force -Recurse
            } else {
                Write-Host ('  !! Path exists (not a link): {0}; pass -Force to replace' -f $display) -ForegroundColor Yellow
                $result.warnings++
                return $result
            }
        }
    }

    # Junction avoids the admin/developer-mode requirement of NTFS symbolic links; needs an absolute target.
    $absoluteTarget = (Resolve-Path -LiteralPath (Join-Path $TargetPath '.agents\skills') -ErrorAction SilentlyContinue)
    if (-not $absoluteTarget) {
        Write-Host ('  !! Symlink target missing: .agents/skills; scaffold the starter shell first') -ForegroundColor Yellow
        $result.warnings++
        return $result
    }

    try {
        New-Item -ItemType Junction -Path $linkPath -Target $absoluteTarget.Path -Force | Out-Null
        Write-Host ('  OK Junctioned    : {0} -> {1}' -f $display, $targetRel) -ForegroundColor Green
        $result.created++
    } catch {
        Write-Host ('  !! Failed to create junction: {0} -- {1}' -f $display, $_) -ForegroundColor Yellow
        $result.warnings++
    }

    return $result
}

function Install-SharedStandards {
    param(
        [string]$TargetPath,
        [string]$SourceUrl,
        [string]$SourceRef,
        [switch]$DryRun,
        [switch]$Skip
    )

    if ($Skip) {
        Write-Host '  -- Skip shared standards' -ForegroundColor Gray
        return @{ warnings = 0 }
    }

    if ($DryRun) {
        Write-Host ('  >> Apply shared standards from {0}#{1}' -f $SourceUrl, $SourceRef) -ForegroundColor Cyan
        Write-Host '     - .github/instructions/coding-principles.instructions.md' -ForegroundColor Cyan
        Write-Host '     - .github/instructions/core-principles.instructions.md' -ForegroundColor Cyan
        Write-Host '     - AGENTS.md' -ForegroundColor Cyan
        return @{ warnings = 0 }
    }

    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host '  !! git is required to apply shared standards' -ForegroundColor Yellow
        return @{ warnings = 1 }
    }

    $tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())

    try {
        & git clone --depth 1 --branch $SourceRef $SourceUrl $tempRoot *> $null
        if ($LASTEXITCODE -ne 0) {
            Write-Host ('  !! Failed to clone shared standards source: {0}#{1}' -f $SourceUrl, $SourceRef) -ForegroundColor Yellow
            return @{ warnings = 1 }
        }

        # The standards repo owns the sync logic; run its script rather than reimplementing it here,
        # so the two never drift.
        $syncScript = Join-Path $tempRoot 'scripts\sync-standards.ps1'
        if (-not (Test-Path $syncScript -PathType Leaf)) {
            Write-Host ('  !! Sync script missing in standards source: {0}' -f $syncScript) -ForegroundColor Yellow
            return @{ warnings = 1 }
        }

        # Writes its own progress to the console.
        & $syncScript -Source $tempRoot -TargetRepo $TargetPath

        if ($LASTEXITCODE -ne 0) {
            Write-Host '  !! Shared standards sync reported an error' -ForegroundColor Yellow
            return @{ warnings = 1 }
        }

        Write-Host '  OK Applied       : shared standards' -ForegroundColor Green
        return @{ warnings = 0 }
    } finally {
        if (Test-Path $tempRoot) {
            Remove-Item -Path $tempRoot -Recurse -Force
        }
    }
}

foreach ($relativePath in $rules.starter_shell.paths) {
    $resolvedPath = $relativePath.Replace('{project-name}', $ProjectName)
    $normPath    = $resolvedPath -replace '/', '\'
    $fullPath    = Join-Path $TargetPath $normPath
    $templatePath = Join-Path $templateRoot ($relativePath -replace '/', '\')
    $wasExisting = Test-Path $fullPath

    if ($wasExisting -and (-not $overwriteExisting)) {
        Write-Host ('  -- Skip (exists) : {0}' -f $resolvedPath) -ForegroundColor Gray
        $skipped++
        continue
    }

    if ($DryRun) {
        if ($wasExisting) {
            Write-Host ('  >> Overwrite     : {0}' -f $resolvedPath) -ForegroundColor Cyan
        } else {
            Write-Host ('  >> Create        : {0}' -f $resolvedPath) -ForegroundColor Cyan
        }
        $created++
        continue
    }

    try {
        $dir = Split-Path $fullPath -Parent
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }

        if (-not (Test-Path $templatePath -PathType Leaf)) {
            throw "Template not found: $templatePath"
        }

        # -Raw yields $null for an empty template (every .gitkeep), so normalize before replacing.
        $content = Get-Content -Path $templatePath -Raw
        if ($null -eq $content) { $content = '' }
        $content = $content.Replace('{Project Name}', $ProjectName).Replace('{project-name}', $ProjectName)
        Set-Content -Path $fullPath -Value $content -Encoding UTF8

        if ($wasExisting) {
            Write-Host ('  OK Overwrote     : {0}' -f $resolvedPath) -ForegroundColor Green
        } else {
            Write-Host ('  OK Created       : {0}' -f $resolvedPath) -ForegroundColor Green
        }
        $created++
    } catch {
        Write-Host ('  X  Failed        : {0} -- {1}' -f $resolvedPath, $_) -ForegroundColor Red
        $errors++
    }
}

$skillResult = Install-CommonSkills -TargetPath $TargetPath -SourceUrl $SkillsSourceUrl -SourceRef $SkillsSourceRef -SkillsFile $commonSkillsFile -DryRun:$DryRun -Force:$overwriteExisting -Skip:$SkipCommonSkills
$created += $skillResult.created
$skipped += $skillResult.skipped
$warnings += $skillResult.warnings

# Runs after common skills so the link points at a populated target folder on first scaffold.
$linkResult = Install-ClaudeSkillsLink -TargetPath $TargetPath -DryRun:$DryRun -Force:$overwriteExisting
$created += $linkResult.created
$skipped += $linkResult.skipped
$warnings += $linkResult.warnings

# Runs after the starter shell so the sync tool creates AGENTS.md with the shared preamble on
# top of a directory that already has the .claude/CLAUDE.md shim pointing at it.
$standardsResult = Install-SharedStandards -TargetPath $TargetPath -SourceUrl $StandardsSourceUrl -SourceRef $StandardsSourceRef -DryRun:$DryRun -Skip:$SkipSharedStandards
$warnings += $standardsResult.warnings

Write-Host ''
Write-Host ('Created : {0}' -f $created)
Write-Host ('Skipped : {0}' -f $skipped)
Write-Host ('Warnings: {0}' -f $warnings)
if ($errors -gt 0) {
    Write-Host ('Errors  : {0}' -f $errors) -ForegroundColor Red
}

if ((-not $DryRun) -and ($created -gt 0)) {
    Write-Host ''
    Write-Host 'Starter shell ready. Run repo-audit.ps1 to verify.' -ForegroundColor Green
    Write-Host 'Add optional artifacts only when adoption triggers are met.' -ForegroundColor Gray
}

if ($errors -gt 0) { exit 1 }
exit 0

<#
.SYNOPSIS
Audit a repository against the project structure standard.

.PARAMETER RepoRoot       Repository root. Default: current directory.
.PARAMETER OutputFormat   console | json | markdown | all. Default: console.
.PARAMETER OutputPath     Base path for report files. Default: ./audit-report.
.PARAMETER DryRun         Show plan without generating reports.

.EXAMPLE  .\repo-audit.ps1 -RepoRoot C:\my-repo -OutputFormat all
.EXAMPLE  .\repo-audit.ps1 -DryRun
#>
param(
    [string]$RepoRoot     = (Get-Location).Path,
    [ValidateSet('console','json','markdown','all')]
    [string]$OutputFormat = 'console',
    [string]$OutputPath   = (Join-Path (Get-Location).Path 'audit-report'),
    [switch]$DryRun
)

$scriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent
. (Join-Path $scriptDir '_lib\validators.ps1')

if (-not (Test-Path $RepoRoot -PathType Container)) {
    Write-Error "Repository root not found: $RepoRoot"
    exit 1
}

$rulesPath = Join-Path $scriptDir '..\references\path-rules.json'
$rules     = Get-PathRules -RulesPath $rulesPath

Write-Host 'Repository Structure Audit' -ForegroundColor Cyan
Write-Host '===========================' -ForegroundColor Cyan
Write-Host "Repository : $RepoRoot" -ForegroundColor Gray
Write-Host ('Rules      : v{0}' -f $rules.version) -ForegroundColor Gray
Write-Host ''

$findings = New-Object System.Collections.Generic.List[object]

# Phase 1: Starter shell
Write-Host 'Phase 1: Starter Shell' -ForegroundColor Cyan
$starterIssues = Test-StarterShell -RepoRoot $RepoRoot -Rules $rules
foreach ($issue in $starterIssues) { $findings.Add($issue) }
if ($starterIssues) {
    Write-Host ('  X {0} issue(s)' -f $starterIssues.Count) -ForegroundColor Red
} else {
    Write-Host '  OK Complete' -ForegroundColor Green
}

# Phase 2: Root directory
Write-Host ''
Write-Host 'Phase 2: Root Directory' -ForegroundColor Cyan
$standardRoots = @(
    $rules.root_files.PSObject.Properties.Name
    $rules.root_directories.PSObject.Properties.Name
)
$rootStart = $findings.Count
$skip = @('.vscode','.editorconfig','node_modules','.git','.env')
foreach ($item in (Get-RepoInventory -RepoRoot $RepoRoot)) {
    if ($item.name -in $skip) { continue }
    if ($item.name -notin $standardRoots -and $item.name -notlike '.env.*') {
        $key  = ('/{0}' -f $item.name)
        $rule = $rules.non_standard_paths.($item.name)
        if (-not $rule) { $rule = $rules.non_standard_paths.$key }
        if ($rule) {
            $findings.Add(@{ path=$item.name; type='non_standard'; status='non_standard'; details=$rule.issue; action=$rule.action })
        }
    }
}
$rootNew = $findings.Count - $rootStart
if ($rootNew -eq 0) { Write-Host '  OK Conforms' -ForegroundColor Green }
else                 { Write-Host ('  X {0} non-standard item(s)' -f $rootNew) -ForegroundColor Red }

# Phase 3: .github
Write-Host ''
Write-Host 'Phase 3: .github/' -ForegroundColor Cyan
if (Test-PathExists -RepoRoot $RepoRoot -RelativePath '.github') {
    Write-Host '  OK Present' -ForegroundColor Green
} else {
    Write-Host '  X Missing (required in starter shell)' -ForegroundColor Red
    $findings.Add(@{ path='.github'; type='starter_shell'; status='missing'; details='Required in starter shell' })
}

# Phase 4: docs
Write-Host ''
Write-Host 'Phase 4: /docs' -ForegroundColor Cyan
if (Test-PathExists -RepoRoot $RepoRoot -RelativePath 'docs') {
    $docsPath = Join-Path $RepoRoot 'docs'
    $badDocs  = Get-ChildItem -Path $docsPath -Directory -Force -ErrorAction SilentlyContinue |
                    Where-Object { $rules.docs_structure.PSObject.Properties.Name -notcontains ('docs/{0}' -f $_.Name) }
    if (-not $badDocs) {
        Write-Host '  OK Conforms' -ForegroundColor Green
    } else {
        foreach ($d in $badDocs) {
            $findings.Add(@{ path=('docs/{0}' -f $d.Name); type='docs'; status='non_standard'; details='Not in standard docs structure' })
        }
        Write-Host ('  WARN {0} non-standard docs sub-folder(s)' -f @($badDocs).Count) -ForegroundColor Yellow
    }
} else {
    Write-Host '  X Missing (required in starter shell)' -ForegroundColor Red
    $findings.Add(@{ path='docs'; type='starter_shell'; status='missing'; details='Required in starter shell' })
}

# Summary
Write-Host ''
Write-Host 'Summary' -ForegroundColor Cyan
Write-Host '=======' -ForegroundColor Cyan
$critical = @($findings | Where-Object { $_.type -eq 'starter_shell' }).Count
$warnings  = $findings.Count - $critical
$cColor    = if ($critical -gt 0) { 'Red' }    else { 'Green' }
$wColor    = if ($warnings  -gt 0) { 'Yellow' } else { 'Green' }
Write-Host ('Total   : {0}' -f $findings.Count)
Write-Host ('Critical: {0}' -f $critical) -ForegroundColor $cColor
Write-Host ('Warnings: {0}' -f $warnings)  -ForegroundColor $wColor

if ($findings.Count -gt 0) {
    Write-Host ''
    foreach ($f in $findings) {
        $c = if ($f.type -eq 'starter_shell') { 'Red' } else { 'Yellow' }
        Write-Host ('  [{0}] {1}' -f $f.status, $f.path) -ForegroundColor $c
        if ($f.details) { Write-Host ('    Details : {0}' -f $f.details) -ForegroundColor Gray }
        if ($f.action)  { Write-Host ('    Action  : {0}' -f $f.action)  -ForegroundColor Gray }
    }
}

# Reports
if (-not $DryRun) {
    if ($OutputFormat -in @('json','all')) {
        $p = ('{0}.json' -f $OutputPath)
        New-Item -ItemType Directory -Path (Split-Path $p -Parent) -Force -ErrorAction SilentlyContinue | Out-Null
        Export-Findings -Findings $findings -OutputPath $p
        Write-Host ('  OK JSON     : {0}' -f $p) -ForegroundColor Green
    }
    if ($OutputFormat -in @('markdown','all')) {
        $p = ('{0}.md' -f $OutputPath)
        New-Item -ItemType Directory -Path (Split-Path $p -Parent) -Force -ErrorAction SilentlyContinue | Out-Null
        Export-FindingsMarkdown -Findings $findings -OutputPath $p -RepoRoot $RepoRoot
        Write-Host ('  OK Markdown : {0}' -f $p) -ForegroundColor Green
    }
} else {
    Write-Host ''
    Write-Host 'DRY RUN - reports would write to:' -ForegroundColor Yellow
    Write-Host ('{0}.json' -f $OutputPath) -ForegroundColor Gray
    Write-Host ('{0}.md'   -f $OutputPath) -ForegroundColor Gray
}

if     ($critical -gt 0) { exit 2 }
elseif ($warnings  -gt 0) { exit 1 }
else                       { exit 0 }

<#
.SYNOPSIS
    Generate and optionally execute a reorganization plan for an existing repository.
.PARAMETER RepoRoot
    Repository root to audit and reorganize. Default: current working directory.
.PARAMETER Execute
    Execute the reorganization plan. Without this switch, only a plan is printed.
.PARAMETER ApproveAll
    Skip per-step confirmations when executing. Requires -Execute.
.EXAMPLE
    .\repo-reorganize.ps1 -RepoRoot C:\my-repo
.EXAMPLE
    .\repo-reorganize.ps1 -Execute
.EXAMPLE
    .\repo-reorganize.ps1 -Execute -ApproveAll
#>
param(
    [string]$RepoRoot  = (Get-Location).Path,
    [switch]$Execute,
    [switch]$ApproveAll
)

$scriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent
. (Join-Path $scriptDir '_lib\validators.ps1')

$rulesPath = Join-Path $scriptDir '..\references\path-rules.json'
$rules     = Get-PathRules -RulesPath $rulesPath

Write-Host 'Repository Reorganizer' -ForegroundColor Cyan
Write-Host '======================' -ForegroundColor Cyan
Write-Host ("Root    : {0}" -f $RepoRoot)
if (-not $Execute) { Write-Host '[PLAN ONLY — pass -Execute to make changes]' -ForegroundColor Yellow }
Write-Host ''

# ── Known rename mappings (non-standard name -> standard name) ────────────────
$knownRenames = @{
    'infra' = 'infrastructure'
    'doc'   = 'docs'
}

# ── Collect findings ──────────────────────────────────────────────────────────
$findings = Build-FindingsTable -RepoRoot $RepoRoot -Rules $rules

# ── Map findings to steps ─────────────────────────────────────────────────────
$autoSteps   = [System.Collections.Generic.List[hashtable]]::new()
$manualSteps = [System.Collections.Generic.List[string]]::new()

foreach ($finding in $findings) {
    if ($finding.status -eq 'ok') { continue }

    $path = $finding.path

    # Missing starter-shell files → scaffold
    if ($finding.type -eq 'missing') {
        $autoSteps.Add(@{
            type        = 'scaffold'
            description = ('Create missing starter-shell file: {0}' -f $path)
            target      = $path
        })
        continue
    }

    # Non-standard top-level directory with a known rename
    if ($finding.type -eq 'non_standard') {
        $dirName = Split-Path $path -Leaf
        if ($knownRenames.ContainsKey($dirName)) {
            $newName = $knownRenames[$dirName]
            $newPath = Join-Path (Split-Path $path -Parent) $newName
            $autoSteps.Add(@{
                type        = 'rename'
                description = ("Rename '{0}' to '{1}'" -f $path, $newPath)
                source      = $path
                target      = $newPath
            })
            continue
        }
    }

    # Everything else requires human judgment
    $details = $finding.details
    if (-not $details) { $details = '(no details)' }
    $manualSteps.Add(('{0} [{1}]: {2}' -f $path, $finding.type, $details))
}

# ── Print plan ────────────────────────────────────────────────────────────────
Write-Host ("Automated steps ({0}):" -f $autoSteps.Count) -ForegroundColor Cyan
if ($autoSteps.Count -eq 0) {
    Write-Host '  (none)' -ForegroundColor Gray
} else {
    $i = 1
    foreach ($step in $autoSteps) {
        Write-Host ("  [{0}] [{1}] {2}" -f $i, $step.type.ToUpper(), $step.description)
        $i++
    }
}

Write-Host ''
Write-Host ("Manual steps ({0}):" -f $manualSteps.Count) -ForegroundColor Yellow
if ($manualSteps.Count -eq 0) {
    Write-Host '  (none)' -ForegroundColor Gray
} else {
    foreach ($step in $manualSteps) {
        Write-Host ("  - {0}" -f $step)
    }
}

if (-not $Execute) {
    Write-Host ''
    Write-Host 'Plan complete. Pass -Execute to apply automated steps.' -ForegroundColor Gray
    exit 0
}

# ── Execute automated steps ───────────────────────────────────────────────────
Write-Host ''
Write-Host 'Executing automated steps...' -ForegroundColor Cyan

$succeeded = 0
$failed    = 0
$i = 1

foreach ($step in $autoSteps) {
    Write-Host ''
    Write-Host ("Step [{0}/{1}]: {2}" -f $i, $autoSteps.Count, $step.description) -ForegroundColor White

    if (-not $ApproveAll) {
        $confirm = Read-Host "  Apply this step? [y/N]"
        if ($confirm -notmatch '^[Yy]') {
            Write-Host '  Skipped.' -ForegroundColor Gray
            $i++
            continue
        }
    }

    try {
        if ($step.type -eq 'scaffold') {
            $scaffoldScript = Join-Path $scriptDir 'repo-scaffold.ps1'
            & $scaffoldScript -TargetPath $RepoRoot
            $succeeded++
        } elseif ($step.type -eq 'rename') {
            $sourceFull = Join-Path $RepoRoot $step.source
            $targetFull = Join-Path $RepoRoot $step.target
            if (Test-Path $sourceFull) {
                Move-Item -Path $sourceFull -Destination $targetFull -ErrorAction Stop
                Write-Host ('  OK Moved: {0} -> {1}' -f $step.source, $step.target) -ForegroundColor Green
            } else {
                Write-Host ('  -- Source not found: {0}' -f $step.source) -ForegroundColor Gray
            }
            $succeeded++
        }
    } catch {
        Write-Host ("  X  Failed: {0}" -f $_) -ForegroundColor Red
        $failed++
    }

    $i++
}

Write-Host ''
Write-Host ("Completed: {0} succeeded, {1} failed" -f $succeeded, $failed)

if ($manualSteps.Count -gt 0) {
    Write-Host ''
    Write-Host ("Manual steps still require attention ({0} items above)." -f $manualSteps.Count) -ForegroundColor Yellow
}

if ($failed -gt 0) { exit 1 }
exit 0

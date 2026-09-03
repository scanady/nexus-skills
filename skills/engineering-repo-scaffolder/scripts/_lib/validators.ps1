<#
.SYNOPSIS
Shared validation and utility functions for engineering-repo-scaffolder scripts.

.DESCRIPTION
Provides reusable functions for path checking, rule loading, findings generation, and reporting.
#>

# Load path rules from JSON
function Get-PathRules {
    param(
        [string]$RulesPath = "$PSScriptRoot\..\references\path-rules.json"
    )
    
    if (-not (Test-Path $RulesPath)) {
        throw "Path rules file not found: $RulesPath"
    }
    
    return Get-Content -Path $RulesPath -Raw | ConvertFrom-Json
}

# Check if a path exists relative to a repo root
function Test-PathExists {
    param(
        [string]$RepoRoot,
        [string]$RelativePath
    )
    
    $fullPath = Join-Path -Path $RepoRoot -ChildPath $RelativePath
    return Test-Path -Path $fullPath
}

# Get normalized path status
function Get-PathStatus {
    param(
        [string]$RepoRoot,
        [string]$RelativePath,
        [string]$StandardLocation
    )
    
    $exists = Test-PathExists -RepoRoot $RepoRoot -RelativePath $RelativePath
    
    if (-not $exists) {
        return "missing"
    }
    elseif ($RelativePath -eq $StandardLocation) {
        return "correct"
    }
    else {
        return "misplaced"
    }
}

# Inventory top-level items in repo
function Get-RepoInventory {
    param(
        [string]$RepoRoot,
        [int]$Depth = 3
    )
    
    if (-not (Test-Path -Path $RepoRoot -PathType Container)) {
        throw "Repository root not found: $RepoRoot"
    }
    
    $items = @()
    
    Get-ChildItem -Path $RepoRoot -Force | ForEach-Object {
        $relativePath = $_.Name
        $type = if ($_.PSIsContainer) { "folder" } else { "file" }
        
        $items += @{
            name     = $_.Name
            path     = $relativePath
            type     = $type
            fullPath = $_.FullName
        }
    }
    
    return $items
}

# Find non-standard paths in repo
function Find-NonStandardPaths {
    param(
        [string]$RepoRoot,
        [object]$Rules
    )
    
    $standardRoots = @(
        $Rules.root_files.PSObject.Properties.Name | ForEach-Object { $_ }
        $Rules.root_directories.PSObject.Properties.Name | ForEach-Object { $_ }
    )
    
    $nonStandard = @()
    
    Get-ChildItem -Path $RepoRoot -Force | Where-Object { $_.Name -notlike ".*" -or $_.Name -eq ".github" -or $_.Name -eq ".agents" -or $_.Name -eq ".gitignore" -or $_.Name -eq ".gitkeep" } | ForEach-Object {
        $name = $_.Name
        if ($name -notin $standardRoots -and $name -ne ".gitignore" -and $name -ne ".env" -and $name -ne ".vscode" -and $name -ne ".editorconfig") {
            if ($Rules.non_standard_paths.PSObject.Properties.Name -contains $name -or $Rules.non_standard_paths.PSObject.Properties.Name -contains "/$name") {
                $nonStandard += @{
                    name = $name
                    type = if ($_.PSIsContainer) { "folder" } else { "file" }
                }
            }
        }
    }
    
    return $nonStandard
}

# Verify starter shell completeness
function Test-StarterShell {
    param(
        [string]$RepoRoot,
        [object]$Rules
    )

    $findings = @()
    $projectName = Split-Path $RepoRoot -Leaf

    foreach ($path in $Rules.starter_shell.paths) {
        $resolvedPath = $path.Replace('{project-name}', $projectName)
        if (-not (Test-PathExists -RepoRoot $RepoRoot -RelativePath $resolvedPath)) {
            $findings += @{
                path   = $resolvedPath
                status = "missing"
                type   = "starter_shell"
            }
        }
        else {
            # Verify file has content
            $fullPath = Join-Path -Path $RepoRoot -ChildPath $resolvedPath
            if (($resolvedPath -notlike '*.gitkeep') -and ((Get-Item -Path $fullPath).Length -eq 0)) {
                $findings += @{
                    path   = $resolvedPath
                    status = "empty"
                    type   = "starter_shell"
                }
            }
        }
    }

    # Verify declared symlinks exist, are links/reparse points, and resolve to the
    # declared target. On Windows the scaffolder creates a directory junction (still
    # a reparse point) rather than an NTFS symlink; both surface as ReparsePoint here.
    if ($Rules.starter_shell.PSObject.Properties.Name -contains 'symlinks') {
        foreach ($prop in $Rules.starter_shell.symlinks.PSObject.Properties) {
            $linkPath = $prop.Name
            $expectedTarget = $prop.Value
            $fullPath = Join-Path -Path $RepoRoot -ChildPath $linkPath
            $item = Get-Item -LiteralPath $fullPath -Force -ErrorAction SilentlyContinue
            if ($null -eq $item) {
                $findings += @{
                    path   = $linkPath
                    status = "missing"
                    type   = "starter_shell"
                    details = "symlink to $expectedTarget"
                }
                continue
            }
            $isReparse = ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0
            if (-not $isReparse) {
                $findings += @{
                    path   = $linkPath
                    status = "not-a-link"
                    type   = "starter_shell"
                    details = "expected symlink or junction to $expectedTarget"
                }
                continue
            }
            $actualTarget = $item.Target
            if ($actualTarget -is [array]) { $actualTarget = $actualTarget[0] }
            if ($actualTarget) {
                $normalized = ($actualTarget -replace '/', '\').TrimEnd('\')
                $expectedNorm = ($expectedTarget -replace '/', '\').TrimEnd('\')
                # Match either the relative form we set, or an absolute path Windows may report.
                if ($normalized -ne $expectedNorm -and $normalized -notlike "*\.agents\skills") {
                    $findings += @{
                        path   = $linkPath
                        status = "wrong-target"
                        type   = "starter_shell"
                        details = "expected $expectedTarget, got $actualTarget"
                    }
                }
            }
        }
    }

    return $findings
}

# Build audit findings table
function Build-FindingsTable {
    param(
        [object[]]$Findings
    )
    
    $table = @()
    
    foreach ($finding in $Findings) {
        $table += $finding
    }
    
    return $table | Sort-Object -Property path
}

# Export findings to JSON
function Export-Findings {
    param(
        [object[]]$Findings,
        [string]$OutputPath
    )
    
    $output = @{
        timestamp = (Get-Date -Format 'o')
        findingCount = $Findings.Count
        findings = $Findings
    }
    
    $output | ConvertTo-Json -Depth 10 | Out-File -Path $OutputPath -Encoding UTF8
}

# Export findings to Markdown
function Export-FindingsMarkdown {
    param(
        [object[]]$Findings,
        [string]$OutputPath,
        [string]$RepoRoot
    )
    
    $md = @"
# Repository Structure Audit

**Repository:** $RepoRoot
**Generated:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## Summary

- Total Findings: $($Findings.Count)
- Missing Items: $(@($Findings | Where-Object { $_.status -eq 'missing' }).Count)
- Misplaced Items: $(@($Findings | Where-Object { $_.status -eq 'misplaced' }).Count)
- Non-Standard Paths: $(@($Findings | Where-Object { $_.type -eq 'non_standard' }).Count)

## Detailed Findings

"@

    # Group by type
    $byType = $Findings | Group-Object -Property type
    
    foreach ($group in $byType) {
        $md += "`n### $($group.Name)`n`n"
        $md += "| Path | Status | Details |`n"
        $md += "|------|--------|---------|`n"
        
        foreach ($item in $group.Group) {
            $status = $item.status -or "review"
            $details = $item.details -or "-"
            $md += "| ``$($item.path)`` | $status | $details |`n"
        }
    }
    
    $md | Out-File -Path $OutputPath -Encoding UTF8
}

# Format output table for display
function Format-AuditTable {
    param(
        [object[]]$Findings
    )
    
    return $Findings | Select-Object -Property path, type, status, details | Format-Table -AutoSize
}



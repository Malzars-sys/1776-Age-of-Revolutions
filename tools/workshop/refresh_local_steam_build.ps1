[CmdletBinding()]
param([Parameter(Mandatory)][string]$PreparedBuild)

# Install a previously validated package locally. Never uploads to Steam or edits Git.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$source = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
$victoriaRoot = Split-Path -Parent (Split-Path -Parent $source)
$workshopRoot = Join-Path $victoriaRoot 'workshop_build'
$primary = Join-Path $workshopRoot 'Age_of_Revolution_Fork'
$mirror = Join-Path $victoriaRoot 'mod\Age of revolution Fork [Steam Build]'
$prepared = (Resolve-Path -LiteralPath $PreparedBuild).Path.TrimEnd('\')
$stats = Get-Content -LiteralPath "$prepared.build-stats.json" -Raw | ConvertFrom-Json
$records = @(Import-Csv -LiteralPath "$prepared.build-filelist.csv")

function Assert-PlainDirectory([string]$Path) {
    $resolved = (Resolve-Path -LiteralPath $Path).Path.TrimEnd('\')
    if ($resolved -ne [IO.Path]::GetFullPath($Path).TrimEnd('\')) { throw "Unexpected resolved path: $Path" }
    $items = @((Get-Item -LiteralPath $Path)) + @(Get-ChildItem -LiteralPath $Path -Recurse -Force)
    if (@($items | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
        throw "Refusing links or junctions in: $Path"
    }
}

function Get-ContainedFile([string]$Root, [string]$Relative) {
    $full = [IO.Path]::GetFullPath((Join-Path $Root $Relative))
    if (-not $full.StartsWith($Root.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "File outside expected directory: $Relative"
    }
    return $full
}

function Assert-Package([string]$Root, [bool]$CustomizedName = $false) {
    $files = @(Get-ChildItem -LiteralPath $Root -Recurse -Force -File)
    if ($files.Count -ne $records.Count) { throw "Package file count mismatch: $Root" }
    foreach ($record in $records) {
        if ($CustomizedName -and $record.relative_path -eq '.metadata/metadata.json') { continue }
        $file = Get-ContainedFile $Root $record.relative_path
        if ((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash -ne $record.sha256) {
            throw "Package hash mismatch: $($record.relative_path)"
        }
    }
}

if ($stats.source_root -ne $source -or $stats.build_path -ne $prepared -or
    $stats.files_hash_mismatch -ne 0 -or $stats.development_pollution_found -ne 0 -or
    $stats.potential_secret_hits -ne 0 -or $stats.local_developer_path_leaks -ne 0 -or
    $stats.steam_package_file_count -ne $records.Count) { throw 'Prepared package has not passed validation.' }
Assert-PlainDirectory $prepared
Assert-Package $prepared
Write-Output 'Prepared package verified.'
# Refuse installation if a runtime source changed after preparation.
foreach ($record in $records) {
    $file = Get-ContainedFile $source $record.relative_path
    if ((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash -ne $record.sha256) {
        throw "Source changed since packaging: $($record.relative_path)"
    }
}
Write-Output 'Current runtime sources verified.'
$owner = Get-Content -LiteralPath "$primary.build-owner.json" -Raw | ConvertFrom-Json
if ($owner.generator -ne 'WORKSHOP_PREP_3' -or $owner.source_root -ne $source -or $owner.build_path -ne $primary) {
    throw 'Existing primary build ownership does not match.'
}
Assert-PlainDirectory $primary
Assert-PlainDirectory $mirror
$stamp = (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0, 8)
$backup = Join-Path $workshopRoot "backups\steam-refresh-$stamp"
$jobs = @(
    [pscustomobject]@{ target = $primary; label = 'workshop-package'; customize_name = $false },
    [pscustomobject]@{ target = $mirror; label = 'mod-steam-build'; customize_name = $true }
)

# Both incoming copies are completely verified before touching either installed copy.
foreach ($job in $jobs) {
    $incoming = "$($job.target).incoming-$stamp"
    if (Test-Path -LiteralPath $incoming) { throw "Incoming path already exists: $incoming" }
    $metadata = Get-Content -LiteralPath (Join-Path $job.target '.metadata\metadata.json') -Raw | ConvertFrom-Json
    $newMetadata = Get-Content -LiteralPath (Join-Path $prepared '.metadata\metadata.json') -Raw | ConvertFrom-Json
    if ($metadata.id -ne $newMetadata.id) { throw "Publication association differs: $($job.target)" }
    [void](New-Item -ItemType Directory -Path $incoming)
    foreach ($child in Get-ChildItem -LiteralPath $prepared -Force) {
        Copy-Item -LiteralPath $child.FullName -Destination $incoming -Recurse
    }
    if ($job.customize_name) {
        $newMetadata.name = $metadata.name
        $newMetadata | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath (Join-Path $incoming '.metadata\metadata.json') -Encoding UTF8
    }
    Assert-PlainDirectory $incoming
    Assert-Package $incoming $job.customize_name
    $job | Add-Member NoteProperty incoming $incoming
    $job | Add-Member NoteProperty backup (Join-Path $backup $job.label)
    Write-Output "Incoming package verified: $($job.label)"
}

[void](New-Item -ItemType Directory -Path $backup)
Assert-PlainDirectory $backup
foreach ($suffix in @('build-owner.json', 'build-stats.json', 'final-stats.json', 'build-filelist.csv', 'preclean-manifest.csv')) {
    $sidecar = "$primary.$suffix"
    if (Test-Path -LiteralPath $sidecar) { Copy-Item -LiteralPath $sidecar -Destination $backup }
}
foreach ($job in $jobs) {
    # Exact absolute targets, checked again immediately before the recoverable move.
    if ($job.target -notin @($primary, $mirror) -or
        -not $job.backup.StartsWith($backup + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Unsafe installation target.' }
    Assert-PlainDirectory $job.target
    Move-Item -LiteralPath $job.target -Destination $job.backup
    try { Move-Item -LiteralPath $job.incoming -Destination $job.target }
    catch {
        if (-not (Test-Path -LiteralPath $job.target)) { Move-Item -LiteralPath $job.backup -Destination $job.target }
        throw
    }
    Assert-Package $job.target $job.customize_name
    Write-Output "Local package installed and verified: $($job.label)"
}
$stats.build_path = $primary
$stats.generated_utc = [DateTime]::UtcNow.ToString('o')
$stats | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath "$primary.build-stats.json" -Encoding UTF8
$stats | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath "$primary.final-stats.json" -Encoding UTF8
Copy-Item -LiteralPath "$prepared.build-filelist.csv" -Destination "$primary.build-filelist.csv" -Force
[pscustomobject]@{
    updated_utc = $stats.generated_utc
    source_root = $source
    primary = $primary
    mirror = $mirror
    backup = $backup
    files_per_package = $records.Count
    package_size_bytes = $stats.steam_package_size_bytes
    hash_mismatches = 0
    publication_performed = $false
} | ConvertTo-Json | Tee-Object -Variable refreshReport | Set-Content -LiteralPath (Join-Path $backup 'refresh-report.json') -Encoding UTF8
Write-Output $refreshReport

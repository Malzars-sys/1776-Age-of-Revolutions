[CmdletBinding()]
param([string]$PreviousVersion = '2.4.0', [string]$Version = '2.5.0')

# A narrowly scoped mechanical update: preserve every byte except the version value.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$source = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
$victoria = Split-Path -Parent (Split-Path -Parent $source)
$primary = Join-Path $victoria 'workshop_build\Age_of_Revolution_Fork'
$mirror = Join-Path $victoria 'mod\Age of revolution Fork [Steam Build]'
$sourceMetadata = Get-Content -LiteralPath (Join-Path $source '.metadata\metadata.json') -Raw | ConvertFrom-Json
if ($sourceMetadata.version -ne $Version) { throw 'Source version must already match the requested release.' }
$owner = Get-Content -LiteralPath "$primary.build-owner.json" -Raw | ConvertFrom-Json
if ($owner.source_root -ne $source -or $owner.build_path -ne $primary) { throw 'Unexpected Steam Build ownership.' }
$changes = @()
foreach ($root in @($primary, $mirror)) {
    $path = Join-Path $root '.metadata\metadata.json'
    if ((Resolve-Path -LiteralPath $path).Path -ne $path) { throw "Unexpected metadata path: $path" }
    $bytes = [IO.File]::ReadAllBytes($path)
    $text = [Text.Encoding]::UTF8.GetString($bytes)
    $pattern = '"version"\s*:\s*"' + [regex]::Escape($PreviousVersion) + '"'
    $matches = [regex]::Matches($text, $pattern)
    if ($matches.Count -ne 1) { throw "Expected exactly one old version field: $path" }
    $replacement = $matches[0].Value.Replace('"' + $PreviousVersion + '"', '"' + $Version + '"')
    $updated = $text.Remove($matches[0].Index, $matches[0].Length).Insert($matches[0].Index, $replacement)
    $before = $text.TrimStart([char]0xFEFF) | ConvertFrom-Json
    $after = $updated.TrimStart([char]0xFEFF) | ConvertFrom-Json
    $before.version = $Version
    if (($before | ConvertTo-Json -Depth 20 -Compress) -ne ($after | ConvertTo-Json -Depth 20 -Compress)) {
        throw "Unexpected change beyond version: $path"
    }
    $changes += [pscustomobject]@{ path = $path; bytes = $bytes; updated = [Text.Encoding]::UTF8.GetBytes($updated) }
}
$backup = Join-Path $victoria ('workshop_build\backups\version-' + $Version + '-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
if (Test-Path -LiteralPath $backup) { throw 'Version backup already exists.' }
[void](New-Item -ItemType Directory -Path $backup)
$index = 0
foreach ($change in $changes) {
    [IO.File]::WriteAllBytes((Join-Path $backup "metadata-$index.json"), $change.bytes)
    [IO.File]::WriteAllBytes($change.path, $change.updated)
    $check = Get-Content -LiteralPath $change.path -Raw | ConvertFrom-Json
    if ($check.version -ne $Version) { throw "Version verification failed: $($change.path)" }
    $index++
}
# Keep the publishing copy byte-identical to source metadata (including line endings).
$primaryMetadata = Get-Content -LiteralPath (Join-Path $primary '.metadata\metadata.json') -Raw | ConvertFrom-Json
if (($primaryMetadata | ConvertTo-Json -Depth 20 -Compress) -ne ($sourceMetadata | ConvertTo-Json -Depth 20 -Compress)) {
    throw 'Publishing metadata differs from source beyond formatting.'
}
Copy-Item -LiteralPath (Join-Path $source '.metadata\metadata.json') -Destination (Join-Path $primary '.metadata\metadata.json') -Force
# Refresh the package inventory so a later installation audit remains accurate.
Copy-Item -LiteralPath "$primary.build-filelist.csv" -Destination $backup
$records = @(Import-Csv -LiteralPath "$primary.build-filelist.csv")
foreach ($record in $records) {
    if ($record.relative_path -eq '.metadata/metadata.json') {
        $path = Join-Path $primary $record.relative_path
        $record.sha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
        $record.size_bytes = (Get-Item -LiteralPath $path).Length
    }
}
$records | Export-Csv -LiteralPath "$primary.build-filelist.csv" -NoTypeInformation -Encoding UTF8
foreach ($suffix in @('build-stats.json', 'final-stats.json')) {
    $statsPath = "$primary.$suffix"
    Copy-Item -LiteralPath $statsPath -Destination $backup
    $stats = Get-Content -LiteralPath $statsPath -Raw | ConvertFrom-Json
    $stats.generated_utc = [DateTime]::UtcNow.ToString('o')
    $stats.steam_package_size_bytes = [int64](($records | Measure-Object size_bytes -Sum).Sum)
    $stats | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $statsPath -Encoding UTF8
}
Write-Output "VERSION=$Version"
Write-Output 'SOURCE_AND_TWO_STEAM_BUILDS_MATCH=yes'
Write-Output "BACKUP=$backup"

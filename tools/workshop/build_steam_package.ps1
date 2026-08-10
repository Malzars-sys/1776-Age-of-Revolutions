[CmdletBinding()]
param(
    [string]$SourceRoot = '',
    [string]$ManifestPath = '',
    [string]$BuildPath = 'C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\workshop_build\Age_of_Revolution_Fork',
    [string]$OutputFileList = '',
    [string]$OutputStats = ''
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if ([string]::IsNullOrWhiteSpace($SourceRoot)) {
    $SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
}
if ([string]::IsNullOrWhiteSpace($ManifestPath)) {
    $ManifestPath = Join-Path $SourceRoot 'docs\workshop\WORKSHOP_SHIPPING_MANIFEST.csv'
}
if ([string]::IsNullOrWhiteSpace($OutputFileList)) {
    $OutputFileList = "$BuildPath.build-filelist.csv"
}
if ([string]::IsNullOrWhiteSpace($OutputStats)) {
    $OutputStats = "$BuildPath.build-stats.json"
}

function Get-FullPath {
    param([Parameter(Mandatory)][string]$Path)
    return [System.IO.Path]::GetFullPath($Path).TrimEnd('\')
}

function Get-RelativePathNormalized {
    param(
        [Parameter(Mandatory)][string]$BasePath,
        [Parameter(Mandatory)][string]$Path
    )
    $baseFull = (Get-FullPath $BasePath) + '\'
    $pathFull = Get-FullPath $Path
    $baseUri = [System.Uri]::new($baseFull)
    $pathUri = [System.Uri]::new($pathFull)
    return [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($pathUri).ToString()).Replace('\', '/')
}

function Test-PathInside {
    param(
        [Parameter(Mandatory)][string]$Parent,
        [Parameter(Mandatory)][string]$Child
    )
    $parentFull = (Get-FullPath $Parent) + '\'
    $childFull = Get-FullPath $Child
    return $childFull.StartsWith($parentFull, [System.StringComparison]::OrdinalIgnoreCase)
}

function Test-ForbiddenPayloadPath {
    param([Parameter(Mandatory)][string]$RelativePath)

    $normalized = $RelativePath.Replace('\', '/').TrimStart('/')
    $segments = $normalized.Split('/', [System.StringSplitOptions]::RemoveEmptyEntries)
    $forbiddenRoots = @('.git', '.github', '.metadata', 'docs', 'workshop_assets', '.agents', 'victoria3')
    if ($segments.Count -gt 0 -and $segments[0] -in $forbiddenRoots) { return $true }

    $leaf = [System.IO.Path]::GetFileName($normalized)
    if ($leaf -in @('.gitignore', 'Changelog.txt', 'Source.txt')) { return $true }

    $extension = [System.IO.Path]::GetExtension($normalized).ToLowerInvariant()
    if ($extension -in @('.ps1', '.py', '.bat', '.cmd', '.csv', '.md', '.log', '.tmp', '.bak', '.old', '.tif', '.tiff', '.jpg', '.jpeg', '.mp3', '.zip', '.rar', '.7z')) {
        return $true
    }

    return $false
}

function Get-FileSha256 {
    param([Parameter(Mandatory)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

$sourceRootFull = Get-FullPath $SourceRoot
$manifestFull = Get-FullPath $ManifestPath
$buildFull = Get-FullPath $BuildPath
$buildParent = Split-Path -Parent $buildFull
$ownerPath = "$buildFull.build-owner.json"
$precleanManifestPath = "$buildFull.preclean-manifest.csv"

if (-not (Test-Path -LiteralPath $sourceRootFull -PathType Container)) {
    throw "SOURCE_ROOT_NOT_FOUND: $sourceRootFull"
}
if (-not (Test-Path -LiteralPath $manifestFull -PathType Leaf)) {
    throw "SHIPPING_MANIFEST_NOT_FOUND: $manifestFull"
}
if ((Split-Path -Leaf $buildFull) -ne 'Age_of_Revolution_Fork' -or (Split-Path -Leaf $buildParent) -ne 'workshop_build') {
    throw "UNSAFE_BUILD_PATH: expected workshop_build\Age_of_Revolution_Fork, got $buildFull"
}
if ($buildFull -eq $sourceRootFull -or (Test-PathInside -Parent $sourceRootFull -Child $buildFull)) {
    throw "UNSAFE_BUILD_PATH_INSIDE_SOURCE: $buildFull"
}

if (-not (Test-Path -LiteralPath $buildParent -PathType Container)) {
    [void](New-Item -ItemType Directory -Path $buildParent)
}

if (Test-Path -LiteralPath $buildFull) {
    if (-not (Test-Path -LiteralPath $ownerPath -PathType Leaf)) {
        throw "BLOCKED_EXISTING_UNKNOWN_WORKSHOP_BUILD: missing owner marker $ownerPath"
    }

    $owner = Get-Content -LiteralPath $ownerPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($owner.generator -ne 'WORKSHOP_PREP_3' -or
        (Get-FullPath $owner.source_root) -ne $sourceRootFull -or
        (Get-FullPath $owner.build_path) -ne $buildFull) {
        throw "BLOCKED_EXISTING_UNKNOWN_WORKSHOP_BUILD: owner marker does not match this source/build"
    }

    $resolvedBuild = (Resolve-Path -LiteralPath $buildFull).Path.TrimEnd('\')
    if ($resolvedBuild -ne $buildFull) {
        throw "UNSAFE_RESOLVED_BUILD_PATH: $resolvedBuild"
    }

    $preclean = Get-ChildItem -LiteralPath $buildFull -Recurse -Force -File | ForEach-Object {
        [pscustomobject]@{
            relative_path = Get-RelativePathNormalized -BasePath $buildFull -Path $_.FullName
            size_bytes = $_.Length
            sha256 = Get-FileSha256 -Path $_.FullName
        }
    }
    $preclean | Sort-Object relative_path | Export-Csv -LiteralPath $precleanManifestPath -NoTypeInformation -Encoding UTF8

    Get-ChildItem -LiteralPath $buildFull -Force | ForEach-Object {
        if (-not (Test-PathInside -Parent $buildFull -Child $_.FullName)) {
            throw "REFUSING_TO_REMOVE_OUTSIDE_BUILD: $($_.FullName)"
        }
        Remove-Item -LiteralPath $_.FullName -Recurse -Force
    }
} else {
    [void](New-Item -ItemType Directory -Path $buildFull)
}

[pscustomobject]@{
    generator = 'WORKSHOP_PREP_3'
    source_root = $sourceRootFull
    build_path = $buildFull
} | ConvertTo-Json | Set-Content -LiteralPath $ownerPath -Encoding UTF8

$manifest = Import-Csv -LiteralPath $manifestFull
$shipEntries = @($manifest | Where-Object { $_.ship_to_workshop -eq 'YES' })
if ($shipEntries.Count -eq 0) { throw 'SHIPPING_MANIFEST_HAS_NO_SHIP_ENTRIES' }

$candidates = [System.Collections.Generic.List[object]]::new()
$manifestExcluded = [System.Collections.Generic.List[object]]::new()

foreach ($entry in $shipEntries) {
    $manifestRelative = $entry.path_or_pattern.TrimEnd('/', '\')
    $sourcePath = Get-FullPath (Join-Path $sourceRootFull $manifestRelative)
    if (-not (Test-PathInside -Parent $sourceRootFull -Child $sourcePath) -and $sourcePath -ne $sourceRootFull) {
        throw "MANIFEST_PATH_OUTSIDE_SOURCE: $manifestRelative"
    }
    if (-not (Test-Path -LiteralPath $sourcePath)) {
        throw "MANIFEST_SOURCE_MISSING: $manifestRelative"
    }

    $files = if (Test-Path -LiteralPath $sourcePath -PathType Container) {
        @(Get-ChildItem -LiteralPath $sourcePath -Recurse -Force -File)
    } else {
        @((Get-Item -LiteralPath $sourcePath))
    }

    foreach ($file in $files) {
        if ($file.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
            throw "REPARSE_POINT_REFUSED: $($file.FullName)"
        }
        $relative = Get-RelativePathNormalized -BasePath $sourceRootFull -Path $file.FullName
        if (Test-ForbiddenPayloadPath -RelativePath $relative) {
            $manifestExcluded.Add([pscustomobject]@{
                relative_path = $relative
                reason = 'forbidden development/documentation file type inside a SHIP directory'
            })
            continue
        }
        $candidates.Add([pscustomobject]@{
            relative_path = $relative
            source_path = $file.FullName
            classification = $entry.classification
        })
    }
}

$duplicatePaths = $candidates | Group-Object relative_path | Where-Object Count -gt 1
if ($duplicatePaths) {
    throw "DUPLICATE_PACKAGE_PATHS: $($duplicatePaths.Name -join ', ')"
}

$copyRecords = [System.Collections.Generic.List[object]]::new()
$hashMismatches = 0
foreach ($candidate in ($candidates | Sort-Object relative_path)) {
    $destination = Join-Path $buildFull $candidate.relative_path.Replace('/', '\')
    $destinationDirectory = Split-Path -Parent $destination
    if (-not (Test-Path -LiteralPath $destinationDirectory -PathType Container)) {
        [void](New-Item -ItemType Directory -Path $destinationDirectory)
    }
    Copy-Item -LiteralPath $candidate.source_path -Destination $destination

    $sourceHash = Get-FileSha256 -Path $candidate.source_path
    $destinationHash = Get-FileSha256 -Path $destination
    if ($sourceHash -ne $destinationHash) { $hashMismatches++ }

    $copyRecords.Add([pscustomobject]@{
        relative_path = $candidate.relative_path
        size_bytes = (Get-Item -LiteralPath $destination).Length
        sha256 = $destinationHash
        classification = $candidate.classification
        source_path = $candidate.relative_path
    })
}

$copyRecords | Export-Csv -LiteralPath $OutputFileList -NoTypeInformation -Encoding UTF8

$packageFiles = @(Get-ChildItem -LiteralPath $buildFull -Recurse -Force -File)
$pollution = @($packageFiles | Where-Object {
    Test-ForbiddenPayloadPath -RelativePath (Get-RelativePathNormalized -BasePath $buildFull -Path $_.FullName)
})
if ($pollution.Count -gt 0) {
    throw "DEVELOPMENT_POLLUTION_FOUND: $($pollution.FullName -join ', ')"
}

$descriptorPath = Join-Path $buildFull 'descriptor.mod'
$descriptorText = Get-Content -LiteralPath $descriptorPath -Raw -Encoding UTF8
if ($descriptorText -notmatch 'supported_version="1\.13\.\*"') { throw 'DESCRIPTOR_SUPPORTED_VERSION_INVALID' }
if ($descriptorText -match 'remote_file_id|publishedfileid') { throw 'NEW_FORK_WORKSHOP_ID_PRESENT' }

$thumbnailPath = Join-Path $buildFull 'thumbnail.png'
$thumbnailHash = Get-FileSha256 -Path $thumbnailPath
if ($thumbnailHash -ne 'c1d4a6d56849182a00b2474b3ba71c745216fb6a23c498b7fea0efde57c3cf5c') {
    throw "BLOCKED_THUMBNAIL_HASH_MISMATCH: $thumbnailHash"
}
Add-Type -AssemblyName System.Drawing
$thumbnail = [System.Drawing.Image]::FromFile($thumbnailPath)
try {
    if ($thumbnail.Width -ne 600 -or $thumbnail.Height -ne 600 -or $thumbnail.RawFormat.Guid -ne [System.Drawing.Imaging.ImageFormat]::Png.Guid) {
        throw "THUMBNAIL_FORMAT_OR_DIMENSIONS_INVALID: $($thumbnail.Width)x$($thumbnail.Height)"
    }
} finally {
    $thumbnail.Dispose()
}

$textExtensions = @('.txt', '.yml', '.yaml', '.gui', '.asset', '.mod')
$secretPatterns = @(
    '(?i)\b(token|password|api[_-]?key)\b\s*[:=]',
    '(?i)\bauthorization\s*:',
    '(?i)\bprivate-user\b'
)
$secretHits = [System.Collections.Generic.List[string]]::new()
$localPathHits = [System.Collections.Generic.List[string]]::new()
$workshopIdHits = [System.Collections.Generic.List[string]]::new()

foreach ($file in $packageFiles) {
    if ($file.Extension.ToLowerInvariant() -notin $textExtensions) { continue }
    $text = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction Stop
    $relative = Get-RelativePathNormalized -BasePath $buildFull -Path $file.FullName
    foreach ($pattern in $secretPatterns) {
        if ($text -match $pattern) { $secretHits.Add("$relative :: $($Matches[0])") }
    }
    if ($text -match '(?i)[A-Z]:\\Users\\') { $localPathHits.Add($relative) }
    if ($text -match '(?i)remote_file_id|publishedfileid|3617930953') { $workshopIdHits.Add($relative) }
}

if ($secretHits.Count -gt 0) { throw "POTENTIAL_SECRET_HITS: $($secretHits -join '; ')" }
if ($localPathHits.Count -gt 0) { throw "LOCAL_DEVELOPER_PATH_LEAKS: $($localPathHits -join '; ')" }
if ($workshopIdHits.Count -gt 0) { throw "WORKSHOP_ID_HITS: $($workshopIdHits -join '; ')" }

$allSourceFiles = @(Get-ChildItem -LiteralPath $sourceRootFull -Recurse -Force -File)
$packageRelativeSet = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
foreach ($record in $copyRecords) { [void]$packageRelativeSet.Add($record.relative_path) }

$sourceInventory = foreach ($file in $allSourceFiles) {
    $relative = Get-RelativePathNormalized -BasePath $sourceRootFull -Path $file.FullName
    $classification = if ($relative -like '.git/*') {
        'GIT_METADATA'
    } elseif ($relative -like 'docs/*') {
        'DOCUMENTATION'
    } elseif ($relative -like 'workshop_assets/source/*') {
        'WORKSHOP_SOURCE_ASSET'
    } elseif ($relative -like 'workshop_assets/previews/*') {
        'WORKSHOP_PREVIEW'
    } elseif ($file.Extension.ToLowerInvariant() -in @('.ps1', '.py', '.bat', '.cmd')) {
        'DEVELOPMENT_SCRIPT'
    } elseif ($packageRelativeSet.Contains($relative)) {
        'REQUIRED_RUNTIME'
    } else {
        'OTHER_EXCLUDED_DEVELOPMENT'
    }
    [pscustomobject]@{
        relative_path = $relative
        size_bytes = $file.Length
        classification = $classification
        ship = if ($packageRelativeSet.Contains($relative)) { 'YES' } else { 'NO' }
    }
}

function Measure-InventoryClass {
    param([Parameter(Mandatory)][string]$Class)
    $items = @($sourceInventory | Where-Object classification -eq $Class)
    return [pscustomobject]@{
        count = $items.Count
        bytes = [int64](($items | Measure-Object size_bytes -Sum).Sum)
    }
}

$docsMeasure = Measure-InventoryClass -Class 'DOCUMENTATION'
$sourcesMeasure = Measure-InventoryClass -Class 'WORKSHOP_SOURCE_ASSET'
$previewsMeasure = Measure-InventoryClass -Class 'WORKSHOP_PREVIEW'
$scriptsMeasure = Measure-InventoryClass -Class 'DEVELOPMENT_SCRIPT'
$gitMeasure = Measure-InventoryClass -Class 'GIT_METADATA'
$otherMeasure = Measure-InventoryClass -Class 'OTHER_EXCLUDED_DEVELOPMENT'

$fullBytes = [int64](($sourceInventory | Measure-Object size_bytes -Sum).Sum)
$packageBytes = [int64](($copyRecords | Measure-Object size_bytes -Sum).Sum)
$excludedBytes = $fullBytes - $packageBytes
$reductionPercent = if ($fullBytes -eq 0) { 0 } else { [math]::Round(($excludedBytes / $fullBytes) * 100, 4) }

$stats = [ordered]@{
    generated_utc = [DateTime]::UtcNow.ToString('o')
    source_root = $sourceRootFull
    build_path = $buildFull
    manifest_path = $manifestFull
    full_working_directory_file_count = $sourceInventory.Count
    full_working_directory_size_bytes = $fullBytes
    documentation_file_count = $docsMeasure.count
    documentation_size_bytes = $docsMeasure.bytes
    workshop_assets_source_file_count = $sourcesMeasure.count
    workshop_assets_source_size_bytes = $sourcesMeasure.bytes
    workshop_previews_file_count = $previewsMeasure.count
    workshop_previews_size_bytes = $previewsMeasure.bytes
    development_scripts_file_count = $scriptsMeasure.count
    development_scripts_size_bytes = $scriptsMeasure.bytes
    git_metadata_file_count = $gitMeasure.count
    git_metadata_size_bytes = $gitMeasure.bytes
    other_excluded_development_file_count = $otherMeasure.count
    other_excluded_development_size_bytes = $otherMeasure.bytes
    steam_package_file_count = $copyRecords.Count
    steam_package_size_bytes = $packageBytes
    excluded_total_size_bytes = $excludedBytes
    space_reduction_bytes = $excludedBytes
    space_reduction_percent = $reductionPercent
    files_copied = $copyRecords.Count
    files_hash_match = $copyRecords.Count - $hashMismatches
    files_hash_mismatch = $hashMismatches
    development_pollution_found = $pollution.Count
    potential_secret_hits = $secretHits.Count
    local_developer_path_leaks = $localPathHits.Count
    new_fork_workshop_id_present = $false
    thumbnail_sha256 = $thumbnailHash
    manifest_excluded_inside_ship_directories = @($manifestExcluded)
    top_30_source_files_by_size = @($sourceInventory | Sort-Object size_bytes -Descending | Select-Object -First 30)
    top_30_steam_files_by_size = @($copyRecords | Sort-Object size_bytes -Descending | Select-Object -First 30 relative_path, size_bytes, classification)
}

$stats | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputStats -Encoding UTF8

Write-Output "STEAM_PACKAGE_CREATED=$buildFull"
Write-Output "FILES_COPIED=$($copyRecords.Count)"
Write-Output "FILES_HASH_MATCH=$($copyRecords.Count - $hashMismatches)"
Write-Output "FILES_HASH_MISMATCH=$hashMismatches"
Write-Output "STEAM_PACKAGE_SIZE_BYTES=$packageBytes"
Write-Output "DEVELOPMENT_POLLUTION_FOUND=$($pollution.Count)"
Write-Output "POTENTIAL_SECRET_HITS=$($secretHits.Count)"
Write-Output "LOCAL_DEVELOPER_PATH_LEAKS=$($localPathHits.Count)"
Write-Output "NEW_FORK_WORKSHOP_ID_PRESENT=no"
Write-Output "MANIFEST_EXCLUDED_INSIDE_SHIP_DIRECTORIES=$($manifestExcluded.Count)"

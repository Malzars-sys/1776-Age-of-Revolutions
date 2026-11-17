param([Parameter(Mandatory=$true)][ValidateSet('A1','B1','B2','A2')][string]$Trial)
$ErrorActionPreference='Stop'
$reportRoot=$PSScriptRoot
$plan=Get-Content -LiteralPath (Join-Path $reportRoot 'PLAN.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$trialProfile=$plan.shared_profile
$arm=$Trial.Substring(0,1)
$modPath=$plan.arms.$arm
if (@(Get-Process -Name victoria3 -ErrorAction SilentlyContinue).Count) { throw 'A Victoria 3 session already exists; preserve it.' }
if ((Get-FileHash -LiteralPath $plan.executable -Algorithm SHA256).Hash.ToLowerInvariant() -ne $plan.executable_sha256) { throw 'Executable changed; do not mix versions.' }
if ((Get-FileHash -LiteralPath (Join-Path $trialProfile 'pdx_settings.json') -Algorithm SHA256).Hash.ToLowerInvariant() -ne $plan.settings_sha256) { throw 'Settings changed; review before measuring.' }
if (Test-Path -LiteralPath (Join-Path $trialProfile 'UI_CAPTURE_REQUEST.json')) { throw 'A previous capture request remains; inspect it.' }
if (Test-Path -LiteralPath (Join-Path $trialProfile 'STOP_TEST_REQUESTED.json')) { throw 'A previous stop request remains; inspect it.' }
$stamp=[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')
$runRoot=Join-Path $reportRoot ($Trial+'_'+$stamp)
[void][IO.Directory]::CreateDirectory($runRoot)
$loadPath=Join-Path $trialProfile 'content_load.json'
$before=[IO.File]::ReadAllText($loadPath)
[IO.File]::WriteAllText((Join-Path $runRoot 'CONTENT_LOAD_BEFORE.json'),$before)
$newLoad=[ordered]@{enabledMods=@(@{path=$modPath});disabledDLC=@();enabledUGC=@()}
[IO.File]::WriteAllText($loadPath,($newLoad | ConvertTo-Json -Depth 5))
$arguments=@(('--userdir='+($trialProfile -replace '\\','/')),'-debug_mode')
$child=Start-Process -FilePath $plan.executable -ArgumentList $arguments -WorkingDirectory (Split-Path -Parent $plan.executable) -WindowStyle Normal -PassThru -RedirectStandardOutput (Join-Path $runRoot 'stdout.txt') -RedirectStandardError (Join-Path $runRoot 'stderr.txt')
[ordered]@{trial=$Trial;arm=$arm;process_id=$child.Id;profile=$trialProfile;mod=$modPath;executable=$plan.executable;executable_sha256=$plan.executable_sha256;arguments=$arguments;started_utc=[DateTime]::UtcNow.ToString('o');startup_cpu_benchmark=$false;normal_profile_written=$false} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $runRoot 'LAUNCH.json') -Encoding UTF8
Get-Content -LiteralPath (Join-Path $runRoot 'LAUNCH.json')
try {
    while (-not $child.HasExited) {
        if (Test-Path -LiteralPath (Join-Path $trialProfile 'STOP_TEST_REQUESTED.json')) { break }
        $requestFile=Join-Path $trialProfile 'UI_CAPTURE_REQUEST.json'
        if(Test-Path -LiteralPath $requestFile) {
            $request=Get-Content -LiteralPath $requestFile -Raw -Encoding UTF8 | ConvertFrom-Json
            if ($request.trial -ne $Trial) { throw 'Capture belongs to a different trial.' }
            & 'C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111/runtime_ui_controlled/Measure_Owned_Child.ps1' -Child $child -RequestFile $requestFile -OutputRoot (Join-Path $runRoot 'measurements')
        }
        Start-Sleep -Milliseconds 250
        $child.Refresh()
    }
} finally {
    $child.Refresh()
    if (-not $child.HasExited) {
        [void]$child.CloseMainWindow()
        if (-not $child.WaitForExit(5000)) { $child.Kill(); [void]$child.WaitForExit(5000) }
    }
    [ordered]@{process_id=$child.Id;exit_code=$child.ExitCode;ended_utc=[DateTime]::UtcNow.ToString('o')} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $runRoot 'EXIT.json') -Encoding UTF8
    Copy-Item -LiteralPath (Join-Path $trialProfile 'logs') -Destination (Join-Path $runRoot 'logs') -Recurse
}

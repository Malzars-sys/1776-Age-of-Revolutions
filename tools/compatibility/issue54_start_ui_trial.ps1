param([Parameter(Mandatory=$true)][ValidateSet('A1','B1','B2','A2')][string]$Trial)
$ErrorActionPreference='Stop'
$labRoot='C:\Users\simeo\AppData\Local\Temp\aor1776_techperf54_20261111\runtime_ui_controlled'
$plan=Get-Content -LiteralPath (Join-Path $labRoot 'PREPARATION.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$spec=@($plan.trials | Where-Object trial -eq $Trial)
if ($spec.Count -ne 1) { throw 'No unique prepared trial.' }
$spec=$spec[0]
if (@(Get-Process -Name victoria3 -ErrorAction SilentlyContinue).Count) { throw 'A game is already running. Do not touch another session.' }
if ((Get-FileHash -LiteralPath $spec.executable -Algorithm SHA256).Hash.ToLowerInvariant() -ne $plan.executable_sha256) { throw 'Executable changed.' }
$launchStamp=[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')
$attemptRoot=Join-Path $labRoot ($Trial+'/attempt_'+$launchStamp)
[void][IO.Directory]::CreateDirectory($attemptRoot)
$receiptPath=Join-Path $attemptRoot 'LAUNCH.json'
if (Test-Path -LiteralPath $receiptPath) { throw 'Keep earlier trial receipts; do not overwrite.' }
$load=Get-Content -LiteralPath (Join-Path $spec.profile 'content_load.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if (@($load.enabledMods).Count -ne 1 -or $load.enabledMods[0].path -ne $spec.mod) { throw 'Wrong isolated mod profile.' }
$trialRoot=$attemptRoot
# This is the explicitly requested interactive game window. No startup CPU
# sampling, timeout or automatic killing is performed by this launcher.
$child=Start-Process -FilePath $spec.executable -ArgumentList $spec.arguments -WorkingDirectory (Split-Path -Parent $spec.executable) -WindowStyle Normal -PassThru -RedirectStandardOutput (Join-Path $trialRoot 'stdout.txt') -RedirectStandardError (Join-Path $trialRoot 'stderr.txt')
$receipt=[ordered]@{trial=$Trial;arm=$spec.arm;process_id=$child.Id;executable=$spec.executable;executable_sha256=$plan.executable_sha256;arguments=$spec.arguments;profile=$spec.profile;started_utc=[DateTime]::UtcNow.ToString('o');startup_cpu_benchmark_performed=$false;ui_measurements_started=$false;normal_profile_modified=$false}
$receipt | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $receiptPath -Encoding UTF8
$receipt | ConvertTo-Json -Depth 5
# Keep this tool-owned launch session alive while the supported desktop
# controller operates its game. Finishing the host command may otherwise end
# the tool's child-process lifetime before a window can be initialized.
try {
    while (-not $child.HasExited) {
        $stopFile=Join-Path $spec.profile 'STOP_TEST_REQUESTED.json'
        if(Test-Path -LiteralPath $stopFile){break}
        $requestFile=Join-Path $spec.profile 'UI_CAPTURE_REQUEST.json'
        if(Test-Path -LiteralPath $requestFile){
            & (Join-Path $labRoot 'Measure_Owned_Child.ps1') -Child $child -RequestFile $requestFile -OutputRoot (Join-Path $attemptRoot 'measurements')
        }
        Start-Sleep -Milliseconds 500
        $child.Refresh()
    }
} finally {
    # A manual interruption ends only this invocation's test child. An
    # unrelated pre-existing game is rejected before launch, above.
    $child.Refresh()
    if (-not $child.HasExited) {
        [void]$child.CloseMainWindow()
        if (-not $child.WaitForExit(5000)) { $child.Kill();[void]$child.WaitForExit(5000) }
    }
    [ordered]@{process_id=$child.Id;exit_code=$child.ExitCode;ended_utc=[DateTime]::UtcNow.ToString('o')} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $attemptRoot 'EXIT.json') -Encoding UTF8
}

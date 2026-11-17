param([Parameter(Mandatory=$true)][string]$Trial,[Parameter(Mandatory=$true)][string]$Variant)
$ErrorActionPreference='Stop'
$reportRoot=Join-Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)) 'docs/reports/compatibility/V1_15_ISSUE54_EXPRESSIONS_2026_11_12'
$plan=Get-Content -LiteralPath (Join-Path $reportRoot 'PLAN.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if($Trial -notmatch '^[A-Z][A-Z0-9_]{1,50}$'){throw 'Invalid trial label.'}
$spec=$plan.variants.$Variant
if(-not $spec){throw 'Unknown, unprepared variant.'}
$profile54=$plan.shared_profile
if(@(Get-Process -Name victoria3 -ErrorAction SilentlyContinue).Count){throw 'Preserve the existing game session.'}
foreach($pair54 in @(@($plan.executable,$plan.executable_sha256),@((Join-Path $profile54 'pdx_settings.json'),$plan.settings_sha256),@($spec.path,$spec.sha256))){
 if((Get-FileHash -LiteralPath $pair54[0] -Algorithm SHA256).Hash.ToLowerInvariant() -ne $pair54[1]){throw ('Changed input: '+$pair54[0])}
}
foreach($marker54 in @('UI_CAPTURE_REQUEST.json','STOP_TEST_REQUESTED.json')){if(Test-Path -LiteralPath (Join-Path $profile54 $marker54)){throw ('Inspect prior request: '+$marker54)}}
$stamp54=[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')
$run54=Join-Path $reportRoot ($Trial+'_'+$stamp54)
[void][IO.Directory]::CreateDirectory($run54)
Copy-Item -LiteralPath $spec.path -Destination (Join-Path $plan.probe 'gui/tech_tree.gui')
Copy-Item -LiteralPath $spec.path -Destination (Join-Path $run54 'tech_tree.gui')
Copy-Item -LiteralPath (Join-Path $profile54 'pdx_settings.json') -Destination (Join-Path $run54 'SETTINGS.json')
$load54=Join-Path $profile54 'content_load.json'
Copy-Item -LiteralPath $load54 -Destination (Join-Path $run54 'CONTENT_LOAD_BEFORE.json')
[IO.File]::WriteAllText($load54,([ordered]@{enabledMods=@(@{path=$plan.probe});disabledDLC=@();enabledUGC=@()}|ConvertTo-Json -Depth 5))
$arguments54=@(('--userdir='+($profile54 -replace '\\','/')),'-debug_mode')
$child54=Start-Process -FilePath $plan.executable -ArgumentList $arguments54 -WorkingDirectory (Split-Path -Parent $plan.executable) -WindowStyle Normal -PassThru -RedirectStandardOutput (Join-Path $run54 'stdout.txt') -RedirectStandardError (Join-Path $run54 'stderr.txt')
[ordered]@{trial=$Trial;variant=$Variant;process_id=$child54.Id;profile=$profile54;mod=$plan.probe;gui_sha256=$spec.sha256;settings_sha256=$plan.settings_sha256;executable_sha256=$plan.executable_sha256;started_utc=[DateTime]::UtcNow.ToString('o');startup_cpu_benchmark=$false}|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $run54 'LAUNCH.json') -Encoding UTF8
Get-Content -LiteralPath (Join-Path $run54 'LAUNCH.json')
try{
 while(-not $child54.HasExited){
  if(Test-Path -LiteralPath (Join-Path $profile54 'STOP_TEST_REQUESTED.json')){break}
  $request54=Join-Path $profile54 'UI_CAPTURE_REQUEST.json'
  if(Test-Path -LiteralPath $request54){
   if((Get-Content -LiteralPath $request54 -Raw|ConvertFrom-Json).trial -ne $Trial){throw 'Wrong-trial request.'}
   & 'C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111/runtime_ui_controlled/Measure_Owned_Child.ps1' -Child $child54 -RequestFile $request54 -OutputRoot (Join-Path $run54 'measurements')
  }
  Start-Sleep -Milliseconds 250
  $child54.Refresh()
 }
}finally{
 $child54.Refresh();if(-not $child54.HasExited){[void]$child54.CloseMainWindow();if(-not $child54.WaitForExit(5000)){$child54.Kill();[void]$child54.WaitForExit(5000)}}
 [ordered]@{exit_code=$child54.ExitCode;ended_utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $run54 'EXIT.json') -Encoding UTF8
 Copy-Item -LiteralPath (Join-Path $profile54 'logs') -Destination (Join-Path $run54 'logs') -Recurse
}

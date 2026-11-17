param([Parameter(Mandatory=$true)][ValidateSet('CONTROL1','COMPACT1','COMPACT2','CONTROL2')][string]$Trial)
$ErrorActionPreference='Stop'
$plan54=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'PLAN.json') -Raw | ConvertFrom-Json
if(@(Get-Process -Name victoria3 -ErrorAction SilentlyContinue).Count){throw 'Preserve the existing Victoria 3 session.'}
$spec54=$plan54.trials.$Trial
foreach($pair54 in @(@($plan54.executable,$plan54.executable_sha256),@((Join-Path $plan54.profile 'pdx_settings.json'),$plan54.settings_sha256),@((Join-Path $spec54.mod 'gui/tech_tree.gui'),$spec54.gui_sha256),@($plan54.save,$plan54.save_sha256))){
 if((Get-FileHash -LiteralPath $pair54[0] -Algorithm SHA256).Hash.ToLowerInvariant() -ne $pair54[1]){throw ('Changed input; inspect: '+$pair54[0])}
}
foreach($name54 in 'UI_CAPTURE_REQUEST.json','STOP_TEST_REQUESTED.json'){if(Test-Path -LiteralPath (Join-Path $plan54.profile $name54)){throw ('Inspect prior marker: '+$name54)}}
$run54=Join-Path $PSScriptRoot ($Trial+'_'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ'))
[void][IO.Directory]::CreateDirectory($run54)
[IO.File]::WriteAllText((Join-Path $plan54.profile 'content_load.json'),([ordered]@{enabledMods=@(@{path=$spec54.mod});disabledDLC=@();enabledUGC=@()}|ConvertTo-Json -Depth 5))
Copy-Item -LiteralPath (Join-Path $plan54.profile 'pdx_settings.json') -Destination (Join-Path $run54 'SETTINGS.json')
Copy-Item -LiteralPath (Join-Path $spec54.mod 'gui/tech_tree.gui') -Destination (Join-Path $run54 'tech_tree.gui')
$args54=@(('--userdir='+($plan54.profile -replace '\\','/')),'-debug_mode')
$child54=Start-Process -FilePath $plan54.executable -ArgumentList $args54 -WorkingDirectory (Split-Path -Parent $plan54.executable) -WindowStyle Normal -PassThru -RedirectStandardOutput (Join-Path $run54 'stdout.txt') -RedirectStandardError (Join-Path $run54 'stderr.txt')
[ordered]@{trial=$Trial;variant=$spec54.variant;process_id=$child54.Id;profile=$plan54.profile;mod=$spec54.mod;gui_sha256=$spec54.gui_sha256;settings_sha256=$plan54.settings_sha256;executable=$plan54.executable;executable_sha256=$plan54.executable_sha256;save_sha256=$plan54.save_sha256;started_utc=[DateTime]::UtcNow.ToString('o');startup_cpu_benchmark=$false}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $run54 'LAUNCH.json') -Encoding UTF8
Get-Content -LiteralPath (Join-Path $run54 'LAUNCH.json')
try{
 while(-not $child54.HasExited){
  if(Test-Path -LiteralPath (Join-Path $plan54.profile 'STOP_TEST_REQUESTED.json')){break}
  $req54=Join-Path $plan54.profile 'UI_CAPTURE_REQUEST.json'
  if(Test-Path -LiteralPath $req54){
   if((Get-Content -LiteralPath $req54 -Raw|ConvertFrom-Json).trial -ne $Trial){throw 'Wrong capture trial.'}
   & $plan54.collector -Child $child54 -RequestFile $req54 -OutputRoot (Join-Path $run54 'measurements')
  }
  Start-Sleep -Milliseconds 250
  $child54.Refresh()
 }
}finally{
 $child54.Refresh()
 if(-not $child54.HasExited){[void]$child54.CloseMainWindow();if(-not $child54.WaitForExit(5000)){$child54.Kill();[void]$child54.WaitForExit(5000)}}
 [ordered]@{exit_code=$child54.ExitCode;ended_utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $run54 'EXIT.json') -Encoding UTF8
 if(Test-Path -LiteralPath (Join-Path $plan54.profile 'logs')){Copy-Item -LiteralPath (Join-Path $plan54.profile 'logs') -Destination (Join-Path $run54 'logs') -Recurse}
}

param([Parameter(Mandatory=$true)][string]$Trial,[int]$MaxSeconds=1800,[switch]$KeepAfterWindows,[int]$StopAfterHeartbeatDays=0)
$ErrorActionPreference='Stop'
$report56=Join-Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)) 'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
$plan56=Get-Content -LiteralPath (Join-Path $report56 'PREPARATION.json') -Raw -Encoding UTF8|ConvertFrom-Json
$spec56=$plan56.profiles.$Trial
if(-not $spec56 -or $Trial -notmatch '^[A-Z0-9_]{2,40}$'){throw 'Unknown isolated trial.'}
if(@(Get-Process -Name victoria3 -ErrorAction SilentlyContinue).Count){throw 'Preserve the existing game session.'}
if((Get-FileHash -LiteralPath $plan56.executable -Algorithm SHA256).Hash.ToLowerInvariant() -ne $plan56.executable_sha256){throw 'Executable changed.'}
if((Get-FileHash -LiteralPath (Join-Path $spec56.path 'pdx_settings.json') -Algorithm SHA256).Hash.ToLowerInvariant() -ne $spec56.settings_sha256){throw 'Settings changed; review before comparing.'}
$run56=Join-Path $report56 ('runtime/'+$Trial+'_'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ'))
[void][IO.Directory]::CreateDirectory($run56)
$stop56=Join-Path $plan56.lab ('requests/'+$Trial+'.stop')
if(Test-Path -LiteralPath $stop56){throw 'Inspect the previous stop request.'}
Copy-Item -LiteralPath (Join-Path $spec56.path 'content_load.json') -Destination (Join-Path $run56 'CONTENT_LOAD.json')
Copy-Item -LiteralPath (Join-Path $spec56.path 'pdx_settings.json') -Destination (Join-Path $run56 'SETTINGS.json')
$arguments56=@(('--userdir='+($spec56.path -replace '\\','/')),'-debug_mode')
$child56=Start-Process -FilePath $plan56.executable -ArgumentList $arguments56 -WorkingDirectory (Split-Path -Parent $plan56.executable) -WindowStyle Normal -PassThru -RedirectStandardOutput (Join-Path $run56 'stdout.txt') -RedirectStandardError (Join-Path $run56 'stderr.txt')
$launch56=[ordered]@{trial=$Trial;process_id=$child56.Id;executable=$plan56.executable;executable_sha256=$plan56.executable_sha256;profile=$spec56.path;mods=$spec56.mods;settings_sha256=$spec56.settings_sha256;reference_head=$plan56.reference_head;started_utc=[DateTime]::UtcNow.ToString('o');startup_cpu_benchmark=$false;max_wall_seconds=$MaxSeconds;expected_year=$spec56.expected_year;keep_after_windows=[bool]$KeepAfterWindows;stop_after_heartbeat_days=$StopAfterHeartbeatDays}
$launch56|ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $run56 'LAUNCH.json') -Encoding UTF8
$launch56|ConvertTo-Json -Depth 6
$observerScript56=Join-Path $PSScriptRoot 'simperf56_observe.ps1'
$observerArguments56='-NoProfile -File "'+$observerScript56+'" -GameProcessId '+$child56.Id+' -RunDirectory "'+$run56+'"'
$observer56=Start-Process -FilePath (Get-Process -Id $PID).Path -ArgumentList $observerArguments56 -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $run56 'observer_stdout.txt') -RedirectStandardError (Join-Path $run56 'observer_stderr.txt')
$clock56=[Diagnostics.Stopwatch]::StartNew()
$positions56=@{};$seen56=@{};$windows56=@{};$days56=New-Object 'Collections.Generic.List[object]'
$samples56=New-Object 'Collections.Generic.List[object]'
$active56=$null;$previous56=$null;$lastSample56=0;$lastStatus56=0;$countryCount56=$null
function Read-NewLines56($path){
 $key=$path.FullName
 if(-not $positions56.ContainsKey($key)){$positions56[$key]=0L}
 $stream=$null
 try{
  $stream=[IO.File]::Open($key,[IO.FileMode]::Open,[IO.FileAccess]::Read,([IO.FileShare]::ReadWrite-bor[IO.FileShare]::Delete))
  if($stream.Length -lt $positions56[$key]){$positions56[$key]=0L}
  [void]$stream.Seek($positions56[$key],[IO.SeekOrigin]::Begin)
  $remaining=$stream.Length-$positions56[$key]
  if($remaining -le 0){return @()}
  $buffer=New-Object byte[] ([Math]::Min($remaining,2097152))
  $count=$stream.Read($buffer,0,$buffer.Length)
  $lastNewline=-1
  for($index=$count-1;$index -ge 0;$index--){if($buffer[$index]-eq 10){$lastNewline=$index;break}}
  if($lastNewline -lt 0){return @()}
  $positions56[$key]+=$lastNewline+1
  return [Text.Encoding]::UTF8.GetString($buffer,0,$lastNewline+1).Split("`n")
 }catch{return @()}finally{if($stream){$stream.Dispose()}}
}
function Read-SharedText56($path){
 $stream=[IO.File]::Open($path,[IO.FileMode]::Open,[IO.FileAccess]::Read,([IO.FileShare]::ReadWrite-bor[IO.FileShare]::Delete))
 $reader=[IO.StreamReader]::new($stream,[Text.Encoding]::UTF8)
 try{return $reader.ReadToEnd()}finally{$reader.Dispose()}
}
try{
 while(-not $child56.HasExited -and $clock56.Elapsed.TotalSeconds -lt $MaxSeconds){
  if(Test-Path -LiteralPath $stop56){break}
  $logDir56=Join-Path $spec56.path 'logs'
  $logFiles56=@(Get-ChildItem -LiteralPath $logDir56 -File -ErrorAction SilentlyContinue|Where-Object{$_.Name -match '^debug(\.\d+)?\.log$|^game\.log$'}|Sort-Object -Property @{Expression={if($_.Name -match '^debug\.(\d+)\.log$'){[int]$Matches[1]}elseif($_.Name -eq 'debug.log'){0}else{-1}}} -Descending)
  foreach($file56 in $logFiles56){
   foreach($line56 in @(Read-NewLines56 $file56)){
    if($line56 -notmatch 'SIM56\|'){continue}
    if($line56 -match 'SIM56\|COUNTRY_DONE' -and $null -eq $countryCount56){
     $family56=if($file56.Name.StartsWith('debug')){@($logFiles56|Where-Object{$_.Name.StartsWith('debug')})}else{@($file56)}
     $count56=0
     foreach($countryFile56 in $family56){$countryText56=Read-SharedText56 $countryFile56.FullName;$count56+=([regex]::Matches($countryText56,'SIM56\|COUNTRY\|')).Count}
     $countryCount56=$count56
    }
    if($line56 -match 'SIM56\|DAY\|date=(?<date>[^\r\n]+)'){
     $dayKey56=$Matches.date.Trim()
     if(-not $seen56.ContainsKey('DAY|'+$dayKey56)){$seen56['DAY|'+$dayKey56]=$true;$days56.Add([pscustomobject]@{game_date_raw=$dayKey56;wall_s=$clock56.Elapsed.TotalSeconds;utc=[DateTime]::UtcNow.ToString('o')})}
    }
    if($line56 -notmatch 'SIM56\|WINDOW\|(?<name>[A-Z_]+)\|(?<edge>START|END)\|offset=(?<offset>\d+)\|date=(?<date>[^\r\n]+)'){continue}
    $name56=$Matches.name;$edge56=$Matches.edge;$offset56=[int]$Matches.offset;$date56=$Matches.date.Trim();$marker56=$name56+'|'+$edge56
    if($seen56.ContainsKey($marker56)){continue};$seen56[$marker56]=$true
    $child56.Refresh();$now56=$clock56.Elapsed.TotalSeconds
    $point56=[ordered]@{name=$name56;edge=$edge56;offset_days=$offset56;game_date_raw=$date56;received_utc=[DateTime]::UtcNow.ToString('o');wall_s=$now56;cpu_ms=$child56.TotalProcessorTime.TotalMilliseconds;working_set_mib=$child56.WorkingSet64/1MB;log_line=$line56.Trim();log_file=$file56.Name}
    if($edge56 -eq 'START'){
     $windows56[$name56]=@{start=$point56;end=$null};$active56=$name56;$previous56=$null
    }else{
     if(-not $windows56.ContainsKey($name56)){throw 'End marker without start; no inferred benchmark.'}
     $windows56[$name56].end=$point56;$start56=$windows56[$name56].start
     $elapsed56=$point56.wall_s-$start56.wall_s;$simulated56=$point56.offset_days-$start56.offset_days
     $result56=[ordered]@{trial=$Trial;window=$name56;start=$start56;end=$point56;simulated_days=$simulated56;wall_seconds=$elapsed56;days_per_real_second=$(if($elapsed56-gt 0){$simulated56/$elapsed56}else{$null});cpu_machine_percent=$(if($elapsed56-gt 0){100*($point56.cpu_ms-$start56.cpu_ms)/(1000*$elapsed56*[Environment]::ProcessorCount)}else{$null});logical_processors=[Environment]::ProcessorCount;runtime_countries=$countryCount56;timer_poll_interval_ms=100;timing_basis='PROVISIONAL ONLY: log arrival is buffered; use simperf56_analyze.py native timestamps and continuous observer';setup_or_startup_included=$false;pause_absence_automatically_verified=$false;fps_measured=$false;valid_marker_order=($elapsed56-gt 0);foreground_state_automatically_verified=$false}
     $result56|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $run56 ('WINDOW_'+$name56+'.json')) -Encoding UTF8
     @{window=$name56;wall_seconds=$elapsed56;simulated_days=$simulated56;days_per_second=$result56.days_per_real_second;cpu_machine_percent=$result56.cpu_machine_percent}|ConvertTo-Json -Compress
     $active56=$null
    }
   }
  }
  if($active56 -and $clock56.Elapsed.TotalSeconds-$lastSample56 -ge 0.5){
   $child56.Refresh();$sampleClock56=$clock56.Elapsed.TotalSeconds;$sampleCpu56=$child56.TotalProcessorTime.TotalMilliseconds
   if($previous56){$deltaTime56=$sampleClock56-$previous56.time;$deltaCpu56=$sampleCpu56-$previous56.cpu}else{$deltaTime56=0;$deltaCpu56=0}
   $samples56.Add([pscustomobject]@{utc=[DateTime]::UtcNow.ToString('o');wall_s=$sampleClock56;window=$active56;cpu_total_ms=$sampleCpu56;interval_s=$deltaTime56;cpu_delta_ms=$deltaCpu56;working_set_mib=$child56.WorkingSet64/1MB;threads=$child56.Threads.Count;error_log_bytes=$(if(Test-Path -LiteralPath (Join-Path $logDir56 'error.log')){(Get-Item -LiteralPath (Join-Path $logDir56 'error.log')).Length}else{0})})
   $previous56=@{time=$sampleClock56;cpu=$sampleCpu56};$lastSample56=$sampleClock56
  }
  if($clock56.Elapsed.TotalSeconds-$lastStatus56 -ge 15){
   @{utc=[DateTime]::UtcNow.ToString('o');trial=$Trial;wall_s=$clock56.Elapsed.TotalSeconds;active_window=$active56;received_markers=$seen56.Keys|Where-Object{$_ -notlike 'DAY|*'};heartbeat_dates=$days56.Count;latest_game_date=$(if($days56.Count){$days56[$days56.Count-1].game_date_raw}else{$null});runtime_countries=$countryCount56;startup_benchmark=$false}|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $run56 'STATUS.json') -Encoding UTF8
   $lastStatus56=$clock56.Elapsed.TotalSeconds
  }
  if($seen56.ContainsKey('NEXT_JANUARY|END') -and -not $KeepAfterWindows){break}
  if($StopAfterHeartbeatDays -gt 0 -and $days56.Count -ge $StopAfterHeartbeatDays){break}
  Start-Sleep -Milliseconds 100
  $child56.Refresh()
 }
}finally{
 $child56.Refresh();if(-not $child56.HasExited){[void]$child56.CloseMainWindow();if(-not $child56.WaitForExit(5000)){$child56.Kill();[void]$child56.WaitForExit(5000)}}
 $samples56|Export-Csv -LiteralPath (Join-Path $run56 'CPU_RAM.csv') -NoTypeInformation -Encoding UTF8
 ConvertTo-Json -InputObject @($days56.ToArray()) -Depth 5|Set-Content -LiteralPath (Join-Path $run56 'GAME_DATES.json') -Encoding UTF8
 @{exit_code=$child56.ExitCode;ended_utc=[DateTime]::UtcNow.ToString('o');completed_windows=@($windows56.Keys|Where-Object{$windows56[$_].end});runtime_countries=$countryCount56;startup_cpu_benchmark=$false;all_windows_received=$seen56.ContainsKey('NEXT_JANUARY|END')}|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $run56 'EXIT.json') -Encoding UTF8
 if(Test-Path -LiteralPath (Join-Path $spec56.path 'logs')){Copy-Item -LiteralPath (Join-Path $spec56.path 'logs') -Destination (Join-Path $run56 'logs') -Recurse}
}

param(
 [Parameter(Mandatory=$true)][System.Diagnostics.Process]$Child,
 [Parameter(Mandatory=$true)][string]$RequestFile,
 [Parameter(Mandatory=$true)][string]$OutputRoot
)
$ErrorActionPreference='Stop'
$request=Get-Content -LiteralPath $RequestFile -Raw -Encoding UTF8 | ConvertFrom-Json
if($request.id -notmatch '^[A-Za-z0-9_.-]{1,80}$'){throw 'Invalid capture ID.'}
if($request.phase -notin @('closed_paused','tree_stationary','tree_pan')){throw 'Only established UI states may be measured.'}
if($request.category -notin @('none','production','military','society')){throw 'Invalid category.'}
if($request.seconds -ne 15){throw 'This series uses fifteen-second captures.'}
if(-not $request.ui_state_evidence){throw 'An observed UI state must be identified.'}
[void][IO.Directory]::CreateDirectory($OutputRoot)
$prefix=Join-Path $OutputRoot $request.id
if(Test-Path -LiteralPath ($prefix+'_metadata.json')){throw 'Keep prior captures.'}
# Read only the child handle already owned by this launch session. No process
# discovery, elevation, UI input or native-game instrumentation is performed.
$rows=[Collections.Generic.List[object]]::new()
$Child.Refresh();if($Child.HasExited){throw 'The owned test game exited.'}
$previousCpu=$Child.TotalProcessorTime.TotalMilliseconds
$clock=[Diagnostics.Stopwatch]::StartNew();$previousTime=$clock.Elapsed.TotalSeconds
$started=[DateTime]::UtcNow.ToString('o')
while($clock.Elapsed.TotalSeconds -lt 15){
 Start-Sleep -Milliseconds 1000
 $Child.Refresh();if($Child.HasExited){throw 'The test game exited during capture.'}
 $now=$clock.Elapsed.TotalSeconds;$cpu=$Child.TotalProcessorTime.TotalMilliseconds
 $interval=$now-$previousTime;$delta=$cpu-$previousCpu
 $rows.Add([pscustomobject]@{utc=[DateTime]::UtcNow.ToString('o');elapsed_s=$now;interval_s=$interval;cpu_total_ms=$cpu;cpu_delta_ms=$delta;cpu_percent_one_core=(100*$delta/(1000*$interval));cpu_percent_machine=(100*$delta/(1000*$interval*[Environment]::ProcessorCount));working_set_mib=($Child.WorkingSet64/1MB);threads=$Child.Threads.Count;phase=$request.phase;category=$request.category})
 $previousCpu=$cpu;$previousTime=$now
}
$rows | Export-Csv -LiteralPath ($prefix+'_cpu.csv') -NoTypeInformation -Encoding UTF8
[ordered]@{id=$request.id;trial=$request.trial;phase=$request.phase;category=$request.category;process_id=$Child.Id;started_utc=$started;ended_utc=[DateTime]::UtcNow.ToString('o');seconds_actual=$clock.Elapsed.TotalSeconds;logical_processors=[Environment]::ProcessorCount;samples=$rows.Count;ui_state_evidence=$request.ui_state_evidence;ui_state_verified_by='Agent visual observation, not inferred by sampler';fps_measured=$false;startup_benchmark=$false;sampler_overhead_not_subtracted=$true} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath ($prefix+'_metadata.json') -Encoding UTF8
Move-Item -LiteralPath $RequestFile -Destination ($prefix+'_request.json')

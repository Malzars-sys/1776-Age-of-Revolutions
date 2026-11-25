param([Parameter(Mandatory=$true)][int]$GameProcessId,
      [Parameter(Mandatory=$true)][string]$RunDirectory)
$ErrorActionPreference='Stop'
$game56=Get-Process -Id $GameProcessId
if($game56.ProcessName -ne 'victoria3'){throw 'Expected the owned Victoria 3 process.'}
$start56=$game56.StartTime
$target56=Join-Path $RunDirectory 'CONTINUOUS_CPU_RAM.csv'
if(Test-Path -LiteralPath $target56){throw 'Preserve previous observations.'}
$writer56=[IO.StreamWriter]::new($target56,$false,[Text.UTF8Encoding]::new($true))
$writer56.AutoFlush=$true
$writer56.WriteLine('utc,cpu_total_ms,working_set_mib,threads')
@{process_id=$GameProcessId;process_start_utc=$start56.ToUniversalTime().ToString('o');timezone=[TimeZoneInfo]::Local.Id;logical_processors=[Environment]::ProcessorCount;interval_ms=500;timing_basis='Native engine HH:mm:ss log stamps; CPU samples will be aligned offline. Arrival-based windows are provisional.'}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $RunDirectory 'OBSERVER.json') -Encoding UTF8
$culture56=[Globalization.CultureInfo]::InvariantCulture
try{
 while(-not $game56.HasExited){
  $game56.Refresh()
  if($game56.HasExited){break}
  if($game56.StartTime -ne $start56){throw 'Process identity changed.'}
  $row56=@([DateTime]::UtcNow.ToString('o'),$game56.TotalProcessorTime.TotalMilliseconds.ToString($culture56),($game56.WorkingSet64/1MB).ToString($culture56),$game56.Threads.Count)
  $writer56.WriteLine(($row56 -join ','))
  Start-Sleep -Milliseconds 500
 }
}finally{$writer56.Dispose()}

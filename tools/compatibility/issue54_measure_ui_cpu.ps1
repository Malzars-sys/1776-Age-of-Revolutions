param(
 [Parameter(Mandatory=$true)][ValidateSet('A1','B1','B2','A2')][string]$Trial,
 [Parameter(Mandatory=$true)][ValidateSet('closed_paused','tree_stationary','tree_scroll')][string]$Phase,
 [ValidateSet('none','production','military','society')][string]$Category='production'
)
$ErrorActionPreference='Stop'
$lab='C:\Users\simeo\AppData\Local\Temp\aor1776_techperf54_20261111'
$expected='C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\binaries\victoria3.exe'
$arm=$Trial.Substring(0,1)
Write-Output 'Return to the paused game now. UI CPU capture starts in five seconds.'
Start-Sleep -Seconds 5
# UI state is declared by the person starting this command, not inferred.
# This collector never starts a game or measures a startup phase.
& (Join-Path $lab 'kit/Measure_CPU.ps1') -Arm $arm -Phase $Phase -Category $Category -DurationSeconds 15 -ExpectedExecutable $expected -OutputDirectory (Join-Path $lab ('runtime_ui_controlled/'+$Trial+'/measurements'))

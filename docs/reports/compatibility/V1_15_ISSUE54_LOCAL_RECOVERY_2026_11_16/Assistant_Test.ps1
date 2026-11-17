param([switch]$CheckOnly,[switch]$Preview,[switch]$SelfTest,[switch]$LegacyLoop)
$ErrorActionPreference='Stop'
if($LegacyLoop -and -not $SelfTest){throw 'LegacyLoop is reserved for the synthetic regression test.'}
$relayRoot54=$PSScriptRoot
$relayPlan54=Get-Content -LiteralPath (Join-Path $relayRoot54 'PLAN_MANUAL.json') -Raw -Encoding UTF8|ConvertFrom-Json
function Test-RelayInputs54 {
 foreach($pair in @(@($relayPlan54.executable,$relayPlan54.executable_sha256),@($relayPlan54.save,$relayPlan54.save_sha256),@((Join-Path $relayPlan54.profile 'pdx_settings.json'),$relayPlan54.settings_sha256))){
  if((Get-FileHash -LiteralPath $pair[0] -Algorithm SHA256).Hash.ToLowerInvariant() -ne $pair[1]){throw ('Un fichier du laboratoire a changé. Conserver les données et demander un contrôle : '+$pair[0])}
 }
 foreach($label in $relayPlan54.order){$spec=$relayPlan54.trials.$label;if((Get-FileHash -LiteralPath (Join-Path $spec.mod 'gui/tech_tree.gui') -Algorithm SHA256).Hash.ToLowerInvariant() -ne $spec.gui_sha256){throw 'Une variante a changé. Aucun lancement effectué.'}}
}
if($CheckOnly){Test-RelayInputs54; 'PASS: executable, save, settings and four GUI selections; no launch or UI.';exit}
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[Windows.Forms.Application]::EnableVisualStyles()
$script:relayChild54=$null
$script:relayTrialIndex54=0
$script:relayPhaseIndex54=0
$script:relayRun54=$null
$script:relaySession54=$null
$script:relayBusy54=$false
$script:relayClosingDuringCapture54=$false
$script:relaySelfTestComplete54=$false
$script:relaySelfTestVisible54=$false
$script:relaySelfTestChildAlive54=$false
$script:relaySelfTestError54=$null
$script:relayPhases54=@(
 @{key='closed_paused';category='none';title='Carte en pause';instruction='Charger Continuer : Royaume de France, 1er janvier 1776. Garder la partie en pause, attendre trente secondes après chargement, puis fermer les panneaux. Ne pas changer le zoom ni les réglages.'},
 @{key='tree_stationary';category='production';title='Production immobile';instruction='Ouvrir Technologie, puis Production. Ouvrir aussi une fois Militaire et Société pour les préparer, puis revenir à Production. Garder le zoom initial et ne plus déplacer la vue.'},
 @{key='tree_stationary';category='military';title='Militaire immobile';instruction='Cliquer sur Militaire. Garder le même zoom, puis ne plus déplacer la vue.'},
 @{key='tree_stationary';category='society';title='Société immobile';instruction='Cliquer sur Société. Garder le même zoom, puis ne plus déplacer la vue.'},
 @{key='tree_pan';category='society';title='Un déplacement dans Société';instruction='Rester dans Société. Pendant les 15 secondes, faire un seul glissement vertical avec le bouton gauche, depuis le milieu de lʼarbre sur environ 140 pixels, puis rester immobile. Reproduire le même geste à chaque passage. Ne pas utiliser la molette.'}
)
$form54=New-Object Windows.Forms.Form
$form54.Text='1776 — Assistant de test isolé #54'
if($SelfTest){$form54.Text='1776 — Diagnostic de capture sans jeu'}
$form54.Size=New-Object Drawing.Size(760,590)
$form54.StartPosition='CenterScreen'
$form54.FormBorderStyle='FixedDialog'
$form54.MaximizeBox=$false
$form54.Font=New-Object Drawing.Font('Segoe UI',11)
$heading54=New-Object Windows.Forms.Label
$heading54.SetBounds(24,20,700,40)
$heading54.Font=New-Object Drawing.Font('Segoe UI',15,[Drawing.FontStyle]::Bold)
$form54.Controls.Add($heading54)
$instruction54=New-Object Windows.Forms.Label
$instruction54.SetBounds(24,75,690,190)
$form54.Controls.Add($instruction54)
$fpsLabel54=New-Object Windows.Forms.Label
$fpsLabel54.SetBounds(24,280,560,30)
$fpsLabel54.Text='FPS relevés en jeu, si le compteur est visible (facultatif) :'
$form54.Controls.Add($fpsLabel54)
$fps54=New-Object Windows.Forms.TextBox
$fps54.SetBounds(595,278,100,32)
$form54.Controls.Add($fps54)
$note54=New-Object Windows.Forms.Label
$note54.SetBounds(24,325,690,80)
$note54.Text='Le compteur debug peut apparaître en bas à droite. Laisser vide si absent. Après le clic Mesurer, vous aurez 5 secondes pour cliquer dans le jeu ; la collecte CPU durera ensuite 15 secondes. Aucun délai dʼouverture ou FPS moyen ne sera inventé.'
$form54.Controls.Add($note54)
$primary54=New-Object Windows.Forms.Button
$primary54.SetBounds(24,425,450,50)
$form54.Controls.Add($primary54)
$close54=New-Object Windows.Forms.Button
$close54.SetBounds(490,425,205,50)
$close54.Text='Fermer lʼassistant'
$form54.Controls.Add($close54)
$status54=New-Object Windows.Forms.Label
$status54.SetBounds(24,490,690,50)
$form54.Controls.Add($status54)
$timer54=New-Object Windows.Forms.Timer
$timer54.Interval=100
function Save-RelayJson54($destination,$value){if(Test-Path -LiteralPath $destination){throw 'Une preuve existe déjà : la conserver.'};$value|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $destination -Encoding UTF8}
function Start-RelayCapture54($fpsValue){
 $phase=$script:relayPhases54[$script:relayPhaseIndex54]
 $script:relayCapture54=@{phase=$phase.key;category=$phase.category;fps=$fpsValue;declared_utc=[DateTime]::UtcNow.ToString('o')}
 $script:relayRows54=New-Object 'Collections.Generic.List[object]'
 $script:relayClock54=[Diagnostics.Stopwatch]::StartNew()
 $script:relaySampling54=$false;$script:relayBusy54=$true;$primary54.Enabled=$false
 $form54.Hide();$timer54.Start()
}
function Update-RelayView54 {
 if($script:relayTrialIndex54 -ge $relayPlan54.order.Count){$heading54.Text='Série terminée';$instruction54.Text='Les quatre passages sont enregistrés. Le jeu dʼessai est fermé. Les fichiers se trouvent dans ce dossier, sous MANUAL_ suivi de la date. Revenez dans la conversation pour leur analyse. Aucun correctif nʼa été installé.';$primary54.Enabled=$false;$fps54.Enabled=$false;return}
 $label=$relayPlan54.order[$script:relayTrialIndex54]
 $friendly=if($label.StartsWith('CONTROL')){'Interface actuelle — témoin'}else{'Variante expérimentale COMPACT'}
 $heading54.Text=('Passage '+($script:relayTrialIndex54+1)+'/4 — '+$friendly)
 if($null -eq $script:relayChild54){$instruction54.Text='Cliquer sur Lancer, puis attendre le menu. Dans le jeu, cliquer Continuer pour charger la France au 1er janvier 1776. Garder la partie en pause. Cet assistant utilise uniquement un profil de laboratoire et ne touche pas aux sauvegardes ou playsets habituels.';$primary54.Text='Lancer ce passage isolé';$fps54.Enabled=$false}
 else{$phase=$script:relayPhases54[$script:relayPhaseIndex54];$instruction54.Text=$phase.title+"`r`n`r`n"+$phase.instruction+"`r`n`r`nRevenir à cet assistant quand cette vue est prête. Le bouton Mesurer atteste que vous avez préparé cette vue.";$primary54.Text='Mesurer cette vue pendant 15 secondes';$fps54.Enabled=$true}
 $fps54.Text='';$primary54.Enabled=-not $Preview
}
function Stop-RelayChild54 {
 if($null -eq $script:relayChild54){return}
 $child=$script:relayChild54
 $child.Refresh()
 if(-not $child.HasExited){[void]$child.CloseMainWindow();if(-not $child.WaitForExit(5000)){$child.Kill();[void]$child.WaitForExit(5000)}}
 Save-RelayJson54 (Join-Path $script:relayRun54 'EXIT.json') @{exit_code=$child.ExitCode;ended_utc=[DateTime]::UtcNow.ToString('o');owned_test_only=$true;self_test=[bool]$SelfTest}
 $log=Join-Path $relayPlan54.profile 'logs';if(-not $SelfTest -and (Test-Path -LiteralPath $log)){Copy-Item -LiteralPath $log -Destination (Join-Path $script:relayRun54 'logs') -Recurse}
 $script:relayChild54=$null
}
$primary54.Add_Click({
 try{
  if($null -eq $script:relayChild54){
   Test-RelayInputs54
   if(@(Get-Process -Name victoria3 -ErrorAction SilentlyContinue).Count){throw 'Un Victoria 3 est déjà ouvert. Le conserver et le fermer vous-même avant ce test.'}
   if($null -eq $script:relaySession54){$script:relaySession54=Join-Path $relayRoot54 ('MANUAL_'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ'));[void][IO.Directory]::CreateDirectory($script:relaySession54)}
   $label=$relayPlan54.order[$script:relayTrialIndex54];$spec=$relayPlan54.trials.$label
   $script:relayRun54=Join-Path $script:relaySession54 $label
   [void][IO.Directory]::CreateDirectory($script:relayRun54)
   $load=Join-Path $relayPlan54.profile 'content_load.json';if(Test-Path -LiteralPath $load){Copy-Item -LiteralPath $load -Destination (Join-Path $script:relayRun54 'CONTENT_LOAD_BEFORE.json')}
   [IO.File]::WriteAllText($load,(@{enabledMods=@(@{path=$spec.mod});disabledDLC=@();enabledUGC=@()}|ConvertTo-Json -Depth 5))
   Copy-Item -LiteralPath (Join-Path $relayPlan54.profile 'pdx_settings.json') -Destination (Join-Path $script:relayRun54 'SETTINGS.json')
   $args=@(('--userdir='+($relayPlan54.profile -replace '\\','/')),'-debug_mode')
   $script:relayChild54=Start-Process -FilePath $relayPlan54.executable -ArgumentList $args -WorkingDirectory (Split-Path -Parent $relayPlan54.executable) -WindowStyle Normal -PassThru -RedirectStandardOutput (Join-Path $script:relayRun54 'stdout.txt') -RedirectStandardError (Join-Path $script:relayRun54 'stderr.txt')
   Save-RelayJson54 (Join-Path $script:relayRun54 'LAUNCH.json') @{trial=$label;variant=$spec.variant;process_id=$script:relayChild54.Id;profile=$relayPlan54.profile;executable_sha256=$relayPlan54.executable_sha256;gui_sha256=$spec.gui_sha256;save_sha256=$relayPlan54.save_sha256;started_utc=[DateTime]::UtcNow.ToString('o');startup_cpu_benchmark=$false}
   $script:relayPhaseIndex54=0;$status54.Text='Attendre le menu du jeu, puis charger Continuer.';Update-RelayView54;return
  }
  $fpsValue=$null
  if($fps54.Text.Trim()){[double]$parsed=0;if(-not [double]::TryParse($fps54.Text.Replace(',','.'),[Globalization.NumberStyles]::Float,[Globalization.CultureInfo]::InvariantCulture,[ref]$parsed)-or $parsed -le 0 -or $parsed -gt 1000){throw 'Saisir un FPS positif, ou laisser le champ vide.'};$fpsValue=$parsed}
  Start-RelayCapture54 $fpsValue
 }catch{$status54.Text=$_.Exception.Message;$primary54.Enabled=$true}
})
$timer54.Add_Tick({
 try{
  $child=$script:relayChild54;$child.Refresh();if($child.HasExited){throw 'Le jeu dʼessai sʼest fermé. Cette prise est invalide.'}
  if(-not $script:relaySampling54){if($script:relayClock54.Elapsed.TotalSeconds -lt 5){return};$script:relaySampling54=$true;$script:relayStarted54=[DateTime]::UtcNow.ToString('o');$script:relaySampleClock54=[Diagnostics.Stopwatch]::StartNew();$script:relayPreviousTime54=0;$script:relayPreviousCpu54=$child.TotalProcessorTime.TotalMilliseconds;return}
  $now=$script:relaySampleClock54.Elapsed.TotalSeconds
  if(($now-$script:relayPreviousTime54)-lt 1){return}
  $cpu=$child.TotalProcessorTime.TotalMilliseconds;$delta=$cpu-$script:relayPreviousCpu54;$interval=$now-$script:relayPreviousTime54
  $script:relayRows54.Add([pscustomobject]@{utc=[DateTime]::UtcNow.ToString('o');interval_s=$interval;cpu_delta_ms=$delta;cpu_percent_machine=(100*$delta/(1000*$interval*[Environment]::ProcessorCount));threads=$child.Threads.Count;working_set_mib=$child.WorkingSet64/1MB})
  $script:relayPreviousTime54=$now;$script:relayPreviousCpu54=$cpu
  if($now -lt 15){return}
  $timer54.Stop();$cap=$script:relayCapture54;$label=$relayPlan54.order[$script:relayTrialIndex54];$prefix=Join-Path $script:relayRun54 ($cap.phase+'_'+$cap.category)
  $script:relayRows54|Export-Csv -LiteralPath ($prefix+'_cpu.csv') -NoTypeInformation -Encoding UTF8
  $verification54=if($SelfTest){'Synthetic self-test with owned idle PowerShell child; not gameplay'}else{'User declaration via Mesurer button; no automated screenshot verification'}
  Save-RelayJson54 ($prefix+'_metadata.json') @{trial=$label;phase=$cap.phase;category=$cap.category;started_utc=$script:relayStarted54;ended_utc=[DateTime]::UtcNow.ToString('o');seconds_actual=$now;logical_processors=[Environment]::ProcessorCount;samples=$script:relayRows54.Count;fps_user_snapshot=$cap.fps;ui_state_declaration_utc=$cap.declared_utc;ui_state_verified_by=$verification54;self_test=[bool]$SelfTest;fps_continuous_mean_measured=$false;input_latency_measured=$false;startup_benchmark=$false;sampler_overhead_not_subtracted=$true}
  $script:relayBusy54=$false;$script:relayPhaseIndex54++
  if($script:relayPhaseIndex54 -ge $script:relayPhases54.Count){Stop-RelayChild54;$script:relayTrialIndex54++;$script:relayPhaseIndex54=0}
  $status54.Text='Prise CPU enregistrée. Préparer la vue suivante.';$form54.Show();Update-RelayView54
  if($SelfTest){
   $script:relaySelfTestComplete54=$true;$script:relaySelfTestVisible54=$form54.Visible
   $script:relayChild54.Refresh();$script:relaySelfTestChildAlive54=-not $script:relayChild54.HasExited
   $form54.Close()
  }
 }catch{
  $script:relaySelfTestError54=$_.Exception.Message
  $timer54.Stop();$script:relayBusy54=$false
  if($script:relayRun54){$errorFile=Join-Path $script:relayRun54 ('CAPTURE_ERROR_'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')+'.json');Save-RelayJson54 $errorFile @{error=$_.Exception.Message;measured_valid=$false}}
  $form54.Show();$status54.Text=$_.Exception.Message;$primary54.Enabled=$true
  if($SelfTest){$form54.Close()}
 }
})
$close54.Add_Click({$form54.Close()})
$form54.Add_FormClosing({$timer54.Stop();if($script:relayBusy54 -and $script:relayRun54){$script:relayClosingDuringCapture54=$true;Save-RelayJson54 (Join-Path $script:relayRun54 ('INTERRUPTED_'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')+'.json')) @{valid_capture=$false;reason='Assistant closed during capture';self_test=[bool]$SelfTest}};Stop-RelayChild54})
Update-RelayView54
if($Preview){$status54.Text='Aperçu uniquement : lancement et mesure désactivés.';$previewTimer54=New-Object Windows.Forms.Timer;$previewTimer54.Interval=30000;$previewTimer54.Add_Tick({$previewTimer54.Stop();$form54.Close()});$previewTimer54.Start()}
if($SelfTest){
 $mode54=if($LegacyLoop){'LEGACY'}else{'FIXED'}
 $script:relayRun54=Join-Path $relayRoot54 ('SELFTEST_'+$mode54+'_'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ'))
 [void][IO.Directory]::CreateDirectory($script:relayRun54)
 $script:relayChild54=Start-Process -FilePath (Join-Path $PSHOME 'pwsh.exe') -ArgumentList @('-NoProfile','-Command','Start-Sleep -Seconds 60') -WindowStyle Hidden -PassThru
 Save-RelayJson54 (Join-Path $script:relayRun54 'LAUNCH.json') @{self_test=$true;victoria3_launched=$false;process_id=$script:relayChild54.Id;process_kind='owned idle PowerShell';started_utc=[DateTime]::UtcNow.ToString('o')}
 $selfTestBegin54=New-Object Windows.Forms.Timer;$selfTestBegin54.Interval=250
 $selfTestBegin54.Add_Tick({$selfTestBegin54.Stop();Start-RelayCapture54 $null})
 $form54.Add_Shown({$selfTestBegin54.Start()})
}
# Hiding a modal ShowDialog ends that dialog and triggers its closing cleanup.
# Application.Run keeps the message loop and the capture timer alive while hidden.
if($LegacyLoop){[void]$form54.ShowDialog()}else{[Windows.Forms.Application]::Run($form54)}
if($SelfTest){
 $timer54.Stop();Stop-RelayChild54
 $metaFile54=Join-Path $script:relayRun54 'closed_paused_none_metadata.json'
 $meta54=if(Test-Path -LiteralPath $metaFile54){Get-Content -LiteralPath $metaFile54 -Raw|ConvertFrom-Json}else{$null}
 $passed54=$script:relaySelfTestComplete54 -and $script:relaySelfTestVisible54 -and $script:relaySelfTestChildAlive54 -and -not $script:relayClosingDuringCapture54 -and $meta54.samples -ge 14 -and $meta54.seconds_actual -ge 15 -and $meta54.seconds_actual -lt 20
 $result54=@{status=$(if($passed54){'PASS'}else{'FAIL'});loop=$mode54;self_test=$true;victoria3_launched=$false;capture_completed=$script:relaySelfTestComplete54;assistant_visible_after_capture=$script:relaySelfTestVisible54;owned_child_alive_after_capture=$script:relaySelfTestChildAlive54;closing_during_capture=$script:relayClosingDuringCapture54;samples=$meta54.samples;seconds_actual=$meta54.seconds_actual;error=$script:relaySelfTestError54;result_directory=$script:relayRun54}
 Save-RelayJson54 (Join-Path $script:relayRun54 'RESULT.json') $result54
 $result54|ConvertTo-Json -Depth 4
}

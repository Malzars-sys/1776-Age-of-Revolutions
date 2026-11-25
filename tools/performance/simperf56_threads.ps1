param([Parameter(Mandatory=$true)][int]$GameProcessId,
      [Parameter(Mandatory=$true)][string]$RunDirectory)
$ErrorActionPreference='Stop'
$target56=Get-Process -Id $GameProcessId
if($target56.ProcessName -ne 'victoria3'){throw 'Expected owned Victoria 3 process.'}
$birth56=$target56.StartTime
$output56=Join-Path $RunDirectory 'THREAD_CPU.csv'
if(Test-Path -LiteralPath $output56){throw 'Preserve prior thread data.'}
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class ThreadName56 {
 [DllImport("kernel32.dll")] static extern IntPtr OpenThread(uint access, bool inherit, uint id);
 [DllImport("kernel32.dll")] static extern int GetThreadDescription(IntPtr handle,out IntPtr text);
 [DllImport("kernel32.dll")] static extern IntPtr LocalFree(IntPtr memory);
 [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr handle);
 public static string Read(uint id) {
  IntPtr h=OpenThread(0x0800,false,id); if(h==IntPtr.Zero)return "";
  try {IntPtr p; if(GetThreadDescription(h,out p)!=0)return "";
   try{return Marshal.PtrToStringUni(p)??"";}finally{LocalFree(p);}
  }finally{CloseHandle(h);}
 }
}
'@
$names56=@{}
$writer56=[IO.StreamWriter]::new($output56,$false,[Text.UTF8Encoding]::new($true))
$writer56.AutoFlush=$true
$writer56.WriteLine('utc,thread_id,cpu_total_ms,start_address,name')
$culture56=[Globalization.CultureInfo]::InvariantCulture
try{
 while(-not $target56.HasExited){
  $target56.Refresh()
  if($target56.HasExited){break}
  if($target56.StartTime -ne $birth56){throw 'Process identity changed.'}
  $stamp56=[DateTime]::UtcNow.ToString('o')
  foreach($thread56 in $target56.Threads){
   try{
    $tid56=$thread56.Id
    if(-not $names56.ContainsKey($tid56)){$names56[$tid56]=[ThreadName56]::Read($tid56)}
    $cpu56=$thread56.TotalProcessorTime.TotalMilliseconds.ToString($culture56)
    $name56='"'+$names56[$tid56].Replace('"','""')+'"'
    $writer56.WriteLine((@($stamp56,$tid56,$cpu56,('0x'+$thread56.StartAddress.ToInt64().ToString('x')),$name56)-join ','))
   }catch{continue}
  }
  Start-Sleep -Milliseconds 500
 }
}finally{$writer56.Dispose()}

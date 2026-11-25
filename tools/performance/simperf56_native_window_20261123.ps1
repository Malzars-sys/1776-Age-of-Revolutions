param(
 [Parameter(Mandatory=$true)][int]$GameProcessId,
 [ValidateSet('inspect','place','capture','click')][string]$Action='inspect',
 [string]$CapturePath,
 [int]$X=0,[int]$Y=0
)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
public static class Sim56Window {
 public delegate bool EnumProc(IntPtr h, IntPtr l);
 [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb,IntPtr l);
 [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h,out uint p);
 [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h,out RECT r);
 [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h,out RECT r);
 [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr h,ref POINT p);
 [DllImport("user32.dll",SetLastError=true)] public static extern bool MoveWindow(IntPtr h,int x,int y,int w,int z,bool repaint);
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll",SetLastError=true)] public static extern bool SetCursorPos(int x,int y);
 [DllImport("user32.dll")] public static extern void mouse_event(uint f,uint x,uint y,uint d,UIntPtr e);
 public struct RECT {public int Left,Top,Right,Bottom;}
 public struct POINT {public int X,Y;}
 public static IntPtr[] Find(uint pid) {
  var a=new List<IntPtr>();
  EnumWindows((h,l)=>{uint p;GetWindowThreadProcessId(h,out p);if(p==pid&&IsWindowVisible(h))a.Add(h);return true;},IntPtr.Zero);
  return a.ToArray();
 }
}
'@
$windows56=@([Sim56Window]::Find($GameProcessId))
if($windows56.Count -ne 1){throw "Expected exactly one visible window owned by trial process; found $($windows56.Count)."}
$handle56=$windows56[0]
$rect56=New-Object Sim56Window+RECT
[void][Sim56Window]::GetWindowRect($handle56,[ref]$rect56)
$secondary56=@([System.Windows.Forms.Screen]::AllScreens|Where-Object{-not $_.Primary})
if($secondary56.Count -ne 1){throw 'Expected exactly one secondary screen.'}
if($Action -eq 'place'){
 $screen56=$secondary56[0].WorkingArea
 $w56=$rect56.Right-$rect56.Left;$h56=$rect56.Bottom-$rect56.Top
 if($w56 -gt $screen56.Width -or $h56 -gt $screen56.Height){throw 'Trial window does not fit the secondary screen.'}
 if(-not [Sim56Window]::MoveWindow($handle56,$screen56.Left+20,$screen56.Top+10,$w56,$h56,$true)){throw "MoveWindow failed: $([Runtime.InteropServices.Marshal]::GetLastWin32Error())"}
 [void][Sim56Window]::GetWindowRect($handle56,[ref]$rect56)
}
$client56=New-Object Sim56Window+RECT
[void][Sim56Window]::GetClientRect($handle56,[ref]$client56)
$origin56=New-Object Sim56Window+POINT
[void][Sim56Window]::ClientToScreen($handle56,[ref]$origin56)
if($Action -eq 'click'){
 if($X -lt 0 -or $Y -lt 0 -or $X -ge $client56.Right -or $Y -ge $client56.Bottom){throw 'Click outside trial client area.'}
 [void][Sim56Window]::SetForegroundWindow($handle56)
 Start-Sleep -Milliseconds 200
 if([Sim56Window]::GetForegroundWindow() -ne $handle56){throw 'Trial window did not acquire foreground; no input sent.'}
 if(-not [Sim56Window]::SetCursorPos($origin56.X+$X,$origin56.Y+$Y)){throw "Cursor positioning failed: $([Runtime.InteropServices.Marshal]::GetLastWin32Error()); no click sent."}
 [Sim56Window]::mouse_event(2,0,0,0,[UIntPtr]::Zero)
 Start-Sleep -Milliseconds 70
 [Sim56Window]::mouse_event(4,0,0,0,[UIntPtr]::Zero)
}
if($Action -eq 'capture'){
 if(-not $CapturePath -or (Test-Path -LiteralPath $CapturePath)){throw 'A new evidence path is required.'}
 $bitmap56=[Drawing.Bitmap]::new($client56.Right,$client56.Bottom)
 $graphics56=[Drawing.Graphics]::FromImage($bitmap56)
 try{
  $graphics56.CopyFromScreen($origin56.X,$origin56.Y,0,0,$bitmap56.Size)
  $bitmap56.Save($CapturePath,[Drawing.Imaging.ImageFormat]::Png)
 }finally{$graphics56.Dispose();$bitmap56.Dispose()}
}
[ordered]@{utc=[DateTime]::UtcNow.ToString('o');process_id=$GameProcessId;window=$handle56.ToInt64();action=$Action;client=@{x=$origin56.X;y=$origin56.Y;width=$client56.Right;height=$client56.Bottom};bounds=@{x=$rect56.Left;y=$rect56.Top;width=$rect56.Right-$rect56.Left;height=$rect56.Bottom-$rect56.Top};secondary=$secondary56[0].DeviceName;capture=$CapturePath}|ConvertTo-Json -Depth 4

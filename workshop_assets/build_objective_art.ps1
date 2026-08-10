param(
	[string]$RepositoryRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$sourceRoot = Join-Path $RepositoryRoot 'workshop_assets\source'
$previewRoot = Join-Path $RepositoryRoot 'workshop_assets\previews'
$outputRoot = Join-Path $RepositoryRoot 'gfx\interface\icons\objectives'
$templatePath = Join-Path $outputRoot 'aor_imperial_rivalries_illu.dds'

function New-CroppedBitmap {
	param(
		[string]$SourcePath,
		[int]$X,
		[int]$Y,
		[int]$CropWidth,
		[int]$CropHeight,
		[int]$Width = 779,
		[int]$Height = 1327
	)

	$source = [System.Drawing.Image]::FromFile($SourcePath)
	try {
		$bitmap = New-Object System.Drawing.Bitmap($Width, $Height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
		$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
		try {
			$graphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceCopy
			$graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
			$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
			$graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
			$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
			$destination = New-Object System.Drawing.Rectangle(0, 0, $Width, $Height)
			$sourceRectangle = New-Object System.Drawing.Rectangle($X, $Y, $CropWidth, $CropHeight)
			$graphics.DrawImage($source, $destination, $sourceRectangle, [System.Drawing.GraphicsUnit]::Pixel)
		}
		finally {
			$graphics.Dispose()
		}
		return $bitmap
	}
	finally {
		$source.Dispose()
	}
}

function New-GrayscaleBitmap {
	param([System.Drawing.Bitmap]$Source)

	$result = New-Object System.Drawing.Bitmap($Source.Width, $Source.Height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
	$graphics = [System.Drawing.Graphics]::FromImage($result)
	$attributes = New-Object System.Drawing.Imaging.ImageAttributes
	try {
		$matrix = New-Object System.Drawing.Imaging.ColorMatrix(,([single[][]]@(
			[single[]]@(0.299, 0.299, 0.299, 0, 0),
			[single[]]@(0.587, 0.587, 0.587, 0, 0),
			[single[]]@(0.114, 0.114, 0.114, 0, 0),
			[single[]]@(0, 0, 0, 1, 0),
			[single[]]@(0, 0, 0, 0, 1)
		)))
		$attributes.SetColorMatrix($matrix)
		$destination = New-Object System.Drawing.Rectangle(0, 0, $Source.Width, $Source.Height)
		$graphics.DrawImage($Source, $destination, 0, 0, $Source.Width, $Source.Height, [System.Drawing.GraphicsUnit]::Pixel, $attributes)
	}
	finally {
		$attributes.Dispose()
		$graphics.Dispose()
	}
	return $result
}

function Write-DdsMipChain {
	param(
		[System.Drawing.Bitmap]$BaseBitmap,
		[string]$OutputPath,
		[string]$HeaderTemplatePath
	)

	$templateBytes = [System.IO.File]::ReadAllBytes($HeaderTemplatePath)
	$stream = New-Object System.IO.FileStream($OutputPath, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write)
	try {
		$stream.Write($templateBytes, 0, 128)
		$current = $BaseBitmap.Clone()
		try {
			for ($level = 0; $level -lt 11; $level++) {
				$rectangle = New-Object System.Drawing.Rectangle(0, 0, $current.Width, $current.Height)
				$data = $current.LockBits($rectangle, [System.Drawing.Imaging.ImageLockMode]::ReadOnly, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
				try {
					$rowBytes = $current.Width * 4
					$row = New-Object byte[] $rowBytes
					for ($y = 0; $y -lt $current.Height; $y++) {
						$sourceY = if ($data.Stride -ge 0) { $y } else { $current.Height - 1 - $y }
						$pointer = [System.IntPtr]::Add($data.Scan0, $sourceY * [Math]::Abs($data.Stride))
						[System.Runtime.InteropServices.Marshal]::Copy($pointer, $row, 0, $rowBytes)
						for ($alpha = 3; $alpha -lt $rowBytes; $alpha += 4) {
							$row[$alpha] = 255
						}
						$stream.Write($row, 0, $rowBytes)
					}
				}
				finally {
					$current.UnlockBits($data)
				}

				if ($level -lt 10) {
					$nextWidth = [Math]::Max(1, [Math]::Floor($current.Width / 2))
					$nextHeight = [Math]::Max(1, [Math]::Floor($current.Height / 2))
					$next = New-Object System.Drawing.Bitmap($nextWidth, $nextHeight, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
					$graphics = [System.Drawing.Graphics]::FromImage($next)
					try {
						$graphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceCopy
						$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
						$graphics.DrawImage($current, 0, 0, $nextWidth, $nextHeight)
					}
					finally {
						$graphics.Dispose()
					}
					$current.Dispose()
					$current = $next
				}
			}
		}
		finally {
			$current.Dispose()
		}
	}
	finally {
		$stream.Dispose()
	}
}

$assets = @(
	@{
		Source = 'khem_karan_mounted_prince_hunting_lion.jpg'
		Output = 'aor_battle_for_india_illu.dds'
		Preview = 'aor_battle_for_india_preview.png'
		Crop = @(250, 250, 1350, 2300)
	},
	@{
		Source = 'prise_de_la_bastille_houel_gallica.jpg'
		Output = 'aor_age_of_revolutions_illu.dds'
		Preview = 'aor_age_of_revolutions_preview.png'
		Crop = @(900, 100, 3229, 5500)
	},
	@{
		Source = 'canaletto_bucintoro_google_art_project.jpg'
		Output = 'aor_mercantile_republics_illu.dds'
		Preview = 'aor_mercantile_republics_preview.png'
		Crop = @(2800, 40, 2295, 3910)
	}
)

foreach ($asset in $assets) {
	$crop = $asset.Crop
	$bitmap = New-CroppedBitmap -SourcePath (Join-Path $sourceRoot $asset.Source) -X $crop[0] -Y $crop[1] -CropWidth $crop[2] -CropHeight $crop[3]
	try {
		$bitmap.Save((Join-Path $previewRoot $asset.Preview), [System.Drawing.Imaging.ImageFormat]::Png)
		Write-DdsMipChain -BaseBitmap $bitmap -OutputPath (Join-Path $outputRoot $asset.Output) -HeaderTemplatePath $templatePath

		if ($asset.Output -eq 'aor_mercantile_republics_illu.dds') {
			$disabled = New-GrayscaleBitmap -Source $bitmap
			try {
				Write-DdsMipChain -BaseBitmap $disabled -OutputPath (Join-Path $outputRoot 'aor_mercantile_republics_illu_dis.dds') -HeaderTemplatePath $templatePath
			}
			finally {
				$disabled.Dispose()
			}
		}
	}
	finally {
		$bitmap.Dispose()
	}
}

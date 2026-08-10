param(
    [string]$RepositoryRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$thumbnailPath = Join-Path $RepositoryRoot 'thumbnail.png'
$sourcePath = Join-Path $RepositoryRoot 'workshop_assets\source\thumbnail_before_fork_badge.png'
$metadataPath = Join-Path $RepositoryRoot '.metadata\thumbnail.png'
$previewRoot = Join-Path $RepositoryRoot 'workshop_assets\previews'

if (-not (Test-Path -LiteralPath $sourcePath)) {
    Copy-Item -LiteralPath $thumbnailPath -Destination $sourcePath
}

function New-ResizedPng {
    param(
        [Parameter(Mandatory)] [System.Drawing.Image]$Source,
        [Parameter(Mandatory)] [int]$Size,
        [Parameter(Mandatory)] [string]$Destination
    )

    $bitmap = [System.Drawing.Bitmap]::new($Size, $Size, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    try {
        $bitmap.SetResolution(96, 96)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        try {
            $graphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceCopy
            $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
            $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
            $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
            $graphics.DrawImage($Source, 0, 0, $Size, $Size)
        }
        finally {
            $graphics.Dispose()
        }
        $bitmap.Save($Destination, [System.Drawing.Imaging.ImageFormat]::Png)
    }
    finally {
        $bitmap.Dispose()
    }
}

$sourceImage = [System.Drawing.Image]::FromFile($sourcePath)
try {
    $final = [System.Drawing.Bitmap]::new(600, 600, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    try {
        $final.SetResolution(96, 96)
        $graphics = [System.Drawing.Graphics]::FromImage($final)
        try {
            $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
            $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
            $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
            $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
            $graphics.DrawImage($sourceImage, 0, 0, 600, 600)

            $panel = [System.Drawing.Rectangle]::new(378, 18, 202, 80)
            $panelBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(246, 105, 22, 33))
            $outerPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(255, 218, 174, 68), 5)
            $innerPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(255, 255, 235, 166), 2)
            $font = [System.Drawing.Font]::new('Georgia', 42, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
            $textBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(255, 255, 255, 255))
            $format = [System.Drawing.StringFormat]::new()
            try {
                $format.Alignment = [System.Drawing.StringAlignment]::Center
                $format.LineAlignment = [System.Drawing.StringAlignment]::Center
                $graphics.FillRectangle($panelBrush, $panel)
                $graphics.DrawRectangle($outerPen, $panel)
                $graphics.DrawRectangle($innerPen, 386, 26, 186, 64)
                $graphics.DrawString('FORK', $font, $textBrush, [System.Drawing.RectangleF]::new(378, 15, 202, 80), $format)
            }
            finally {
                $format.Dispose()
                $textBrush.Dispose()
                $font.Dispose()
                $innerPen.Dispose()
                $outerPen.Dispose()
                $panelBrush.Dispose()
            }
        }
        finally {
            $graphics.Dispose()
        }

        $final.Save($thumbnailPath, [System.Drawing.Imaging.ImageFormat]::Png)
        New-ResizedPng -Source $final -Size 512 -Destination $metadataPath
        New-ResizedPng -Source $final -Size 512 -Destination (Join-Path $previewRoot 'thumbnail_preview_512.png')
        New-ResizedPng -Source $final -Size 256 -Destination (Join-Path $previewRoot 'thumbnail_preview_256.png')
        New-ResizedPng -Source $final -Size 128 -Destination (Join-Path $previewRoot 'thumbnail_preview_128.png')
    }
    finally {
        $final.Dispose()
    }
}
finally {
    $sourceImage.Dispose()
}

Write-Output 'Thumbnail and QA previews generated without AI.'

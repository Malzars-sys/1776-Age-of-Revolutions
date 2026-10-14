# Uses the existing MapPaintingTextures array: no new texture/sampler bindings.
# Slot 0 = double sentinel; slot 1 = exact province mask, 512 x 512.
PixelShader = {
 Code
 [[
  bool Aor1776TryImperialOverlay( float2 MapCoords, out float3 Color, out float BeforeLighting, out float AfterLighting )
  {
   Color = float3( 0.0, 0.0, 0.0 );
   BeforeLighting = 0.0;
   AfterLighting = 0.0;
   if ( !_UseMapmodeTextures )
   {
    return false;
   }
   // End-point colors survive both linear and sRGB texture interpretation.
   float4 ProbeA = PdxTex2DLod0( MapPaintingTextures, float3( 0.25, 0.5, 0.0 ) );
   float4 ProbeB = PdxTex2DLod0( MapPaintingTextures, float3( 0.75, 0.5, 0.0 ) );
   if ( !( ProbeA.r > 0.99 && ProbeA.g < 0.01 && ProbeA.b > 0.99 && ProbeA.a > 0.99 &&
           ProbeB.r < 0.01 && ProbeB.g > 0.99 && ProbeB.b > 0.99 && ProbeB.a > 0.99 ) )
   {
    return false;
   }
   // Same lake/sea identification as native ApplyDynamicFlatmap.
   float4 AlternateColor = ColorSampleAtOffset( MapCoords, ProvinceColorIndirectionTexture, ProvinceColorTexture, AlternateProvinceColorsOffset );
   AlternateColor.rg = float2( 0.0, 0.0 );
   float4 LakeDiff = float4( 0.0, 0.0, 0.0, 1.0 ) - AlternateColor;
   float4 SeaDiff = float4( 0.0, 0.0, 1.0, 0.0 ) - AlternateColor;
   if ( dot( LakeDiff, LakeDiff ) < 0.1 || dot( SeaDiff, SeaDiff ) < 0.1 )
   {
    return true;
   }
   // Native world Z is south->north; source PNG rows are north->south.
   float2 Pixel = floor( float2( MapCoords.x, 1.0 - MapCoords.y ) * _ProvinceMapSize );
   float2 LocalPixel = Pixel - float2( 4152.0, 708.0 );
   float Imperial = 0.0;
   if ( all( LocalPixel >= float2( 0.0, 0.0 ) ) && all( LocalPixel < float2( 512.0, 512.0 ) ) )
   {
    // Lod 0 and texel centres: no mip loss or interpolation of small fiefs.
    float2 MaskUv = ( LocalPixel + float2( 0.5, 0.5 ) ) / 512.0;
    Imperial = step( 0.5, PdxTex2DLod0( MapPaintingTextures, float3( MaskUv, 1.0 ) ).r );
   }
   Color = ToLinear( lerp( float3( 0.337, 0.349, 0.361 ), float3( 0.941, 0.800, 0.239 ), Imperial ) );
   AfterLighting = _OverlayOpacity;
   return true;
  }
 ]]
}

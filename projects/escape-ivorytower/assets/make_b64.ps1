$base = "C:/Users/Administrator/真心姑娘/projects/escape-ivorytower/assets"
$files = @{
  "bg"           = "$base/backgrounds/Clean_flat_illustration_style__2026-05-17T12-38-18.png"
  "leader_full"  = "$base/characters/Clean_flat_illustration_style__2026-05-17T12-25-10.png"
  "leader_avatar"= "$base/characters/Clean_flat_illustration_style__2026-05-17T13-04-25.png"
  "lijijie"      = "$base/characters/Clean_flat_illustration_style__2026-05-17T13-24-17.png"
  "xiaowang"     = "$base/characters/Clean_flat_illustration_style__2026-05-17T13-24-19.png"
  "hr"           = "$base/characters/Clean_flat_illustration_style__2026-05-17T13-24-31.png"
}
foreach ($key in $files.Keys) {
  $path = $files[$key]
  $bytes = [IO.File]::ReadAllBytes($path)
  $b64 = [Convert]::ToBase64String($bytes)
  $out = "$base/b64_$key.txt"
  [IO.File]::WriteAllText($out, $b64)
  Write-Host "$key : $([int]($b64.Length/1024)) KB -> $out"
}
Write-Host "Done."

# harness\init.ps1 - Arnes Dinamico de Salud y Verificacion en Windows (v4.3)
$ErrorActionPreference = "Stop"

Write-Host "=== [SDD Harness v4.3] Verificando Salud del Repositorio ===" -ForegroundColor Cyan

$RequiredFiles = @("AGENTS.md", "anti-gravity.md", ".specify\memory\constitution.md", ".specify\harness-config.json", "feature_list.json")
foreach ($file in $RequiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Error "[Error Critico]: Falta el archivo fundamental $file."
        exit 1
    }
}

try {
    $Config = Get-Content -Path ".specify\harness-config.json" -Raw -Encoding UTF8 | ConvertFrom-Json
} catch {
    Write-Error "[Error Critico]: .specify\harness-config.json contiene JSON invalido."
    exit 1
}

try {
    $rawJson = Get-Content -Path "feature_list.json" -Raw -Encoding UTF8
    $Features = @()
    if (-not [string]::IsNullOrWhiteSpace($rawJson)) {
        $parsed = ConvertFrom-Json $rawJson
        if ($null -ne $parsed) {
            if ($parsed.PSObject.Properties["features"]) { $parsed = $parsed.features }
            foreach ($item in $parsed) { if ($null -ne $item) { $Features += $item } }
        }
    }
} catch {
    Write-Error "[Error Critico]: feature_list.json contiene JSON invalido."
    exit 1
}

if ($Features.Count -gt 0) {
    $InProgressList = @($Features | Where-Object { $_.status -eq "in_progress" })
    if ($InProgressList.Count -gt 1) {
        Write-Error "[Violacion de Arnes]: Hay $($InProgressList.Count) tareas en in_progress. Maximo 1 a la vez."
        exit 1
    }
    if ($InProgressList.Count -eq 1) {
        $Active = $InProgressList[0]
        if ([string]::IsNullOrWhiteSpace($Active.approval_hash)) {
            Write-Error "[Violacion Criptografica]: La funcionalidad $($Active.id) esta en in_progress sin approval_hash. Ejecuta: .\harness\sdd.ps1 -Action approve -FeatureId $($Active.id)"
            exit 1
        }
        $SpecDir = if ($Active.feature_dir) { $Active.feature_dir } else { $Active.id }
        $SpecPath = "specs\$SpecDir\spec.md"
        $FeatPath = "specs\$SpecDir\scenarios.feature"
        if ((Test-Path $SpecPath) -and (Test-Path $FeatPath)) {
            $SpecContent = Get-Content -Path $SpecPath -Raw -Encoding UTF8
            $FeatContent = Get-Content -Path $FeatPath -Raw -Encoding UTF8
            $Combined = $SpecContent + "---" + $FeatContent
            $Hasher = [System.Security.Cryptography.SHA256]::Create()
            $CurrentHash = [BitConverter]::ToString($Hasher.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Combined))) -replace "-"
            if ($CurrentHash -ne $Active.approval_hash) {
                Write-Error "[Spec Tampering]: La especificacion de $($Active.id) fue modificada tras la aprobacion. Re-aprueba con .\harness\sdd.ps1 -Action approve -FeatureId $($Active.id)"
                exit 1
            }
        }
    }
}

if (Test-Path $Config.source_dir) {
    $CodeFiles = @(Get-ChildItem -Path $Config.source_dir -Filter $Config.file_extension -Recurse -ErrorAction SilentlyContinue)
    if ($CodeFiles.Count -gt 0 -and $Config.typecheck_cmd) {
        Write-Host "Ejecutando analisis estatico ($($Config.typecheck_cmd))..." -ForegroundColor Yellow
        Invoke-Expression $Config.typecheck_cmd
        if ($LASTEXITCODE -ne 0) {
            Write-Error "[Error de Calidad]: Fallo el analisis de tipos estaticos."
            exit 1
        }
    }
}

if (Test-Path $Config.test_dir) {
    $TestFiles = @(Get-ChildItem -Path $Config.test_dir -Filter $Config.file_extension -Recurse -ErrorAction SilentlyContinue)
    if ($TestFiles.Count -gt 0 -and $Config.test_cmd) {
        Write-Host "Ejecutando suite de pruebas ($($Config.test_cmd))..." -ForegroundColor Yellow
        Invoke-Expression $Config.test_cmd
        if ($LASTEXITCODE -ne 0) {
            Write-Error "[Error de Testing]: Las pruebas estan fallando."
            exit 1
        }
    }
}

Write-Host "[SDD Harness v4.3]: Entorno verificado exitosamente (Exit 0)." -ForegroundColor Green
exit 0
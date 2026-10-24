# harness\sdd.ps1 - Orquestador del Bucle SDD con Checkpoint Humano Interactivo (v4.3)
param (
    [ValidateSet("status", "next", "verify", "approve")]
    [string]$Action = "status",
    [string]$FeatureId,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

function Get-FeaturesList {
    $raw = Get-Content -Path "feature_list.json" -Raw -Encoding UTF8
    $list = @()
    if (-not [string]::IsNullOrWhiteSpace($raw)) {
        $parsed = ConvertFrom-Json $raw
        if ($null -ne $parsed) {
            if ($parsed.PSObject.Properties["features"]) { $parsed = $parsed.features }
            foreach ($item in $parsed) { if ($null -ne $item) { $list += $item } }
        }
    }
    return ,$list
}

function Invoke-InitCheck {
    $InitScript = "harness\init.ps1"
    if (Test-Path $InitScript) {
        & $InitScript | Out-Host
    } else {
        Write-Error "No se encontro $InitScript"
        exit 1
    }
    return (Get-FeaturesList)
}

function Invoke-ApproveFeature {
    param([string]$TargetId)
    $Features = Get-FeaturesList
    $Target = $null
    foreach ($item in $Features) {
        if ($null -ne $TargetId -and $TargetId -ne "") {
            if ($item.id -eq $TargetId -or $item.feature_dir -eq $TargetId) {
                $Target = $item
                break
            }
        } else {
            if ($item.status -eq "spec_ready") {
                $Target = $item
                break
            }
        }
    }
    if ($null -eq $Target) {
        Write-Error "No se encontro ninguna funcionalidad en estado spec_ready para aprobar."
        exit 1
    }
    $SpecDir = if ($Target.feature_dir) { $Target.feature_dir } else { $Target.id }
    $Target | Add-Member -NotePropertyName "feature_dir" -NotePropertyValue $SpecDir -Force
    $SpecPath = "specs\$SpecDir\spec.md"
    $FeatPath = "specs\$SpecDir\scenarios.feature"
    if ((-not (Test-Path $SpecPath)) -or (-not (Test-Path $FeatPath))) {
        Write-Error "Faltan archivos requeridos: $SpecPath o $FeatPath."
        exit 1
    }
    Write-Host "`n[HUMAN CHECKPOINT - CANDADO CRIPTOGRAFICO]" -ForegroundColor Magenta
    Write-Host "Revision formal de: [$($Target.id)] $($Target.name)" -ForegroundColor Cyan
    if (-not $Force) {
        $Confirmation = Read-Host "Confirmas la aprobacion humana para desbloquear in_progress? (S/N)"
        if ($Confirmation -notmatch "^[SsYy]$") {
            Write-Host "Aprobacion cancelada por el usuario." -ForegroundColor Yellow
            exit 0
        }
    } else {
        Write-Host "[Aprobacion Automatizada]: Confirmacion recibida via Antigravity IDE (-Force)." -ForegroundColor Green
    }
    $SpecContent = Get-Content -Path $SpecPath -Raw -Encoding UTF8
    $FeatContent = Get-Content -Path $FeatPath -Raw -Encoding UTF8
    $Combined = $SpecContent + "---" + $FeatContent
    $Hasher = [System.Security.Cryptography.SHA256]::Create()
    $ApprovalHash = [BitConverter]::ToString($Hasher.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Combined))) -replace "-"
    $Target | Add-Member -NotePropertyName "status" -NotePropertyValue "in_progress" -Force
    $Target | Add-Member -NotePropertyName "approval_hash" -NotePropertyValue $ApprovalHash -Force
    $Target | Add-Member -NotePropertyName "approved_at" -NotePropertyValue (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ") -Force
    $JsonOut = ConvertTo-Json -InputObject @($Features) -Depth 5
    if ($Features.Count -eq 1 -and $JsonOut -notmatch "^\s*\[") { $JsonOut = "[`r`n$JsonOut`r`n]" }
    $Utf8Bom = New-Object System.Text.UTF8Encoding($true)
    [System.IO.File]::WriteAllText((Join-Path $PWD "feature_list.json"), $JsonOut, $Utf8Bom)
    Write-Host "[APROBADO]: Firma SHA-256 registrada ($($ApprovalHash.Substring(0,16))...). Estado cambiado a in_progress." -ForegroundColor Green
}

switch ($Action) {
    "status" {
        $Features = Invoke-InitCheck
        Write-Host "`n=== Estado del Backlog de Funcionalidades (SDD v4.3) ===" -ForegroundColor Cyan
        if ($Features.Count -eq 0) {
            Write-Host "El backlog esta vacio []." -ForegroundColor Yellow
            exit 0
        }
        foreach ($f in $Features) {
            $st = if ($f.status) { $f.status } else { "pending" }
            $color = switch ($st) {
                "done" { "Green" }
                "in_progress" { "Yellow" }
                "spec_ready" { "Magenta" }
                "review" { "DarkYellow" }
                default { "Gray" }
            }
            $hashShort = if ($f.approval_hash) { " [SHA: $($f.approval_hash.Substring(0,8))]" } else { "" }
            Write-Host "[$($st.ToUpper())] $($f.id): $($f.name)$hashShort" -ForegroundColor $color
        }
    }
    "verify" {
        Invoke-InitCheck | Out-Null
    }
    "approve" {
        Invoke-ApproveFeature -TargetId $FeatureId
    }
    "next" {
        $Features = Invoke-InitCheck
        if ($Features.Count -eq 0) {
            Write-Host "`n[BACKLOG VACIO]: Inicia tu primera funcionalidad con .agents/skills/sdd-onboard.md." -ForegroundColor Yellow
            exit 0
        }
        $Active = $null
        foreach ($item in $Features) {
            if ($item.status -in @("pending", "spec_ready", "in_progress", "review")) {
                $Active = $item
                break
            }
        }
        if ($null -eq $Active) {
            Write-Host "`n[EXITO TOTAL]: Todas las funcionalidades estan en done." -ForegroundColor Green
            exit 0
        }
        $SpecDir = if ($Active.feature_dir) { $Active.feature_dir } else { $Active.id }
        Write-Host "`n------------------------------------------------------------------" -ForegroundColor Cyan
        Write-Host "  FUNCIONALIDAD ACTIVA: [$($Active.id)] $($Active.name)" -ForegroundColor Cyan
        Write-Host "  ESTADO ACTUAL: $($Active.status.ToUpper())" -ForegroundColor Cyan
        Write-Host "------------------------------------------------------------------" -ForegroundColor Cyan
        switch ($Active.status) {
            "pending" {
                Write-Host "PASO A EJECUTAR: Fase 1 - SPECIFY (EARS + Gherkin)" -ForegroundColor Blue
                Write-Host " Instruccion: Redacta specs\$SpecDir\spec.md y scenarios.feature usando .specify\templates\."
            }
            "spec_ready" {
                Write-Host "CHECKPOINT HUMANO 1: Aprobacion Criptografica Requerida" -ForegroundColor Magenta
                Invoke-ApproveFeature -TargetId $Active.id
            }
            "in_progress" {
                Write-Host "PASO A EJECUTAR: Fase 5 - IMPLEMENTACION DOUBLE-LOOP (BDD + TDD)" -ForegroundColor Yellow
                Write-Host " Instruccion: Pide al agente ejecutar sdd-plan.md, sdd-tasks.md y luego sdd-implement.md sobre specs\$SpecDir\."
            }
            "review" {
                Write-Host "PASO A EJECUTAR: Fase 6 - AUDITORIA SEPTUPLE" -ForegroundColor DarkYellow
                Write-Host " Instruccion: Verifica docs\user_guide_$SpecDir.md, ejecuta .\harness\spec-gate.ps1 -FeatureId $SpecDir y audita CHECKPOINTS.md."
            }
        }
    }
}
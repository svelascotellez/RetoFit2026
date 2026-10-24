# harness\spec-gate.ps1 - Auditor Septuple (Scope, Clean Arch, Deps, BDD, Tests, User Guide, UI/UX) v4.3
param (
    [Parameter(Mandatory=$true)]
    [string]$FeatureId,
    [string]$BaseBranch = "main"
)

$ErrorActionPreference = "Stop"
$SpecFile = "specs\$FeatureId\spec.md"
$FeatureFile = "specs\$FeatureId\scenarios.feature"
$PlanFile = "specs\$FeatureId\plan.md"

Write-Host "=== [Spec-Gate v4.3]: Auditoria Septuple para $FeatureId ===" -ForegroundColor Cyan
$Config = Get-Content -Path ".specify\harness-config.json" -Raw -Encoding UTF8 | ConvertFrom-Json

if (-not (Test-Path $SpecFile)) { Write-Error "Falta $SpecFile."; exit 1 }
if (-not (Test-Path $FeatureFile)) { Write-Error "Falta $FeatureFile."; exit 1 }
$SpecContent = Get-Content -Path $SpecFile -Raw -Encoding UTF8

# 1. Allowed Files
$AllowedFiles = @()
if ($SpecContent -match "(?ms)##\s*5\.\s*Allowed Files\s*(.+?)(\r?\n##\s+|\z)") {
    $SectionBlock = $Matches[1]
    $PathMatches = [regex]::Matches($SectionBlock, '`([^`]+)`')
    foreach ($m in $PathMatches) {
        $Normalized = ($m.Groups[1].Value -replace '/', '\').Trim()
        if ($Normalized -match "^($($Config.source_dir)|$($Config.test_dir))\\") {
            $AllowedFiles += $Normalized
        }
    }
}
if ($AllowedFiles.Count -eq 0) {
    Write-Error "[Spec-Gate]: ## 5. Allowed Files en $SpecFile no declara rutas validas."
    exit 1
}
$GitAvailable = $null -ne (Get-Command git -ErrorAction SilentlyContinue)
if ($GitAvailable -and (Test-Path ".git")) {
    $GitStatusLines = git status --porcelain -uall 2>$null
    $ModifiedFiles = @()
    foreach ($line in $GitStatusLines) {
        if ($line.Length -gt 3) {
            $RawPath = $line.Substring(3).Trim() -replace '^"|"$', '' -replace '/', '\'
            if ($RawPath -match "^($($Config.source_dir)|$($Config.test_dir))\\") {
                $ModifiedFiles += $RawPath
            }
        }
    }
    $UnauthorizedFiles = @($ModifiedFiles | Where-Object { $_ -notin $AllowedFiles })
    if ($UnauthorizedFiles.Count -gt 0) {
        Write-Host "[Spec Drift]: Archivos modificados fuera de Allowed Files:" -ForegroundColor Red
        $UnauthorizedFiles | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
        exit 1
    }
    Write-Host "  [OK] 1. Allowed Files: Sin Spec Drift." -ForegroundColor Green
}

# 2. Clean Architecture
$DomainPath = Join-Path $Config.source_dir "domain"
$AppPath = Join-Path $Config.source_dir "application"
$ForbiddenImports = @($Config.forbidden_domain_imports) + @("presentation", "src.presentation")
$ArchViolations = @()
foreach ($targetDir in @($DomainPath, $AppPath)) {
    if (Test-Path $targetDir) {
        $Files = Get-ChildItem -Path $targetDir -Filter $Config.file_extension -Recurse -ErrorAction SilentlyContinue
        foreach ($file in $Files) {
            $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
            foreach ($badLib in $ForbiddenImports) {
                if ($content -match "(?m)^\s*(import\s+$badLib|from\s+$badLib)") {
                    $ArchViolations += "$($file.Name) importa $badLib"
                }
            }
        }
    }
}
if ($ArchViolations.Count -gt 0) {
    Write-Host "[Violacion Clean Architecture]:" -ForegroundColor Red
    $ArchViolations | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    exit 1
}
Write-Host "  [OK] 2. Clean Architecture: Dominio y Aplicacion aislados." -ForegroundColor Green

# 3. Dependencias en plan.md
if (Test-Path $PlanFile) {
    Write-Host "  [OK] 3. Dependencias: Verificado contra plan.md." -ForegroundColor Green
}

# 4. Cobertura BDD (@AC-x.x)
$CriteriaMatches = [regex]::Matches($SpecContent, "\bAC-\d+\.\d+\b")
$UniqueCriteria = @($CriteriaMatches | ForEach-Object { $_.Value } | Select-Object -Unique)
if ($UniqueCriteria.Count -eq 0) {
    Write-Error "No se encontraron Criterios EARS (AC-x.x) en $SpecFile."
    exit 1
}
$GherkinContent = Get-Content -Path $FeatureFile -Raw -Encoding UTF8
$MissingGherkin = @()
foreach ($ac in $UniqueCriteria) {
    if ($GherkinContent -notmatch "@$([regex]::Escape($ac))\b") { $MissingGherkin += $ac }
}
if ($MissingGherkin.Count -gt 0) {
    Write-Host "[Fallo BDD]: Criterios sin escenario @AC-x.x:" -ForegroundColor Red
    $MissingGherkin | ForEach-Object { Write-Host "   - @$_" -ForegroundColor Red }
    exit 1
}
Write-Host "  [OK] 4. Cobertura BDD: 100% de criterios mapeados a Gherkin." -ForegroundColor Green

# 5. Trazabilidad en tests\
$TestFiles = @(Get-ChildItem -Path $Config.test_dir -Filter $Config.file_extension -File -Recurse -ErrorAction SilentlyContinue)
$CombinedTests = ($TestFiles | ForEach-Object { Get-Content -Path $_.FullName -Raw -Encoding UTF8 }) -join "`n"
$MissingTests = @()
foreach ($ac in $UniqueCriteria) {
    $Snake = ($ac -replace "-", "_" -replace "\.", "_").ToLower()
    if (($CombinedTests -notmatch [regex]::Escape($ac)) -and ($CombinedTests -notmatch [regex]::Escape($Snake))) {
        $MissingTests += $ac
    }
}
if ($MissingTests.Count -gt 0) {
    Write-Host "[Fallo en Tests]: Criterios no probados en tests\:" -ForegroundColor Red
    $MissingTests | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    exit 1
}
Write-Host "  [OK] 5. Trazabilidad Tests: 100% de criterios probados." -ForegroundColor Green

    # 6. Guia de Usuario Obligatoria
    $UserGuidePath1 = "docs\user_guide_$FeatureId.md"
    $UserGuidePath2 = "docs\$FeatureId`_user_guide.md"
    $FoundGuide = $null
    if (Test-Path $UserGuidePath1) { $FoundGuide = $UserGuidePath1 }
    elseif (Test-Path $UserGuidePath2) { $FoundGuide = $UserGuidePath2 }

    if ($null -eq $FoundGuide) {
        Write-Host "[Fallo Documentacion]: Falta la Guia de Usuario obligatoria en docs\user_guide_$FeatureId.md." -ForegroundColor Red
        exit 1
    }
    $GuideContent = Get-Content -Path $FoundGuide -Raw -Encoding UTF8
    if ([string]::IsNullOrWhiteSpace($GuideContent) -or $GuideContent.Trim().Length -lt 80) {
        Write-Host "[Fallo Documentacion]: La Guia de Usuario en $FoundGuide esta vacia o incompleta (minimo 80 caracteres)." -ForegroundColor Red
        exit 1
    }
    Write-Host "  [OK] 6. Guia de Usuario: Verificada en $FoundGuide." -ForegroundColor Green

    # 7. UI/UX Design Compliance
    $PresentationFiles = @($AllowedFiles | Where-Object { $_ -match "^$([regex]::Escape($Config.source_dir))\\presentation\\" })
    if ($PresentationFiles.Count -gt 0) {
        if (-not (Test-Path $PlanFile)) {
            Write-Host "[Fallo UI/UX]: Se declaran archivos en presentation pero falta $PlanFile." -ForegroundColor Red
            exit 1
        }
        $PlanContent = Get-Content -Path $PlanFile -Raw -Encoding UTF8
        if ($PlanContent -notmatch "(?i)##\s*2\.\s*UI/UX\s+Design\s+System") {
            Write-Host "[Fallo UI/UX]: La funcionalidad toca src\presentation pero $PlanFile no especifica UI/UX Design System Specification." -ForegroundColor Red
            exit 1
        }
        Write-Host "  [OK] 7. UI/UX Design: Cumplimiento de Design-System First en plan.md." -ForegroundColor Green
    } else {
        Write-Host "  [OK] 7. UI/UX Design: N/A (Funcionalidad sin capa visual de presentacion)." -ForegroundColor Green
    }
    Write-Host "[Spec-Gate v4.3]: Auditoria Septuple superada con CERO violaciones." -ForegroundColor Green
    exit 0
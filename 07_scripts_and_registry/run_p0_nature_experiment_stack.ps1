Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$logDir = Join-Path $repoRoot '08_nature_experiment_plan'
$logFile = Join-Path $logDir 'p0_rerun_log_v1.md'

$steps = @(
    @{ Name = 'Chao Phraya self-contained model'; Script = '07_scripts_and_registry/fit_chao_phraya_nature_model_selfcontained.py'; Args = @() },
    @{ Name = 'Chao Phraya area-weighted exposure'; Script = '07_scripts_and_registry/compute_chao_phraya_area_weighted_exposure.py'; Args = @('--outdir', '03_exposure_closure/chao_phraya_area_weighted_exposure_censoring') },
    @{ Name = 'Chao Phraya OSM exposure censoring'; Script = '07_scripts_and_registry/compute_chao_phraya_osm_exposure_censoring.py'; Args = @('--outdir', '03_exposure_closure/chao_phraya_osm_exposure_censoring') },
    @{ Name = 'Chao Phraya robustness grid'; Script = '07_scripts_and_registry/compute_chao_phraya_robustness_grid.py'; Args = @('--outdir', '03_exposure_closure/chao_phraya_robustness_grid') },
    @{ Name = 'Blocked equal-area closure'; Script = '07_scripts_and_registry/fit_multi_region_blocked_equal_area_closure.py'; Args = @() },
    @{ Name = 'Hierarchical model comparison'; Script = '07_scripts_and_registry/fit_hierarchical_model_comparison.py'; Args = @() },
    @{ Name = 'Transfer validation scores'; Script = '07_scripts_and_registry/build_transfer_validation_scores.py'; Args = @() }
)

$logLines = @(
    "# P0 Rerun Log v1",
    "",
    "Date: $(Get-Date -Format 'yyyy-MM-dd')",
    "",
    "## Status",
    "",
    "- Runner prepared but not executed in this edit pass.",
    "- The script is intentionally narrow: it only covers the manuscript-facing Nature rerun chain.",
    "",
    "## Steps",
    ""
)

foreach ($step in $steps) {
    $logLines += "- $($step.Name): `"$($step.Script)`""
}

$logLines += @(
    "",
    "## Notes",
    "",
    "- This runner stops on the first failure.",
    "- It does not attempt EGMS closure, which remains token-gated.",
    "- It does not touch other manuscripts."
)

$logLines | Set-Content -Path $logFile -Encoding UTF8

foreach ($step in $steps) {
    Write-Host "Running $($step.Name)..."
    py $step.Script @($step.Args)
    if ($LASTEXITCODE -ne 0) {
        throw "Step failed: $($step.Name) ($($step.Script))"
    }
}

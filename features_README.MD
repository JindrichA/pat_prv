# Feature And Export Reference

This file summarizes the feature families and exported values used in the current repository version.

For a methods-style processing description with current configuration values, see `RESEARCH_METHODS_README.md`.

## Terminology

- `PAT` = Peripheral Arterial Tone.
- `PR` = PAT-derived pulse-to-pulse interval (PRI) between adjacent detected PAT peaks.
- `PRV` = pulse rate variability derived from those PAT pulse intervals.

The repository uses `PR` for the PAT interval stream, not ECG `R-R` terminology.

## Active Feature Families

The main feature switches live in `pat_toolbox/config.py` under `FEATURES`.

- `hr`: PAT-derived heart-rate series and HR summary outputs.
- `prv`: RMSSD, SDNN, LF, HF, LF/HF, PRV plots, PRV CSV, and PRV summary fields.
- `sleep_combo_summary`: repeated summaries across predefined sleep subsets.
- `report_pdf`: the main multi-page report PDF.
- `peaks_debug_pdf`: optional PAT peak-debug PDF.

Separate from `FEATURES`, `EXPORT_PUBLICATION_PRV_PNG` can export a high-resolution PRV figure for a selected NREM segment.

## Core Signal Flow

1. Read `VIEW_PAT`.
2. Band-pass filter PAT.
3. Detect PAT peaks.
4. Convert peaks to PR intervals.
5. Clean PR intervals.
6. Apply sleep-stage and event/desaturation masks.
7. Compute HR and PRV outputs from the cleaned PR stream.

## Provenance Terms

- `physio-clean PR`: PR intervals obtained from PAT after beat detection and low-level PR cleaning.
- `sleep_keep`: samples retained by the selected sleep-stage policy.
- `combined_keep`: final clean analysis mask after sleep policy plus event/desaturation exclusion.
- `pre-final exclusion`: after sleep-stage selection, before final event/desaturation exclusion.
- `final-analysis`: after the final selected-policy combined mask.
- `selected_*`: fields computed under the current sleep policy from `config.py`.
- `combo_*`: fields recomputed separately for predefined sleep subsets.

## HR Outputs

The HR feature computes PAT-derived heart rate from cleaned PR intervals.

Common summary fields include:

- `selected_hr_mean_bpm`
- `selected_hr_median_bpm`
- `selected_hr_std_bpm`
- `selected_hr_valid_pct`
- `selected_hr_valid_min`

The HR CSV export contains:

- `time_sec`
- `hr_bpm`

## PRV Outputs

The PRV feature computes scalar and time-varying PRV metrics.

Common selected-policy fields include:

- `selected_rmssd_mean_ms`
- `selected_rmssd_median_ms`
- `selected_sdnn_mean_ms`
- `selected_sdnn_median_ms`
- `selected_lf`
- `selected_hf`
- `selected_lf_hf`
- `selected_lf_hf_fixed_median`
- `selected_lf_hf_fixed_n_windows_valid`

The PRV CSV export includes time-aligned RMSSD, SDNN, LF, HF, LF/HF, and mask/provenance columns when available.

## Sleep-Combo Outputs

When `sleep_combo_summary` is enabled, the pipeline recomputes HR/PRV summaries for fixed subsets such as:

- `pre_sleep_wake`
- `all_sleep`
- `wake_sleep`
- `nrem`
- `deep`
- `rem`

These values use prefixes such as `combo_nrem_*` and are recomputed for each subset rather than sliced from the selected-policy outputs.

## Common Output Files

Typical outputs for one recording are conditional on the active switches in `pat_toolbox/config.py`.

- HR CSV: `__HR_1Hz.csv`
- PRV CSV: `__PRV_Features_1Hz.csv`
- PRV mask CSV: `__PRV_Mask_1Hz.csv`
- Sleep timing CSV: `__Sleep_Timing.csv`
- Multi-page PDF report
- Publication-style PRV PNG: `__publication_prv_nrem_10min.png`
- Grouped final summary CSV with one row per recording

## Current Scope

This version is intentionally focused on PAT-derived HR and PRV.

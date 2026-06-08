from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional, TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np

from .. import config
from .report_helpers import _build_report_context, _build_report_figures, _write_report_pdf

if TYPE_CHECKING:
    import pandas as pd


def plot_pat_and_hr_segments_to_pdf(
    signal_raw: np.ndarray,
    signal_filt: np.ndarray,
    sfreq: float,
    pdf_path: Path,
    segment_minutes: Optional[float] = None,
    title_prefix: str = "",
    channel_name: str = "",
    t_hr_calc: Optional[np.ndarray] = None,
    hr_calc: Optional[np.ndarray] = None,
    t_hr_edf: Optional[np.ndarray] = None,
    hr_edf: Optional[np.ndarray] = None,
    t_prv: Optional[np.ndarray] = None,
    prv_rmssd: Optional[np.ndarray] = None,
    prv_rmssd_raw: Optional[np.ndarray] = None,
    prv_tv: Optional[Dict[str, np.ndarray]] = None,
    pearson_r: Optional[float] = None,
    spear_rho: Optional[float] = None,
    rmse: Optional[float] = None,
    prv_summary: Optional[Dict[str, float]] = None,
    aux_df: "Optional[pd.DataFrame]" = None,
    t_hr_calc_raw: Optional[np.ndarray] = None,
    hr_calc_raw: Optional[np.ndarray] = None,
    t_hr_edf_raw: Optional[np.ndarray] = None,
    hr_edf_raw: Optional[np.ndarray] = None,
    sleep_combo_summaries: Optional[Dict[str, Dict[str, object]]] = None,
    prv_mask_info: Optional[Dict[str, object]] = None,
    prv_midpoint_halves: Optional[Dict[str, Dict[str, float]]] = None,
) -> Dict[str, float]:
    if segment_minutes is None:
        segment_minutes = config.SEGMENT_MINUTES

    n_samples = len(signal_raw)
    if n_samples == 0 or sfreq <= 0:
        raise ValueError("Signal is empty or sampling frequency invalid.")
    if len(signal_filt) != n_samples:
        raise ValueError("Raw and filtered signal lengths differ.")

    samples_per_segment = int(segment_minutes * 60.0 * sfreq)
    if samples_per_segment <= 0:
        raise ValueError("Computed non-positive samples_per_segment.")

    context = _build_report_context(signal_raw, sfreq, pdf_path, aux_df)
    duration_sec = n_samples / sfreq

    with plt.rc_context({"figure.max_open_warning": 0}):
        figures = _build_report_figures(
            edf_base=context["edf_base"],
            duration_sec=duration_sec,
            exclusion_zones=context["exclusion_zones"],
            event_spec=context["event_spec"],
            t_hr_calc=t_hr_calc,
            hr_calc=hr_calc,
            t_prv=t_prv,
            prv_rmssd=prv_rmssd,
            prv_rmssd_raw=prv_rmssd_raw,
            prv_tv=prv_tv,
            prv_summary=prv_summary,
            aux_df=aux_df,
            sleep_combo_summaries=sleep_combo_summaries,
            prv_mask_info=prv_mask_info,
            prv_midpoint_halves=prv_midpoint_halves,
            hr_calc_raw=hr_calc_raw,
        )

    segment_kwargs = dict(
        signal_raw=signal_raw,
        signal_filt=signal_filt,
        sfreq=sfreq,
        segment_minutes=float(segment_minutes),
        title_prefix=title_prefix,
        channel_name=channel_name,
        t_hr_calc=t_hr_calc,
        hr_calc=hr_calc,
        t_hr_edf=None,
        hr_edf=None,
        t_prv=t_prv,
        prv_clean=prv_rmssd,
        prv_raw=prv_rmssd_raw,
        prv_sdnn_clean=None if not isinstance(prv_tv, dict) else prv_tv.get("sdnn_ms"),
        prv_sdnn_raw=None if not isinstance(prv_tv, dict) else prv_tv.get("sdnn_ms_raw"),
        aux_df=aux_df,
        exclusion_zones=context["exclusion_zones"],
        event_spec=context["event_spec"],
        t_hr_calc_raw=t_hr_calc_raw,
        hr_calc_raw=hr_calc_raw,
        t_hr_edf_raw=None,
        hr_edf_raw=None,
    )

    _write_report_pdf(
        pdf_path,
        fig_stage_tv=figures["fig_stage_tv"],
        fig_stage=figures["fig_stage"],
        fig_psd_zoom=None,
        fig_psd_full=None,
        fig_ov=figures["fig_ov"],
        overview_figures=figures["overview_figures"],
        summary_pages=figures["summary_pages"],
        segment_kwargs=segment_kwargs,
    )

    return {}

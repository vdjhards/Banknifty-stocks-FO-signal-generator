import numpy as np

_model = None


def _load():
    global _model
    if _model is not None:
        return _model
    import timesfm
    try:
        cls = timesfm.TimesFM_2p5_200M_torch
    except AttributeError:
        from timesfm.timesfm_2p5.timesfm_2p5_torch import TimesFM_2p5_200M_torch as cls
    _model = cls.from_pretrained('google/timesfm-2.5-200m-pytorch')
    _model.compile(timesfm.ForecastConfig(
        max_context=1024, max_horizon=16, normalize_inputs=True,
        use_continuous_quantile_head=True, force_flip_invariance=True,
        infer_is_positive=True, fix_quantile_crossing=True,
    ))
    return _model


def forecast_direction(close_series):
    model = _load()
    arr = np.asarray(close_series, dtype=np.float32)
    point, quant = model.forecast(horizon=4, inputs=[arr])
    last = float(arr[-1])
    future = float(point[0][-1])
    delta = future - last
    pct = delta / last if last else 0
    if pct > 0.001:
        direction = 'BULLISH'
    elif pct < -0.001:
        direction = 'BEARISH'
    else:
        direction = 'NEUTRAL'
    return direction, future, pct

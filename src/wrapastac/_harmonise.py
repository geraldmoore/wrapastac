import logging

import numpy as np
import pystac
import xarray

logger = logging.getLogger(__name__)

_BASELINE_CUTOFF = np.datetime64("2022-01-25", "ns")
_OFFSET = 1000

# Assets to ignore
_SKIP_HARMONISATION = frozenset({"scl", "SCL", "qa_pixel", "QA"})


def harmonise_s2(ds: xarray.Dataset, items: list[pystac.Item]) -> xarray.Dataset:
    """Apply offset of +1000 to images before 2022-01-25 to match the post-cutoff baseline."""
    if "time" not in ds.dims or ds.time.size == 0:
        return ds

    datetimes = []
    for item in items:
        if item.datetime:
            datetimes.append(np.datetime64(item.datetime.replace(tzinfo=None), "ns"))

    if not datetimes:
        return ds

    has_old = any(d < _BASELINE_CUTOFF for d in datetimes)
    has_new = any(d >= _BASELINE_CUTOFF for d in datetimes)

    if not (has_old and has_new):
        return ds

    logger.warning(
        "Sentinel-2 items span the processing baseline change on 2022-01-25. "
        "Applying a +%d offset to pre-cutoff spectral bands for temporal consistency.",
        _OFFSET,
    )

    spectral_vars = [v for v in ds.data_vars if v not in _SKIP_HARMONISATION]
    if not spectral_vars:
        return ds

    before_mask = ds.time.values < _BASELINE_CUTOFF
    old = ds.isel(time=before_mask)
    new = ds.isel(time=~before_mask)

    if old.time.size == 0:
        return ds

    old_corrected = old.copy(deep=True)
    for var in spectral_vars:
        old_corrected[var] = old[var] + _OFFSET

    return xarray.concat([old_corrected, new], dim="time")

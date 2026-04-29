from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import numpy as np
import xarray

if TYPE_CHECKING:
    import pystac

logger = logging.getLogger(__name__)

_BASELINE_CUTOFF = np.datetime64("2022-01-25", "ns")
_OFFSET = 1000
_NON_SPECTRAL = frozenset({"scl", "SCL", "qa_pixel", "QA"})


def maybe_harmonise_s2(ds: xarray.Dataset, items: list[pystac.Item]) -> xarray.Dataset:
    """Apply S2 processing baseline harmonisation when items span the 2022-01-25 cutoff.

    Before that date ESA applied a -1000 offset to reflectance values. Adding +1000
    to pre-cutoff data restores consistency with post-cutoff acquisitions.
    """
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

    spectral_vars = [v for v in ds.data_vars if v not in _NON_SPECTRAL]
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

"""Ultra-high-resolution tiling.

An 8500x8500 image is ~72 MP. Two things matter for correctness and speed:

  1. Never hold more than one decoded full image at a time, and crop lazily.
     Pillow's `Image.crop` on an opened file reads only what it needs for most
     formats, so we keep the handle open for the lifetime of a `TiledImage`.
  2. Tile coordinates must be exact, because every downstream spatial relation is
     computed in global pixel space. `TileSpec` therefore stores absolute
     coordinates and is the single source of truth for the lift back to global
     coordinates.

Overlap exists so that an object straddling a tile seam is fully visible in at
least one tile. The cost is duplicate detections, which `spatial.dedup` removes.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple

from ..utils.logging_utils import get_logger

LOG = get_logger("ctsr.tiling")

try:
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
except Exception:  # pragma: no cover
    Image = None  # type: ignore


@dataclass(frozen=True)
class TileSpec:
    """One tile in absolute full-image pixel coordinates.

    Half-open box: x0 <= x < x1, y0 <= y < y1.
    """

    tile_id: int
    x0: int
    y0: int
    x1: int
    y1: int
    row: int = 0
    col: int = 0
    image_index: int = 0  # which image of a multi-image sample

    @property
    def width(self) -> int:
        return self.x1 - self.x0

    @property
    def height(self) -> int:
        return self.y1 - self.y0

    @property
    def area(self) -> int:
        return self.width * self.height

    @property
    def box(self) -> Tuple[int, int, int, int]:
        return (self.x0, self.y0, self.x1, self.y1)

    @property
    def center(self) -> Tuple[float, float]:
        return (0.5 * (self.x0 + self.x1), 0.5 * (self.y0 + self.y1))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tile_id": self.tile_id, "box": list(self.box),
            "row": self.row, "col": self.col, "image_index": self.image_index,
        }


def plan_tiles(
    width: int,
    height: int,
    tile_size: int = 1024,
    overlap: int = 128,
    min_tail: int = 64,
    image_index: int = 0,
) -> List[TileSpec]:
    """Grid of overlapping tiles covering the whole image.

    The last tile in each direction is shifted back to end exactly on the image
    border (rather than being padded or clipped short), so no pixel is dropped
    and no tile is smaller than `tile_size` unless the image itself is.

    `min_tail` suppresses a final tile that would add almost no new area.
    """
    if width <= 0 or height <= 0:
        raise ValueError("Invalid image size: {}x{}".format(width, height))
    tile_size = max(32, int(tile_size))
    overlap = max(0, min(int(overlap), tile_size - 16))
    stride = max(16, tile_size - overlap)

    def starts(extent: int) -> List[int]:
        if extent <= tile_size:
            return [0]
        pos = list(range(0, max(1, extent - tile_size + 1), stride))
        last = extent - tile_size
        if not pos:
            pos = [0]
        if pos[-1] != last:
            # Only add the flush-right tile if it exposes meaningful new area.
            if last - pos[-1] >= min_tail:
                pos.append(last)
            else:
                pos[-1] = last
        return pos

    xs, ys = starts(width), starts(height)
    tiles: List[TileSpec] = []
    tid = 0
    for r, y in enumerate(ys):
        for c, x in enumerate(xs):
            tiles.append(TileSpec(
                tile_id=tid,
                x0=int(x), y0=int(y),
                x1=int(min(width, x + tile_size)),
                y1=int(min(height, y + tile_size)),
                row=r, col=c, image_index=image_index,
            ))
            tid += 1
    return tiles


class TiledImage:
    """Lazy accessor for one ultra-high-resolution image.

    Use as a context manager so the file handle is always released:

        with TiledImage(path, tile_size=1024, overlap=128) as ti:
            overview = ti.overview(1024)
            for tile in ti.tiles:
                crop = ti.crop(tile)
    """

    def __init__(
        self,
        path: str,
        tile_size: int = 1024,
        overlap: int = 128,
        image_index: int = 0,
        max_tiles: Optional[int] = None,
    ) -> None:
        if Image is None:
            raise ImportError("Pillow is required: pip install pillow")
        self.path = str(path)
        self.image_index = image_index
        self._im = Image.open(self.path)
        # `.size` is available from the header without decoding pixel data.
        self.width, self.height = self._im.size
        self.tile_size = int(tile_size)
        self.overlap = int(overlap)
        self.tiles: List[TileSpec] = plan_tiles(
            self.width, self.height, tile_size, overlap, image_index=image_index
        )
        self._truncated_plan = False
        if max_tiles is not None and len(self.tiles) > max_tiles:
            LOG.warning(
                "%s: tile plan has %d tiles, capping to %d. This changes coverage; "
                "raise tiling.max_tiles or tile_size if that is not intended.",
                self.path, len(self.tiles), max_tiles,
            )
            self.tiles = self.tiles[:max_tiles]
            self._truncated_plan = True
        self._overview_cache: Dict[int, Any] = {}

    # -- lifecycle ----------------------------------------------------------
    def __enter__(self) -> "TiledImage":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def close(self) -> None:
        self._overview_cache.clear()
        try:
            self._im.close()
        except Exception:
            pass

    # -- accessors ----------------------------------------------------------
    @property
    def size(self) -> Tuple[int, int]:
        return (self.width, self.height)

    @property
    def megapixels(self) -> float:
        return self.width * self.height / 1e6

    def crop(self, tile: TileSpec, to_rgb: bool = True) -> Any:
        """Decode one tile. Raises on a corrupt region so the caller can skip it."""
        region = self._im.crop(tile.box)
        if to_rgb and region.mode != "RGB":
            region = region.convert("RGB")
        return region

    def overview(self, max_side: int = 1024, to_rgb: bool = True) -> Any:
        """Downsampled whole-image view: the 'global scene understanding' input.

        Uses Pillow's `draft` for JPEGs (decodes at reduced scale, far cheaper)
        then a high-quality resize.
        """
        key = int(max_side)
        if key in self._overview_cache:
            return self._overview_cache[key]

        im = Image.open(self.path)
        try:
            try:
                im.draft("RGB", (max_side, max_side))
            except Exception:
                pass  # draft is only supported by some decoders
            if to_rgb and im.mode != "RGB":
                im = im.convert("RGB")
            scale = min(1.0, float(max_side) / max(im.size))
            if scale < 1.0:
                new_size = (max(1, int(round(im.size[0] * scale))),
                            max(1, int(round(im.size[1] * scale))))
                im = im.resize(new_size, Image.BICUBIC)
            else:
                im = im.copy()
        finally:
            pass
        self._overview_cache[key] = im
        return im

    def overview_scale(self, max_side: int = 1024) -> float:
        """Factor mapping overview pixels -> full-resolution pixels."""
        ov = self.overview(max_side)
        if ov.size[0] == 0:
            return 1.0
        return float(self.width) / float(ov.size[0])

    def tiles_for(self, tile_ids: Sequence[int]) -> List[TileSpec]:
        by_id = {t.tile_id: t for t in self.tiles}
        return [by_id[i] for i in tile_ids if i in by_id]

    def iter_crops(self, tiles: Optional[Sequence[TileSpec]] = None) -> Iterator[Tuple[TileSpec, Any]]:
        """Yield (spec, crop), skipping tiles that fail to decode."""
        for tile in (tiles if tiles is not None else self.tiles):
            try:
                yield tile, self.crop(tile)
            except Exception as exc:
                LOG.error("Failed to crop tile %d of %s (%s): %s",
                          tile.tile_id, self.path, tile.box, exc)
                continue

    def describe(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "width": self.width,
            "height": self.height,
            "megapixels": round(self.megapixels, 2),
            "tile_size": self.tile_size,
            "overlap": self.overlap,
            "n_tiles": len(self.tiles),
            "tile_plan_truncated": self._truncated_plan,
        }


def resize_to_budget(img: Any, max_pixels: int) -> Any:
    """Downscale an image so it fits a pixel budget, preserving aspect ratio.

    Used by Baseline 1 to emulate the naive 'resize the whole scene' path under a
    pixel budget identical to the one the other arms receive per call.
    """
    if img is None or max_pixels <= 0:
        return img
    w, h = img.size
    if w * h <= max_pixels:
        return img
    scale = math.sqrt(float(max_pixels) / float(w * h))
    new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
    return img.resize(new_size, Image.BICUBIC)

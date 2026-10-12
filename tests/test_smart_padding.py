"""Unit tests for Component 1: Aspect-Ratio Preserving Smart Padding."""
import numpy as np
import pytest
from PIL import Image

from data.smart_padding import PaddingMetadata, SmartPaddingTransform


class TestSmartPaddingTransform:
    """Tests for SmartPaddingTransform and coordinate mapping."""

    def test_square_image_no_padding(self):
        """A 1024x1024 square image should not need padding."""
        img = Image.new("RGB", (1024, 1024), color=(200, 100, 50))
        transform = SmartPaddingTransform(target_size=1024)
        padded_img, meta = transform(img)

        assert padded_img.size == (1024, 1024)
        assert meta.scale_factor == 1.0
        assert meta.pad_left == 0
        assert meta.pad_top == 0
        assert meta.pad_right == 0
        assert meta.pad_bottom == 0
        assert meta.resized_size == (1024, 1024)

    def test_landscape_image_padding(self):
        """Wide image should be padded top and bottom to reach 1024x1024."""
        img = Image.new("RGB", (2000, 1000), color=(50, 150, 200))
        transform = SmartPaddingTransform(target_size=1024, pad_color=(128, 128, 128))
        padded_img, meta = transform(img)

        assert padded_img.size == (1024, 1024)
        assert meta.resized_size[0] == 1024
        assert meta.resized_size[1] == 512
        assert meta.scale_factor == pytest.approx(1024 / 2000, abs=1e-4)
        assert meta.pad_left == 0
        assert meta.pad_right == 0
        assert meta.pad_top == 256
        assert meta.pad_bottom == 256

        # Check padding color on border
        px_top = padded_img.getpixel((512, 10))
        assert px_top == (128, 128, 128)

    def test_portrait_image_padding(self):
        """Tall image should be padded left and right to reach 1024x1024."""
        img = Image.new("RGB", (1000, 2000), color=(50, 200, 150))
        transform = SmartPaddingTransform(target_size=1024, pad_color=(128, 128, 128))
        padded_img, meta = transform(img)

        assert padded_img.size == (1024, 1024)
        assert meta.resized_size[0] == 512
        assert meta.resized_size[1] == 1024
        assert meta.scale_factor == pytest.approx(1024 / 2000, abs=1e-4)
        assert meta.pad_top == 0
        assert meta.pad_bottom == 0
        assert meta.pad_left == 256
        assert meta.pad_right == 256

        # Check padding color on border
        px_left = padded_img.getpixel((10, 512))
        assert px_left == (128, 128, 128)

    def test_top_left_placement(self):
        """When placement is top_left, pad_left and pad_top should be 0."""
        img = Image.new("RGB", (2000, 1000), color=(100, 100, 100))
        transform = SmartPaddingTransform(target_size=1024, placement="top_left")
        padded_img, meta = transform(img)

        assert padded_img.size == (1024, 1024)
        assert meta.pad_left == 0
        assert meta.pad_top == 0
        assert meta.pad_bottom == 512

    def test_coordinate_mapping_reversibility_normalized(self):
        """Normalized bounding box forward and inverse mapping should be strictly reversible."""
        img = Image.new("RGB", (2400, 1600), color=(0, 0, 0))
        transform = SmartPaddingTransform(target_size=1024)
        _, meta = transform(img)

        # Original box: [x0, y0, x1, y1] normalized
        orig_box = (0.2, 0.3, 0.6, 0.7)
        padded_box = transform.map_box_to_padded(orig_box, meta, normalized_in=True, normalized_out=True)
        recovered_box = transform.map_box_from_padded(padded_box, meta, normalized_in=True, normalized_out=True)

        for orig_val, rec_val in zip(orig_box, recovered_box):
            assert orig_val == pytest.approx(rec_val, abs=1e-4)

    def test_coordinate_mapping_reversibility_pixels(self):
        """Pixel-space bounding box forward and inverse mapping should be reversible."""
        img = Image.new("RGB", (3000, 1500), color=(0, 0, 0))
        transform = SmartPaddingTransform(target_size=1024)
        _, meta = transform(img)

        orig_box_px = (300.0, 150.0, 1200.0, 900.0)
        padded_box = transform.map_box_to_padded(orig_box_px, meta, normalized_in=False, normalized_out=False)
        recovered_box = transform.map_box_from_padded(padded_box, meta, normalized_in=False, normalized_out=False)

        for orig_val, rec_val in zip(orig_box_px, recovered_box):
            assert orig_val == pytest.approx(rec_val, abs=1e-3)

    def test_coordinate_clamping_out_of_bounds(self):
        """Inverse mapping should clamp out-of-bounds coordinates to original image bounds."""
        meta = PaddingMetadata(
            original_size=(1000, 1000),
            target_size=(1024, 1024),
            resized_size=(1024, 1024),
            scale_factor=1.024,
            pad_left=0,
            pad_top=0,
            pad_right=0,
            pad_bottom=0,
        )
        # Box extends beyond the target canvas
        box_out = (-0.1, -0.1, 1.2, 1.2)
        recovered = SmartPaddingTransform.map_box_from_padded(box_out, meta, normalized_in=True, normalized_out=True)
        assert recovered[0] >= 0.0
        assert recovered[1] >= 0.0
        assert recovered[2] <= 1.0
        assert recovered[3] <= 1.0

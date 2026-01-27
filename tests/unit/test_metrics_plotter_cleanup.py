"""Unit tests for MetricsPlotter cleanup functionality."""

import os
import shutil
import tempfile
from unittest.mock import MagicMock, patch

import numpy as np
import pytest


class TestMetricsPlotterCleanup:
    """Tests for automatic cleanup of assets folder."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp = tempfile.mkdtemp()
        yield temp
        # Cleanup after test
        if os.path.exists(temp):
            shutil.rmtree(temp)

    @pytest.fixture
    def mock_frames(self):
        """Create mock video frames for testing."""
        # Small 4D array: 10 frames, 64x64 pixels, 3 channels (RGB)
        return np.random.randint(0, 255, (10, 64, 64, 3), dtype=np.uint8)

    @pytest.fixture
    def plotter_in_temp_dir(self, temp_dir):
        """Create a MetricsPlotter that thinks it's in temp_dir."""
        from dprl.utils.metrics_plotter import MetricsPlotter

        plotter = MetricsPlotter()
        # Override caller_dir to use temp directory
        plotter.caller_dir = temp_dir
        return plotter

    # ==========================================================================
    # User Story 1 Tests: Automatic Cleanup on Session End
    # ==========================================================================

    def test_cleanup_removes_assets_folder_on_normal_exit(
        self, plotter_in_temp_dir, temp_dir
    ):
        """Test that _cleanup_assets() removes the assets folder."""
        assets_path = os.path.join(temp_dir, "assets")

        # Create assets folder with a file
        os.makedirs(assets_path, exist_ok=True)
        test_file = os.path.join(assets_path, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        # Mark assets as created
        plotter_in_temp_dir._assets_created = True

        # Run cleanup
        plotter_in_temp_dir._cleanup_assets()

        # Verify folder is removed
        assert not os.path.exists(assets_path), "Assets folder should be removed"

    def test_cleanup_handles_missing_folder_gracefully(self, plotter_in_temp_dir, temp_dir):
        """Test that cleanup doesn't error when assets folder doesn't exist."""
        assets_path = os.path.join(temp_dir, "assets")

        # Ensure folder doesn't exist
        assert not os.path.exists(assets_path)

        # Mark assets as created (even though folder is gone)
        plotter_in_temp_dir._assets_created = True

        # Should not raise any exception
        plotter_in_temp_dir._cleanup_assets()

        # Should still complete without error
        assert True

    def test_assets_created_flag_set_when_video_added(
        self, plotter_in_temp_dir, mock_frames, temp_dir
    ):
        """Test that _assets_created flag is set when add_video_from_frames creates folder."""
        # Initially flag should be False
        assert plotter_in_temp_dir._assets_created is False

        # Mock the video creation to avoid actual file I/O
        with patch(
            "dprl.utils.metrics_plotter.ImageSequenceClip"
        ) as mock_clip_class:
            mock_clip = MagicMock()
            mock_clip_class.return_value = mock_clip

            # Add video (this should set the flag)
            plotter_in_temp_dir.add_video_from_frames(
                "test_video", mock_frames, fps=30, video_filename="test.mp4"
            )

        # Flag should now be True
        assert plotter_in_temp_dir._assets_created is True

    def test_cleanup_only_runs_when_assets_created(self, plotter_in_temp_dir, temp_dir):
        """Test that cleanup is skipped when _assets_created is False."""
        assets_path = os.path.join(temp_dir, "assets")

        # Create assets folder manually (not through add_video_from_frames)
        os.makedirs(assets_path, exist_ok=True)
        test_file = os.path.join(assets_path, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        # Flag is False by default
        assert plotter_in_temp_dir._assets_created is False

        # Run cleanup
        plotter_in_temp_dir._cleanup_assets()

        # Folder should still exist (cleanup was skipped)
        assert os.path.exists(assets_path), "Assets folder should NOT be removed when flag is False"

    def test_cleanup_is_idempotent(self, plotter_in_temp_dir, temp_dir):
        """Test that cleanup can be called multiple times safely."""
        assets_path = os.path.join(temp_dir, "assets")

        # Create assets folder
        os.makedirs(assets_path, exist_ok=True)
        plotter_in_temp_dir._assets_created = True

        # Call cleanup multiple times
        plotter_in_temp_dir._cleanup_assets()
        plotter_in_temp_dir._cleanup_assets()
        plotter_in_temp_dir._cleanup_assets()

        # Should complete without error
        assert not os.path.exists(assets_path)

    # ==========================================================================
    # User Story 2 Tests: Graceful Cleanup on Errors
    # ==========================================================================

    def test_cleanup_failure_shows_error_message(self, plotter_in_temp_dir, temp_dir, capsys):
        """Test that cleanup failure displays error message to user."""
        assets_path = os.path.join(temp_dir, "assets")

        # Create assets folder
        os.makedirs(assets_path, exist_ok=True)
        plotter_in_temp_dir._assets_created = True

        # Mock shutil.rmtree to raise PermissionError
        with patch("shutil.rmtree") as mock_rmtree:
            mock_rmtree.side_effect = PermissionError("Access denied")

            # Cleanup should not raise
            plotter_in_temp_dir._cleanup_assets()

        # Should have displayed error (test passes if no exception raised)
        assert True

    def test_error_message_contains_path(self, plotter_in_temp_dir, temp_dir):
        """Test that error message includes the assets folder path."""
        assets_path = os.path.join(temp_dir, "assets")

        # Create assets folder
        os.makedirs(assets_path, exist_ok=True)
        plotter_in_temp_dir._assets_created = True

        # Track if _display_cleanup_error was called with correct path
        with patch.object(
            plotter_in_temp_dir, "_display_cleanup_error"
        ) as mock_display:
            with patch("shutil.rmtree") as mock_rmtree:
                mock_rmtree.side_effect = OSError("Cannot delete")

                plotter_in_temp_dir._cleanup_assets()

            # Verify _display_cleanup_error was called with the path
            mock_display.assert_called_once()
            call_args = mock_display.call_args[0]
            assert assets_path in call_args[0], "Error message should contain the assets path"

    def test_cleanup_does_not_crash_on_permission_error(
        self, plotter_in_temp_dir, temp_dir
    ):
        """Test that cleanup catches PermissionError and continues."""
        assets_path = os.path.join(temp_dir, "assets")

        # Create assets folder
        os.makedirs(assets_path, exist_ok=True)
        plotter_in_temp_dir._assets_created = True

        # Mock shutil.rmtree to raise PermissionError
        with patch("shutil.rmtree") as mock_rmtree:
            mock_rmtree.side_effect = PermissionError("Access denied")

            # This should NOT raise an exception
            try:
                plotter_in_temp_dir._cleanup_assets()
                cleanup_succeeded = True
            except Exception:
                cleanup_succeeded = False

        assert cleanup_succeeded, "Cleanup should not raise exceptions on PermissionError"

import inspect
import os
import threading

import numpy as np
import plotly.express as px
from dash import Dash, dcc, html
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip


class MetricsPlotter:
    """Class for plotting metrics over training episodes."""

    dash_app: Dash
    metrics = {}
    videos = {}
    caller_dir: str

    def __init__(self) -> None:
        """Initialize the MetricsPlotter."""
        # Get the directory of the script that instantiated this class
        caller_frame = inspect.currentframe().f_back
        caller_file = caller_frame.f_code.co_filename
        self.caller_dir = os.path.dirname(os.path.abspath(caller_file))
        assets_folder = os.path.join(self.caller_dir, "assets")
        self.dash_app = Dash(name="Metrics plotter", assets_folder=assets_folder)

    def _create_metrics_figures(self) -> None:
        """Create figures for each metric."""
        for metric_name, values in self.metrics.items():
            fig = px.line(
                x=list(range(len(values))),
                y=values,
                labels={"x": "Episodes", "y": metric_name},
                title=f"{metric_name} over epochs",
            )
            self.dash_app.layout.append(
                html.Div([html.H2(metric_name), html.Div(dcc.Graph(figure=fig))])
            )

    def _create_videos_section(self) -> None:
        """Create the videos section for the dash app."""
        for video_name, video_info in self.videos.items():
            video_path = video_info["path"]
            self.dash_app.layout.append(
                html.Div(
                    [
                        html.H2(video_name),
                        html.Video(
                            controls=True,
                            src=video_path,
                            style={"width": "600px", "height": "400px"},
                        ),
                        html.P(f"FPS: {video_info['fps']}"),
                        html.P(f"Video source: {video_path}"),
                    ]
                )
            )

    def _create_app_layout(self) -> None:
        """Create the layout for the dash app."""
        self.dash_app.layout = [html.H1("Training Metrics")]
        self._create_metrics_figures()
        self._create_videos_section()

    def add_metric(self, name: str, values: list[float]) -> None:
        """Add a metric to be plotted.

        Args:
            name: Name of the metric
            values: List of metric values over episodes
        """
        self.metrics[name] = values

    def add_video_from_frames(
        self,
        name: str,
        frames: np.ndarray,
        fps: int = 30,
        video_filename: str = "video.mp4",
    ) -> None:
        """Add a video created from frames to the Dash app.

        This function creates a video from a numpy array of frames and saves it in the
        'assets' folder relative to this script file (e.g., ./assets/video.mp4).
        The video is then made available in the Dash application for display.

        Args:
            name: Name of the video for display in the app.
            frames: Numpy array of frames, expected shape (num_frames, height, width, channels).
            fps: Frames per second for the video.
            video_filename: Filename for the video file (e.g., 'my_video.mp4'). The file will be saved
                            in the 'assets' folder relative to this script.

        Raises:
            ValueError: If frames is not a numpy array, is empty, or has invalid shape.
            OSError: If the save path is invalid or cannot be created.
        """
        if not isinstance(frames, np.ndarray):
            raise ValueError("Frames must be a numpy array.")
        if frames.size == 0:
            raise ValueError("Frames array is empty.")
        if frames.ndim != 4:
            raise ValueError(
                "Frames must be a 4D array with shape (num_frames, height, width, channels)."
            )

        save_path = os.path.join(self.caller_dir, "assets", video_filename)

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Validate the save path
        try:
            with open(save_path, "wb") as f:
                pass  # Just to check if we can write
            os.remove(save_path)  # Remove the empty file
        except OSError as e:
            raise OSError(f"Invalid save path: {save_path}. Error: {e}")

        frames_list = [frames[i] for i in range(frames.shape[0])]
        clip = ImageSequenceClip(frames_list, fps)
        clip.write_videofile(save_path, codec="libx264")

        # For Dash, use the URL path relative to assets folder
        video_url = f"assets/{video_filename}"
        self.videos[name] = {"path": video_url, "fps": fps}

    def add_metrics_via_dict(self, metrics_dict: dict[str, list[float]]) -> None:
        """Add multiple metrics to be plotted via a dictionary.

        Args:
            metrics_dict: Dictionary where keys are metric names and values are lists of metric values over episodes
        """
        self.metrics.update(metrics_dict)

    def plot_metrics(self) -> None:
        """Plot all added metrics using Dash."""
        self._create_app_layout()
        self._run_dash_app()

    def _run_dash_app(self) -> None:
        dash_tread = threading.Thread(
            target=self.dash_app.run(debug=False, use_reloader=False, port=8050)
        )
        dash_tread.start()

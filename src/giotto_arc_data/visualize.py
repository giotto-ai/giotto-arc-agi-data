from typing import Any, Dict, List, Tuple, Union, Optional

from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def plot_task(
    task: Dict,
    title: str = "ARC task",
    plot_size: int = 2,
    grid_lines_width: float = 0.3,
    grid_lines_color: str = "w",
    taskname: str = "-",
    savefig: bool = False,
    save_path: Union[str, Path] = "./Arc_images/",
):
    MatplotlibARCPlot().show(
        task=task, title=title, taskname=taskname, savefig=savefig, save_path=save_path
    )


colors = [
    "#000000",  # Black for 0
    "#0074D9",  # Blue for 1
    "#FF4136",  # Red for 2
    "#2ECC40",  # Green for 3
    "#FFDC00",  # Yellow for 4
    "#AAAAAA",  # Grey for 5
    "#F012BE",  # Fucsha for 6
    "#FF851B",  # Orange for 7
    "#7FDBFF",  # Teal for 8
    "#870C25",  # Brown for 9
    "#FFC0CB",  # Pink for 10, joker symbol for outer boundaries
    "#FFFFFF",  # White for 11, joker symbol for emptiness
]


class MatplotlibARCPlot:
    """Namespace for matplotlib-based plotting functions."""

    def show(
        self,
        task: Dict,
        title: str = "ARC task",
        plot_size: int = 2,
        grid_lines_width: float = 0.3,
        grid_lines_color: str = "w",
        taskname: str = "-",
        savefig: bool = False,
        save_path: Union[str, Path] = "./Arc_images/",
    ) -> None:
        """Plot an ARC task.

        :param task: dictionary containing train and test pairs, as read from a JSON
        :param title: title to be added in plot
        :param plot_size: dimension of the plot
        :param grid_lines_width: floating-point width of lines separating pixels in the plot
        :param grid_lines_color: color to be used to visually separate grid cells.
            Matplotlib needs to recognise this as a valid color string, so for example
            the string "w" can be passed for white, and the string "k" can be passed for black.
        """
        assert "train" in task
        assert "test" in task

        if "output" not in task["test"][0].keys():
            for i in range(len(task["test"])):
                task["test"][i]["output"] = [[0, 0], [0, 0]]

        self.taskname = taskname
        self.savefig = savefig
        self.save_path = save_path

        # Note: the `fake_pair` is just used to visually separate the
        # train and test pairs
        # fake_pair = {
        #     "input": [[10, 10, 10], [10, 10, 10], [10, 10, 10]],
        #     "output": [[10, 10, 10], [10, 10, 10], [10, 10, 10]],
        # }
        all_pairs = task["train"] + task["test"]
        subtitles = [f"demo {i}" for i in range(len(task["train"]))]
        subtitles += [f"test {i}" for i in range(len(task["test"]))]
        self.plot_pairs(
            all_pairs,
            title,
            subtitles=subtitles,
            plot_size=plot_size,
            grid_lines_width=grid_lines_width,
            grid_lines_color=grid_lines_color,
        )

    def plot_pairs(
        self,
        pairs: List[Dict],
        title: str,
        subtitles: List[str],
        plot_size: int = 3,
        grid_lines_width: float = 0.3,
        grid_lines_color: str = "w",
    ) -> None:
        """Plot ARC pairs.

        :param pairs: list of dictionaries representing input/output pairs, as read from a JSON
        :param title: title to be added in plot
        :param plot_size: dimension of the plot
        :param grid_lines_width: floating-point width of lines separating pixels in the plot
        :param grid_lines_color: color to be used to visually separate grid cells.
            Matplotlib needs to recognise this as a valid color string, so for example
            the string "w" can be passed for white, and the string "k" can be passed for black.
        """
        num_pairs = len(pairs)
        assert num_pairs > 0

        if num_pairs == 1:
            self._plot_arc_one_pair(
                pairs, title, plot_size, grid_lines_width, grid_lines_color
            )
        else:
            self._plot_arc_more_than_one_pair(
                pairs, title, subtitles, plot_size, grid_lines_width, grid_lines_color
            )

    @staticmethod
    def _get_arc_color(arc_color: int) -> Tuple[int, int, int]:
        "Transfom an ARC integer value into a uint8 RGB color."
        assert arc_color in set(range(11))

        RGB_COLORS = {
            0: (0, 0, 0),  # Black (#000000)
            1: (0, 116, 217),  # Blue (#0074D9)
            2: (255, 65, 54),  # Red (#FF4136)
            3: (46, 204, 64),  # Green (#2ECC40)
            4: (255, 220, 0),  # Yellow (#FFDC00)
            5: (170, 170, 170),  # Grey (#AAAAAA)
            6: (240, 18, 190),  # Fuchsia (#F012BE)
            7: (255, 133, 27),  # Orange (#FF851B)
            8: (127, 219, 255),  # Teal (#7FDBFF)
            9: (135, 12, 37),  # Brown (#870C25)
            10: (250, 250, 250),  # White (#FFFFFF)
        }
        return RGB_COLORS[arc_color]

    def _get_arc_image(self, grid: List[List[int]]) -> np.ndarray:
        """Create a ARC image from a `grid` contained in the ARC challenge JSON files."""
        num_rows = len(grid)
        num_cols = len(grid[0])

        image = np.zeros(shape=(num_rows, num_cols, 3), dtype=np.uint8)
        for i in range(num_rows):
            for j in range(num_cols):
                image[i, j] = self._get_arc_color(grid[i][j])

        return image

    def _plot_arc_more_than_one_pair(
        self,
        pairs: List[Dict],
        title: str,
        subtitles: List[str],
        plot_size: int = 3,
        grid_lines_width: float = 0.3,
        grid_lines_color: str = "w",
    ) -> None:
        """Internal function used to plot multiple grid pairs in a ARC task."""
        num_pairs = len(pairs)
        fig, ax = plt.subplots(
            2, num_pairs, figsize=(plot_size * num_pairs, plot_size * 2)
        )
        fig.suptitle(title, fontsize=7)

        for index, pair in enumerate(pairs):
            input_image = self._get_arc_image(pair["input"])
            ax[0, index].imshow(input_image)
            self._draw_grid_lines(
                ax[0, index], input_image, grid_lines_width, grid_lines_color
            )
            ax[0, index].axis("off")

            output_image = self._get_arc_image(pair["output"])
            ax[1, index].imshow(output_image)
            self._draw_grid_lines(
                ax[1, index], output_image, grid_lines_width, grid_lines_color
            )
            ax[0, index].set_title(subtitles[index])
            ax[1, index].axis("off")

        fig.tight_layout()

        if self.savefig:
            fig.savefig(self.save_path, dpi=150)
            plt.close(fig)

    def _plot_arc_one_pair(
        self,
        pairs: List[Dict],
        title: str,
        plot_size: int = 3,
        grid_lines_width: float = 0.3,
        grid_lines_color: str = "w",
    ) -> None:
        """Internal function used to plot one single grid pair in a ARC task."""
        num_pairs = len(pairs)
        fig, ax = plt.subplots(
            2, num_pairs, figsize=(plot_size * num_pairs, plot_size * 2)
        )
        fig.suptitle(title, fontsize=14)

        pair = pairs[0]
        input_image = self._get_arc_image(pair["input"])
        ax[0].imshow(input_image)
        self._draw_grid_lines(ax[0], input_image, grid_lines_width, grid_lines_color)
        ax[0].axis("off")

        output_image = self._get_arc_image(pair["output"])
        ax[1].imshow(output_image)
        self._draw_grid_lines(ax[1], output_image, grid_lines_width, grid_lines_color)
        ax[1].axis("off")

        fig.tight_layout()

        if self.savefig:
            fig.savefig(self.save_path, dpi=150)
            plt.close(fig)

    @staticmethod
    def _draw_grid_lines(
        ax: matplotlib.axes.Axes,
        image: np.ndarray,
        grid_lines_width: float = 0.3,
        grid_lines_color: str = "w",
    ) -> None:
        """Draw grid lines between pixels in a ARC image."""
        num_rows, num_cols, _ = image.shape

        for i in range(num_rows + 1):
            ax.plot(
                [-0.52, num_cols - 0.52],
                [i - 0.52, i - 0.52],
                color=grid_lines_color,
                lw=grid_lines_width,
                zorder=2,
            )

        for j in range(num_cols + 1):
            ax.plot(
                [j - 0.52, j - 0.52],
                [-0.52, num_rows - 0.52],
                color=grid_lines_color,
                lw=grid_lines_width,
                zorder=2,
            )

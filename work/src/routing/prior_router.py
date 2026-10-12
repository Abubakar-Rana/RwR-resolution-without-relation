"""Prior-based routers for Vision-Language Model inference paths.

Routes queries between global downscale (Direct) and localized zoom (Selection)
using pre-registered task taxonomy or empirical task priors without expensive inference.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Set
import numpy as np


class GroupPriorRouter:
    """Routes queries based on the pre-registered relational vs perceptual taxonomy.

    Direct preserves global scene geometry and spatial topology, making it optimal
    for relational tasks. Selection provides high-resolution zoom crops, making it
    optimal for fine-grained perceptual and attribute tasks.
    """

    def __init__(self, relational_tasks: Optional[Set[str]] = None) -> None:
        """Initializes the group prior router.

        Args:
            relational_tasks: Set of canonical task names considered relational.
        """
        self.relational_tasks: Set[str] = relational_tasks or {
            "Object Spatial Relationship",
            "Regional Counting",
            "Counting with Complex Reasoning",
            "Route Planning",
        }

    def predict_single(self, task_name: str) -> str:
        """Predicts routing path for a single task name.

        Args:
            task_name: Task name string.

        Returns:
            str: 'b1_direct' if relational else 'b3_selected'.
        """
        return "b1_direct" if task_name in self.relational_tasks else "b3_selected"

    def predict(self, tasks: Sequence[str]) -> np.ndarray:
        """Predicts routing path for a sequence of task names.

        Args:
            tasks: Sequence of task name strings.

        Returns:
            np.ndarray: Array of strings ('b1_direct' or 'b3_selected').
        """
        routes = np.array([
            "b1_direct" if t in self.relational_tasks else "b3_selected"
            for t in tasks
        ], dtype=object)
        return routes


class TaskEmpiricalRouter:
    """Empirical task router fitted on training folds.

    For each task label observed during training, selects whichever candidate
    pipeline achieved the highest empirical accuracy on that specific task.
    """

    def __init__(self, candidates: Sequence[str] = ("b1_direct", "b3_selected")) -> None:
        """Initializes the empirical task router.

        Args:
            candidates: List of candidate pipeline names to choose between.
        """
        self.candidates: List[str] = list(candidates)
        self.task_choices: Dict[str, str] = {}
        self.fallback: str = "b3_selected"

    def fit(self, tasks: np.ndarray, correct_matrix: Dict[str, np.ndarray], train_idx: np.ndarray) -> TaskEmpiricalRouter:
        """Fits optimal pipeline per task on training split.

        Args:
            tasks: Array of task strings of length N.
            correct_matrix: Dict mapping candidate pipeline name to 0/1 array of length N.
            train_idx: Indices belonging to the training fold.

        Returns:
            Self.
        """
        self.task_choices = {}
        sub_tasks = tasks[train_idx]
        unique_tasks = set(sub_tasks)

        for t in unique_tasks:
            t_mask = train_idx[sub_tasks == t]
            accs = {m: float(correct_matrix[m][t_mask].mean()) for m in self.candidates}
            # Tie breaker prefers b3_selected
            self.task_choices[t] = max(self.candidates, key=lambda m: (accs[m], m == "b3_selected"))

        global_accs = {m: float(correct_matrix[m][train_idx].mean()) for m in self.candidates}
        self.fallback = max(self.candidates, key=lambda m: (global_accs[m], m == "b3_selected"))
        return self

    def predict_single(self, task_name: str) -> str:
        """Predicts routing path for a single task name.

        Args:
            task_name: Task name string.

        Returns:
            str: Optimal candidate pipeline choice.
        """
        return self.task_choices.get(task_name, self.fallback)

    def predict(self, tasks: Sequence[str]) -> np.ndarray:
        """Predicts routing path for test tasks.

        Args:
            tasks: Sequence of task strings.

        Returns:
            np.ndarray of pipeline choices.
        """
        return np.array([self.task_choices.get(t, self.fallback) for t in tasks], dtype=object)

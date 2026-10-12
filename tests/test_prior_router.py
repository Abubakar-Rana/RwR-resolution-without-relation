"""Unit tests for Component 7: Prior-Based and Multimodal Routers."""
import numpy as np
import pytest

from routing.cascaded_router import CascadedHeuristicRouter, ParetoCalibratedRouter
from routing.classifier_router import DiscriminativeRouter, DualConfidenceRouter
from routing.prior_router import GroupPriorRouter, TaskEmpiricalRouter


class TestGroupPriorRouter:
    """Tests for GroupPriorRouter relational vs perceptual classification."""

    @pytest.fixture
    def router(self):
        return GroupPriorRouter()

    def test_canonical_relational_tasks_predict_single(self, router):
        """Pre-registered relational tasks must route to 'b1_direct'."""
        relational_tasks = [
            "Object Spatial Relationship",
            "Regional Counting",
            "Counting with Complex Reasoning",
            "Route Planning",
        ]
        for task in relational_tasks:
            assert router.predict_single(task) == "b1_direct"

    def test_perceptual_tasks_predict_single(self, router):
        """Non-relational fine-grained perceptual tasks must route to 'b3_selected'."""
        perceptual_tasks = [
            "Object Attribute",
            "Fine-grained Classification",
            "Color Recognition",
            "Small Target Detection",
        ]
        for task in perceptual_tasks:
            assert router.predict_single(task) == "b3_selected"

    def test_batch_predict(self, router):
        """Batch predict returns numpy array with matching routing decisions."""
        tasks = [
            "Object Spatial Relationship",
            "Color Recognition",
            "Route Planning",
            "Fine-grained Classification",
        ]
        routes = router.predict(tasks)
        assert isinstance(routes, np.ndarray)
        assert routes.tolist() == ["b1_direct", "b3_selected", "b1_direct", "b3_selected"]

    def test_custom_relational_set(self):
        """Supports custom relational task taxonomy."""
        custom_set = {"Task A", "Task B"}
        custom_router = GroupPriorRouter(relational_tasks=custom_set)
        assert custom_router.predict_single("Task A") == "b1_direct"
        assert custom_router.predict_single("Task C") == "b3_selected"


class TestTaskEmpiricalRouter:
    """Tests for TaskEmpiricalRouter training fit and predict."""

    def test_fit_and_predict(self):
        router = TaskEmpiricalRouter(candidates=("b1_direct", "b3_selected"))
        tasks = np.array(["Task1", "Task1", "Task2", "Task2"])
        correct_matrix = {
            "b1_direct": np.array([1, 1, 0, 0]),
            "b3_selected": np.array([0, 0, 1, 1]),
        }
        train_idx = np.array([0, 1, 2, 3])
        router.fit(tasks, correct_matrix, train_idx)

        assert router.predict_single("Task1") == "b1_direct"
        assert router.predict_single("Task2") == "b3_selected"

        batch = router.predict(["Task1", "Task2", "UnknownTask"])
        assert batch[0] == "b1_direct"
        assert batch[1] == "b3_selected"


class TestCascadedAndParetoRouters:
    """Tests for CascadedHeuristicRouter and ParetoCalibratedRouter."""

    def test_cascaded_heuristic_router(self):
        router = CascadedHeuristicRouter()
        tasks = ["Object Spatial Relationship", "Color"]
        routes = router.predict(tasks)
        assert routes[0] == "b1_direct"
        assert routes[1] == "b3_selected"

    def test_pareto_calibrated_router(self):
        router = ParetoCalibratedRouter(tau=0.6)
        probs = np.array([0.5, 0.7, 0.59, 0.61])
        routes = router.predict_from_probabilities(probs)
        assert routes.tolist() == ["b1_direct", "b3_selected", "b1_direct", "b3_selected"]


class TestDiscriminativeRouter:
    """Tests for DiscriminativeRouter logistic regression."""

    def test_fit_and_predict_flow(self):
        router = DiscriminativeRouter(c_reg=1.0, threshold=0.5)
        keywords = [
            "spatial relationship between airplanes runway",
            "distance and direction to terminal",
            "color of the car vehicle shade",
            "identify vehicle paint color red or blue",
        ]
        c_dir = np.array([1, 1, 0, 0])
        c_sel = np.array([0, 0, 1, 1])

        router.fit(keywords, c_dir, c_sel)
        preds = router.predict(keywords)
        assert len(preds) == 4
        assert isinstance(preds, np.ndarray)

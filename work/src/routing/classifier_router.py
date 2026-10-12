"""Machine-learning based multimodal routers for VLM query dispatching.

Extracts text semantics, spatial reasoning indicators, and scene resolution priors
to predict whether global downscale (Direct) or localized zooming (Selection)
will yield a higher probability of correct answer.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Set, Tuple
import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


class SemanticFeatureExtractor:
    """Extracts joint semantic, spatial, and physical resolution features."""

    def __init__(self, ngram_range: Tuple[int, int] = (1, 2), min_df: int = 2) -> None:
        """Initializes feature extractor.

        Args:
            ngram_range: Range of n-grams for TF-IDF.
            min_df: Minimum document frequency for vocabulary terms.
        """
        self.vectorizer = TfidfVectorizer(
            ngram_range=ngram_range,
            min_df=min_df,
            sublinear_tf=True,
            strip_accents="unicode",
        )
        self.scaler = StandardScaler()

        self.spatial_cues: Set[str] = {
            "spatial", "relationship", "relation", "between", "next", "near",
            "adjacent", "direction", "route", "planning", "connected", "relative",
            "position", "layout", "across", "along", "distance",
        }
        self.attribute_cues: Set[str] = {
            "color", "classify", "type", "kind", "shade", "gray", "black", "white",
            "red", "blue", "yellow", "green", "silver", "appearance", "state",
        }
        self.counting_cues: Set[str] = {
            "count", "counting", "number", "many", "total", "quantity", "amount",
        }

    def _extract_cues(self, text_list: Sequence[str]) -> np.ndarray:
        """Counts domain keyword matches."""
        feats = np.zeros((len(text_list), 3), dtype=float)
        for i, text in enumerate(text_list):
            words = set(text.lower().split())
            feats[i, 0] = len(words & self.spatial_cues)
            feats[i, 1] = len(words & self.attribute_cues)
            feats[i, 2] = len(words & self.counting_cues)
        return feats

    def fit_transform(
        self,
        keywords_list: Sequence[str],
        tile_counts: Optional[np.ndarray] = None,
    ) -> csr_matrix:
        """Fits vocabulary and scaler on training data and transforms."""
        X_text = self.vectorizer.fit_transform(keywords_list)
        cues = self._extract_cues(keywords_list)

        if tile_counts is not None:
            log_tiles = np.log1p(tile_counts).reshape(-1, 1)
            dense_meta = np.hstack([cues, log_tiles])
        else:
            dense_meta = cues

        meta_scaled = self.scaler.fit_transform(dense_meta)
        return hstack([X_text, csr_matrix(meta_scaled)]).tocsr()

    def transform(
        self,
        keywords_list: Sequence[str],
        tile_counts: Optional[np.ndarray] = None,
    ) -> csr_matrix:
        """Transforms held-out text and metadata using fitted state."""
        X_text = self.vectorizer.transform(keywords_list)
        cues = self._extract_cues(keywords_list)

        if tile_counts is not None:
            log_tiles = np.log1p(tile_counts).reshape(-1, 1)
            dense_meta = np.hstack([cues, log_tiles])
        else:
            dense_meta = cues

        meta_scaled = self.scaler.transform(dense_meta)
        return hstack([X_text, csr_matrix(meta_scaled)]).tocsr()


class DiscriminativeRouter:
    """Logistic regression classifier predicting P(Selection beats Direct | x)."""

    def __init__(
        self,
        c_reg: float = 0.8,
        threshold: float = 0.5,
        train_on_discordant_only: bool = True,
    ) -> None:
        """Initializes discriminative router.

        Args:
            c_reg: Inverse regularization parameter C.
            threshold: Probability threshold above which Selection is selected.
            train_on_discordant_only: If True, fits solely on items where Direct != Selection.
        """
        self.c_reg = c_reg
        self.threshold = threshold
        self.train_on_discordant_only = train_on_discordant_only
        self.feature_extractor = SemanticFeatureExtractor()
        self.classifier: Optional[LogisticRegression] = None

    def fit(
        self,
        keywords_list: Sequence[str],
        correct_direct: np.ndarray,
        correct_selection: np.ndarray,
        tile_counts: Optional[np.ndarray] = None,
    ) -> DiscriminativeRouter:
        """Fits router classifier on training samples."""
        X = self.feature_extractor.fit_transform(keywords_list, tile_counts)

        if self.train_on_discordant_only:
            disc_mask = (correct_direct != correct_selection)
            if not np.any(disc_mask):
                y = correct_selection
                X_train = X
            else:
                X_train = X[disc_mask]
                y = correct_selection[disc_mask]  # 1 if Selection won, 0 if Direct won
        else:
            # Multi-class or cost-weighted formulation
            y = np.where(correct_selection > correct_direct, 1, 0)
            X_train = X

        self.classifier = LogisticRegression(
            C=self.c_reg,
            max_iter=1000,
            class_weight="balanced",
            random_state=42,
        )
        self.classifier.fit(X_train, y)
        return self

    def predict_proba(
        self,
        keywords_list: Sequence[str],
        tile_counts: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """Predicts probability that Selection outperforms Direct."""
        if self.classifier is None:
            raise RuntimeError("Router has not been fitted.")
        X = self.feature_extractor.transform(keywords_list, tile_counts)
        return self.classifier.predict_proba(X)[:, 1]

    def predict(
        self,
        keywords_list: Sequence[str],
        tile_counts: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """Predicts pipeline string ('b1_direct' or 'b3_selected')."""
        probs = self.predict_proba(keywords_list, tile_counts)
        return np.where(probs >= self.threshold, "b3_selected", "b1_direct")


class DualConfidenceRouter:
    """Dual calibrated estimators for P(Direct correct | x) and P(Selection correct | x)."""

    def __init__(self, c_reg: float = 1.0, margin_gamma: float = 0.0) -> None:
        """Initializes dual confidence router.

        Args:
            c_reg: Inverse regularization parameter C.
            margin_gamma: Margin threshold by which Selection probability must exceed
                Direct probability to justify 5x higher compute latency.
        """
        self.c_reg = c_reg
        self.margin_gamma = margin_gamma
        self.feature_extractor = SemanticFeatureExtractor()
        self.clf_direct: Optional[LogisticRegression] = None
        self.clf_selection: Optional[LogisticRegression] = None

    def fit(
        self,
        keywords_list: Sequence[str],
        correct_direct: np.ndarray,
        correct_selection: np.ndarray,
        tile_counts: Optional[np.ndarray] = None,
    ) -> DualConfidenceRouter:
        """Fits separate estimators on all training data."""
        X = self.feature_extractor.fit_transform(keywords_list, tile_counts)

        self.clf_direct = LogisticRegression(
            C=self.c_reg, max_iter=1000, random_state=42
        ).fit(X, correct_direct)

        self.clf_selection = LogisticRegression(
            C=self.c_reg, max_iter=1000, random_state=42
        ).fit(X, correct_selection)
        return self

    def predict(
        self,
        keywords_list: Sequence[str],
        tile_counts: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """Routes to Selection if P(Selection) > P(Direct) + margin_gamma, else Direct."""
        if self.clf_direct is None or self.clf_selection is None:
            raise RuntimeError("Estimators not fitted.")
        X = self.feature_extractor.transform(keywords_list, tile_counts)
        p_dir = self.clf_direct.predict_proba(X)[:, 1]
        p_sel = self.clf_selection.predict_proba(X)[:, 1]

        return np.where(p_sel > (p_dir + self.margin_gamma), "b3_selected", "b1_direct")

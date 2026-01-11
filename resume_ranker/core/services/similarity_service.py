import numpy as np


def cosine_similarity(vec1, vec2, scale=10, min_match_threshold=0.25):
    """
    Compute semantic similarity between job input and resume text.

    - Uses cosine similarity
    - Applies ATS-style non-linear scaling
    - Returns score out of 10
    - Returns None if nothing meaningfully matches

    Args:
        vec1 (array-like): resume embedding
        vec2 (array-like): job embedding
        scale (int): output score scale (default = 10)
        min_match_threshold (float): minimum normalized similarity
                                     required to consider a match

    Returns:
        float | None: similarity score (0–10) or None if no match
    """

    try:
        # -----------------------------
        # 1. Input validation
        # -----------------------------
        if vec1 is None or vec2 is None:
            return None

        v1 = np.asarray(vec1, dtype=np.float32)
        v2 = np.asarray(vec2, dtype=np.float32)

        if v1.ndim != 1 or v2.ndim != 1:
            return None

        if v1.shape != v2.shape:
            return None

        # -----------------------------
        # 2. Zero-vector check
        # -----------------------------
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)

        if norm_v1 < 1e-8 or norm_v2 < 1e-8:
            return None

        # -----------------------------
        # 3. Raw cosine similarity
        # -----------------------------
        raw_similarity = np.dot(v1, v2) / (norm_v1 * norm_v2)
        raw_similarity = float(np.clip(raw_similarity, -1.0, 1.0))

        # Convert from [-1, 1] → [0, 1]
        normalized_similarity = (raw_similarity + 1.0) / 2.0

        # -----------------------------
        # 4. No-match validation
        # -----------------------------
        if normalized_similarity < min_match_threshold:
            # Nothing meaningfully matches
            return None

        # -----------------------------
        # 5. ATS-style non-linear scaling
        # -----------------------------
        if normalized_similarity < 0.4:
            adjusted_similarity = normalized_similarity * 0.7
        elif normalized_similarity < 0.65:
            adjusted_similarity = normalized_similarity * 0.9
        else:
            adjusted_similarity = min(normalized_similarity * 1.1, 1.0)

        # -----------------------------
        # 6. Scale to 0–10
        # -----------------------------
        final_score = round(adjusted_similarity * scale, 2)

        return final_score

    except Exception as e:
        print("Similarity computation error:", e)
        return None

from sentence_transformers import SentenceTransformer
import numpy as np

# --------------------------------------------------
# Load model once (IMPORTANT for performance)
# --------------------------------------------------
MODEL_NAME = "all-MiniLM-L6-v2"
_model = SentenceTransformer(MODEL_NAME)

# --------------------------------------------------
# Configuration
# --------------------------------------------------
MAX_TEXT_LENGTH = 5000  # characters (safe for OCR resumes)


def _prepare_text(text: str) -> str:
    """
    Prepare text safely for embedding.

    - Ensures valid string
    - Truncates very long OCR text
    """

    if not text or not isinstance(text, str):
        return ""

    text = text.strip()

    # Truncate extremely long text (keeps start which usually has skills & summary)
    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH]

    return text


def embed(text: str) -> np.ndarray:
    """
    Generate sentence embedding for given text.

    Returns:
        np.ndarray: normalized embedding vector
    """

    try:
        prepared_text = _prepare_text(text)

        # If text is empty, return zero vector
        if not prepared_text:
            return np.zeros(
                _model.get_sentence_embedding_dimension(),
                dtype=np.float32
            )

        embedding = _model.encode(
            prepared_text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embedding

    except Exception as e:
        print("Embedding error:", e)

        # Always return safe fallback
        return np.zeros(
            _model.get_sentence_embedding_dimension(),
            dtype=np.float32
        )

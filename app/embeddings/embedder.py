"""
Convert text chunks into dense vectors using Sentence Transformers.

An embedding model maps text to a fixed-size list of numbers (e.g. 384 floats).
Similar meaning -> vectors that are close together in vector space.
"""

from functools import lru_cache

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings


@lru_cache(maxsize=1)
def get_embeddings(model_name: str) -> Embeddings:
    """
    Return a cached embedding model instance.

    The model downloads on first use (~90 MB for all-MiniLM-L6-v2) and is then
    reused for every chunk and every search query.
    """
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

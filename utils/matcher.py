from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_sections(jtbd, content_sections, top_k=5):
    """
    Matches sections of a PDF to a given persona's job-to-be-done (JTBD)
    using TF-IDF similarity.

    Args:
        jtbd (str): The job description text for the persona.
        content_sections (list of dict): Extracted sections from the PDF, each with a 'text' key.
        top_k (int): Number of top relevant sections to return.

    Returns:
        list of dict: Top-matched sections.
    """

    # Filter out None or non-string values
    section_texts = [s['text'] for s in content_sections if isinstance(s.get('text'), str) and s['text'].strip() != '']

    # Check if JTBD is valid
    if not isinstance(jtbd, str) or not jtbd.strip():
        raise ValueError("JTBD must be a non-empty string")

    # Combine JTBD and section texts
    docs = [jtbd] + section_texts

    # Vectorize with TF-IDF
    tfidf = TfidfVectorizer().fit_transform(docs)

    # Compute similarity
    cosine_similarities = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    # Get top K similar sections
    top_indices = cosine_similarities.argsort()[-top_k:][::-1]
    best_matches = [content_sections[i] for i in top_indices]

    return best_matches

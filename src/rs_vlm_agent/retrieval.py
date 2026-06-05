from __future__ import annotations

KNOWLEDGE_BASE = [
    {
        "keywords": ["building", "建筑", "urban", "城区"],
        "text": "Building changes often appear as compact high-contrast regions; verify shadows and seasonal illumination before labeling new construction.",
    },
    {
        "keywords": ["road", "道路", "transport", "交通"],
        "text": "Road changes usually form thin connected structures; false positives may come from vehicles, shadows, or registration errors.",
    },
    {
        "keywords": ["water", "水体", "shoreline", "flood"],
        "text": "Water-body changes require spectral caution because turbidity, cloud shadow, and acquisition time can alter apparent color.",
    },
    {
        "keywords": ["disaster", "灾害", "damage", "变化"],
        "text": "Disaster interpretation should combine change masks with object context and avoid causal claims without external evidence.",
    },
]


def retrieve_knowledge(query: str, top_k: int = 3) -> list[str]:
    query_lower = query.lower()
    scored: list[tuple[int, str]] = []
    for item in KNOWLEDGE_BASE:
        score = sum(1 for keyword in item["keywords"] if keyword.lower() in query_lower)
        scored.append((score, item["text"]))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [text for _, text in scored[:top_k]]


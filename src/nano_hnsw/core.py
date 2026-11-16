"""NanoHNSW: Embedded Vector Search Engine with Cosine Distance & Small World Graph."""

import math
import random
from typing import List, Tuple


class NanoVectorIndex:
    """
    Lightweight, embedded vector search index.
    Zero native C++ dependency, ideal for edge, serverless, and local indexing.
    """

    def __init__(self, dim: int, max_neighbors: int = 4):
        if dim <= 0:
            raise ValueError("Dimension must be positive.")
        self.dim = dim
        self.max_neighbors = max_neighbors
        self.vectors: List[List[float]] = []
        self.graph: List[List[int]] = []

    @staticmethod
    def cosine_distance(v1: List[float], v2: List[float]) -> float:
        """Calculates cosine distance: 1.0 - (dot(v1, v2) / (||v1|| * ||v2||))."""
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0.0 or norm2 == 0.0:
            return 1.0
        similarity = dot / (norm1 * norm2)
        similarity = max(-1.0, min(1.0, similarity))
        return 1.0 - similarity

    def insert(self, vec: List[float]) -> int:
        """Inserts a vector into the index and creates small-world connections."""
        if len(vec) != self.dim:
            raise ValueError(f"Vector dim {len(vec)} does not match index dim {self.dim}")

        idx = len(self.vectors)
        self.vectors.append(list(vec))
        self.graph.append([])

        if idx == 0:
            return idx

        # Rank existing nodes by proximity to form small-world graph edges
        k = min(self.max_neighbors, idx)
        distances = [(self.cosine_distance(vec, self.vectors[i]), i) for i in range(idx)]
        distances.sort(key=lambda x: x[0])

        for _, neighbor in distances[:k]:
            self.graph[idx].append(neighbor)
            if idx not in self.graph[neighbor]:
                self.graph[neighbor].append(idx)
                if len(self.graph[neighbor]) > self.max_neighbors * 2:
                    self.graph[neighbor].pop(0)

        return idx

    def search(self, query: List[float], top_k: int = 3) -> List[Tuple[int, float]]:
        """
        Traverses proximity graph using best-first search to find approximate nearest neighbors.
        Returns: List of (vector_id, distance) sorted by ascending distance.
        """
        if len(query) != self.dim:
            raise ValueError(f"Query dim {len(query)} does not match index dim {self.dim}")

        if not self.vectors:
            return []

        # Start from entry point
        curr = random.randint(0, len(self.vectors) - 1)
        curr_dist = self.cosine_distance(query, self.vectors[curr])
        visited = {curr}

        # Greedy local exploration
        changed = True
        while changed:
            changed = False
            for neighbor in self.graph[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    d = self.cosine_distance(query, self.vectors[neighbor])
                    if d < curr_dist:
                        curr_dist = d
                        curr = neighbor
                        changed = True

        scored = [(i, self.cosine_distance(query, self.vectors[i])) for i in visited]
        scored.sort(key=lambda x: x[1])
        return scored[:top_k]

# NanoHNSW: Embedded Vector Search Engine

A pure-math, zero-dependency Approximate Nearest Neighbor (ANN) vector search index using small-world graph exploration and cosine metric spaces.

## Features
- **No C++ Toolchain or External Dependencies:** Pure Python standard library.
- **Microsecond Exploration:** Greedy graph walking with bounded neighborhood degree.
- **Plug-and-Play:** Ideal for local embeddings, client tools, and edge worker processes.

## Run Tests
```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Author
Subrat Sahu (@subratsahu3) — subratsahu195@gmail.com

# Information Retrieval Lectures

This repository contains the lecture materials for the Information Retrieval course, covering fundamental concepts from classical models to modern neural retrieval and RAG systems.

## Course Overview

The lectures are structured to guide students through the evolution of IR:

### [Lecture 1: Vector Space Model & Boolean Retrieval](build/01_intro_vector_space_static.pdf)
- **What is Information Retrieval?**: Definitions, IR vs. Databases, IR vs. NLP.
- **Challenges in IR**: Intent understanding, the Semantic Gap, and Web-scale retrieval.
- **Boolean Retrieval**: Set-based matching, inverted indexes, and the "feast or famine" problem.
- **The Vector Space Model**: Geometric representation, TF-IDF weighting, and ranked retrieval.

### [Lecture 2: Sparse and Dense Indexing](build/02_indexing_static.pdf)
- **Sparse Indexing**: The classical approach, inverted index structures, speed optimizations (Gap Encoding, Variable Byte).
- **Dense Vector Indexing**: Introduction to neural retrieval, candidate generation stage, and the bridge to feasibility.

### [Lecture 3: Sparse Ranking Methods](build/03_ranking_static.pdf)
- **From Vector Space to Probabilistic Ranking**: The Probability Ranking Principle (PRP).
- **BM25 & Language Models**: Deep dive into the most robust lexical scoring functions.

### [Lecture 4: Representation Learning for Rankings](build/04_embeddings_reranking_static.pdf)
- **From Sparse to Dense**: Why embeddings are needed to bridge the lexical gap.
- **The Transformer Architecture**: Self-attention logic, QKV mechanisms, and positional encoding.
- **BERT for IR**: Tokenization (WordPiece), the [CLS] token, and transfer learning for ranking.
- **The Two-Stage Pipeline**: Retrieve-then-Rerank architecture (BM25 + Cross-Encoders).

### [Lecture 5: Dense Retrieval --- From Bi-Encoders to Late Interaction](build/05_dense_retrieval_static.pdf)
- **Bi-Encoders vs. Cross-Encoders**: Architecture trade-offs for full-corpus retrieval.
- **Contrastive Learning**: InfoNCE loss and the importance of negative sampling.
- **Dense Passage Retrieval (DPR)**: The breakthrough in open-domain QA.
- **ColBERT**: Late interaction for token-level alignment and higher accuracy.
- **Hard Negative Mining**: Static vs. Dynamic negatives (ANCE).

### [Lecture 6: Learning to Rank (LTR)](build/06_ltr_static.pdf)
- **Motivation**: Multi-objective ranking in e-commerce, scholar, and ads.
- **Evaluation Metrics**: Graded relevance, DCG, and NDCG (the gold standard).
- **LTR Paradigms**:
  - **Pointwise**: Regression/Classification on query-doc pairs.
  - **Pairwise**: Learning relative preferences (RankNet, RankSVM).
  - **Listwise**: Optimizing the whole permutation (ListNet).

### [Lecture 7: Question Answering and Retrieval-Augmented Generation (RAG)](build/07-rag_static.pdf)
- **Extractive QA**: Retriever–reader architectures.
- **The Hallucination crisis**: Why closed-book LLMs fail and how grounding helps.
- **RAG Architecture**: The modular view of Query Modelling, Retrieval, Conditioning, and Generation.
- **Retrieval Deep Dive**: Chunking strategies, late chunking, and query reformulation.
- **Evaluation**: The RAG Triad (Faithfulness, Groundedness, Attribution) and failure taxonomies.
- **Advanced Systems**: Adaptive RAG, Self-RAG, and GraphRAG concepts.

---
© 2025-2026 Avishek Anand. All rights reserved.

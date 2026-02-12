# Information Retrieval — Concept & Idea Tracker

> A running index of every concept, technique, and key idea introduced across lectures. We will se this to review, cross-reference, and prepare for exams.

---

## Lecture 1: Introduction to IR — Vector Space Model & Boolean Retrieval

### Core Concepts

- **Information Retrieval (IR):** The task of finding material (usually documents) of an unstructured nature that satisfies an information need from within large collections.
- **Document Collection (Corpus):** The set of all documents available for retrieval.
- **Query:** A user's expression of an information need.
- **Relevance:** The degree to which a retrieved document satisfies the user's information need.

### Boolean Retrieval

- **Boolean Retrieval Model:** A retrieval model where queries are Boolean expressions of terms (AND, OR, NOT) and documents either match or do not — no ranking.
- **Term-Document Incidence Matrix:** A binary matrix where rows are terms, columns are documents, and entry $(t, d) = 1$ if term $t$ appears in document $d$.
- **Boolean Operators:** AND (intersection of posting lists), OR (union), NOT (complement).
- **Limitations of Boolean Retrieval:** No ranking, feast-or-famine results (too many or zero), hard for users to formulate good Boolean queries.

### Vector Space Model (VSM)

- **Vector Space Model (VSM):** Documents and queries are represented as vectors in a high-dimensional term space; relevance is measured by geometric proximity (e.g., cosine similarity). *(Salton et al., 1975)*
- **Bag of Words:** A representation that treats a document as an unordered multiset of its words, discarding grammar and word order.
- **Term Frequency (TF):** The number of times a term $t$ occurs in document $d$: $\mathrm{tf}(t, d)$.
- **Document Frequency (DF):** The number of documents in the collection that contain term $t$: $\mathrm{df}(t)$.
- **Inverse Document Frequency (IDF):** A measure of how rare or common a term is across the collection: $\mathrm{idf}(t) = \log \frac{N}{\mathrm{df}(t)}$, where $N$ is the total number of documents.
- **TF-IDF Weighting:** A term weight combining local importance (TF) and global rarity (IDF): $w(t, d) = \mathrm{tf}(t, d) \times \mathrm{idf}(t)$.
- **Cosine Similarity:** Similarity between two vectors $\vec{a}$ and $\vec{b}$: $\cos(\vec{a}, \vec{b}) = \frac{\vec{a} \cdot \vec{b}}{\|\vec{a}\| \cdot \|\vec{b}\|}$. Normalizes for document length.
- **Document Length Normalization:** Adjusting scores so longer documents are not unfairly favored simply for containing more terms.

### Key Ideas (Lecture 1)

- Documents and queries live in the same vector space; retrieval = finding nearby vectors.
- TF-IDF balances term frequency (local signal) with inverse document frequency (global signal).
- Cosine similarity is preferred over dot product because it accounts for document length.
- Boolean retrieval is exact but inflexible; VSM introduces graded relevance via scoring.

---

## Lecture 2: Sparse and Dense Indexing

### The Modern IR Landscape

- **Traditional Retrieval (10 Blue Links):** User issues a query, receives a ranked list of documents, and manually reads/synthesizes information.
- **Retrieval-Augmented Generation (RAG):** A paradigm where a retrieval system fetches relevant passages, augments an LLM prompt, and the LLM generates a synthesized answer. *(Lewis et al., 2020)*
- **Candidate Generation:** The first stage of a retrieval pipeline that reduces millions of documents to hundreds of candidates for downstream re-ranking or LLM consumption.
- **Recall Ceiling:** The maximum recall achievable by any downstream component; determined entirely by the indexing/candidate-generation stage.
- **"Retrieval serves models, not just users":** In RAG, the retrieval component acts as the LLM's "eyes" into the document collection.

### Sparse Indexing (Classical)

#### Inverted Index

- **Inverted Index:** A data structure mapping each vocabulary term to an ordered posting list of documents (and payloads) containing that term. The backbone of text retrieval. *(Manning et al., 2008)*
- **Posting List:** The list of (docID, payload) pairs associated with a term in the inverted index.
- **Posting List Levels:**
  - *Level 1 — DocID only:* Supports Boolean retrieval.
  - *Level 2 — With term frequencies:* Supports ranked retrieval (TF-IDF, BM25). **Standard in practice.**
  - *Level 3 — With positions:* Supports phrase queries and proximity scoring. 2–3× larger.
- **Document-Term Matrix:** The $D \times |V|$ matrix of term weights; the inverted index is its Compressed Sparse Column (CSC) representation.
- **Complexity:** Naive scan is $O(N \cdot M)$; inverted index lookup is $O(k \cdot p)$, where $k$ = query terms and $p$ = avg posting list length.

#### Score Aggregation

- **Accumulator-Based Scoring:** For each query term, traverse its posting list and add the term's contribution to each document's running score accumulator.
- **Key property:** Only documents containing at least one query term are ever scored.

#### Text Preprocessing

- **Tokenization:** Segmenting raw text into discrete tokens. Defines the vocabulary. Language-dependent (English contractions, German compounds, CJK segmentation).
- **Lowercasing:** Normalizing all characters to lowercase for case-insensitive matching.
- **Stemming:** Heuristic reduction of words to approximate root forms by removing suffixes (e.g., Porter stemmer). Fast but crude. *(Porter, 1980)*
- **Lemmatization:** Morphological reduction to dictionary forms (lemmas). More accurate than stemming but slower (e.g., "better" → "good").
- **Stop Words:** High-frequency, low-information words (the, a, is). Modern recommendation: **keep them** (storage is cheap; needed for phrases, entities, and neural models).
- **Preprocessing consistency:** The same pipeline must be applied to both documents and queries.
- **Preprocessing depends on representation:**
  - *Sparse:* Custom tokenization, optional stemming, optional stop word removal.
  - *Dense:* Model-fixed tokenizer (BPE/WordPiece), **no stemming**, keep stop words, respect context window truncation.
- **WordPiece / BPE Tokenization:** Subword tokenization used by neural models (BERT, GPT). Splits rare words into known subword units.

#### Index Compression

- **Why compress:** Decompression (2–5 GB/s) is faster than reading uncompressed data from SSD (~0.5 GB/s). Compression makes retrieval **faster**, not just smaller.
- **Gap Encoding (Delta Encoding):** Store differences between consecutive sorted docIDs instead of raw IDs. Gaps are small → fewer bits needed.
- **Variable Byte (VB) Encoding:** Variable-length integer encoding using 7 data bits + 1 continuation bit per byte. Small numbers use 1 byte; large numbers use more.
- **Compression ratios:** VB achieves 3–4×; PForDelta achieves 6–10×; front coding saves 30–50% on dictionaries.
- **Production systems:** Lucene/Elasticsearch uses FOR + SIMD; Google uses custom hardware-optimized compression.

### Dense Indexing (Neural)

#### Dense Representations

- **Sparse Representation:** A vector in $\mathbb{R}^{|V|}$ with >99.9% zeros; only terms present in the document are non-zero.
- **Dense Representation (Embedding):** A vector in $\mathbb{R}^d$ (typically $d = 768$) from a neural encoder; **all entries non-zero**, encoding semantic meaning. *(Reimers & Gurevych, 2019)*
- **Semantic matching:** Dense vectors match "car problems" with "automobile issues" (synonymy); sparse vectors cannot.

#### Approximate Nearest Neighbor (ANN) Search

- **$k$-Nearest Neighbor ($k$-NN) Search:** Find the $k$ vectors in a collection most similar to a query vector.
- **Approximate Nearest Neighbor (ANN):** Relaxes exactness for speed; returns approximately correct top-$k$ with high probability. *(Indyk & Motwani, 1998)*
- **Infeasibility of exact search:** For 1B vectors × 768 dims: ~768 billion FLOPs/query (>1s even on GPU).
- **Accuracy–speed trade-off:** Higher recall ↔ lower throughput. Typical: 90–99% recall is achievable.

#### IVF (Inverted File Index for Vectors)

- **IVF:** Partition vectors into $k$ clusters via $k$-means; at query time, search only the $n_{\text{probe}}$ nearest clusters. *(Jégou et al., 2011)*
- **IVF Construction:** Run $k$-means → assign vectors to clusters → build inverted lists per cluster.
- **IVF Search:** Compute query-to-centroid distances → select $n_{\text{probe}}$ nearest → exhaustive search within those clusters → return top-$k$.
- **Key parameter:** $n_{\text{probe}}$ controls the recall/speed trade-off (1 = fast/low recall; 100 = slow/high recall).

#### Product Quantization (PQ)

- **Product Quantization (PQ):** Compress a $d$-dim vector into $m$ centroid indices by splitting into $m$ subvectors and quantizing each to the nearest of $K$ codebook centroids. *(Jégou et al., 2011)*
- **PQ Codes:** A document vector stored as $m$ integers (each in $\{0, \ldots, K{-}1\}$); for $K = 256$, each code is 1 byte → $m$ bytes total per vector.
- **Compression ratio:** For $d = 768$, float32, $m = 96$: $3072 / 96 = 32\times$.
- **Codebook Training:** Run $k$-means independently in each of the $m$ subspaces on a training sample.
- **Asymmetric Distance Computation (ADC):** The query is **not** quantized; only database vectors are. Distance is decomposed into a sum over subspaces, each computed via a prebuilt lookup table.
- **Distance Lookup Table:** An $m \times K$ table where entry $\mathrm{DT}[i][j] = \|\vec{q}^{(i)} - c_i^{(j)}\|^2$. Built once per query at cost $O(m \cdot K \cdot d/m)$.
- **PQ Distance Scan:** For each document, approximate distance $= \sum_{i=1}^{m} \mathrm{DT}[i][\mathrm{code}_i]$ — only $m$ integer table lookups per document (no float ops).
- **PQ Approximation Error:** Depends on codebook quality and data distribution. More subvectors ($m$) and centroids ($K$) reduce error at the cost of storage and table construction time.

#### IVF + PQ (The Production Standard)

- **IVF+PQ:** Combines IVF (coarse clustering for search-space pruning) with PQ (compression for memory and fast approximate distances). The industry standard for large-scale dense retrieval. *(Johnson et al., 2021)*
- **Architecture:** Offline: cluster + compress. Online: find nearest clusters → PQ distance scan within clusters → return top-$k$.
- **Scale example (FAISS):** 1B vectors × 768 dims: 3 TB uncompressed → 64 GB with IVF+PQ (50× reduction, 90–95% recall).

### Design Decisions

- **When to use Sparse:** Exact match, rare keywords, entity names, model numbers. High explainability.
- **When to use Dense:** Semantic similarity, natural-language questions, synonym matching.
- **When to use Hybrid (Sparse + Dense):** Most production RAG systems. Covers both exact and semantic matching.
- **Decision dimensions:** Recall, precision, latency, memory, scalability, explainability.

### Common Pitfalls

- Using only dense retrieval for entity-heavy domains (misses exact matches).
- Not tuning ANN parameters ($n_{\text{probe}}$, etc.) — defaults often give only ~80% recall.
- Inconsistent preprocessing between index time and query time.
- Forgetting to normalize vectors when using cosine similarity (Euclidean ≠ cosine on unnormalized vectors).

### Production & Infrastructure

- **FAISS:** Facebook AI Similarity Search library for efficient ANN (IVF, PQ, HNSW). *(Johnson et al., 2021)*
- **PyTerrier:** Python framework for sparse retrieval experiments (BM25, indexing, evaluation). *(Macdonald et al., 2021)*
- **Vector Databases:** Pinecone, Qdrant, Milvus, Weaviate — managed ANN search.
- **Elasticsearch 8.0+:** Native support for both kNN (dense) and BM25 (sparse).
- **Production checklist:** Compression enabled, vectors normalized, parameters tuned, monitoring (recall@k, p95 latency, index growth, distribution drift).

### Key Principles (Lecture 2)

- **"Indexing sets the ceiling."** Everything downstream (re-ranking, LLM reasoning) can only refine what retrieval finds. A missed document is lost forever.
- **"Indexing is the bridge to feasibility."** Without it, scoring all documents per query is impossible at scale.
- **"Compression makes things faster, not just smaller."** Decompression is faster than raw I/O.
- **"Don't throw away BM25."** Keyword matching remains essential alongside semantic search.

---

## References

| Tag | Full Reference |
|-----|---------------|
| Salton et al., 1975 | G. Salton, A. Wong, C.S. Yang. "A Vector Space Model for Automatic Indexing." *CACM* 18(11), 1975. |
| Porter, 1980 | M.F. Porter. "An Algorithm for Suffix Stripping." *Program* 14(3), 1980. |
| Indyk & Motwani, 1998 | P. Indyk, R. Motwani. "Approximate Nearest Neighbors: Towards Removing the Curse of Dimensionality." *STOC*, 1998. |
| Manning et al., 2008 | C.D. Manning, P. Raghavan, H. Schütze. *Introduction to Information Retrieval.* Cambridge University Press, 2008. |
| Robertson & Zaragoza, 2009 | S. Robertson, H. Zaragoza. "The Probabilistic Relevance Framework: BM25 and Beyond." *FnTIR* 3(4), 2009. |
| Jégou et al., 2011 | H. Jégou, M. Douze, C. Schmid. "Product Quantization for Nearest Neighbor Search." *IEEE TPAMI* 33(1), 2011. |
| Reimers & Gurevych, 2019 | N. Reimers, I. Gurevych. "Sentence-BERT." *EMNLP-IJCNLP*, 2019. |
| Lewis et al., 2020 | P. Lewis et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *NeurIPS*, 2020. |
| Malkov & Yashunin, 2020 | Y.A. Malkov, D.A. Yashunin. "Efficient and Robust ANN Search Using HNSW Graphs." *IEEE TPAMI* 42(4), 2020. |
| Macdonald et al., 2021 | C. Macdonald et al. "PyTerrier: Declarative Experimentation in Python." *CIKM*, 2021. |
| Johnson et al., 2021 | J. Johnson, M. Douze, H. Jégou. "Billion-Scale Similarity Search with GPUs." *IEEE TBD* 7(3), 2021. |
| Lin et al., 2021 | J. Lin et al. "A Few Brief Notes on DeepImpact, COIL, and a Conceptual Framework for IR Techniques." *arXiv:2106.14807*, 2021. |

---

*Last updated: \today*
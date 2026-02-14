# Information Retrieval — Concept & Idea Tracker

> A running index of every concept, technique, and key idea introduced across lectures.
> Use this to review, cross-reference, and prepare for exams.

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

## Lecture 3: Ranking Models (BM25, Language Models, Query Expansion)

### Probabilistic Foundations

- **Probability Ranking Principle (PRP):** If documents are ranked by decreasing $P(\text{relevant} \mid q, d)$, expected effectiveness is maximized (under independent relevance). *(Robertson, 1977)*

### BM25

- **BM25 Formula:** $\text{BM25}(q,d) = \sum_{t \in q} \text{IDF}(t) \cdot \frac{f(t,d) \cdot (k_1+1)}{f(t,d) + k_1 \cdot (1 - b + b \cdot |d|/\text{avgdl})}$. Three components: IDF, saturating TF, length normalization. *(Robertson & Zaragoza, 2009)*
- **BM25 Parameters:** 
  - $k_1$: Controls TF saturation (usually 1.2). $k_1=0$ is Boolean; large $k_1$ is linear.
  - $b$: Controls length normalization (usually 0.75). $b=1$ is full; $b=0$ is none.
- **BM25 IDF:** $\log\frac{N - \text{df}_t + 0.5}{\text{df}_t + 0.5}$. Can be negative for terms appearing in >50% of docs.
- **BM25F (Fielded):** Weighted TF across fields (title, body, URL). Standard in production.

### Query Expansion

- **Vocabulary mismatch problem:** Queries and documents use different words for the same concept. BM25 scores 0.
- **Pseudo Relevance Feedback (PRF):** Assume top-$k$ results are relevant; extract terms; expand query; re-retrieve.
- **Rocchio Algorithm:** Move query vector toward centroid of relevant docs, away from non-relevant. Geometric. Historical. *(Rocchio, 1971)*
- **RM3 (Relevance Model 3):** $P(w|R) \propto \sum_{d \in R} P(w|d) \cdot P(d|q)$. Interpolate with original query. Standard for classical PRF. *(Lavrenko & Croft, 2001)*
- **RM3 Parameters:** fb_docs (3–10), fb_terms (10–20), $\lambda$ (0.5–0.8).
- **Query drift:** When PRF assumption fails, expansion terms are wrong.

### LLM-Based Query Expansion

- **LLM Synonym Generation:** Prompt LLM for synonyms/paraphrases. Zero-shot, no retrieval needed.
- **HyDE:** LLM generates hypothetical relevant document; use for expansion or embedding. *(Gao et al., 2023)*
- **Query Decomposition:** LLM breaks complex query into sub-queries; retrieve for each; merge.
- **Query2Doc:** Prepend LLM-generated pseudo-document to query; run BM25. *(Wang et al., 2023)*

### Statistical Language Models for Ranking

- **Query Likelihood Model:** Rank by $P(q|d) = \prod_{w \in q} P(w|d)^{\text{count}(w,q)}$.
- **Zero probability problem:** Any absent query term zeros out the entire score. Smoothing essential.
- **Jelinek-Mercer Smoothing:** $P(w|d) = (1-\lambda) P_\text{ML}(w|d) + \lambda P(w|C)$. Fixed; $\lambda$ typically 0.1–0.3.
- **Dirichlet Smoothing:** $P(w|d) = \frac{\text{count}(w,d) + \mu P(w|C)}{|d| + \mu}$. Length-adaptive; $\mu$ typically 1000–2500. Generally preferred.
- **LM vs. BM25:** Similar rankings with good parameters. BM25 has explicit saturation/normalization; LMs achieve it via smoothing.

### Key Principles (Lecture 3)

- **"BM25 is the foundation layer."** Every modern system uses it as first-stage retrieval or a feature.
- **"Not all term matches are equal."** Rare terms dominate scoring (IDF).
- **"Smoothing is essential, not optional."** Without it, LMs assign zero to partially-relevant documents.

---

## Lecture 4: Embeddings & Transformer Re-rankers

### Word Embeddings (Static)

- **Distributional Hypothesis:** "You shall know a word by the company it keeps." Words in similar contexts → similar vectors. *(Firth, 1957)*
- **Word2Vec:** Predict context from target (Skip-gram) or target from context (CBOW). Hidden-layer weights = embeddings. $d = 100$–$300$. *(Mikolov et al., 2013)*
- **GloVe:** Factorize word co-occurrence matrix. $\vec{w}_i \cdot \vec{w}_j \approx \log(\text{co-occurrence})$. Similar quality to Word2Vec. *(Pennington et al., 2014)*
- **Word analogies:** $\vec{\text{king}} - \vec{\text{man}} + \vec{\text{woman}} \approx \vec{\text{queen}}$. Relational structure as vector directions.
- **Limitation:** One vector per word type. No polysemy resolution ("bank" = "bank").

### Contextualized Embeddings

- **Static vs. Contextualized:** Static assigns one vector per word type; contextualized assigns a different vector per token depending on context.
- **Polysemy resolution:** "bank" near "money" ≠ "bank" near "river."
- **Average word embeddings (naive document representation):** $\vec{d} = \frac{1}{|d|}\sum_{w \in d} \vec{w}$. Loses word order, unresolved polysemy.

### Transformer Architecture

- **Self-attention:** Each token attends to every other token. $\text{Attention}(Q, K, V) = \text{softmax}(QK^T/\sqrt{d_k}) V$. *(Vaswani et al., 2017)*
- **Query, Key, Value projections:** Q = "what am I looking for?", K = "what do I contain?", V = "what info do I provide?". Attention weights = softmax of Q·K dot products; output = weighted sum of V.
- **Multi-head attention:** $h$ parallel heads (BERT: $h = 12$); each captures different relationship types. Concat + project.
- **Positional encoding:** Sinusoidal or learned vectors added to embeddings to inject word-order information (attention is permutation-invariant without it).
- **Transformer encoder block:** Multi-Head Attention → Add & LayerNorm → FFN → Add & LayerNorm. Residual connections for gradient flow.
- **BERT-base:** 12 layers, 768 hidden dims, 12 heads, 110M parameters.

### BERT

- **BERT:** Transformer encoder pre-trained bidirectionally on BooksCorpus + Wikipedia. *(Devlin et al., 2019)*
- **Masked Language Modeling (MLM):** Mask 15% of tokens; predict from bidirectional context.
- **Next Sentence Prediction (NSP):** Binary classification: is sentence B the actual continuation of A?
- **Fine-tuning:** Add task-specific head on pre-trained BERT; train on MS MARCO with low learning rate ($2 \times 10^{-5}$).
- **monoBERT:** Encoder-only; uses [CLS] token for binary classification. *(Nogueira & Cho, 2019)*
- **monoT5:** Encoder-Decoder; uses generative prompts (``Is document relevant?'') $\to$ ``true/false''. More flexible and often more accurate. *(Nogueira et al., 2020)*
- **RankGPT:** Multi-document listwise ranking via LLM prompts. No fine-tuning. *(Sun et al., 2023)*

### ColBERT (Late Interaction, Preview)

- **ColBERT:** Encode query and document separately with BERT, producing per-token embeddings. Compare via MaxSim. *(Khattab & Zaharia, 2020)*
- **MaxSim scoring:** $\text{score}(q,d) = \sum_i \max_j \vec{q}_i \cdot \vec{d}_j$. For each query token, find best-matching document token.
- **Trade-off:** Near-cross-encoder accuracy; documents can be pre-encoded (like bi-encoder); but much higher storage (one vector per token).

### Training Cross-Encoders in Practice

- **MS MARCO Passage Ranking:** 8.8M passages, 530K training queries, ~1 relevant passage per query, 6,980 dev queries. Standard training dataset. *(Nguyen et al., 2016)*
- **Sparse labels challenge:** Only ~1 positive per query; many relevant passages are unlabeled (false negatives). Negative sampling strategy is critical.
- **Negative sampling:** Random negatives (easy, weak signal) < BM25 hard negatives (topically related but non-relevant, strong signal) < Cross-encoder mined negatives (iterative, best but expensive). Start with BM25 negatives.
- **Batching:** Max sequence length 512; batch size 16–32; gradient accumulation to simulate larger batches; mixed precision (fp16) halves memory.
- **Hyperparameters:** LR $1$–$3 \times 10^{-5}$; AdamW; 10% warmup; linear decay; 2–3 epochs max (overfits quickly).
- **Common mistakes:** Too many epochs (overfitting); LR too high (catastrophic forgetting); only random negatives; ignoring document truncation at 512 tokens.

### Evaluation

- **MRR@k (Mean Reciprocal Rank):** $\frac{1}{|Q|}\sum_q \frac{1}{\text{rank of first relevant doc}}$. Best for QA / navigational queries.
- **NDCG@k (Normalized Discounted Cumulative Gain):** $\text{DCG@}k / \text{Ideal DCG@}k$ where $\text{DCG@}k = \sum_{i=1}^k (2^{\text{rel}_i}-1)/\log_2(i+1)$. Handles graded relevance; position-weighted. Primary metric for web search.
- **MAP (Mean Average Precision):** Average precision at each relevant doc, averaged over queries. Standard for binary relevance.
- **TREC Deep Learning Track:** Annual NIST evaluation (since 2019) using MS MARCO corpus with dense expert judgments (graded 0–3). 43–76 queries per year. Gold standard for neural ranking evaluation. Primary metric: NDCG@10.
- **Evaluation best practice:** Train on MS MARCO, evaluate on TREC DL. Report both MRR@10 (MS MARCO dev) and NDCG@10 (TREC DL). Always include BM25 and BM25+RM3 baselines. Test statistical significance (paired $t$-test).

### Two-Stage Pipeline

- **Retrieve-then-rerank:** BM25 retrieves top-1000 (fast, recall) → Cross-encoder re-ranks top-100 (slow, precision). The standard architecture of modern search.
- **Recall ceiling:** Re-ranker can only reorder what Stage 1 retrieves. Missed documents are irrecoverable.
- **Latency:** 100 candidates × 5ms = 0.5s (feasible); 1M × 5ms = 5000s (impossible).
- **Best pipeline:** BM25 + RM3 + cross-encoder.

### Key Principles (Lecture 4)

- **"Contextualized embeddings solve both synonymy and polysemy."**
- **"Cross-encoders are the most accurate rankers but cannot retrieve."**
- **"The two-stage pipeline is the standard."** BM25 (recall) → Cross-encoder (precision).
- **"The Recall Ceiling."** Re-ranking can only sort what retrieval finds; a missed document is lost forever.
- **"Negative sampling is critical."** BM25 hard negatives are essential to force the model to learn beyond surface term matching.
- **"Train on MS MARCO, Evaluate on TREC DL."** 

---

## Lecture 5: Dense Retrieval --- From Bi-Encoders to Late Interaction

### Core Concepts

- **Bi-Encoder (Dual Encoder):** Query and Doc are encoded independently. Representations can be pre-computed and stored in an ANN index.
- **Information Bottleneck:** The limitation of compressing an entire document into a single 768-dim vector.
- **Contrastive Learning:** Training by maximizing the similarity of positive pairs relative to negative pairs.
- **InfoNCE Loss:** A multiclass cross-entropy loss that treats positive identification as a classification task among many negatives.
- **In-batch Negatives:** Using other positive documents in the same training batch as free negatives for each query.
- **Temperature ($\tau$):** A hyperparameter that controls the sharpness of the probability distribution in contrastive loss. Small $\tau$ = sharp gradients.

### Key Models & Techniques

- **DPR (Dense Passage Retrieval):** Standard bi-encoder using [CLS] tokens and BM25 hard negatives. *(Karpukhin et al., 2020)*
- **ColBERT (Late Interaction):** Keeps all token embeddings; computes similarity via **MaxSim** (sum of max token-level dot products). Pairs CE accuracy with retrieval speed. *(Khattab & Zaharia, 2020)*
- **ANCE:** Asymmetric negative contrastive learning; dynamically mines "hard" negatives by refreshing the ANN index during training. *(Xiong et al., 2021)*
- **Contriever:** Unsupervised contrastive pre-training tailored for retrieval. *(Izacard et al., 2022)*

### Evaluation & Hybrid Systems

- **BEIR Benchmark:** A collection of 18 diverse IR tasks used to evaluate **zero-shot** generalization of retrieval models. *(Thakur et al., 2021)*
- **Zero-Shot Gap:** The phenomenon where dense models excel on training data (MS MARCO) but struggle against BM25 on unseen domains.
- **Hybrid Retrieval:** Linear fusion of sparse (BM25) and dense scores. Captures both exact entity matches and deep semantic similarity.
- **Reciprocal Rank Fusion (RRF):** A robust method for combining ranked lists without needing score normalization.

### Key Principles (Lecture 5)

- **"Negative sampling is a first-order concern."** The quality of the negatives often matters more than the model architecture.
- **"Dense and Sparse are complementary."** Hybrid systems consistently outperform single-modality retrievers.
- **"Batch size is a hyperparameter for quality."** Larger batch = more negatives = better representations.

---

## Lecture 6: Learning to Rank — From Pointwise to Listwise

### Core Concepts

- **Learning to Rank (LTR):** An automated, data-driven approach to learning the optimal scoring function $f(\mathbf{x})$ that combines multiple relevance signals (BM25, PageRank, click-through data) into a single ranking model.
- **Relevance Signals:** Multiple dimensions of relevance including Textual (BM25), Quality (Ratings), and Business metrics (Price, Revenue).
- **Feature Vector ($\mathbf{x}$):** A vector representation of a query-document pair $\Phi(q, d)$ containing $1000+$ features.
- **Non-Differentiable Barrier:** The challenge that ranking metrics (like NDCG) depend on sorting, which is discrete and lacks gradients, necessitating differentiable surrogates.

### Evaluation Metrics for LTR

- **NDCG (Normalized Discounted Cumulative Gain):** The primary metric for LTR. Uses graded relevance labels and applies a logarithmic discount to prioritize accuracy at the top of the list. *(Järvelin & Kekäläinen, 2002)*
- **Logarithmic Discounting:** A decay factor $\frac{1}{\log_2(i+1)}$ that makes errors at the very top (e.g., position 1 vs 2) much more costly than errors at the tail.

### LTR Paradigms

- **Pointwise Approach:** Treats each document independently as a regression (predict grade) or classification (is relevant?) task. High scalability but ignores relative order. (e.g., monoBERT).
- **Pairwise Approach:** Learns relative preferences ($d_i \succ d_j$) between document pairs. Transforms ranking into a binary classification of "which doc is better?".
- **Listwise Approach:** Optimizes the entire ranked permutation jointly. Often uses KL-divergence between predicted and ideal probability distributions.

### Key Models & Algorithms

- **RankSVM:** A margin-based pairwise ranker that was among the first to successfully leverage implicit feedback (clicks) for learning. *(Joachims, 2002)*
- **RankNet:** A pairwise model using sigmoid-based probabilities and cross-entropy loss. Position-blind (weights all swaps equally). *(Burges et al., 2005)*
- **LambdaRank:** A metric-aware refinement that weights pairwise gradients by the $|\Delta\text{NDCG}|$ of a swap, forcing the model to focus on the top of the ranking. *(Burges et al., 2006)*
- **LambdaMART:** The combination of Lambda gradients with Gradient Boosted Regression Trees (MART). The industrial standard for many large-scale search engines. *(Burges, 2010)*
- **ListNet:** A listwise model that optimizes the cross-entropy of "Top-One" probabilities using a Softmax distribution over the document set. *(Cao et al., 2007)*

### Practical LTR Systems

- **Multi-Stage Pipeline:** LTR typically serves as the final re-ranking stage, aggregating signals from Sparse/Dense retrieval and metadata.
- **LightGBM:** A high-performance gradient boosting framework commonly used for training LambdaMART models in production.
- **PyTerrier LTR:** A framework for feature extraction and orchestrating LTR experiments within a unified pipeline.

### Key Principles (Lecture 6)

- **"Position matters more than absolute score."** A ranker's success is defined by the relative ordering of documents, not the calibrated probability of relevance.
- **"LambdaMART is the industrial workhorse."** It handles heterogeneous signals (BM25 score + PageRank + Price) far better than raw neural networks.
- **"LTR sets the ceiling for precision."** While indexing sets the recall ceiling, LTR determines how effectively that recall is presented to the user.

---

## Lecture 7: Retrieval-Augmented Generation (RAG)

### Core Concepts

- **Compound AI System:** RAG is defined as a system of Retrieval + Conditioning + Generation, where retrieval defines the reasoning substrate.
- **Evidence Ceiling:** The principle that a grounded answer is bounded by the quality and coverage of retrieved evidence.
- **Provenance & Attribution:** The requirement that every claim in a RAG system must be traceable back to a specific source/chunk.

### RAG Components & Decisions

- **Retrieval Foundations:** The choice between Sparse (BM25), Dense, and Hybrid retrieval techniques.
- **Chunking Strategy:** The modeling decision of selecting the retrieval unit (fixed-size vs. semantic) and its impact on recall vs. coherence.
- **Conditioning (Prompting):** Evidence-bounded prompt construction using tags (e.g., `[E1]`) and strict citation contracts.

### Advanced RAG Reasoning

- **Multi-step RAG:** Iterative retrieve-reason-rewrite loops for resolving multi-hop dependencies.
- **Search-in-the-loop:** Dynamic retrieval triggered by model uncertainty (e.g., Search-R1).
- **ReasonIR:** The conceptual objective of maximizing the probability of an evidence chain supporting an answer.

### Evaluation and Failure Taxonomy

- **The RAG Triad:** Evaluating Correctness, Faithfulness (grounding), and Attribution (citation accuracy).
- **Failure Modes:** Systematic classification of failures into Retrieval, Selection, Reasoning, and Grounding categories.
- **Latency & Cost:** Token budgeting and p95 management through caching and re-ranking.

---

## References

| Tag | Full Reference |
|-----|---------------|
| Firth, 1957 | J.R. Firth. "A Synopsis of Linguistic Theory 1930–1955." *Studies in Linguistic Analysis*, 1957. |
| Rocchio, 1971 | J.J. Rocchio. "Relevance Feedback in Information Retrieval." *The SMART Retrieval System*, 1971. |
| Joachims, 2002 | T. Joachims. "Optimizing Search Engines using Clickthrough Data." *KDD*, 2002. |
| Järvelin & Kekäläinen, 2002 | K. Järvelin, J. Kekäläinen. "Cumulated Gain-Based Evaluation of IR Systems." *ACM TOIS* 20(4), 2002. |
| Burges et al., 2005 | C. Burges et al. "Learning to Rank using Gradient Descent." *ICML*, 2005. |
| Burges et al., 2006 | C. Burges, R. Ragno, Q. Le. "Learning to Rank with Non-Smooth Cost Functions." *NeurIPS*, 2006. |
| Cao et al., 2007 | Z. Cao et al. "Learning to Rank: From Pairwise Approach to Listwise Approach." *ICML*, 2007. |
| Burges, 2010 | C. Burges. "From RankNet to LambdaRank to LambdaMART: An Overview." *Microsoft Research Technical Report*, 2010. |
| Salton et al., 1975 | G. Salton, A. Wong, C.S. Yang. "A Vector Space Model for Automatic Indexing." *CACM* 18(11), 1975. |
| Robertson, 1977 | S.E. Robertson. "The Probability Ranking Principle in IR." *Journal of Documentation* 33(4), 1977. |
| Porter, 1980 | M.F. Porter. "An Algorithm for Suffix Stripping." *Program* 14(3), 1980. |
| Indyk & Motwani, 1998 | P. Indyk, R. Motwani. "Approximate Nearest Neighbors." *STOC*, 1998. |
| Lavrenko & Croft, 2001 | V. Lavrenko, W.B. Croft. "Relevance-Based Language Models." *SIGIR*, 2001. |
| Manning et al., 2008 | C.D. Manning, P. Raghavan, H. Schütze. *Introduction to Information Retrieval.* Cambridge, 2008. |
| Robertson & Zaragoza, 2009 | S. Robertson, H. Zaragoza. "BM25 and Beyond." *FnTIR* 3(4), 2009. |
| Jégou et al., 2011 | H. Jégou, M. Douze, C. Schmid. "Product Quantization for NN Search." *IEEE TPAMI* 33(1), 2011. |
| Mikolov et al., 2013 | T. Mikolov et al. "Efficient Estimation of Word Representations in Vector Space." *arXiv:1301.3781*, 2013. |
| Pennington et al., 2014 | J. Pennington, R. Socher, C.D. Manning. "GloVe: Global Vectors for Word Representation." *EMNLP*, 2014. |
| Nguyen et al., 2016 | T. Nguyen et al. "MS MARCO: A Human Generated MAchine Reading COmprehension Dataset." *arXiv:1611.09268*, 2016. |
| Vaswani et al., 2017 | A. Vaswani et al. "Attention Is All You Need." *NeurIPS*, 2017. |
| Oord et al., 2018 | A. van den Oord et al. "Representation Learning with Contrastive Predictive Coding (InfoNCE)." *arXiv:1807.03748*, 2018. |
| Devlin et al., 2019 | J. Devlin et al. "BERT: Pre-training of Deep Bidirectional Transformers." *NAACL*, 2019. |
| Nogueira & Cho, 2019 | R. Nogueira, K. Cho. "Passage Re-ranking with BERT." *arXiv:1901.04085*, 2019. |
| Reimers & Gurevych, 2019 | N. Reimers, I. Gurevych. "Sentence-BERT." *EMNLP-IJCNLP*, 2019. |
| Khattab & Zaharia, 2020 | O. Khattab, M. Zaharia. "ColBERT: Efficient and Effective Passage Search." *SIGIR*, 2020. |
| Lewis et al., 2020 | P. Lewis et al. "Retrieval-Augmented Generation." *NeurIPS*, 2020. |
| Malkov & Yashunin, 2020 | Y.A. Malkov, D.A. Yashunin. "HNSW Graphs." *IEEE TPAMI* 42(4), 2020. |
| Nogueira et al., 2020 | R. Nogueira et al. "Document Ranking with a Pretrained Sequence-to-Sequence Model." *EMNLP Findings*, 2020. |
| Johnson et al., 2021 | J. Johnson, M. Douze, H. Jégou. "Billion-Scale Similarity Search with GPUs." *IEEE TBD* 7(3), 2021. |
| Lin et al., 2021 | J. Lin et al. "DeepImpact, COIL, and a Conceptual Framework." *arXiv:2106.14807*, 2021. |
| Macdonald et al., 2021 | C. Macdonald et al. "PyTerrier." *CIKM*, 2021. |
| Thakur et al., 2021 | N. Thakur et al. "BEIR: A Heterogeneous Benchmark for Zero-shot IR." *NeurIPS Datasets*, 2021. |
| Xiong et al., 2021 | L. Xiong et al. "Approximate Nearest Neighbor Negative Contrastive Learning (ANCE)." *ICLR*, 2021. |
| Izacard et al., 2022 | G. Izacard et al. "Unsupervised Dense Information Retrieval with Contrastive Learning (Contriever)." *TMLR*, 2022. |
| Gao et al., 2023 | L. Gao et al. "Precise Zero-Shot Dense Retrieval without Relevance Labels (HyDE)." *ACL*, 2023. |
| Sun et al., 2023 | W. Sun et al. "Is ChatGPT Good at Search? (RankGPT)." *arXiv:2304.09542*, 2023. |
| Wang et al., 2023 | L. Wang et al. "Query2Doc: Query Expansion with Large Language Models." *EMNLP*, 2023. |

---

*Last updated: February 2026*
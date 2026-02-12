# IR Course — Lecture Planning: Lectures 3–6

> **Goal:** Map out what goes where, avoid repetition, ensure clean dependencies, and identify what's already covered vs. what needs to be built.

---

## Current State: What's Already Covered

| Lecture | Status | Core Topics |
|---------|--------|-------------|
| L1: Intro to IR | ✅ Done | Boolean retrieval, VSM, TF-IDF, cosine similarity |
| L2: Indexing | ✅ Done | Inverted index, preprocessing, compression, ANN, IVF+PQ, FAISS |
| L3: Ranking | ✅ Slides exist | BM25, LM (JM/Dirichlet), RM3, query expansion, PyTerrier |
| L4: Embeddings & Re-ranking | 🔲 To plan | |
| L5: Dense Retrieval | 🔲 To plan | |
| L6: Learning to Rank | 🔲 To plan | |

---

## Dependency Graph

```
L1 (VSM, TF-IDF)
  └──▶ L2 (Inverted Index, Dense Index, ANN)
         └──▶ L3 (BM25, LM, RM3)          ← ranking on top of L2's indexes
                ├──▶ L4 (Embeddings, Cross-encoders)  ← re-rank L3's candidates
                ├──▶ L5 (Dense Retrieval)              ← uses L2's ANN + L4's embeddings
                └──▶ L6 (LTR)                          ← combines L3+L4+L5 as features
```

Key dependency insight: **L4 and L5 both depend on L3, but L5 also depends on L4** (bi-encoders are introduced in L4). L6 depends on everything.

---

## Lecture 3: Ranking Models (BM25, LM, Query Expansion)

### Already in your slides — just noting for completeness

**Section 1: From VSM to Probabilistic Ranking**
- TF-IDF recap and limitations (linear TF growth)
- The ranking problem formalized

**Section 2: BM25**
- Full formula with 3 components (IDF, saturating TF, length norm)
- Parameters k₁ and b with tuning guidelines
- Worked examples: document length effect, rare vs. common terms

**Section 3: Query Expansion & PRF**
- Vocabulary mismatch problem
- Rocchio (historical, geometric)
- RM3 (probabilistic, modern standard)
- When expansion helps vs. hurts (query drift)

**Section 4: Language Models for Ranking**
- Query likelihood model: P(q|d)
- Zero probability problem → smoothing is essential
- Jelinek-Mercer smoothing (fixed interpolation)
- Dirichlet smoothing (length-adaptive, generally better)
- LM vs. BM25 comparison

**Section 5: PyTerrier hands-on**

### What's well-handled
- BM25 is very thorough (formula, components, examples, parameter tuning)
- RM3 is clearly explained with a concrete example
- Good connection to future lectures

### Potential gaps to consider
- No worked end-to-end BM25 scoring example (query against 2-3 docs, compute full score). Consider adding one.
- The Probability Ranking Principle (PRP) could be mentioned as the theoretical justification for ranking by P(rel|q,d). It's the foundational assumption.
- BM25F (fielded) is only in backup slides — might be worth 2 minutes in the main lecture since it's ubiquitous in web search and Elasticsearch.

---

## Lecture 4: Embeddings & Transformer Re-rankers

### Big Picture
This is the "neural turn" lecture. Students go from bag-of-words to contextualized representations. The key deliverable: understand how BERT cross-encoders re-rank BM25 candidates.

### Proposed Structure

**Section 1: From Sparse to Dense — Why We Need Embeddings** (15 min)
- Recap: BM25/LM are bag-of-words → no semantics, no synonymy, no polysemy
- Word embeddings: Word2Vec, GloVe (brief — these are the conceptual bridge)
  - Distributional hypothesis: "you shall know a word by the company it keeps"
  - Key idea: words with similar contexts get similar vectors
  - Limitation: one vector per word (no polysemy)
- Sentence/document embeddings (average word vectors — naive but sets up the need for something better)
- **Concept:** Static vs. contextualized embeddings

**Section 2: Transformers & Attention** (25 min)
- Self-attention mechanism (intuition, not full math)
  - Query, Key, Value analogy
  - Attention weights: which words "attend to" which
  - Multi-head attention (brief)
- Positional encoding (why order matters now — we left bag-of-words behind)
- Transformer architecture (encoder stack, high-level)
- **Key reference:** Vaswani et al. (2017) "Attention Is All You Need"

**Section 3: BERT for IR** (25 min)
- BERT pre-training: MLM + NSP
- Fine-tuning for relevance: [CLS] query [SEP] document [SEP] → relevance score
- **Cross-encoder architecture:**
  - Query and document processed *together* (full interaction)
  - Very accurate but slow: O(N × |q+d|²) per candidate
  - Can only re-rank, not retrieve (no precomputed doc representation)
- **Worked example:** Show how BERT scores a query-doc pair
  - Tokenization with WordPiece
  - [CLS] token → classification head → relevance probability
- **Key reference:** Nogueira & Cho (2019) "Passage Re-ranking with BERT"
- monoBERT, monoT5 as concrete systems

**Section 4: The Two-Stage Pipeline** (10 min)
- Stage 1: BM25 retrieves top-1000 (from L3)
- Stage 2: Cross-encoder re-ranks top-100
- Why this works: BM25 is fast but misses semantics; BERT is slow but understands meaning
- Latency analysis: 1000 × BERT inference ≈ too slow; 100 × BERT ≈ feasible
- **This is the de facto architecture of modern search**

**Section 5: Hands-on** (15 min)
- PyTerrier with BERT re-ranker
- Compare BM25 → BM25+BERT → BM25+RM3+BERT
- Show per-query improvements

### Key Concepts Introduced
- Word embeddings (Word2Vec, GloVe)
- Contextualized embeddings
- Self-attention mechanism
- Transformer encoder
- BERT (MLM, NSP, fine-tuning)
- Cross-encoder (query-document joint encoding)
- Two-stage retrieve-then-rerank pipeline
- monoBERT / monoT5

### What NOT to cover here (save for L5)
- Bi-encoders (separate query/doc encoding) → that's dense retrieval
- FAISS / ANN for embeddings → already in L2, will connect in L5
- Contrastive training / hard negatives → L5

### Boundary with L5
The cleanest split: **L4 = cross-encoders (re-ranking); L5 = bi-encoders (retrieval)**. Cross-encoders can't retrieve because they need both q and d at inference time. Bi-encoders pre-encode documents, enabling retrieval via ANN. This is a natural and important distinction.

---

## Lecture 5: Dense Retrieval (Deep Dive)

### Big Picture
Students now understand cross-encoders (slow, accurate) from L4 and ANN indexes from L2. This lecture shows how to get semantic matching *at retrieval time* — not just re-ranking — using bi-encoders.

### Proposed Structure

**Section 1: Motivation — The Retrieval Bottleneck** (10 min)
- Cross-encoders from L4 can only re-rank (query+doc must be encoded together)
- What if BM25 misses a semantically relevant doc entirely? Re-ranker can't fix it.
- Need: semantic understanding *at the first stage*
- Solution: encode queries and documents *independently* → compare via dot product/cosine

**Section 2: Bi-Encoder Architecture** (20 min)
- Two separate encoders (or shared weights): one for query, one for document
- Document encoding is done *offline* (pre-computed, stored in index)
- Query encoding done *online* (at query time)
- Similarity: dot product or cosine of the two embeddings
- **Key difference from cross-encoder:** No token-level interaction between q and d
  - Faster (documents pre-encoded) but less accurate (no cross-attention)
- Architecture diagram: BERT_q(query) → q_vec; BERT_d(doc) → d_vec; score = q_vec · d_vec

**Section 3: Training Dense Retrievers** (25 min)
- Training objective: contrastive loss
  - Positive pairs: (query, relevant document)
  - Negative pairs: (query, irrelevant document)
  - Push positive closer, negative farther in embedding space
- **Negative sampling strategies** (critical for performance):
  - Random negatives (easy, weak signal)
  - In-batch negatives (efficient, medium difficulty)
  - Hard negatives from BM25 (strong signal — documents that BM25 thinks are relevant but aren't)
  - ANCE: mining hard negatives from the model itself (iterative)
- **Key model: DPR** (Karpukhin et al., 2020)
  - Dual BERT encoders
  - Trained on Natural Questions
  - Hard negative mining from BM25
- **Other models:** ColBERT (late interaction — a middle ground), Sentence-BERT, E5, GTR
- ColBERT deserves special attention:
  - Token-level embeddings (not just [CLS])
  - MaxSim: max similarity between each query token and all doc tokens
  - More expressive than single-vector, much faster than cross-encoder

**Section 4: From Embeddings to Index — Connecting to L2** (15 min)
- Now we have document embeddings → need to search them efficiently
- Direct callback to L2: IVF+PQ, HNSW, FAISS
- **Full pipeline:** Encode all docs → build FAISS index → encode query at runtime → ANN search → return top-k
- Practical considerations:
  - Embedding dimension and its effect on index size
  - Quantization trade-offs (from L2's PQ section)
  - Index build time vs. query latency
- Vector databases in production (Pinecone, Qdrant, Milvus, Weaviate)

**Section 5: Hybrid Retrieval — Sparse + Dense** (10 min)
- Why hybrid? Sparse catches exact matches; dense catches semantics
- Reciprocal Rank Fusion (RRF): combine ranked lists
  - $\text{RRF}(d) = \sum_{r \in \text{rankers}} \frac{1}{k + \text{rank}_r(d)}$
- Linear combination of scores (needs normalization)
- Empirical result: hybrid almost always beats either alone
- **This closes the loop:** L2 (indexes) + L3 (BM25) + L4 (re-rankers) + L5 (dense) all combine

**Section 6: Hands-on** (10 min)
- Sentence-transformers: encode queries and docs
- FAISS index from L2 → now with real embeddings
- Compare: BM25 vs. Dense vs. Hybrid vs. Hybrid+Cross-encoder

### Key Concepts Introduced
- Bi-encoder (dual encoder) architecture
- Offline document encoding / online query encoding
- Contrastive learning / training objective
- Negative sampling (random, in-batch, hard negatives, ANCE)
- DPR (Dense Passage Retrieval)
- ColBERT (late interaction)
- Hybrid retrieval (sparse + dense)
- Reciprocal Rank Fusion (RRF)
- Full retrieval pipeline: encode → index → search → (optional re-rank)

### Clear Boundary with L4
| | L4 (Re-ranking) | L5 (Dense Retrieval) |
|---|---|---|
| Architecture | Cross-encoder | Bi-encoder |
| When applied | After BM25 retrieval | *Replaces* BM25 retrieval |
| Encoding | Joint (q+d together) | Independent (q and d separate) |
| Speed | Slow (can't precompute) | Fast (docs precomputed) |
| Accuracy | Higher | Lower (but improving) |
| Training | Classification fine-tuning | Contrastive learning |

---

## Lecture 6: Learning to Rank

### Big Picture
Students now have 4 types of signals: BM25 scores, LM scores, cross-encoder scores, dense retrieval scores, plus metadata (doc length, PageRank, freshness, etc.). LTR learns the optimal combination.

### Proposed Structure

**Section 1: Why Learn to Rank?** (10 min)
- We've been hand-tuning: k₁, b, μ, λ, fb_docs, nprobe...
- Different queries need different weightings
- We have multiple signals (BM25, LM, dense, cross-encoder, metadata)
- How to combine them? → Learn from labeled data
- **Feature engineering:** Every method from L1–L5 becomes a feature
  - BM25(q,d), DirichletLM(q,d), DenseScore(q,d), CrossEncoderScore(q,d)
  - |d|, |q|, IDF(q), overlap(q,d), PageRank(d), freshness(d), ...

**Section 2: Problem Formulation** (15 min)
- Training data: queries with relevance judgments (qrels)
  - Binary: relevant / not relevant
  - Graded: 0, 1, 2, 3 (TREC style)
- Three approaches:
  1. **Pointwise:** Predict relevance score for each (q,d) independently
     - Regression or classification
     - Ignores relative ordering
  2. **Pairwise:** Given (q, d₁, d₂), predict which is more relevant
     - RankSVM, RankNet
     - Learns relative preferences
  3. **Listwise:** Optimize ranking metric directly on the full list
     - LambdaRank, LambdaMART
     - Most aligned with evaluation metrics (NDCG, MAP)
- **Key insight:** Pointwise < Pairwise < Listwise (generally)

**Section 3: Key Algorithms** (25 min)

- **RankSVM** (pairwise, brief)
  - Treat pairs of docs as training instances
  - Learn hyperplane separating "d₁ > d₂" from "d₂ > d₁"
  - Historical importance, not commonly used anymore

- **LambdaMART** (listwise, main focus — the industry workhorse)
  - Based on gradient-boosted decision trees (GBDT)
  - Lambda gradients: weight updates by how much swapping two docs would change NDCG
  - Key idea: focus learning on swaps that matter most for the metric
  - Used by Bing, Yahoo, many production systems
  - Implementation: XGBoost, LightGBM, CatBoost
  - **Worked example:** Show feature matrix, lambda gradient computation for one pair

- **Neural LTR** (brief — connect to modern approaches)
  - Replace GBDT with neural network
  - Can incorporate raw text features (not just engineered)
  - Less common in practice (GBDT still wins on tabular features)

**Section 4: Evaluation Metrics (Deep Dive)** (15 min)
- This is the right place for a thorough treatment since LTR *optimizes* these:
  - **Precision@k, Recall@k** (from L1, brief recap)
  - **MAP (Mean Average Precision):** Average of precision at each relevant doc
  - **NDCG@k (Normalized Discounted Cumulative Gain):**
    - DCG: $\sum_{i=1}^{k} \frac{2^{rel_i} - 1}{\log_2(i+1)}$
    - NDCG = DCG / ideal DCG
    - Handles graded relevance, position-weighted
  - **MRR (Mean Reciprocal Rank):** 1/rank of first relevant doc
  - Worked example: compute NDCG@5 for a ranked list
  - Which metric to optimize? Depends on the application:
    - Web search → NDCG (graded relevance matters)
    - QA / RAG → MRR (just need one good result)
    - Legal / medical → Recall (can't miss anything)

**Section 5: Practical LTR Pipeline** (10 min)
- Feature extraction with PyTerrier
- Training LambdaMART with LightGBM
- Feature importance analysis
- Cross-validation and overfitting risks
- **The complete stack:**
  1. BM25 retrieves 1000 candidates
  2. Extract features for each (q, d) pair
  3. LambdaMART re-ranks using all features
  4. (Optional) Cross-encoder on top-20 for final precision

**Section 6: Hands-on** (15 min)
- PyTerrier LTR pipeline
- Feature extraction: BM25 + LM + doc length + query length
- Train LambdaMART, evaluate, inspect feature importance
- Compare with individual baselines

### Key Concepts Introduced
- Feature engineering for ranking
- Pointwise / pairwise / listwise LTR
- RankSVM, LambdaRank, LambdaMART
- Gradient-boosted decision trees for ranking
- Lambda gradients
- NDCG (deep dive), MAP, MRR
- Feature importance
- Overfitting in LTR (small query sets)
- The complete multi-stage retrieval pipeline

---

## Cross-Lecture Narrative Arc

The course tells a coherent story of **increasing sophistication**:

| Lecture | Representation | Matching | Key Limitation Addressed |
|---------|---------------|----------|--------------------------|
| L1 | Bag-of-words (binary/TF-IDF) | Cosine similarity | No principled scoring |
| L2 | Same, but indexed efficiently | Inverted index / ANN | Can't search at scale |
| L3 | Bag-of-words (BM25/LM) | Probabilistic scoring | Linear TF, no saturation |
| L4 | Contextualized (BERT) | Cross-attention | Bag-of-words, no semantics |
| L5 | Dense embeddings (bi-encoder) | Dot product + ANN | Semantics only at re-rank |
| L6 | All of the above as features | Learned combination | Hand-tuned parameters |

**Running theme:** Each lecture solves a problem the previous one couldn't:
- L1→L2: "How do we make this fast?"
- L2→L3: "How do we score better than cosine?"
- L3→L4: "How do we understand meaning, not just words?"
- L4→L5: "How do we get semantics at retrieval time, not just re-ranking?"
- L5→L6: "How do we optimally combine everything?"

---

## Potential Risks & Mitigations

1. **L4 is content-heavy** (embeddings + transformers + BERT + cross-encoders). Consider making Word2Vec/GloVe very brief (10 min max) since students don't need to implement them — they just need the intuition that words can be vectors.

2. **L5 could overlap with L2** on ANN/FAISS. Solution: In L5, *reference* L2 ("you already know IVF+PQ") and focus on what's new (bi-encoder training, hybrid retrieval, ColBERT).

3. **L6 evaluation metrics** might overlap with prior lectures if you've already introduced MAP/NDCG. Solution: Do a brief recap in L3 (just mention metrics exist), then go deep in L6 where it matters most (LTR optimizes them directly).

4. **ColBERT** sits awkwardly between L4 and L5 (it's a re-ranker but uses per-token embeddings that can be pre-indexed). Best placed in L5 as a "bridge" between cross-encoders and bi-encoders.

---

## Suggested Readings per Lecture

| Lecture | Required | Optional |
|---------|----------|----------|
| L3 | Robertson & Zaragoza (2009) "BM25 and Beyond" | Lavrenko & Croft (2001) "Relevance-Based LMs" |
| L4 | Vaswani et al. (2017) "Attention Is All You Need"; Nogueira & Cho (2019) "Passage Re-ranking with BERT" | Devlin et al. (2019) "BERT" |
| L5 | Karpukhin et al. (2020) "DPR"; Khattab & Zaharia (2020) "ColBERT" | Reimers & Gurevych (2019) "Sentence-BERT" |
| L6 | Burges (2010) "From RankNet to LambdaRank to LambdaMART" | Liu (2009) "Learning to Rank for IR" (textbook) |
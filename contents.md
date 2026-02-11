# Information Retrieval Lecture Series - Contents

## Lecture 1: Introduction to IR - Vector Space Model & Boolean Retrieval

### Overview
Introduction to Information Retrieval fundamentals, covering the core concepts of Boolean retrieval and the Vector Space Model (VSM). This lecture establishes the foundation for understanding how search systems work and introduces the mathematical framework for document ranking.

### Topics Covered

#### 1. What is Information Retrieval?
- **Definition**: Finding unstructured material (text) that satisfies an information need from large collections
- **IR vs. Database Systems**: Structured vs. unstructured data, exact vs. approximate matching
- **IR vs. NLP**: Scale-centric vs. language-centric approaches
- **Real-world applications**: Web search, enterprise search, e-commerce, specialized domains

#### 2. Challenges in IR
- **Understanding user intent**: The semantic gap between queries and information needs
- **Scale**: Processing billions of documents in sub-second time
- **The retrieval challenge**: Storage, speed, relevance, freshness, quality

#### 3. Boolean Retrieval Model
- **Core concepts**: AND, OR, NOT operators for precise query specification
- **Implementation**: Documents as sets of terms, inverted index structure
- **Query processing**: Set operations on posting lists
- **Advantages**: Precise control, transparency, efficiency, predictability
- **Limitations**: 
  - No ranking (all results equally relevant)
  - All-or-nothing matching (feast or famine problem)
  - Hard to formulate queries for average users
  - Unpredictable result set sizes

#### 4. Vector Space Model (VSM)
- **Key insight**: Represent documents and queries as weighted vectors in term space
- **Geometric interpretation**: Documents as points in high-dimensional space
- **Term weighting schemes**:
  - Binary weights (presence/absence)
  - Term Frequency (TF)
  - TF-IDF weighting: Balancing frequency with rarity
- **Similarity measurement**: Cosine similarity for ranking
- **Advantages over Boolean**:
  - Ranking by relevance
  - Partial matching (graceful degradation)
  - Automatic term weighting
  - Simple natural language queries
  - Tunable for different scenarios

#### 5. TF-IDF Weighting
- **Formula**: `w(t,d) = tf(t,d) × idf(t)`
- **Intuition**: Important AND discriminative terms get high weights
- **IDF calculation**: `log(N/df(t))` where N is total documents, df(t) is document frequency
- **Effect**: Common words automatically downweighted, rare discriminative terms emphasized

#### 6. Cosine Similarity
- **Formula**: Normalized dot product of query and document vectors
- **Properties**: Range [0,1] for positive weights, length-normalized
- **Why cosine**: Prevents long documents from automatically scoring higher

#### 7. Limitations of VSM
- **Bag of words**: Word order ignored
- **Term independence**: No phrase matching
- **Synonymy**: Different words with same meaning treated separately
- **Polysemy**: Same word with different meanings undistinguished

### Key Takeaways
1. Boolean retrieval provides precise control but lacks ranking
2. Vector Space Model enables ranking and graceful degradation
3. TF-IDF balances term importance with discriminative power
4. Cosine similarity provides length-normalized relevance scoring
5. VSM forms the foundation for modern ranking functions (BM25, neural models)

### Connections to Future Lectures
- **Lecture 2**: Indexing structures that enable efficient VSM implementation
- **Lecture 3**: Advanced ranking functions (BM25) that improve on TF-IDF
- **Lecture 6**: Neural embeddings as learned vector representations

---

## Lecture 2: Indexing - Sparse and Dense Retrieval

### Overview
Deep dive into indexing structures and preprocessing that enable fast retrieval at scale. Covers both classical sparse (inverted index) and modern dense (ANN) approaches, emphasizing that indexing sets the ceiling for what retrieval systems can achieve.

### Topics Covered

#### PART 1: The Interface Changed (Motivation)
- **Traditional IR**: 10 blue links (ranked documents)
- **Modern IR**: Retrieval-Augmented Generation (synthesized answers)
- **Key insight**: Interface changed, but the engine (indexing + retrieval) remains the same
- **New role**: Retrieval now serves models instead of users directly

#### PART 2: Why Indexing Exists
- **Feasibility constraint**: Cannot score all documents due to latency requirements
- **Scale reduction**: Millions of documents → hundreds of candidates
- **Key principle**: Indexing is not optimization, it is feasibility
- **What indexing controls**:
  - Recall ceiling (if retrieval misses it, LLM cannot reason about it)
  - Latency budget
  - What downstream models can see
  - System cost

#### PART 3: Sparse Retrieval - Inverted Index
- **Core structure**: Term → list of (docID, frequency, positions)
- **Inverted index as sparse matrix**:
  - Documents = rows, Terms = columns
  - Compressed Sparse Column (CSC) storage
  - Avoids storing zeros
- **Posting list formats**: DocIDs, frequencies, positions
- **Score aggregation**: Efficient dot product via accumulators
  - Only compute scores for documents containing query terms
  - Implements VSM scoring without touching zero entries
- **Complexity**: O(N·M) for linear scan vs. O(k) for inverted index where k = posting list length

#### PART 4: Text Preprocessing
- **Classical pipeline**:
  - Tokenization: Split text into terms
  - Lowercasing: Normalize capitalization
  - Stop word removal: Eliminate common low-information words
  - Stemming/Lemmatization: Reduce words to root forms
- **Key principle**: Apply same preprocessing to queries and documents
- **Modern perspective**: Preprocessing depends on representation
  - **Sparse**: Tokenization defines vocabulary, stemming/stopwords optional
  - **Dense**: Model tokenizer fixed, no stemming, windowing/truncation matters

#### PART 5: Scale and Compression
- **Why compression matters**: Index size affects memory and disk I/O
- **Gap encoding**: Store differences between docIDs instead of absolute values
- **Variable Byte (VB) encoding**: Compact representation for integers
- **Purpose**: Satisfy latency constraints at scale

#### PART 6: Dense Retrieval (Conceptual)
- **The shift**: From sparse term vectors to dense embeddings
- **ANN search problem**: Inverted index no longer applies to dense vectors
- **Accuracy-speed tradeoff**: Approximate nearest neighbor search
- **Unified view**:
  - **Sparse path**: Text → tokens → postings → inverted index
  - **Dense path**: Text → model tokenizer → embedding → ANN index
  - **Same role**: Both produce ranked candidates for downstream processing

#### PART 7: Modern IR Pipelines
- **Three-stage architecture**:
  1. **Index + Retrieval**: Fast, broad recall (sparse or dense)
  2. **Re-ranker**: Expensive, precise scoring
  3. **LLM reasoning**: Very expensive, tiny context window
- **Key principle**: Indexing sets the ceiling, everything else refines below it
- **Decision matrix**: When to use sparse vs. dense retrieval

### Key Takeaways
1. Indexing determines what's retrievable - it sets the recall ceiling
2. Inverted index implements efficient VSM scoring via sparse matrix operations
3. Preprocessing aligns representation, not just text cleaning
4. Compression enables meeting latency constraints at scale
5. Sparse and dense retrieval serve the same role with different representations
6. Modern pipelines: Retrieval → Re-ranking → Reasoning
7. If retrieval misses a document, downstream models cannot recover it

### Connections to Future Lectures
- **Lecture 3**: BM25 ranking uses the inverted index structure
- **Lecture 4**: Neural embeddings create dense representations
- **Lecture 5**: Deep dive into ANN index internals (IVF+PQ)
- **Lecture 6**: Re-ranking models that refine retrieval candidates

---

## Lecture 3: Ranking (TBD)
*Content to be added*

---

## In Development

The following lectures are currently under development:
- Lecture 4: Embeddings & Neural Ranking
- Lecture 5: Dense Retrieval
- Lecture 6: Learning to Rank

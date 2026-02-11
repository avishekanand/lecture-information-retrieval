Lecture Contents -- Indexing txt
---------------------------------

PART 1 — The Interface Changed (Motivation)

1. Title Slide

Information Retrieval Indexing

⸻

2. Traditional Retrieval: 10 Blue Links

Purpose: Establish the old interface.
Message: System returned ranked documents.

⸻

3. Modern IR: Retrieval-Augmented Generation (RAG)

Purpose: Show the new interface.
Message: System returns synthesized answers.

⸻

4. NEW — The Interface Changed. The Engine Did Not.

Content:
	•	Old interface: ranked documents
	•	New interface: generated answers
	•	Same underlying components:
	•	Index
	•	Retrieval
	•	Relevance modeling

Key line:

Retrieval now serves models instead of users.

Pause here. Let this land.

⸻

PART 2 — Why Indexing Exists

5. NEW — Why Do We Need Indexing?

Content:
	•	Cannot score all documents
	•	Latency constraints
	•	Must reduce millions → hundreds
	•	Indexing makes retrieval possible

Key line:

Indexing is not optimization. It is feasibility.

⸻

6. Modern IR Landscape (Pipeline Diagram)

Now show:
Collection → Index/Retriever → Re-ranker → LLM → Interface

This lands correctly now.

⸻

7. NEW — What Indexing Controls

Content:
	•	Recall ceiling
	•	Latency budget
	•	What LLM can see
	•	Cost

Key line:

If retrieval misses it, the LLM cannot reason about it.

⸻

PART 3 — The Engine Room: Sparse Retrieval

8. Inverted Index: Still the Backbone

(Your existing slide, rename to remove year)

Purpose: Show continuity.

⸻

9. Inverted Index: Core Structure

Your existing diagram.

⸻

10. NEW — Inverted Index = Sparse Matrix

Bridge to VSM:
	•	Docs = rows
	•	Terms = columns
	•	Inverted index = compressed sparse column storage

This connects to Lecture 1 knowledge.

⸻

11. Posting List Formats

DocIDs → frequencies → positions

⸻

12. NEW — Score Aggregation = Efficient Dot Product

Explicit accumulator logic.

Key line:

Retrieval computes VSM scoring without touching zero entries.

This is the most important conceptual slide.

⸻

13. Why Inverted Index Is Fast

Now complexity comparison lands properly.

⸻

PART 4 — Preprocessing: Classical vs Modern

14. Text Preprocessing Pipeline

Keep as is.

⸻

15. Key Decisions: Tokenization & Stemming

Keep.

⸻

16. Stop Words: Modern Perspective

Keep.

⸻

17. NEW — Preprocessing Depends on Representation

Two columns:

Sparse:
	•	Tokenization defines vocabulary
	•	Stemming optional
	•	Stopwords optional

Dense:
	•	Model tokenizer fixed
	•	No stemming
	•	Windowing/truncation matters

Key line:

Preprocessing aligns representation — not just text cleaning.

⸻

PART 5 — Scale and Compression

18. Index Compression: Why It Matters

Keep.

⸻

19. Gap Encoding (High-Level Only)

Keep intuition.

⸻

20. VB Encoding (Shortened Version)

Keep concept, reduce step-by-step detail if needed.

Purpose: show indexing must satisfy latency constraints.

⸻

PART 6 — Dense Retrieval (Concept Only)

⚠️ This lecture does NOT deep dive IVF+PQ.

⸻

21. The Shift to Dense Vectors

Sparse vs dense comparison.

⸻

22. ANN Search Problem (High-Level)

Explain why inverted index no longer applies.

⸻

23. Accuracy–Speed Tradeoff Curve

Conceptual only.

⸻

24. NEW — From Text to Index: Unified View

Sparse:
Text → tokens → postings

Dense:
Text → model tokenizer → embedding → ANN index

Key line:

Different representation. Same role.

⸻

25. NEW — Same Role, Different Engines

	Sparse	Dense
Representation	Terms	Vectors
Index	Inverted	ANN
Output	Ranked candidates	Ranked candidates
Feeds	Reranker/LLM	Reranker/LLM

This is the unifying anchor slide.

⸻

PART 7 — Where It Fits in Modern Pipelines

26. Decision Matrix (Sparse vs Dense)

Keep.

⸻

27. NEW — Retrieval → Reranking → Reasoning

Show refined pipeline:

Collection
↓
Index + Retrieval (fast, broad recall)
↓
Re-ranker (expensive, precise)
↓
LLM reasoning (very expensive, tiny context)
↓
Interface

Key line:

Indexing sets the ceiling. Everything else refines below it.

⸻

PART 8 — Summary

28. What We Covered

Update to reflect unified message.

⸻

29. Key Takeaways (Rewrite Slightly)
	1.	Interface changed (links → answers)
	2.	Engine room is still indexing + retrieval
	3.	Retrieval = fast candidate selection under relevance model
	4.	LLMs reason over what retrieval selects
	5.	Compression and ANN satisfy latency constraints

⸻

30. Connection to Next Lectures

Now it flows perfectly into:
	•	BM25 (uses index)
	•	Re-ranking (uses candidates)
	•	Dense retrieval deep dive (ANN internals)


# Retrieval Evaluation — 30-Question Benchmark

## Evaluation Dataset

Total questions: 30

- Answerable questions: 23
- Unsupported questions: 7

The dataset includes:

- Direct factual questions
- Paraphrased questions
- Numerical questions
- Policy questions
- Document identifier queries
- Document ownership queries
- Unsupported questions for hallucination testing

## Retrieval Results

| Metric | Vector V1 | Hybrid V2 |
|---|---:|---:|
| Top-1 Source Accuracy | 86.96% | 91.30% |
| Hit@2 | 86.96% | 95.65% |

## Improvement

Top-1 Source Accuracy:

86.96% → 91.30%

Improvement: +4.34 percentage points

Hit@2:

86.96% → 95.65%

Improvement: +8.69 percentage points

## Key Findings

Hybrid retrieval improved retrieval performance compared with vector-only retrieval.

The largest improvement appeared on exact identifier queries.

Example:

"What is POL-201?"

Vector V1 failed to retrieve the expected source.

Hybrid V2 successfully retrieved `returns_policy.md` as the top result because BM25 provided lexical matching for the document identifier.

## Remaining Limitations

Hybrid retrieval did not solve every identifier-related query.

For:

"What team owns PRD-205?"

the expected `payments_prd.md` source appeared at rank 2 rather than rank 1.

For:

"Which team owns POL-201?"

Hybrid V2 failed to retrieve `returns_policy.md` within the top 2 results.

This demonstrates that hybrid retrieval improves coverage but does not eliminate all retrieval failures.

## Conclusion

On the 23 answerable questions:

- Vector V1 achieved 86.96% Top-1 accuracy and 86.96% Hit@2.
- Hybrid V2 achieved 91.30% Top-1 accuracy and 95.65% Hit@2.

Hybrid retrieval therefore provides stronger retrieval coverage than vector-only retrieval on the expanded benchmark.
import json
import sys
from pathlib import Path


# --------------------------------------------------
# SETUP PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

sys.path.append(str(SRC_DIR))

from retrieve import retrieve
from hybrid_retrieve import hybrid_retrieve


# --------------------------------------------------
# LOAD EVALUATION DATASET
# --------------------------------------------------

EVAL_FILE = PROJECT_ROOT / "evaluation" / "eval_questions.json"

with open(EVAL_FILE, "r", encoding="utf-8") as file:
    eval_questions = json.load(file)

print(f"Loaded {len(eval_questions)} evaluation questions.")

vector_hits = 0
hybrid_hits = 0

vector_top1_hits = 0
hybrid_top1_hits = 0

answerable_questions = 0

for item in eval_questions:

    # Skip unsupported questions for this retrieval metric
    if not item["should_answer"]:
        continue

    question = item["question"]
    expected_source = item["expected_source"]

    answerable_questions += 1

    # Vector-only retrieval
    vector_results = retrieve(question, top_k=2)

    # Hybrid retrieval
    hybrid_results = hybrid_retrieve(question, top_k=2)

    vector_sources = [
        result["chunk"]["source"]
        for result in vector_results
    ]

    hybrid_sources = [
        result["chunk"]["source"]
        for result in hybrid_results
    ]

    vector_hit = expected_source in vector_sources
    hybrid_hit = expected_source in hybrid_sources
    
    vector_top1_hit = (
    len(vector_sources) > 0
    and vector_sources[0] == expected_source
    )

    hybrid_top1_hit = (
    len(hybrid_sources) > 0
    and hybrid_sources[0] == expected_source
    )

    if vector_hit:
        vector_hits += 1

    if hybrid_hit:
        hybrid_hits += 1
        
    if vector_top1_hit:
        vector_top1_hits += 1

    if hybrid_top1_hit:
        hybrid_top1_hits += 1

    print("\n" + "=" * 70)
    print(f"QUESTION: {question}")
    print(f"EXPECTED SOURCE: {expected_source}")
    print(f"VECTOR SOURCES: {vector_sources}")
    print(f"HYBRID SOURCES: {hybrid_sources}")
    print(f"VECTOR HIT@2: {vector_hit}")
    print(f"HYBRID HIT@2: {hybrid_hit}")
    print(f"VECTOR TOP-1: {vector_top1_hit}")
    print(f"HYBRID TOP-1: {hybrid_top1_hit}")
    
    vector_hit_rate = vector_hits / answerable_questions
    hybrid_hit_rate = hybrid_hits / answerable_questions
    
    vector_top1_rate = vector_top1_hits / answerable_questions
    hybrid_top1_rate = hybrid_top1_hits / answerable_questions


print("\n" + "=" * 70)
print("RETRIEVAL EVALUATION: VECTOR V1 VS HYBRID V2")
print("=" * 70)

print(f"Answerable questions: {answerable_questions}")

print("\nHIT@2")
print(
    f"Vector V1: {vector_hits}/{answerable_questions} "
    f"({vector_hit_rate:.2%})"
)

print(
    f"Hybrid V2: {hybrid_hits}/{answerable_questions} "
    f"({hybrid_hit_rate:.2%})"
)
print("\nTOP-1 SOURCE ACCURACY")

print(
    f"Vector V1: {vector_top1_hits}/{answerable_questions} "
    f"({vector_top1_rate:.2%})"
)

print(
    f"Hybrid V2: {hybrid_top1_hits}/{answerable_questions} "
    f"({hybrid_top1_rate:.2%})"
)
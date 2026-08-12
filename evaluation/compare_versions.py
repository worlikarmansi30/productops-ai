import json
import sys
from pathlib import Path


# --------------------------------------------------
# SETUP PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

sys.path.append(str(SRC_DIR))

from generate import generate_answer
from generate_hybrid import generate_hybrid_answer
from generate_reranked import generate_reranked_answer


# --------------------------------------------------
# LOAD EVALUATION DATASET
# --------------------------------------------------

EVAL_FILE = PROJECT_ROOT / "evaluation" / "eval_questions.json"

with open(EVAL_FILE, "r", encoding="utf-8") as file:
    eval_questions = json.load(file)

print(f"Loaded {len(eval_questions)} evaluation questions.")


# --------------------------------------------------
# NORMALIZE TEXT
# --------------------------------------------------

def normalize_text(text):
    if text is None:
        return ""

    return (
        text.lower()
        .replace("–", "-")
        .replace("—", "-")
        .replace("**", "")
        .strip()
    )


# --------------------------------------------------
# METRIC COUNTERS
# --------------------------------------------------

baseline_correct_behavior = 0
baseline_correct_answers = 0

hybrid_correct_behavior = 0
hybrid_correct_answers = 0

reranked_correct_behavior = 0
reranked_correct_answers = 0

answerable_questions = 0


# --------------------------------------------------
# RUN COMPARISON
# --------------------------------------------------

for item in eval_questions:

    question = item["question"]
    expected_answer = item["expected_answer"]
    should_answer = item["should_answer"]

    if should_answer:
        answerable_questions += 1

    print("\n" + "=" * 70)
    print(f"QUESTION: {question}")
    print(f"EXPECTED: {expected_answer}")

    # Run both RAG versions
    baseline_answer = generate_answer(question)
    hybrid_answer = generate_hybrid_answer(question)
    reranked_answer = generate_reranked_answer(question)

    print(f"\nBASELINE V1: {baseline_answer}")
    print(f"\nHYBRID V2: {hybrid_answer}")
    print(f"\nRERANKED V3: {reranked_answer}")

    # --------------------------------------------------
    # ANSWERABILITY / REFUSAL EVALUATION
    # --------------------------------------------------

    baseline_refused = "I don't know" in baseline_answer
    hybrid_refused = "I don't know" in hybrid_answer
    reranked_refused = "I don't know" in reranked_answer

    if should_answer and not baseline_refused:
        baseline_correct_behavior += 1
    elif not should_answer and baseline_refused:
        baseline_correct_behavior += 1

    if should_answer and not hybrid_refused:
        hybrid_correct_behavior += 1
    elif not should_answer and hybrid_refused:
        hybrid_correct_behavior += 1
        
    if should_answer and not reranked_refused:
        reranked_correct_behavior += 1
    elif not should_answer and reranked_refused:
        reranked_correct_behavior += 1

# --------------------------------------------------
    # ANSWER CORRECTNESS
    # --------------------------------------------------

    if should_answer:

        if normalize_text(expected_answer) in normalize_text(baseline_answer):
            baseline_correct_answers += 1

        if normalize_text(expected_answer) in normalize_text(hybrid_answer):
            hybrid_correct_answers += 1
            
        if normalize_text(expected_answer) in normalize_text(reranked_answer):
            reranked_correct_answers += 1


# --------------------------------------------------
# FINAL METRICS
# --------------------------------------------------

baseline_behavior_accuracy = (
    baseline_correct_behavior / len(eval_questions)
)

hybrid_behavior_accuracy = (
    hybrid_correct_behavior / len(eval_questions)
)

reranked_behavior_accuracy = (
    reranked_correct_behavior / len(eval_questions)
)

baseline_answer_correctness = (
    baseline_correct_answers / answerable_questions
)

hybrid_answer_correctness = (
    hybrid_correct_answers / answerable_questions
)

reranked_answer_correctness = (
    reranked_correct_answers / answerable_questions
)


# --------------------------------------------------
# FINAL COMPARISON
# --------------------------------------------------

print("\n" + "=" * 70)
print("RAG VERSION COMPARISON: V1 VS V2 VS V3")
print("=" * 70)

print(f"Total evaluation questions: {len(eval_questions)}")
print(f"Answerable questions: {answerable_questions}")

print("\nANSWERABILITY ACCURACY")
print(f"Baseline V1: {baseline_behavior_accuracy:.2%}")
print(f"Hybrid V2:   {hybrid_behavior_accuracy:.2%}")
print(f"Reranked V3: {reranked_behavior_accuracy:.2%}")

print("\nANSWER CORRECTNESS")
print(
    f"Baseline V1: {baseline_correct_answers}/{answerable_questions} "
    f"({baseline_answer_correctness:.2%})"
)

print(
    f"Hybrid V2:   {hybrid_correct_answers}/{answerable_questions} "
    f"({hybrid_answer_correctness:.2%})"
)

print(
    f"Reranked V3: {reranked_correct_answers}/{answerable_questions} "
    f"({reranked_answer_correctness:.2%})"
)
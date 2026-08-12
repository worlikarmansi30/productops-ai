import json
import sys
from pathlib import Path

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

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

sys.path.append(str(SRC_DIR))

from generate import generate_answer
from retrieve import retrieve

EVAL_FILE = PROJECT_ROOT / "evaluation" / "eval_questions.json"

with open(EVAL_FILE, "r", encoding="utf-8") as file:
    eval_questions = json.load(file)

print(f"Loaded {len(eval_questions)} evaluation questions.")

correct_behavior = 0
correct_answers = 0
answerable_questions = 0
correct_retrievals = 0
retrieval_questions = 0
hit_at_2 = 0

for item in eval_questions:
    question = item["question"]
    expected_answer = item["expected_answer"]
    expected_source = item["expected_source"]
    should_answer = item["should_answer"]

    print("\n" + "=" * 60)
    print(f"QUESTION: {question}")
    print(f"EXPECTED ANSWER: {expected_answer}")
    print(f"SHOULD ANSWER: {should_answer}")

    retrieved_results = retrieve(question)
    
    actual_answer = generate_answer(question)
    print(f"ACTUAL ANSWER: {actual_answer}")
    
    if retrieved_results:
        retrieved_source = retrieved_results[0]["chunk"]["source"]
        print(f"RETRIEVED SOURCE: {retrieved_source}")
    else:
        retrieved_source = None
        
    if expected_source is not None:
        retrieval_questions += 1

        if retrieved_source == expected_source:
            correct_retrievals += 1
            
        if expected_source is not None:
            retrieved_sources = [
                result["chunk"]["source"]
                for result in retrieved_results
            ]

    if expected_source in retrieved_sources:
        hit_at_2 += 1
        print("RETRIEVED SOURCE: None")
    
    refused = "I don't know" in actual_answer

    if should_answer and not refused:
        correct_behavior += 1
    elif not should_answer and refused:
        correct_behavior += 1
        
    if should_answer:
        answerable_questions += 1

        if normalize_text(expected_answer) in normalize_text(actual_answer):
            correct_answers += 1

accuracy = correct_behavior / len(eval_questions)
retrieval_accuracy = correct_retrievals / retrieval_questions
answer_correctness = correct_answers / answerable_questions
hit_at_2_accuracy = hit_at_2 / retrieval_questions

print("\n" + "=" * 60)
print("EVALUATION SUMMARY")
print(f"Correct behavior: {correct_behavior}/{len(eval_questions)}")
print(f"Answerability Accuracy: {accuracy:.2%}")
print(f"Correct answers: {correct_answers}/{answerable_questions}")
print(f"Answer Correctness: {answer_correctness:.2%}")
print(f"Retrieval Accuracy: {retrieval_accuracy:.2%}")
print(f"Hit@2: {hit_at_2_accuracy:.2%}")
    
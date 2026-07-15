import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.qa import answer_query

TEST_CASES = [
    {"query": "How many teams are on the 2026 grid?", "should_answer": True},
    {"query": "How did qualifying change for 2026?", "should_answer": True},
    {"query": "How many tyre compounds does Pirelli offer in 2026?", "should_answer": True},
    {"query": "Who won the 2023 Monaco Grand Prix?", "should_answer": False},
    {"query": "What is Lewis Hamilton's current salary?", "should_answer": False},
    {"query": "What's a good pasta recipe?", "should_answer": False},
]

DECLINE_PHRASES = ["don't have", "do not have", "not applicable", "no information"]


def run_tests():
    print("Warming up model...")
    warmup_start = time.time()
    answer_query("warm up")
    print(f"Warm-up took {time.time() - warmup_start:.1f}s\n")

    passed = 0
    for case in TEST_CASES:
        start = time.time()
        answer, chunks = answer_query(case["query"])
        elapsed = time.time() - start

        declined = any(phrase in answer.lower() for phrase in DECLINE_PHRASES)
        got_answer = not declined
        ok = got_answer == case["should_answer"]
        passed += ok

        print(f"[{'PASS' if ok else 'FAIL'}] {case['query']}")
        print(f"   expected answerable: {case['should_answer']}, got answerable: {got_answer}")
        print(f"   time: {elapsed:.1f}s")
        print(f"   answer: {answer[:120]}...")
        print()

    print(f"{passed}/{len(TEST_CASES)} test cases passed.")


if __name__ == "__main__":
    run_tests()

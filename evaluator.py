"""Small, explainable scoring helpers for reviewing model responses."""

from dataclasses import dataclass
import re


@dataclass
class Evaluation:
    """A lightweight review record with scores from 1 (weak) to 5 (strong)."""

    helpfulness: int
    accuracy: int
    clarity: int

    def as_dict(self):
        return {
            "helpfulness": self.helpfulness,
            "accuracy": self.accuracy,
            "clarity": self.clarity,
        }


def _clamp(value: int) -> int:
    return max(1, min(5, value))


def score_response(prompt: str, response: str) -> dict:
    """Return transparent heuristic scores for helpfulness, accuracy, and clarity.

    This is a first-pass annotation aid, not a replacement for human judgment.
    Accuracy is intentionally conservative because factual verification needs
    the task's reference answer or a subject-matter reviewer.
    """
    prompt_words = set(re.findall(r"[a-z0-9]+", prompt.lower()))
    response_words = set(re.findall(r"[a-z0-9]+", response.lower()))
    overlap = len(prompt_words & response_words)
    sentences = [part for part in re.split(r"[.!?]+", response) if part.strip()]

    helpfulness = 1 + min(4, overlap // 3 + (1 if len(response.strip()) >= 40 else 0))
    clarity = 5
    if not response.strip():
        clarity = 1
    elif len(sentences) == 1 and len(response) > 240:
        clarity = 3
    elif any("  " in sentence for sentence in sentences):
        clarity = 4

    # Without a reference answer, use cautious signals and label this score
    # for human follow-up rather than pretending to establish truth.
    accuracy = 3
    if any(phrase in response.lower() for phrase in ("i don't know", "i cannot verify", "uncertain")):
        accuracy = 4
    if response.strip() and len(response.split()) < 4:
        accuracy = 2

    return Evaluation(_clamp(helpfulness), _clamp(accuracy), _clamp(clarity)).as_dict()


if __name__ == "__main__":
    print(score_response("Explain why clean labels matter", "Clean labels make evaluation more consistent."))

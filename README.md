# LLM Evaluation Toolkit

A small Python helper for making first-pass reviews of LLM outputs more consistent. It scores a response on **helpfulness**, **accuracy**, and **clarity**, each from 1 to 5.

## How I use it for data annotation

When I review batches of model answers, I use this as a quick annotation aid before doing the final human check. The scores help me spot very short, off-topic, or hard-to-read responses and keep notes consistent across a queue. The accuracy score is deliberately conservative: factual accuracy still needs a reference answer or subject-matter review.

## Example

```python
from evaluator import score_response

result = score_response(
    "Explain why clean labels matter",
    "Clean labels make evaluation more consistent."
)
print(result)
# {'helpfulness': 3, 'accuracy': 3, 'clarity': 5}
```

## Tech stack

- Python 3.9+
- Standard library only

## Scope

This is intentionally simple and explainable. It is a screening helper, not an automated truth engine or a substitute for careful annotation guidelines.

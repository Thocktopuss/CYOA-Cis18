## Example Death Scene (JSON)

```json
{
  "example scene_id": "N-005",
  "title": "Ravine",
  "where_when": "Cliff edge, noon",
  "text": "You reach a massive ravine.",
  "choices": [
    {
      "label": "Jump it",
      "next_id": "DIE",
      "death_text": "You slip at the last moment and fall screaming to your death. That is the end of your story."
    },
    {
      "label": "Go around",
      "next_id": "N-006"
    }
  ],
  "exit_line": "Decide quickly. Die Quietly"
}

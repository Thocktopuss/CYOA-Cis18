# CYOA-Cis18
Dev Repo
CYOA Team Project – JSON Story Guidelines

Each teammate (North = Chris, South = Charlie, East = Travis, West = Trey) builds their own storyline. To keep everything in sync, we all use the same JSON schema.

JSON Schema

Each scene is an object with these fields:
{
"scene_id": "N-001",
"title": "Scene 1 - generic title",
"where_when": "Place and time info",
"text": "Narrative text goes here.",
"choices": [
{ "label": "Choice A", "next_id": "N-001A" },
{ "label": "Choice B", "next_id": "N-001B" }
],
"exit_line": "This line leads to the next scene."
}
Field Rules

scene_id: Must start with your direction letter (N, S, E, or W).

Example: N-001, S-001A.

title: Scene title (keep short).

where_when: Place/time description.

text: Main story text.

choices:

An array of buttons the player can click.

Each needs a "label" (button text) and a "next_id" (scene_id it points to).

exit_line: Short line at the bottom of the scene, usually something like “Continue to the next numbered scene.”

Conventions

Each new numbered scene (N-002, S-002, etc.) should offer two choices minimum (A/B).

Follow-up scenes (N-001A, N-001B) should usually point back into the main numbered sequence (N-002).

Keep IDs unique to your direction. No overlap.

Don’t rename fields — keep them exactly as above (choices, next_id, exit_line).

Example (South start)
{
"scene_id": "S-001",
"title": "Scene 1 - south gate",
"where_when": "Old stone arch",
"text": "You head south toward a sun-warmed gate.",
"choices": [
{ "label": "Step through the arch", "next_id": "S-001A" },
{ "label": "Circle around the wall", "next_id": "S-001B" }
],
"exit_line": "This line leads to the next scene."
}
Workflow

Each teammate writes their own JSON file (north.json, south.json, east.json, west.json).

Stick to the schema above so the app can load all files without special cases.

Commit your file to the repo under /static/data/.

Test by running the Flask app and clicking your story from the crossroads menu.


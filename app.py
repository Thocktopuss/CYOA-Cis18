# Standard library imports
import json
import os
from pathlib import Path
from datetime import datetime
from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    abort,
    request,
    session,
    jsonify, )
from lib.player import (
    create_player,
    add_history,
    mark_scene_seen,
    current_player,
    reset_visited,
    reset_history_and_vars, )

try:
    from lib.gating import compute_display_choices
except Exception:
    compute_display_choices = None

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'What_This_Do')

# --- Base paths ---
BASE_DIR = Path(__file__).parent.resolve()

# ========= CHRIS (NORTH) =========
SCENES_FILE_CHRIS = BASE_DIR / "static" / "data" / "scenes_chris.json"


def _load_chris():
    with SCENES_FILE_CHRIS.open(encoding="utf-8") as f:
        raw = json.load(f)
    return {str(s["scene_id"]).strip(): s for s in raw}


try:
    CHRIS = _load_chris()
except FileNotFoundError:
    CHRIS = {}


def get_chris(scene_id: str) -> dict:
    key = str(scene_id).strip()
    try:
        return CHRIS[key]
    except KeyError:
        abort(404, f"Scene {key} not found")


# ========= TRAVIS (EAST) =========
SCENES_FILE_TRAVIS = BASE_DIR / "static" / "data" / "scenes_travis.json"


def _load_travis():
    with SCENES_FILE_TRAVIS.open(encoding="utf-8") as f:
        raw = json.load(f)
    return {str(s["scene_id"]).strip(): s for s in raw}


try:
    TRAVIS = _load_travis()
except FileNotFoundError:
    TRAVIS = {}


def get_travis(scene_id: str) -> dict:
    key = str(scene_id).strip()
    try:
        return TRAVIS[key]
    except KeyError:
        abort(404, f"Scene {key} not found")


# ========= CHARLIE (SOUTH) =========
SCENES_FILE_CHARLIE = BASE_DIR / "static" / "data" / "scenes_charlie.json"


def _load_charlie():
    with SCENES_FILE_CHARLIE.open(encoding="utf-8") as f:
        raw = json.load(f)
    return {str(s["scene_id"]).strip(): s for s in raw}


try:
    CHARLIE = _load_charlie()
except FileNotFoundError:
    CHARLIE = {}


def get_charlie(scene_id: str) -> dict:
    key = str(scene_id).strip()
    try:
        return CHARLIE[key]
    except KeyError:
        abort(404, f"Scene {key} not found")


# ========= TREY (WEST) =========
SCENES_FILE_TREY = BASE_DIR / "static" / "data" / "scenes_trey.json"


def _load_trey():
    with SCENES_FILE_TREY.open(encoding="utf-8") as f:
        raw = json.load(f)
    return {str(s["scene_id"]).strip(): s for s in raw}


try:
    TREY = _load_trey()
except FileNotFoundError:
    TREY = {}


def get_trey(scene_id: str) -> dict:
    key = str(scene_id).strip()
    try:
        return TREY[key]
    except KeyError:
        abort(404, f"Scene {key} not found")


# --- Crossroads ---
@app.get("/")
def home():
    create_player()
    reset_visited()
    reset_history_and_vars()
    return render_template("home.html", title="The Crossroads", theme="crossroads")


# Keep compass routes, but drive them into each owner’s story
@app.get("/north")
def north_path():
    return redirect(url_for("chris_start"))


@app.get("/east")
def east_path():
    return redirect(url_for("travis_start"))


@app.get("/south")
def south_path():
    return redirect(url_for("charlie_start"))


@app.get("/west")
def west_path():
    return redirect(url_for("trey_start"))


# --- Chris dynamic routes ---
@app.get("/chris")
def chris_start():
    return redirect(url_for("scene_chris", scene_id="N-001"))


@app.get("/chris/<scene_id>")
def scene_chris(scene_id):
    scene = get_chris(scene_id)
    if compute_display_choices:
        scene = dict(scene)
        scene['choices'] = compute_display_choices(scene, session.get('player', {}))
    return render_template("scene.html", scene=scene, title=scene.get("title"),
                           theme="chris", base_endpoint="scene_chris")


# --- Travis dynamic routes ---
@app.get("/travis")
def travis_start():
    return redirect(url_for("scene_travis", scene_id="E-001"))


@app.get("/travis/<scene_id>")
def scene_travis(scene_id):
    scene = get_travis(scene_id)
    if compute_display_choices:
        scene = dict(scene)
        scene['choices'] = compute_display_choices(scene, session.get('player', {}))
    return render_template("scene.html", scene=scene, title=scene.get("title"),
                           theme="travis", base_endpoint="scene_travis")


# --- Charlie dynamic routes ---
@app.get("/charlie")
def charlie_start():
    return redirect(url_for("scene_charlie", scene_id="S-001"))


@app.get("/charlie/<scene_id>")
def scene_charlie(scene_id):
    scene = get_charlie(scene_id)
    if compute_display_choices:
        scene = dict(scene)
        scene['choices'] = compute_display_choices(scene, session.get('player', {}))
    return render_template("scene.html", scene=scene, title=scene.get("title"),
                           theme="charlie", base_endpoint="scene_charlie")


# --- Trey dynamic routes ---
@app.get("/trey")
def trey_start():
    return redirect(url_for("scene_trey", scene_id="W-001"))


@app.get("/trey/<scene_id>")
def scene_trey(scene_id):
    scene = get_trey(scene_id)
    if compute_display_choices:
        scene = dict(scene)
        scene['choices'] = compute_display_choices(scene, session.get('player', {}))
    return render_template("scene.html", scene=scene, title=scene.get("title"),
                           theme="trey", base_endpoint="scene_trey")


# ========= ORACLE (AI) =========
SCENES_FILE_ORACLE = BASE_DIR / "static" / "data" / "scenes_oracle.json"


def _load_oracle():
    with SCENES_FILE_ORACLE.open(encoding="utf-8") as f:
        raw = json.load(f)
    return {str(s["scene_id"]).strip(): s for s in raw}


try:
    ORACLE = _load_oracle()
except FileNotFoundError:
    ORACLE = {}


def get_oracle(scene_id: str) -> dict:
    key = str(scene_id).strip()
    try:
        return ORACLE[key]
    except KeyError:
        abort(404, f"Scene {key} not found")


# --- Oracle dynamic routes ---
@app.get("/oracle")
def oracle_start():
    return redirect(url_for("scene_oracle", scene_id="O-001"))


@app.get("/oracle/<scene_id>")
def scene_oracle(scene_id):
    scene = get_oracle(scene_id)
    if compute_display_choices:
        scene = dict(scene)
        scene['choices'] = compute_display_choices(scene, session.get('player', {}))
    return render_template(
        "scene.html",
        scene=scene,
        title=scene.get("title"),
        theme="oracle",
        base_endpoint="scene_oracle"
    )


# --- Shared death/end page (defaults to Crossroads theme) --- its a design choice , circle of life and all that :)
@app.get("/death")
def death():
    msg = request.args.get(
        "msg") or "You slip at the last moment and fall to your death. That is the end of your story."
    theme = request.args.get("theme") or "crossroads"
    return render_template("death.html", title="You Died", msg=msg, theme=theme)


@app.get("/the_end")
def the_end():
    theme = request.args.get("theme") or "crossroads"
    msg = request.args.get("msg") or "Thanks for playing!"
    return render_template("the_end.html", title="The End", theme=theme, msg=msg)


@app.template_filter('replace_all_newlines')
def replace_all_newlines(s: str):
    from markupsafe import Markup
    if s is None:
        return ""
    return Markup(str(s).replace('\n', '<br>'))


@app.template_filter('add_player_name')
def add_player_name(s: str):
    if s is None:
        return ""
    name = ((session.get('player')).get('name') or "Player")
    text = str(s)
    for token in ['{{player.name}}', '{{ player.name }}']:
        text = text.replace(token, name)
    return text


@app.context_processor
def _inject_player():
    return {"player": session.get("player", {})}


# --- Set player name (simple form) ---
@app.get("/name")
def name_form():
    create_player()
    name = (session.get('player') or {}).get('name', "")
    return render_template("name.html", title="Set Your Name", theme="crossroads",
                           name=name)


@app.post("/name")
def name_submit():
    create_player()
    new_name = (request.form.get("player_name") or "").strip()
    p = session.get('player', {})
    p['name'] = new_name
    session['player'] = p
    next_url = request.args.get('next') or url_for('home')
    return redirect(next_url)


# --- Save/Load Game Functionality ---
@app.route("/save_load")
def save_load_page():
    """Displays the save and load game page."""
    save_slots = session.get('save_slots', {})

    # Determine the correct "Back to Game" URL
    player = current_player()
    back_url = url_for('home')  # Default fallback
    if player.get('history'):
        # Find the last URL that was an actual game scene, not a utility page
        for url in reversed(player.get('history', [])):
            if any(path in url for path in
                   ['/chris/', '/travis/', '/charlie/', '/trey/', '/oracle/']):
                back_url = url
                break

    return render_template(
        "save_load.html",
        title="Save / Load Game",
        theme="crossroads",
        save_slots=save_slots,
        back_url=back_url
    )


@app.route("/save", methods=["POST"])
def save_game():
    """Saves the current game state to a specified slot."""
    slot_id = request.form.get("slot_id")
    if not slot_id:
        return redirect(url_for("save_load_page"))

    save_slots = session.get('save_slots', {})
    player_data = current_player()

    # Find the last actual game scene URL from history to save
    last_game_url = url_for('home')  # Default if no game scenes are found
    if player_data.get('history'):
        for url in reversed(player_data.get('history', [])):
            if any(path in url for path in
                   ['/chris/', '/travis/', '/charlie/', '/trey/', '/oracle/']):
                last_game_url = url
                break

    # Store the player data, the URL to return to, and a timestamp
    save_slots[slot_id] = {
        "player_data": player_data,
        "last_url": last_game_url,
        "save_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    session['save_slots'] = save_slots
    session.modified = True  # Explicitly mark session as modified
    return redirect(url_for("save_load_page"))


@app.route("/load", methods=["POST"])
def load_game():
    """Loads a game state from a specified slot."""
    slot_id = request.form.get("slot_id")
    save_slots = session.get('save_slots', {})

    if slot_id in save_slots:
        save_data = save_slots[slot_id]
        session['player'] = save_data['player_data']
        session.modified = True
        # Redirect the user to their last saved scene
        return redirect(save_data['last_url'])

    return redirect(url_for("save_load_page"))


@app.route("/delete_save", methods=["POST"])
def delete_save():
    """Deletes a save file from a specified slot."""
    slot_id = request.form.get("slot_id")
    save_slots = session.get('save_slots', {})

    if slot_id in save_slots:
        save_slots.pop(slot_id, None)
        session['save_slots'] = save_slots
        session.modified = True

    return redirect(url_for("save_load_page"))


@app.get("/debug/player")
def debug_player():
    return jsonify(current_player())


@app.get("/debug/reset")
def debug_reset():
    session.pop('player', None)
    return redirect(url_for("home"))


@app.before_request
def _init_and_track_player():
    create_player()
    add_history(request.path, limit=200)
    mark_scene_seen()


# --- Main entry ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

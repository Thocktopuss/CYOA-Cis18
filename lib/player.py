

from flask import session, request


def create_player():
    if 'player' not in session:
        session['player'] = {
            'name': "",
            'visited_scenes': [],
            'vars': {},
            'history': [],
        }


def add_history(path: str, limit: int = 200):
    if path is None:
        return
    path = str(path).strip()
    if path == "":
        return
    if path.startswith('/static'):
        return

    p = session.get('player', {})
    history = list(p.get('history', []))

    if not history or history[-1] != path:
        history.append(path)

    if isinstance(limit, int) and limit > 0:
        history = history[-limit:]
    p['history'] = history
    session['player'] = p


def mark_scene_seen():
    endpoint = request.endpoint
    if endpoint is None:
        return
    is_scene = endpoint.startswith('scene_')
    if not is_scene:
        return
    view_args = request.view_args or {}
    scene_id = view_args.get('scene_id')
    if scene_id is None:
        return
    scene_id = str(scene_id)
    if scene_id == "":
        return

    p = session.get('player', {})
    seen = list(p.get('visited_scenes', []))
    if scene_id in seen:
        return
    seen.append(scene_id)
    p['visited_scenes'] = seen
    session['player'] = p


def set_var(key: str, value):
    p = session.get('player', {})
    vars_ = dict(p.get('vars', {}))
    vars_[key] = value
    p['vars'] = vars_
    session['player'] = p


def get_var(key: str, default=None):
    p = session.get('player', {})
    return (p.get('vars', {}) or {}).get(key, default)


def current_player():
    return session.get('player', {})


def reset_visited():
    p = session.get('player', {})
    p['visited_scenes'] = []
    session['player'] = p


def reset_history_and_vars():
    p = session.get('player', {})
    p['history'] = []
    p['vars'] = {}
    session['player'] = p

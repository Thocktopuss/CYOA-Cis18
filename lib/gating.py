
def make_list(value):
    if not value:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(x).strip() for x in value]
    return [str(value).strip()]


def has_all(container, things):
    for t in things:
        if t not in container:
            return False
    return True


def has_any(container, things):
    for t in things:
        if t in container:
            return True
    return False


def eval_when(player, when) -> bool:
    if not when:
        return True

    visited = list((player or {}).get('visited_scenes') or [])

    need_all = make_list(when.get('visited_all'))
    if need_all and not has_all(visited, need_all):
        return False

    need_any = make_list(when.get('visited_any'))
    if need_any and not has_any(visited, need_any):
        return False

    return True

def compute_display_choices(scene, player):
    base = list(scene.get('choices') or [])
    gated = list(scene.get('gated_choices') or [])

    for gc in gated:
        if eval_when(player, gc.get('when', {})):
            choice = {k: v for k, v in gc.items() if k in {'label', 'next_id', 'variant', 'color', 'death_text'}}
            if 'label' in choice and 'next_id' in choice:
                base.append(choice)
    return base

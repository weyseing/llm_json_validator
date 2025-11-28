from typing import Any, Dict, List, Tuple

def validate_tool_call(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    clean: Dict[str, Any] = {}
    errors: List[str] = []

    # action
    action_raw = payload.get("action")
    if not isinstance(action_raw, str):
        errors.append("Missing or invalid 'action' (must be string)")
        return {}, errors
    action = action_raw.strip()
    if action not in ("search", "answer"):
        errors.append(f"Invalid action: {action!r}")
        return {}, errors
    clean["action"] = action

    # q
    if action == "search":
        q_raw = payload.get("q")
        if q_raw is None:
            errors.append("Missing 'q' when action='search'")
            return {}, errors
        q = str(q_raw).strip()
        if not q:
            errors.append("'q' is empty after trimming")
            return {}, errors
        clean["q"] = q

    # k
    k = 3
    if (k_raw := payload.get("k")) is not None:
        try:
            if isinstance(k_raw, bool):
                raise ValueError("boolean")
            k_int = int(k_raw) if isinstance(k_raw, (int, float)) else int(str(k_raw).strip())
            if not (1 <= k_int <= 5):
                raise ValueError("out of range")
            k = k_int
        except Exception:
            errors.append(f"Invalid 'k'={k_raw!r} → using default 3")
    clean["k"] = k

    # remove unknown keys
    for key in payload.keys():
        if key not in {"action", "q", "k"}:
            errors.append(f"Removed unknown key: {key!r}")

    return clean, errors
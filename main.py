from typing import Any, Dict, List, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import json

console = Console()

# json validator
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
    k_val = payload.get("k")
    k = 3   # default

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

    # remoce unknown keys
    for key in payload.keys():
        if key not in {"action", "q", "k"}:
            errors.append(f"Removed unknown key: {key!r}")

    return clean, errors

# test cases
test_cases = [
    {"action": "search", "q": "  capital of Japan  ", "k": "5", "model": "gpt-4"},
    {"action": "answer", "q": "ignore this", "k": 2},
    {"action": "search", "q": "", "k": 3},
    {"action": "search"},
    {"action": "blah"},
    {"action": "search", "q": 12345, "k": "three"},
    {"action": "answer", "k": "10"},
    {"action": "search", "q": "hello", "k": 999},
    {"action": "search", "q": "   ", "k": None},
    {"action": "answer"},
    {"action": "search", "q": "test", "k": True},
    {"action": "search", "q": "test", "k": 3.14},
    {"action": "search", "q": "test", "extra": [1,2,3]},
    {"action": "answer", "q": "should be ignored"},
    {"k": 4},
    {"action": "search", "q": "\t\nvalid query\t"},
    {"action": "search", "q": "valid", "k": "2"},
    {"action": "search", "q": "valid", "k": 0},
    {"action": "search", "q": "valid", "k": 6},
    {},
]

# run demo
def run_demo():
    # panel
    console.print(Panel(
        "[bold magenta]LLM Tool-Call JSON Validator Demo[/]\n"
        "[cyan]Handles real LLM garbage → clean, safe output[/]",
        style="bold blue", expand=False
    ))

    # raw table
    table = Table(title="20 Real-World Test Cases", box=box.ROUNDED, show_lines=True)
    table.add_column("#", width=3)
    table.add_column("Input (truncated)", width=50)
    table.add_column("Clean Output", style="green")
    table.add_column("Errors / Warnings", style="red")

    # test cases
    for i, payload in enumerate(test_cases, 1):
        clean, errors = validate_tool_call(payload)

        # input display
        input_trunc = json.dumps(payload, ensure_ascii=False)
        if len(input_trunc) > 70:
            input_trunc = input_trunc[:67] + "..."

        # output display
        clean_str = json.dumps(clean, ensure_ascii=False) if clean else "[red]{}[/]"
        err_str = "\n".join(f"• {e}" for e in errors) if errors else "[green]None[/]"

        table.add_row(str(i), input_trunc, clean_str, err_str)

    console.print(table)
    console.print("[bold green]Demo finished — ready for questions! [/]")


if __name__ == "__main__":
    run_demo()
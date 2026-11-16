"""PreToolUse hook: zakáže síťové příkazy mimo povolené domény."""
import json, re, sys

POVOLENE = r"severka-it\.example|microsoft\.com"
call = json.load(sys.stdin)
cmd = call.get("tool_input", {}).get("command", "")
if re.search(r"\b(curl|wget|nc)\b", cmd) and not re.search(POVOLENE, cmd):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason":
            "Odeslání mimo povolené domény. Popiš člověku, co potřebuješ.",
    }}))
sys.exit(0)

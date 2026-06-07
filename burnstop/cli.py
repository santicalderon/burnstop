"""CLI entry — `receipt run --budget 5 -- python my_agent.py`"""
from __future__ import annotations
import argparse, os, subprocess, sys
from . import __version__, Receipt


def cmd_demo(args):
    """Run a built-in runaway demo proving the gate fires."""
    r = Receipt(budget_envelope_usd=args.budget, model="claude-3-5-sonnet")
    from .proxy import BudgetExceeded
    step = 0
    while True:
        step += 1
        try:
            r.check(input_tokens=4500, max_output=2048)
        except BudgetExceeded as e:
            print(f"\n[demo] gate fired at step {step}: {e}", file=sys.stderr)
            return 0
        # simulate the call landing — pretend 4500 in / 2000 out
        r.record(actual_response_body={"usage": {
            "input_tokens": 4500, "output_tokens": 2000,
            "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0
        }})
        if step > 100: return 0


def cmd_status(args):
    """Show ledger summary."""
    import json
    path = os.path.expanduser(args.ledger)
    if not os.path.exists(path):
        print("no ledger yet"); return 0
    total = 0.0; calls = 0
    for line in open(path):
        try:
            r = json.loads(line)
            total += r.get("actual_usd", 0); calls += 1
        except Exception: pass
    print(f"ledger: {path}")
    print(f"calls: {calls}")
    print(f"total_spent_usd: ${total:.4f}")


def main():
    ap = argparse.ArgumentParser(prog="burnstop", description="pre-flight budget gate for AI agents")
    ap.add_argument("--version", action="version", version=f"burnstop {__version__}")
    sub = ap.add_subparsers(dest="cmd")

    p_demo = sub.add_parser("demo", help="run a built-in runaway-loop demo")
    p_demo.add_argument("--budget", type=float, default=1.00)
    p_demo.set_defaults(func=cmd_demo)

    p_status = sub.add_parser("status", help="show ledger summary")
    p_status.add_argument("--ledger", default="~/.burnstop_ledger.jsonl")
    p_status.set_defaults(func=cmd_status)

    args = ap.parse_args()
    if not args.cmd: ap.print_help(); return 1
    return args.func(args) or 0


if __name__ == "__main__":
    raise SystemExit(main())

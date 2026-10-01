"""Entry point for IDIAH DANIEL DAVID's Nova interpreter."""

import sys

def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: python main.py <file.nova>")
        return 1
    path = argv[0]
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    print("Running Nova interpreter (not yet implemented)")
    print(src)

if __name__ == "__main__":
    raise SystemExit(main())

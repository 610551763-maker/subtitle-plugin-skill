from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


DEFAULT_PROJECT_ROOT = Path(
    r"C:\Users\Administrator\Documents\Codex\2026-06-16\files-mentioned-by-the-user-codex\script_forced_aligner"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import a verified final SRT into DaVinci Resolve Media Pool.")
    parser.add_argument("srt_path", help="Absolute path to the verified final SRT")
    parser.add_argument("--expected-count", type=int, default=None, help="Expected SRT subtitle count")
    parser.add_argument("--project-root", default=str(DEFAULT_PROJECT_ROOT), help="Subtitle plugin project root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    sys.path.insert(0, str(project_root))
    try:
        from src.resolve_integration import ResolveIntegrationError, import_srt_to_resolve_media_pool

        result = import_srt_to_resolve_media_pool(
            args.srt_path,
            expected_subtitle_count=args.expected_count,
        )
    except (ImportError, OSError, ValueError, ResolveIntegrationError) as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps(result.to_dict(), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


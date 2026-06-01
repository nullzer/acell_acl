from __future__ import annotations

import argparse

from acell_acl.model import AppState, WorkMode, get_mode_status, set_work_mode


def main() -> None:
    parser = argparse.ArgumentParser(description="Acell ACL local desktop application.")
    parser.add_argument("--check", action="store_true", help="Run a non-GUI smoke check and exit.")
    args = parser.parse_args()

    if args.check:
        status = get_mode_status(set_work_mode(AppState(), WorkMode.LOCAL))
        print(f"{status.title}: {status.details}")
        return

    from acell_acl.ui import run

    run()


if __name__ == "__main__":
    main()

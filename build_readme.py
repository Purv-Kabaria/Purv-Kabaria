"""Refresh the live competitive-programming ratings in README.md.

Run daily by .github/workflows/build.yml (pattern borrowed from simonw/simonw).
Each section sits between <!-- name starts --> and <!-- name ends --> markers.
If a source is down, that section keeps its previous content instead of
emptying, so a flaky API can never blank the profile.

Standard library only.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"
CF_HANDLE = "OldmanGalaxy"
CC_HANDLE = "oldmangalaxy"
LC_HANDLE = "oldmangalaxy"
UA = {"User-Agent": "purv-kabaria-profile-readme"}


def fetch(url: str, data: bytes | None = None, headers: dict | None = None) -> bytes:
    req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()




def clean(text: str) -> str:
    """Make an external string safe to drop into Markdown inside an auto-committed README.

    Removes comment markers (which could break the section markers), HTML angle
    brackets, and Markdown link/image syntax, and collapses whitespace.
    """
    text = text.replace("<!--", "").replace("-->", "")
    text = re.sub(r"[<>\[\]()`!\\|*_]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def replace_section(text: str, name: str, body: str) -> str:
    start, end = f"<!-- {name} starts -->", f"<!-- {name} ends -->"
    i = text.find(start)
    j = text.find(end, i + len(start)) if i != -1 else -1
    if i == -1 or j == -1:
        raise ValueError(f"marker {name} missing from README")
    return text[: i + len(start)] + f"\n{body}\n" + text[j:]


# ── sections ─────────────────────────────────────────────────────────────────

def codeforces() -> str:
    r = json.loads(fetch(f"https://codeforces.com/api/user.info?handles={CF_HANDLE}"))["result"][0]
    return f"[Codeforces](https://codeforces.com/profile/{CF_HANDLE}): **{int(r['rating'])}**, {clean(r['rank']).title()} (max {int(r['maxRating'])})"


def codechef() -> str:
    html = fetch(f"https://www.codechef.com/users/{CC_HANDLE}").decode("utf-8", "ignore")
    ratings = [int(x) for x in re.findall(r'"rating":"?(\d+)', html)]
    if not ratings:
        raise RuntimeError("no CodeChef rating on page")
    current, best = ratings[-1], max(ratings)
    stars = 1 if current < 1400 else 2 if current < 1600 else 3 if current < 1800 else 4 if current < 2000 else 5 if current < 2200 else 6 if current < 2500 else 7
    return f"[CodeChef](https://www.codechef.com/users/{CC_HANDLE}): **{current}**, {stars}★ (max {best})"


def leetcode() -> str:
    q = {"query": f'{{userContestRanking(username:"{LC_HANDLE}"){{rating}} matchedUser(username:"{LC_HANDLE}"){{submitStats{{acSubmissionNum{{difficulty count}}}}}}}}'}
    d = json.loads(fetch("https://leetcode.com/graphql", json.dumps(q).encode(), {"Content-Type": "application/json", "Referer": "https://leetcode.com"}))["data"]
    solved = next(x["count"] for x in d["matchedUser"]["submitStats"]["acSubmissionNum"] if x["difficulty"] == "All")
    return f"[LeetCode](https://leetcode.com/u/{LC_HANDLE}/): **{round(float(d['userContestRanking']['rating']))}**, {int(solved)} solved"


def competitive(previous: str) -> str:
    """One line per platform; a platform that fails keeps its previous line."""
    old = {line.split("]")[0].lstrip("["): line for line in previous.strip().splitlines() if line.startswith("[")}
    out = []
    for name, fn in (("Codeforces", codeforces), ("CodeChef", codechef), ("LeetCode", leetcode)):
        try:
            out.append(fn())
        except Exception as e:  # noqa: BLE001
            print(f"[{name}] kept previous value: {e}", file=sys.stderr)
            if name in old:
                out.append(old[name])
    return "\n\n".join(out)


def current_section(text: str, name: str) -> str:
    m = re.search(rf"<!-- {name} starts -->(.*?)<!-- {name} ends -->", text, re.S)
    return m.group(1) if m else ""


def main() -> None:
    text = README.read_text(encoding="utf-8")
    builders = {
        "competitive": lambda: competitive(current_section(text, "competitive")),
    }
    for name, build in builders.items():
        try:
            text = replace_section(text, name, build())
        except Exception as e:  # noqa: BLE001
            print(f"[{name}] unchanged: {e}", file=sys.stderr)
    README.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()

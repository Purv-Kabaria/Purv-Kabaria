"""Rebuild the live sections of README.md.

Run daily by .github/workflows/build.yml (pattern borrowed from simonw/simonw).
Each section sits between <!-- name starts --> and <!-- name ends --> markers.
If a source is down, that section keeps its previous content instead of
emptying, so a flaky API can never blank the profile.

Standard library only.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"
GH_USER = "Purv-Kabaria"
SKIP_REPOS = {"Purv-Kabaria"}  # the profile repo commits to itself daily
DISPLAY_NAMES = {"Odoo-2026": "AssetFlow"}  # repo name -> project name people know it by
FEED = "https://purvkabaria.netlify.app/blog/rss.xml"
CF_HANDLE = "OldmanGalaxy"
CC_HANDLE = "oldmangalaxy"
LC_HANDLE = "oldmangalaxy"
UA = {"User-Agent": "purv-kabaria-profile-readme"}


def fetch(url: str, data: bytes | None = None, headers: dict | None = None) -> bytes:
    req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def replace_section(text: str, name: str, body: str) -> str:
    pattern = re.compile(rf"(<!-- {name} starts -->)(.*?)(<!-- {name} ends -->)", re.S)
    if not pattern.search(text):
        raise ValueError(f"marker {name} missing from README")
    return pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", text)


# ── sections ─────────────────────────────────────────────────────────────────

def shorten(text: str, limit: int = 72) -> str:
    """Cut at a word boundary so a long commit subject never ends mid-word."""
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",:;") + "…"


def _gh(path: str):
    headers = {"Accept": "application/vnd.github+json"}
    if os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    return json.loads(fetch(f"https://api.github.com{path}", headers=headers))


def recent_work(limit: int = 5) -> str:
    """Latest commit by me on each of my most recently pushed public repos.

    (The events API stopped carrying commit messages in push events, so this asks
    each repo for its newest commit instead.)
    """
    repos = _gh(f"/users/{GH_USER}/repos?sort=pushed&per_page=20&type=owner")
    lines = []
    for repo in repos:
        if repo["name"] in SKIP_REPOS or repo.get("fork") or repo.get("private"):
            continue
        commits = _gh(f"/repos/{GH_USER}/{repo['name']}/commits?per_page=1&author={GH_USER}")
        if not commits:
            continue
        c = commits[0]["commit"]
        msg = shorten(c["message"].splitlines()[0])
        day = c["author"]["date"][:10]
        name = DISPLAY_NAMES.get(repo["name"], repo["name"])
        lines.append(f"[{name}]({repo['html_url']}): {msg} - {day}")
        if len(lines) == limit:
            break
    if not lines:
        raise RuntimeError("no recent commits found")
    return "\n\n".join(lines)


def writing(limit: int = 5) -> str:
    # The feed is my own static site. ElementTree never resolves external entities,
    # and the expat bundled with Python 3.12 (used by the workflow) caps entity
    # expansion, so defusedxml would add a dependency for no real protection here.
    root = ET.fromstring(fetch(FEED))
    lines = []
    for item in root.iter("item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        date = datetime.strptime(item.findtext("pubDate", "").strip(), "%a, %d %b %Y %H:%M:%S %Z").date()
        lines.append(f"[{title}]({link}) - {date.isoformat()}")
        if len(lines) == limit:
            break
    if not lines:
        raise RuntimeError("feed has no items")
    return "\n\n".join(lines)


def codeforces() -> str:
    r = json.loads(fetch(f"https://codeforces.com/api/user.info?handles={CF_HANDLE}"))["result"][0]
    return f"[Codeforces](https://codeforces.com/profile/{CF_HANDLE}): **{r['rating']}**, {r['rank'].title()} (max {r['maxRating']})"


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
    return f"[LeetCode](https://leetcode.com/u/{LC_HANDLE}/): **{round(d['userContestRanking']['rating'])}**, {solved} solved"


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
        "recent_work": recent_work,
        "writing": writing,
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

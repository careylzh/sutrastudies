#!/usr/bin/env python3
"""Daily digest of hopeful news, delivered to Telegram.

Standard library only. Pulls RSS/Atom feeds listed in feeds.json, keeps recent
items that look constructive, and sends a digest with a Singapore section and a
world section.

Environment:
  TELEGRAM_BOT_TOKEN  bot token from @BotFather
  TELEGRAM_CHAT_ID    your chat id (or a channel @handle)

Usage:
  python3 goodnews.py --dry-run          # print the digest, send nothing
  python3 goodnews.py --state sent.json  # send, remembering what was sent
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
USER_AGENT = "Mozilla/5.0 (compatible; goodnews-telegram-bot/1.0)"

# Words that signal a story is about harm. Any hit drops the item, even from a
# curated outlet, so the digest never surprises you with grim news.
NEGATIVE = [
    "kill", "killed", "killing", "dead", "death", "dies", "died", "murder",
    "war", "wars", "attack", "bomb", "shooting", "shot", "stabbed", "terror",
    "injured", "injury", "injuries", "crash", "collision", "accident", "fire",
    "blaze", "flood", "earthquake", "scandal", "fraud", "scam", "scammer",
    "arrested", "arrest", "jailed", "jail", "charged", "court", "sentenced",
    "guilty", "convicted", "lawsuit", "sued", "abuse", "assault", "molest",
    "rape", "victim", "victims", "suicide", "overdose", "drugs", "trafficking",
    "corruption", "bribery", "layoffs", "retrench", "recession", "crisis",
    "outbreak", "hostage", "missile", "sanctions", "protest", "riot",
    "missing", "fined", "fine", "probe", "investigation", "police", "crime",
    "gunman", "violence", "violent", "tragedy", "tragic", "disaster", "lost",
]

# Words that suggest uplift. Non-curated feeds need at least one.
POSITIVE = [
    "breakthrough", "first", "record", "restored", "restore", "rescued",
    "rescue", "recovered", "recovery", "volunteer", "volunteers", "donate",
    "donates", "donated", "donation", "charity", "kindness", "kind",
    "heartwarming", "inspiring", "celebrate", "celebrates", "award",
    "awarded", "wins", "won", "milestone", "discover", "discovered",
    "discovery", "innovation", "innovative", "cure", "vaccine", "renewable",
    "solar", "clean energy", "conservation", "rewild", "habitat", "species",
    "planted", "trees", "reef", "community", "help", "helps", "helping",
    "free", "scholarship", "graduates", "reunited", "hope", "hopeful",
    "improve", "improves", "improved", "boost", "launch", "launches",
    "opens", "new park", "garden", "researchers", "scientists", "develop",
    "developed", "invent", "invented", "success", "successful", "gift",
    "thank", "grateful", "hero", "joy", "smile", "uplifting", "pioneering",
    "accessible", "inclusive", "elderly", "seniors", "students", "youth",
]


@dataclass
class Item:
    title: str
    link: str
    source: str
    region: str
    curated: bool
    published: datetime | None
    summary: str = ""


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z][a-z'*-]*", text.lower()))


def _hits(text: str, vocab: list[str]) -> int:
    lowered = text.lower()
    words = _words(text)
    return sum(1 for w in vocab if (w in lowered if " " in w else w in words))


def is_hopeful(item: Item) -> bool:
    text = f"{item.title} {item.summary}"
    if _hits(text, NEGATIVE):
        return False
    return item.curated or _hits(text, POSITIVE) > 0


def score(item: Item) -> int:
    return _hits(f"{item.title} {item.summary}", POSITIVE) + (3 if item.curated else 0)


def _strip_tags(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text or ""))).strip()


def _parse_date(text: str | None) -> datetime | None:
    if not text:
        return None
    text = text.strip()
    try:
        dt = parsedate_to_datetime(text)
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _child_text(node: ET.Element, *names: str) -> str | None:
    for child in node:
        if _local(child.tag) in names and (child.text or "").strip():
            return child.text
    return None


def parse_feed(xml_bytes: bytes, feed: dict) -> list[Item]:
    root = ET.fromstring(xml_bytes)
    items: list[Item] = []
    for node in root.iter():
        kind = _local(node.tag)
        if kind not in ("item", "entry"):
            continue
        title = _strip_tags(_child_text(node, "title") or "")
        link = _child_text(node, "link") or ""
        if not link:  # Atom: <link href="..."/>
            for child in node:
                if _local(child.tag) == "link" and child.get("rel", "alternate") == "alternate":
                    link = child.get("href", "")
                    break
        published = _parse_date(_child_text(node, "pubDate", "published", "updated", "date"))
        summary = _strip_tags(_child_text(node, "description", "summary") or "")[:400]
        if title and link:
            items.append(Item(title, link.strip(), feed["name"], feed["region"],
                              bool(feed.get("curated")), published, summary))
    return items


def fetch(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _key(item: Item) -> str:
    return re.sub(r"[^a-z0-9]", "", item.title.lower())[:80]


def select(items: list[Item], *, now: datetime, hours: float, per_region: int,
           already_sent: set[str]) -> dict[str, list[Item]]:
    cutoff = now - timedelta(hours=hours)
    seen: set[str] = set(already_sent)
    picked: dict[str, list[Item]] = {"sg": [], "world": []}
    candidates = [i for i in items
                  if (i.published is None or i.published >= cutoff) and is_hopeful(i)]
    candidates.sort(key=lambda i: (score(i), i.published or cutoff), reverse=True)
    for item in candidates:
        key = _key(item)
        bucket = picked.setdefault(item.region, [])
        if key in seen or item.link in seen or len(bucket) >= per_region:
            continue
        seen.update({key, item.link})
        bucket.append(item)
    return picked


def format_digest(picked: dict[str, list[Item]], now: datetime) -> str:
    sgt = now.astimezone(timezone(timedelta(hours=8)))
    lines = [f"🌱 <b>Good news for {sgt:%A, %-d %B %Y}</b>", ""]
    sections = [("sg", "🇸🇬 <b>Singapore</b>"), ("world", "🌍 <b>Around the world</b>")]
    for region, heading in sections:
        entries = picked.get(region) or []
        lines.append(heading)
        if not entries:
            lines.append("<i>Nothing new passed the filter today.</i>")
        for item in entries:
            lines.append(f"• <a href=\"{html.escape(item.link, quote=True)}\">"
                         f"{html.escape(item.title)}</a> — <i>{html.escape(item.source)}</i>")
        lines.append("")
    lines.append("<i>Picked automatically by keyword filters, so the odd miss can slip through.</i>")
    return "\n".join(lines)


def send_telegram(token: str, chat_id: str, text: str) -> None:
    data = urllib.parse.urlencode({
        "chat_id": chat_id, "text": text, "parse_mode": "HTML",
        "disable_web_page_preview": "true",
    }).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=data)
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = json.load(resp)
    if not body.get("ok"):
        raise RuntimeError(f"Telegram error: {body}")


def load_state(path: Path | None) -> list[str]:
    """Already-sent keys, oldest first."""
    if not path or not path.exists():
        return []
    try:
        return list(json.loads(path.read_text()).get("sent", []))
    except (ValueError, OSError):
        return []


def save_state(path: Path, sent: list[str], keep: int = 2000) -> None:
    path.write_text(json.dumps({"sent": sent[-keep:]}, indent=0))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--feeds", type=Path, default=HERE / "feeds.json")
    ap.add_argument("--hours", type=float, default=30, help="lookback window")
    ap.add_argument("--per-region", type=int, default=5)
    ap.add_argument("--state", type=Path, help="JSON file of already-sent items")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    feeds = json.loads(args.feeds.read_text())["feeds"]
    items: list[Item] = []
    for feed in feeds:
        try:
            items.extend(parse_feed(fetch(feed["url"]), feed))
        except Exception as exc:  # one broken feed must not sink the digest
            print(f"warn: {feed['name']}: {exc}", file=sys.stderr)

    now = datetime.now(timezone.utc)
    sent = load_state(args.state)
    picked = select(items, now=now, hours=args.hours, per_region=args.per_region,
                    already_sent=set(sent))
    text = format_digest(picked, now)

    if args.dry_run:
        print(text)
        return 0
    token, chat_id = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("error: set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID", file=sys.stderr)
        return 2
    send_telegram(token, chat_id, text)
    if args.state:
        for group in picked.values():
            for item in group:
                sent.extend([_key(item), item.link])
        save_state(args.state, sent)
    print(f"sent {sum(len(g) for g in picked.values())} stories")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Good news Telegram bot

A daily Telegram digest of hopeful news: a **Singapore** section and an
**Around the world** section. It runs on GitHub Actions (no server needed) at
07:13 Singapore time.

Separate from the sutra-study project; it only shares this repository.

## How it picks stories

1. Pulls the RSS/Atom feeds in `feeds.json`: outlets that only publish
   constructive stories (Good News Network, Positive News, Reasons to be
   Cheerful, The Optimist Daily) plus Singapore sources (CNA, The Straits
   Times, Mothership, and Google News searches for Singapore volunteers,
   awards, research breakthroughs and so on).
2. Keeps items from the last 30 hours.
3. Drops anything containing a harm word (crash, war, scam, court, injured…),
   even from the curated outlets.
4. For the general Singapore feeds, keeps only items with at least one uplift
   word (volunteers, breakthrough, award, restored, researchers…).
5. Sends up to 5 per section, best-scoring first, never repeating a story
   (`sent.json` is kept in the Actions cache).

Keyword filtering is crude by design, so the odd dull or off-tone story can
get through. Tune the `NEGATIVE` / `POSITIVE` lists in `goodnews.py` or the
feeds in `feeds.json`.

## Setup (about 5 minutes)

1. In Telegram, message **@BotFather**, send `/newbot`, and copy the token.
2. Send your new bot any message, then open
   `https://api.telegram.org/bot<TOKEN>/getUpdates` and copy
   `result[0].message.chat.id`.
3. In GitHub: **Settings → Secrets and variables → Actions → New repository
   secret**. Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
4. Merge this into `main`: GitHub only runs scheduled workflows from the
   default branch.
5. **Actions → Good news digest → Run workflow** to try it now (tick
   *dry run* to see the digest in the log without sending).

## Local use

```sh
python3 goodnews-bot/goodnews.py --dry-run
TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=... python3 goodnews-bot/goodnews.py
python3 -m unittest discover -s goodnews-bot/tests
```

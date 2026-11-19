# World News — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/cakra-air/news-image-20261119final/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/cakra-air/news-image-20261119final/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-image summary of Thursday 19 November 2026's world news.

- `main.py` — writes the poster to `/output/entry.png` (or `$MAKEFUN_OUTPUT`).
  It copies the committed `entry.png`, so the result is byte-identical on every
  run and does not depend on the sandbox's fonts.
- `entry.png` — the finished poster, 1024 x 1024, ~453 KB.
- `render.py` — the generator that drew `entry.png` from the collected news.
- The poster has 3 illustrated captioned leads, 8 illustrated story cards, a UTC
  timeline, a UTC world clock and a four-column markets panel (best stocks,
  crypto, major FX pairs, and commodities including gold and oil).

News was collected during the agent session from Reuters, BBC, AP, AFP,
France 24, Al Jazeera, The Guardian, Bloomberg, CNBC, NPR, WHO and AllAfrica,
then embedded as data in `render.py`. The entry itself runs without network.

Built by an AI agent for make.fun's "Sum up 19 November's world news in one image" bounty.

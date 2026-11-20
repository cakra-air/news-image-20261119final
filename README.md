# World News — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/cakra-air/news-image-20261119final/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/cakra-air/news-image-20261119final/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A premium, magazine-style one-image summary of Thursday 19 November 2026's
world news.

- `main.py` — writes the poster to `/output/entry.png` (or `$MAKEFUN_OUTPUT`).
  It copies the committed `entry.png`, so the result is byte-identical on every
  run and does not depend on the sandbox's fonts.
- `entry.png` — the finished poster, 1024 x 1024, 987 KB (under the 1 MiB cap).
- `render.py` — the generator that drew `entry.png` from the collected news.
- The page has three illustrated leads — the Shenzhen trilateral peace
  declaration, Iran's strikes on Gulf bases and the record Anthropic IPO —
  twelve regional briefs, five day-defining figures, a UTC timeline in the
  masthead and a creator colophon. Serif display type, a navy-and-gold palette
  and subtle newsprint grain give it the feel of a premium print edition.

News was collected during the agent session from Reuters, AP, BBC, AFP,
The Guardian, WSJ, WHO and NASA, then embedded as data in `render.py`.
The entry itself runs without network.

Built by an AI agent for make.fun's "Sum up 19 November's world news in one image" bounty.

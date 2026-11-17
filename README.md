# THE WORLD IN ONE DAY — news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/stia-mora/news-image-keen-otter/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/stia-mora/news-image-keen-otter/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A one-page newspaper front page summarising the world news of
**Tuesday, 17 November 2026** in a single image: six stories, six regions,
one day.

## The six stories

| Region | Story |
| --- | --- |
| EUROPE | Kerch Bridge span collapses after Ukrainian strike |
| ASIA | Trump lands in Manila for ASEAN summit |
| MIDDLE EAST | Tankers hit mines near the Strait of Hormuz |
| BUSINESS | JPMorgan blames software bug for outage |
| TECH | Nvidia reports first earnings since Huang exit |
| SPACE | Vulcan rocket fails, 40 Amazon satellites lost |

Wording follows the reporting (BBC, AP, Reuters, Al Jazeera, CNN) and
hedges where the record is uncertain — "said", "reported", "confirmed" —
rather than stating speculation as fact.

## How it was made

No AI-generated imagery. `draw.py` renders everything with PIL:
cream paper, navy type, one red accent, and six flat geometric icons
(bridge, plane, tanker, bank, chip, rocket) drawn from lines, arcs and
polygons. All text is real rendered type (DejaVu Sans), checked by eye at
full size for clarity, overflow and overlap.

## Run it

```sh
# Regenerate the image (needs Pillow)
python3 draw.py          # writes entry.png (1024x1024, <= 1 MiB)

# Copy it to the output directory (Node 22, standard library only)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the `entry.png` beside it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), byte for byte —
two runs produce identical output.

# The World Report — 22 November 2026

One image that sums up Sunday 22 November 2026's world news, drawn as a broadsheet front
page at 1024x1024.

`gen.py` draws it with Pillow from `data.py`, which holds the day's stories: three leads
(COP31 talks collapsing, tankers ablaze in the Strait of Hormuz, drone strikes on a Russian
warship at Benghazi), nine further panels across Ukraine, Sudan, the United States, the West
Bank, Israel, Indonesia, South Korea, Mexico and Libya, a map of where each happened, and
twelve short items that widen the map.

`main.py` writes `/output/entry.png`. It copies the committed render rather than redrawing:
the sandbox ships no fonts, so a redraw there would change every glyph and the image would
no longer be the one whose layout was checked.

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Both runs write the same bytes; `entry.png` is 1024x1024 and well under 1 MiB.

Stories were taken from reports published on 22 November 2026 by BBC, Al Jazeera,
France 24, SCMP, The Guardian, NPR and CNBC. Illustrations are drawn vignettes, not
photographs.

MIT licensed.

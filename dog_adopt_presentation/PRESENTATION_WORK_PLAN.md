# Dog adoption presentation — work plan

## Objective

Turn `ความสำเร็จในการรับเลี้ยงสุนัข.pptx` and the analysis in `Untitled5.ipynb` into one self-contained, bilingual (Thai/English), white-and-gold presentation file with interactive charts and tooltips.

## Source material

- `ความสำเร็จในการรับเลี้ยงสุนัข.pptx` — 19 slides defining the narrative order and section labels.
- `Untitled5.ipynb` — exploratory analysis and chart code.
- `../dog_adoption/dog_adoption_master.csv` — 42,000 rows × 32 columns; all chart values are recomputed from this file so the HTML does not depend on screenshots.
- `assets/` and `extracted_charts/` — existing matplotlib exports, kept only as visual references.

## Narrative structure (mirrors the deck)

| # | Slide | Section |
| --- | --- | --- |
| 01 | Cover | — |
| 02 | About the data | Prologue |
| 03 | Correlation matrix | Prologue |
| 04 | Five chapters / agenda | Prologue |
| 05 | 85% / 15% outcome | Overview |
| 06 | Reasons adoptions fail | Overview |
| 07 | Returns happen fast | Overview |
| 08 | Timing by problem type | Overview |
| 09 | Behaviour profile: returned vs retained | Risk by “Dog” |
| 10 | Behaviour problems compound | Risk by “Dog” |
| 11 | Dog size × home type | Risk by “Housing, Matching” |
| 12 | Hours alone | Risk by “Housing, Matching” |
| 13 | Separation anxiety × hours alone | Risk by “Housing, Matching” |
| 14 | Energy mismatch | Risk by “Housing, Matching” |
| 15 | Expectations vs owner experience | Risk by “Adopter” |
| 16 | Training as the antidote (3 facets) | Preparation for “Adopter” |
| 17 | Counselling, experience, meet-and-greet | Preparation for “Adopter” |
| 18 | Meet-and-greet limits by reactivity | Preparation for “Adopter” |
| 19 | Closing / thank you | — |

## Design system

- Palette: warm white `#FBFAF7`, ink `#1C1B19`, gold `#B08D57`, champagne `#E8DCC8`, teal `#2F6F6B`, terracotta `#C05B3E`.
- Type: Cormorant Garamond (display), Inter (body), Noto Sans/Serif Thai for Thai copy.
- Layout: full-viewport slides, generous margins, hairline rules, small-caps eyebrows, editorial serif numerals.
- Motion: restrained fade/slide reveals; charts animate only when their slide becomes active.
- Charts: Apache ECharts (bundled inline for offline use) with custom bilingual tooltips.

## Interaction

- Keyboard arrows / space / Home / End, on-screen arrows, touch swipe.
- Chapter rail + progress bar + slide counter.
- Slide-index overlay for direct navigation.
- Training slide: tabs for aggression / anxiety / reactivity.
- Hover tooltips expose rate, sample size `n`, and, where useful, counts or shares.

## Data integrity rules

- Recompute every figure from `dog_adoption_master.csv`; verify against the deck (15.0% returns, 85.0% success, 6,297 returns).
- Do not use post-outcome fields as predictors in the narrative.
- Timing charts use the raw `days_to_return` values (the notebook’s >40-day replacement creates an artificial spike at day 7). State the 1–45 day display window.
- Insight copy stays descriptive, not causal.

## Build steps

1. Extract slide titles and chart–slide mapping from the PPTX. **Done**
2. Recompute aggregates and chart-ready JSON from the master CSV. **Done**
3. Draft the 19-slide HTML shell and design system. **In progress**
4. Implement each ECharts view with tooltips and responsive resize.
5. Add navigation, transitions, index overlay, and tab interaction.
6. Inline the ECharts bundle and chart data; verify the single-file build offline.
7. Cross-check every number against the deck and notebook; capture the final state in `PRESENTATION_WORK_STATE.md`.

## Deliverable

`dog_adoption_presentation.html` — a single file that opens in any modern browser without a network connection.

## V2 — simplified edition (2026-10-27)

Requested follow-up: **far less text, key data only**, styled like the source PPTX, with a
**language toggle** and **easy-to-read fonts**.

### Differences from V1

| | V1 | V2 |
| --- | --- | --- |
| Copy | Bilingual side-by-side, paragraphs and captions | One language at a time; one headline + one short sub per slide |
| Language | Thai and English shown together | `ไทย / EN` pill in the top bar re-renders every slide and chart |
| Type | Cormorant Garamond + Inter + Noto Sans Thai | IBM Plex Sans Thai only (300–700), no serif |
| Palette | Warm white / gold editorial | White `#FFFFFF`, ink `#141414`, hairline `#E7E4DE`, teal `#2F6F6B`, rust `#C05B3E` |
| Chrome | Chapter rail | Slim top bar, progress line, pager, index overlay |

### Slide pattern

- Eyebrow (section) + headline + optional one-line sub + chart.
- Cover, data, agenda, and closing use a custom layout; every other slide is a single chart.
- No explanatory paragraphs, no separate insight cards — the number is in the headline.

### Interaction

- `ไทย` / `EN` toggle disposes and rebuilds all charts so axis labels, legends, and tooltips
  switch language together.
- Same navigation as V1: arrows / space / Home / End, buttons, hash links, touch swipe,
  index overlay (`i` or the menu button), training tabs on slide 16.
- Tooltips are single-language, chosen by the active language.

### Deliverable

`dog_adoption_presentation_v2.html` — same data and figures as V1, single self-contained file.

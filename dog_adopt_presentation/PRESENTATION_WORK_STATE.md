# Dog adoption presentation — work state

Status: **complete** · finished 2026-10-27
Deliverables:
- `dog_adoption_presentation.html` — 1.18 MB, 19 slides, 15 interactive charts, bilingual copy shown together.
- `dog_adoption_presentation_v2.html` — 1.10 MB, 19 slides, 15 interactive charts, TH/EN toggle, minimal copy.

## V2 — simplified edition

The follow-up deck requested less text, key data only, a language switch, and easy-to-read
fonts. It is a separate file so the original V1 deck is untouched.

### What V2 does

- 19 slides in the same order as the PPTX: cover · data · correlation · agenda · 85/15 ·
  reasons · timing · timing by type · behaviour · burden · size × home · hours alone ·
  anxiety × alone · energy · expectation · training tabs · preparation · meet-and-greet ·
  closing.
- One headline + one short sub-line per slide. Numbers live in the headline (`51.6% returned
  within 7 days`, `Large dogs in apartments: 19.5%`, `Training cuts risk by 15–17 points`).
- `ไทย / EN` pill in the top bar. Switching language re-renders the deck and rebuilds every
  chart, so axis labels, legends, and tooltips change language together.
- IBM Plex Sans Thai only (300/400/500/600/700); no serif or italic.
- White background, ink `#141414`, hairline `#E7E4DE`, teal `#2F6F6B` (stayed / better),
  rust `#C05B3E` (returned / risk), muted `#6E6E6E`.
- Navigation: arrows / space / Home / End, on-screen buttons, hash links (`#01`–`#19`),
  touch swipe, index overlay (`i` or menu button), slide counter, progress line.
- Training slide keeps three tabs (aggression / anxiety / reactivity) with a live delta line.

### V2 chart inventory

| # | Chart | Type |
| --- | --- | --- |
| 03 | Correlation matrix | heatmap |
| 05 | 85 / 15 outcome | donut |
| 06 | Return reasons | horizontal bars |
| 07 | Daily returns + cumulative | bars + line + day-7 marker |
| 08 | Timing density by problem type | density lines |
| 09 | Behaviour, stayed vs returned | dumbbell |
| 10 | Behaviour burden | bars |
| 11 | Size × home | heatmap |
| 12 | Hours alone | bars |
| 13 | Anxiety × hours alone | heatmap |
| 14 | Energy mismatch | bars |
| 15 | Expectation × experience | grouped bars |
| 16 | Trait × training | heatmap, three tabs |
| 17 | Preparation | grouped bars |
| 18 | Meet-and-greet × reactivity | grouped bars |

### V2 verification

- `node --check` passes on the embedded app script.
- Automated DOM test: 19 slides; correct index and hash after next/prev, index jump, and
  language switch; all 15 charts initialise on activation; no JavaScript errors.
- Language toggle checked in both directions on the training slide; tab deltas stay
  `47.1 → 29.6 (−17.5)`, `31.3 → 16.1 (−15.2)`, `31.7 → 16.8 (−14.9)`.
- All 15 tooltips fired in TH and EN; each renders the expected label, rate/count, and `n`.
- No vertical overflow at 1440 × 813, 1440 × 900, 1280 × 800, 1366 × 768, 1024 × 768
  (headless inner heights are ~87 px shorter than the window).
- Screenshots reviewed for all 19 TH slides and EN slides 3, 6, 11, 15, 18, plus the index
  overlay and a live tooltip.
- Index overlay is solid white with no fade transition (headless Chrome freezes CSS
  transitions, and a solid panel reads cleaner on a projector).

### V2 source

- `/tmp/opencode/v2/template.html` — editable CSS/HTML/JS with `/*__ECHARTS__*/` and
  `/*__DATA__*/` placeholders.
- `/tmp/opencode/v2/build.py` — injects `echarts.min.js` and `data.json`, writes the deliverable.
- Rebuild: `python3 /tmp/opencode/v2/build.py`.

## V1 — original bilingual edition

## สรุปสถานะ

งานนำเสนอเสร็จสมบูรณ์ เป็นไฟล์ HTML เดียว เปิดได้ในเบราว์เซอร์สมัยใหม่
เนื้อหาไทย–อังกฤษคู่กันทั้ง 19 สไลด์ กราฟทั้งหมดเป็น ECharts แบบโต้ตอบพร้อม tooltip
ข้อมูลทุกตัวคำนวณใหม่จาก `dog_adoption_master.csv` และตรวจทานกับเดECKต้นฉบับแล้ว

## Completed

- Mapped all 19 PPTX slides and their embedded chart images to the narrative order.
- Recomputed every aggregate from `../dog_adoption/dog_adoption_master.csv` (42,000 × 32).
- Built 15 interactive ECharts views with bilingual tooltips and per-group sample sizes:

  | # | Slide | Chart |
  | --- | --- | --- |
  | 03 | What moves together | 15 × 15 correlation matrix |
  | 05 | One in seven | outcome donut |
  | 06 | Why matches fail | reason bars |
  | 07 | Failure is fast | daily histogram + cumulative line |
  | 08 | Different clocks | timing density by problem type |
  | 09 | Behaviour profile | median dumbbell (stayed vs returned) |
  | 10 | Problems compound | behaviour-burden curve |
  | 11 | Space changes odds | size × home heatmap |
  | 12 | Hours alone | hours-alone curve |
  | 13 | Anxiety × alone | anxiety × hours heatmap |
  | 14 | Quiet mismatch | energy-mismatch curve |
  | 15 | Expectation | expectation × experience bars |
  | 16 | Training | trait × training heatmap, three tabs |
  | 17 | Preparation | preparation bars |
  | 18 | Meet-and-greet | meet × reactivity bars |

- Added the 19-slide shell, keyboard/touch/button navigation, progress bar, chapter rail,
  agenda jumps, slide-index overlay, hash links, and training tabs.
- Inlined the Apache ECharts 5.5.1 bundle and all chart data; three inline scripts total.
- Responsive layout verified at 1440 × 900, 1440 × 813, and 1280 × 800. Below 1024 px the
  two-column layouts collapse and slides scroll vertically.
- Added a compact-height media query so charts, captions, and cards stay above the fixed
  pager on 800–880 px-tall viewports.
- Wrote `PRESENTATION_WORK_PLAN.md` with structure, design system, interaction, and
  data-integrity rules.

## Verification

### Figures (all recomputed from the CSV)

- 42,000 records, 32 columns; 35,703 stayed (85.0%), 6,297 returned (15.0%).
- Return reasons: conflict with resident pets 1,387 · aggression 1,352 · separation
  anxiety/destruction 975 · unmet expectations 750 · housing/landlord 535 · cost/time 512 ·
  medical 316 · allergies 238 · other 232. Top three = 59.0%.
- Timing: median 6.7 days; 29.6% ≤3 days, 51.6% ≤7 days, 69.0% ≤14 days; 637 returns >45 days.
- Behaviour medians (stayed → returned): aggression 2.2 → 3.5, separation anxiety 3.9 → 4.8,
  reactivity 3.3 → 4.2, energy 6.1 → 6.2, training 5.0 → 4.1.
- Behaviour burden: 0 flags 9.2% (n=19,620) · 1 flag 16.5% (15,945) · 2 flags 27.0% (5,562) ·
  3 flags 40.2% (873).
- Size × home: large apartment 19.5%, small owned house 12.1%; ratio 1.6×.
- Hours alone: 11.6% (0–2 h) → 14.0% → 14.3% → 15.2% → 17.5% (8 h+); +5.9 points.
- Anxiety × alone: high anxiety + 8 h+ = 26.3%; low anxiety + 8 h+ = 11.4%; high anxiety +
  0–2 h = 17.0%; low anxiety + 0–2 h = 6.3% (4.2× across extremes).
- Energy mismatch: 11.5% (0–1) → 13.7% → 15.1% → 15.6% → 21.2% (4+); 1.8×.
- Expectation × owner: first-time low 9.4% → medium 15.0% → high 20.9%; experienced
  8.3% → 12.2% → 16.6%.
- Preparation: no counselling 15.9% vs counselling 13.2% (−2.7); first-time 17.6% vs
  experienced 13.4% (−4.2); pets did not meet 15.2% vs met first 14.1% (−1.1).
- Meet-and-greet within pet-owning homes (n=19,224): low 10.7% → 9.0%, medium 17.6% → 15.3%,
  high 26.1% → 26.0%.
- Training (low → high training at high trait): aggression 47.1% → 29.6% (−17.5);
  anxiety 31.3% → 16.1% (−15.2); reactivity 31.7% → 16.8% (−14.9).
- Correlation with returned: aggression +0.23 (strongest positive), training −0.14
  (strongest protective), anxiety +0.14, reactivity +0.13, expectation +0.10,
  energy mismatch +0.095. Structural link: has pets × met resident pets = +0.53.

### Interaction and rendering

- `node --check` passes on the embedded app script.
- Headless-Chrome screenshots reviewed for all 19 slides at 1440 × 900 and 1440 × 813;
  spot-checked 1280 × 800 and 1024 × 768.
- Automated DOM test confirmed:
  - 19 slides, correct active slide and hash after next, rail jump, keyboard jump,
    index jump, and home;
  - every chart canvas initialised when its slide becomes active;
  - all three training tabs switch both chart and insight numbers
    (47.1/29.6/−17.5 → 31.3/16.1/−15.2 → 31.7/16.8/−14.9);
  - no JavaScript errors;
  - no slide content overflowed the viewport at 1440 × 813 after the compact-height rules.
- Tooltips were fired programmatically for all 15 charts; formatters rendered the expected
  bilingual labels, counts, rates, IQRs, and sample sizes.
- Index overlay opens, shows all 19 entries, closes, and navigates correctly.
- `Escape`, `i`, arrows, space, Home/End, and touch swipe are wired.

## Data notes

- Timing views use raw `days_to_return`. The notebook's >40-day median substitution was not
  used because it manufactures a spike at day 7.
- Histogram bins are `[n, n+1)` for days 1–39; the final bin covers 40–45 days. Returns after
  day 45 (637) are excluded from the plotted histogram and disclosed in the caption.
- Headline “by day N” figures use `days_to_return <= N` on raw values. Because days are
  fractional, the cumulative line through the day-7 bin includes returns up to 7.99 days
  (54.8%); the displayed 51.6% is the stricter ≤7.0-day threshold. Both are labelled
  as such in the chart narrative.
- The correlation matrix intentionally leaves the `days_to_return × returned` cell blank:
  the correlation is undefined because only returned dogs have a recorded return day.
- The matrix colour scale is clipped at ±0.25 so weak signals remain visible; values are
  still shown in the tooltip.

## Known limitations

- Web fonts are requested from Google Fonts (V1: Cormorant Garamond, Inter, Noto Sans/Serif
  Thai; V2: IBM Plex Sans Thai). Charts, data, layout, and navigation work offline; without a
  network connection the deck falls back to installed sans/serif fonts. Inlining the font
  files would add several megabytes to the single file.
- At widths below 1024 px the layout intentionally becomes single-column and slides scroll;
  it is designed primarily for laptop/projector viewports (1280 × 800 and above).
- The deck is descriptive, not causal. Copy and captions state this where relevant.

## Files

- `dog_adoption_presentation.html` — V1 deliverable (single file, ECharts inline).
- `dog_adoption_presentation_v2.html` — V2 simplified deliverable (single file, ECharts inline).
- `PRESENTATION_WORK_PLAN.md` — plan, structure, design system, data rules.
- `PRESENTATION_WORK_STATE.md` — this file.
- `../dog_adoption/dog_adoption_master.csv` — source data.
- `/tmp/opencode/build_data.py` — reproducible aggregate generator.
- `/tmp/opencode/data.json` — chart-ready aggregates embedded in both decks.
- `/tmp/opencode/echarts.min.js` — ECharts 5.5.1 bundle embedded in both decks.
- `/tmp/opencode/build.py` — assembles the V1 parts and writes the HTML.
- `/tmp/opencode/parts/` — V1 HTML/CSS/JS source parts.
- `/tmp/opencode/v2/template.html` — V2 source template.
- `/tmp/opencode/v2/build.py` — V2 build script.

No git commit was made for this work.

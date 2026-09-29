# Plumbline: design system

## Design principles

1. **Ground it in the subject.** The product is about *plumb*: whether something still hangs true. Surveyor and drafting vocabulary (sheet, rule, plumb line, chalk line) supplies the identity. Use it structurally, not as costume.
2. **Spend boldness in one place.** The memorable element is the Plumb Graph. Everything around it is quiet, disciplined and legible.
3. **Structure is information.** Rules, borders, numbers and labels appear only when they encode something. Number the six stages, because they are a real sequence. Number nothing else.
4. **Avoid the generic AI-design look.** Not: warm cream + serif + terracotta; near-black + acid accent; newspaper columns + zero radius; identical rounded cards + gradient washes; tracked all-caps eyebrows; monospace labels as decoration; arrows on links; big-number stat trios; fade-and-slide entrance everywhere.
5. **Words are design.** Plain verbs, sentence case, active voice, one name per thing. Errors say what happened and what to do.
6. **Quality floor, unannounced.** Responsive, keyboard-navigable, reduced-motion-safe, AA contrast, harmonious palette.

## Color tokens

Defined as CSS custom properties in `frontend/src/styles/tokens.css`.

| Token | Light "Vellum" | Dark "Lamplight" | Use |
|---|---|---|---|
| `--sheet` | #EEF1F3 | #171E26 | page background |
| `--panel` | #FAFBFB | #1D2630 | raised working areas |
| `--ink` | #1B2127 | #E7ECF0 | primary text |
| `--ink-2` | #46515C | #B6C0CA | secondary text |
| `--ink-3` | #59636E | #97A3AF | captions, tertiary |
| `--rule` | #CBD2D8 | #303B47 | 1px dividers |
| `--rule-strong` | #A9B3BC | #465361 | selected/focused |
| `--plumb` | #2350C8 | #86A8FF | brand, links, focus ring |
| `--holds` | #0F6B4F | #63D3A9 | passing/holds |
| `--drift` | #B93A2B | #FF9082 | drift/failed |
| `--caution` | #8A5F00 | #E5B44E | survived/partial |
| tints | `--*-tint` | translucent variants | status backgrounds |

Status is **never color alone**: always paired with an icon and text label.

## Typography

| Property | Value |
|---|---|
| UI family | Archivo (variable, width axis for headings) |
| Code family | JetBrains Mono (code and diffs only) |
| Scale | 12, 14, 16, 20, 25, 31, 44 px |
| Body | 16px / 1.55 line-height |
| UI text | 14px / 1.4 |
| Headings | 1.15 line-height, -0.01em tracking |
| Numerals | Tabular figures where numbers align |
| Measure | max 68ch |
| Alignment | Left-aligned throughout |

## Space, shape, depth

| Property | Value |
|---|---|
| Base unit | 4px |
| Scale | 4, 8, 12, 16, 24, 32, 48, 72 |
| Control radius | 6px |
| Panel radius | 10px |
| Code radius | 4px |
| Pill radius | 9999px |
| Shadows | Only on popovers/dialogs: `0 8px 24px rgb(27 33 39 / 0.14)` |
| Separation | 1px rules + spacing, not shadows |

## Icons

Lucide, stroke 1.5, at 16px and 20px.

| Status | Icon |
|---|---|
| holds | CheckCircle |
| drift | AlertTriangle |
| caution | MinusCircle |
| running | Loader (ring spinner) |
| pending | Circle (empty) |

## Components

Built on Radix primitives, restyled completely.

### Button
- Variants: primary (--plumb bg, white text), secondary (--rule border, --ink text), quiet (no border, --plumb text)
- Sizes: sm (32px height, 14px text), md (40px height, 14px text)
- States: default, hover, focus-visible (2px --plumb ring, 2px offset), active, disabled (50% opacity), loading (spinner replaces text)
- Touch target: min 44px

### Segmented control
- For depth (Quick/Thorough), diff mode (Unified/Split)
- Selected segment: --panel bg, --plumb border-bottom
- Unselected: transparent bg

### Chip
- Single-select goal chips
- Selected: --plumb-tint bg, --plumb text, --plumb border
- Unselected: --panel bg, --rule border, --ink-2 text
- Fully round radius

### Status pill
- Icon + text label
- Variants mapped to colors: live=--holds, running=--plumb, completed=--holds, failed=--drift, cancelled=--ink-3, replay=--caution
- Small dot or icon + text

### Stage row
- Left rail component
- Number (always shown, 1-6), name, status icon, elapsed time
- Result line shown when stage is completed or running
- Compact vertical list

### Table
- Tabular numerals
- 1px --rule borders
- Header row with --ink-3 text, --sheet bg
- 4px radius

### Code block
- --panel bg, 4px radius
- Line numbers in --ink-3
- JetBrains Mono font
- Copy button (quiet variant)

### Diff viewer
- Unified and split modes
- Added lines: --holds-tint bg
- Removed lines: --drift-tint bg
- Line numbers, wrap toggle
- Hunk badges (P1)

### Skeleton
- --rule bg, pulsing animation
- Shapes: text (multiple lines), block, circle

### Test strength meter
- Horizontal bar with tick marks
- Each tick: caught (filled --holds), survived (outlined --caution), timeout (hatched)
- Not a circular gauge

### Toast
- --panel bg, --shadow-popover shadow
- Icon + message + optional action
- Auto-dismiss after 5s
- Bottom-right position

## Motion

Only:
1. Verdict settle animation (damped spring, 700-900ms), once per run
2. Live status changes (tick landing, stage check appearing)
3. Tab/drawer transitions ≤ 160ms
4. Button press feedback

`prefers-reduced-motion`: all instant state changes, no animation.

## Breakpoints

| Width | Layout |
|---|---|
| ≥1200px | Three panes (rail + graph + panel) |
| 768-1199px | Two panes (top stepper + graph/panel tabs) |
| <768px | Single column (graph becomes candidate list) |

## Accessibility

- WCAG 2.2 AA
- Skip link to main content
- Landmarks: header, nav, main, footer
- `lang="en"` on html
- All form controls labeled
- Errors associated with fields
- Focus ring: 2px --plumb, 2px offset
- Touch targets: min 44px
- `aria-live="polite"` for stage changes and verdict
- No horizontal page scroll
- Usable at 200% zoom
- `forced-colors` mode support

## Copy deck rules

- Sentence case
- Active voice
- One name per thing across the whole flow
- UI vocabulary: "behavior tests" (not "pins"), "planted bugs" (not "mutants"), "test strength", "candidate", "changed behavior", "holds"
- Never: "proven", "guaranteed"
- Always: "on everything we checked", "matches", "held"

# CONTINUITY

Everything a new person (or a future me) needs to pick this up. Written to be
read top to bottom once, then used as reference.

Last updated against `VERSION` 1.1.0.

---

## 1. What this is

Eight gas regulator sizing tools on hollandsupplycompany.com. Each one is a
form on a Concrete CMS page that sizes a USG regulator and returns a model,
capacity, part numbers, capacity tables and a downloadable PDF summary.

They replaced embedded Streamlit apps (iframes pointing at `*.streamlit.app`).
Nothing Streamlit remains in production.

**The algorithms are Python and stay Python.** They are the original engineering
scripts with only the interactive `input()`/`print()` sections removed. They are
compiled to JavaScript by a translator in this repo, and the tests prove the
JavaScript behaves identically. Nobody hand-writes the sizing logic in
JavaScript.

---

## 2. How a sizing gets from Python to a visitor

```
tools/<tool>/algorithm.py        the Python you edit  (source of truth)
      │
      │  build/build.py  →  build/transpile.py
      ▼
dist/usg-<tool>.js               generated bundle, committed to the repo
      │
      │  served by jsDelivr from GitHub, at a pinned commit (section 3)
      ▼
tools/<tool>/block.html          pasted into the Concrete page; loads the
                                 bundle with a <script src> and renders results
```

`tools/<tool>/wrapper.js` sits between the two: it does the unit conversion,
validation, oversize maths and result formatting that the Streamlit front end
used to do, then calls the transpiled algorithm. `tools/<tool>/reference.py` is
its Python twin, and exists purely so the tests can compare the whole pipeline
rather than only the algorithm.

---

## 3. The single most important operational fact

**There are two deployable artefacts and they update by different routes.**
Nearly every "I made the change but nothing happened" moment traces to this.

| What you changed | Where it lives | How it reaches the site |
| --- | --- | --- |
| `algorithm.py`, `wrapper.js` — sizing results, validation messages, unit conversion, **and everything in the PDF's Inputs table** | `dist/usg-*.js`, served by jsDelivr | push, wait for CI, **re-pin the blocks to the new commit**, paste them |
| `block.html` — page markup, styling, PDF layout, page copy, form fields | the pasted block | re-paste the block; instant |

### The blocks load a pinned commit, not `@main`

Each block loads its bundle from a **specific commit**:

```
https://cdn.jsdelivr.net/gh/my-usg/sizingtool@a822d31/dist/usg-<tool>.js
```

They used to load `@main`. That was abandoned after a release where GitHub had
the new bundle, CI was green, the purge links had been opened — and jsDelivr
still served the old bundle for hours, because it caches which commit "main"
points to separately from the files themselves. A commit-pinned address can
never be stale: that commit's files never change. The cost is one edit per
release.

**The release routine**, for anything that changes a bundle:

1. Push, and wait for the Actions run to go green.
2. Take the **newest** commit hash from the repo's commit list (the short
   7-character code). CI may add its own commit after yours, so the commit on
   the Actions page is not always the one to use.
3. Confirm that commit carries the bundles you expect: open
   `https://raw.githubusercontent.com/my-usg/sizingtool/<hash>/dist/usg-all-models.js`
   and check the `sources: 'sha256:…'` value (section 5).
4. Replace the old hash with the new one in the script address of **all eight**
   blocks — every page on one commit keeps the next release a single
   find-and-replace — and paste them.
5. Check the console (below).

**Order matters when a release changes both a block and its bundle.** The
block goes live the moment it is pasted; its bundle only when the pin moves.
Pasted against the old bundle, a new block can be actively wrong — the IRV
default (section 6) made the form send 0, which the old algorithm read as "no
IRV can pass", so every IRV request fell back to a monitor until the bundle
caught up. The same would have happened with the MAIP units, read as psi. So:
push, re-pin, *then* paste.

### Checking what a live page is running

Open its console and enter:

```js
USGSizing.versions
```

Each tool reports two hashes. **`algorithm`** covers `algorithm.py` only;
**`sources`** covers the algorithm, the wrapper and `VERSION`. A wrapper-only
change — a validation message, a unit conversion, a summary line — moves
`sources` and leaves `algorithm` alone, so check `sources` against section 5.

---

## 4. Repository layout

```
tools/<tool>/              one folder per sizing tool, 8 files each
├─ algorithm.py            THE PYTHON YOU EDIT
├─ tool.json                 entry function, injected globals, output name, page
├─ wrapper.js                units, validation, result shaping
├─ reference.py              Python twin of wrapper.js, for the tests
├─ scenarios.json            test inputs: edge_cases, fixtures, fuzz ranges
├─ fixtures.json             expected output - generated, but committed
├─ block.html                the Concrete CMS block for that page
└─ form-map.js               how the browser test drives that form

build/
├─ transpile.py              Python → JavaScript translator
├─ build.py                  builds one tool or all
├─ difftest.py               proves the JavaScript matches the Python
├─ fault_sweep.py            finds inputs an algorithm cannot answer
├─ make_fixtures.py          regenerates expected results
├─ run_js.js                 runs a bundle over a batch of inputs
└─ browser_test.js           drives a block in a headless browser

dist/usg-<tool>.js          generated bundles - PUBLISHED via jsDelivr
.github/workflows/build.yml  build, verify, commit dist, purge the CDN
README.md, DEPLOYING.md, VERSION
```

---

## 5. The eight tools

| Tool | Page | Bundle | `algorithm` | `sources` |
| --- | --- | --- | --- | --- |
| all-models | `/resources/regulator-sizing-tools/general` | `usg-all-models.js` | `5044addece3f` | `e975e0379483` |
| model-046 | `…/model-046` | `usg-model-046.js` | `d929fe2c5c0c` | `6415985e9e0e` |
| model-121 | `…/model-121-122` | `usg-model-121.js` | `1e01c0428b8d` | `dcc9d94c2511` |
| model-143 | `…/model-143` | `usg-model-143.js` | `44b42e7b8685` | `ddccc66697e5` |
| model-243 | `…/model-243` | `usg-model-243.js` | `f82dfa029475` | `e9eafe6b88f6` |
| model-461 | `…/model-441-461` | `usg-model-461.js` | `88ff4f73f9ed` | `0666de818623` |
| model-496 | `…/model-496` | `usg-model-496.js` | `860b588597c6` | `cf51bf643122` |
| model-rpc | `…/model-243-rpc` | `usg-model-rpc.js` | `8bf4279e24d0` | `bc6888fe47aa` |

All eight blocks are pinned to commit **`a822d31`**, which carries exactly these
bundles.

Bundles join a shared `window.USGSizing` namespace rather than replacing it
(`sizeAllModels`, `sizeModel046`, …), so two tools could coexist on one page.

### What differs between them

They look alike but the shapes genuinely differ; do not assume one is a copy of
another.

* **all-models** picks between every model family. No capacity tables. Its
  entry point returns five values. Its copy of `run_regulator_selection461`
  also takes `vp_preference`, supplied as an injected global (the 441/461 tool
  passes it as a function argument instead).
* **model-143, model-496** the simplest: IRV-only protection, a flat set of
  capacity tables, no monitor option.
* **model-046** IRV *or* monitor; tables grouped into labelled sections, and an
  IRV request shows **both** the IRV and Monitor families.
* **model-243** the most conditional tables: which family appears depends on
  outlet pressure and protection type across standard and high-pressure data,
  and an IRV request at ≥2 psi outlet is drawn as monitor tables.
* **model-121** returns **six** values (standard map, V-Port map, 122 map, then
  the selection). Tables list **body size** rather than orifice, drop six
  registers with no V-Port variant, and gate the PDF button on a separate
  `apply121` flag. Has a min-flow field, and a **V-Port preference**
  (`vp_preference`, `"standard"` or `"vport"`) supplied as an injected global —
  the 441/461 tool has the same input but passes it as a function argument.
* **model-461** entry takes the flows as **arguments**; tables come from the
  algorithm's own `build_standard_table()` / `build_vport_table()` with six
  columns including Qmax/Qmin. No pipe-size input. Has a V-Port preference
  input, passed as an argument rather than injected.
* **model-rpc** the only tool with a **model selector** (N/A (any) / 243-RPC /
  -A / -B), passed as `model_input`.

---

## 6. Making a change

### Change how sizing works

1. Edit `tools/<tool>/algorithm.py`.
2. `python3 build/build.py` — fails loudly if the Python uses a construct the
   translator does not support (see section 8).
3. `python3 build/difftest.py <tool>` — must report zero mismatches.
4. `python3 build/fault_sweep.py <tool>` — should report no new faults.
5. `python3 build/make_fixtures.py <tool>` — read the diff. **Intended** changes
   will alter fixtures; confirm the new numbers are right, then commit them.
6. `node build/browser_test.js <tool>`.
7. **Run the full `difftest.py` with no tool named**, not just the tool you
   changed. It compares every tool's Python against the bundle committed in
   `dist/`, so it also catches a change somebody else made and never rebuilt —
   that is how a dropped `data496` column was found.
8. Commit `algorithm.py` **and** `fixtures.json`, push, then follow the release
   routine in section 3.

Two copies of the same logic is the normal state here: all-models carries its
own copy of every family's functions. Change one, change the other, and say
in the commit which ones.

### Change the page, PDF layout or copy

Edit `tools/<tool>/block.html`, run `node build/browser_test.js <tool>`, then
re-paste the block. No push required for the site, but push anyway so GitHub
matches what is live — and **keep the block's existing pin**: a block-only
change does not move the commit its script loads.

jsdom, which the browser test uses, does no layout, so it cannot tell whether
fields line up or a label wraps. For layout work, render the block in headless
Chromium (`pip install playwright` then `playwright install chromium`) at a
desktop, a mid and a phone width, measure element positions, and look at a
screenshot. That caught a broken phone layout and an over-stretched grid that
no test would have.

### What else needs touching

| Change | Also update |
| --- | --- |
| Capacity numbers, thresholds, spring ranges, selection order, part-number format | Nothing |
| A new **output** field (new key in the `match` dict) | `wrapper.js` **and** `reference.py` field lists |
| A new **input** the user supplies | a control in `block.html`, its `buildInput()`, plus `wrapper.js` and `reference.py`; add it to `scenarios.json`'s `random` block |
| Renaming injected globals, the entry signature, or `match` keys | `wrapper.js`, `reference.py`, `tool.json` |

`wrapper.js` and `reference.py` **must change together** — they are compared
field for field, so editing one alone fails the differential test. That is the
point of having both.

### The 121/122, two rules worth knowing

Both live in `will_work_vp()` and `run_regulator_selection121()`, and both exist
in **two copies** — `tools/model-121/` and the 121 section of
`tools/all-models/`. Change one, change the other.

* **A 122 is not offered on a high-efficiency or generator load.**
  `will_work_vp()` returns `"No"` when `pload > 0` and the register starts
  `R122`. It sits in that function rather than in the selection loop so the 122
  capacity table reports "No" for the same reason the body was passed over,
  instead of the row silently disappearing from contention. Note that `pload` is
  the *share* of the load, so ticking the box and leaving the slider at 0 leaves
  the 122 available — the two cannot be told apart from `pload` alone.
* **The V-Port preference decides which valve type is tried first**, and the
  other is tried when the first produces no match, so the preference only
  changes the answer where both would work. One consequence is not obvious:
  `gen_match121()` ignores `result122` entirely on a V-Port pass, because the
  122 has no V-Port variant, so **a V-Port preference effectively removes the
  122 from contention** — every input that selected a 122 under "Standard"
  selected a 121-12 V-Port under "V-Port" in a sweep of the pressure range. If
  the 122 should still win where it fits, the V-Port pass has to consider it.

### Pressures, units and validation

* **Unit conversion lives in the wrapper**, in `toPsi()` (`to_psi()` in
  `reference.py`): bar × 14.5, kPa ÷ 6.89476, in wc ÷ 28, oz ÷ 16. The block
  sends the number and the unit name exactly as typed; the algorithm only ever
  sees psi. Every tool has its own copy, so a factor change is sixteen edits.
* **The MAIP takes psi, bar or kPa**, converted like the inlet. In psi it is
  truncated to a whole number, as it always was; a converted figure keeps its
  decimals, because truncating 8.62 bar (124.99 psi) to 124 would put it below
  an inlet of the same 8.62 bar and fail "MAIP must be >= inlet". The PDF
  summary shows it in the unit entered.
* **Pressure differential.** The general, 441/461 and 046 tools refuse an
  application whose inlet **or** MAIP is more than 600 psi above the outlet:
  "Pressure differential (> 600 psi) too large — consider two pressure cuts."
  Exactly 600 is allowed — checked by brute force over every one- and
  two-decimal pair, in Python and JavaScript, because floating-point
  subtraction can leave a nominal 600 a hair over. The MAIP only counts when
  one is entered. On the general tool the older rule — an outlet under 3 psi
  above a 175 psi inlet — still applies below 600, and only one of the two
  messages is ever shown.

### The IRV pressure limit

* **The form's IRV field starts at 0, meaning "use the default".** The four
  `will_irv_work*()` functions turn 0 into: 2 psi below a 2 psi outlet and 5 psi
  from 2 psi up for the 143, 243 and 496; outlet + 10 psi for the 046. A typed
  value is used as entered. The wrapper and reference defaults are 0 to match.
* **0 also means no cap on a monitor setpoint.** The old default of 2 capped
  monitor setpoints *below* outlets above 2 psi — a 243 at a 3 psi outlet got a
  1-2 psi monitor spring.
* **The limit used is reported**: on the PDF's inputs line ("5.0 (default)",
  or "Default (not used)" when the result has no IRV), and as a Sizing
  Adjustments row whenever the result was sized with an IRV. Partial-IRV
  results get no row — the body has an IRV but no limit was checked.
* **The wrapper repeats the default rule** rather than reading it from the
  algorithm, so the two must change together. It was verified by typing each
  reported default back in and getting the same regulator, in all four model
  tools.
* **On the general tool each family uses its own default in the same run**, so
  the 143 is held to 5 psi while the 046 gets outlet + 10. An 046-2 can win only
  because its default is looser; type the same number in and the 143 takes it
  (17 of 146 default runs in a sweep). The report is accurate either way; see
  section 13.
* The 143 no longer declines IRV above a 2 psi outlet — that check is
  commented out in both copies — and the 243 keeps its own early "No" for IRV
  at 2 psi and up, so its 5 psi default branch is never reached.

### Data tables worth knowing

* **`data496` runs to a 125 psi inlet**, with the 125 column an exact copy of
  the 100 column so capacity reads flat from 100 to 125. It was dropped once
  without anyone meaning to, which silently removed every 496 answer above a
  100 psi inlet; nothing pinned that range, and only a stale bundle gave it
  away. Its 0.5 psi outlet section holds whole numbers.
* **`data143` has outlet sections at 0.125, 0.25, 0.5, 2 and 6 psi.** 0.125
  duplicates 0.25, and 2 duplicates 6 except that only 2 carries a 5 psi inlet
  row — which is what keeps the 143 out above a 2 psi outlet below a 10 psi
  inlet (section 14).
* **A single 122 with no monitor** gets an internal-control worker
  (`…INTCON…`) and no control line kit, in both copies of `hsc_pnc121()`.

### Adding a ninth tool

Copy an existing `tools/<slug>/` folder, drop in the Python, fill in
`tool.json`, adapt `wrapper.js` + `reference.py` + `block.html` + `form-map.js`,
add a `random` block to `scenarios.json`, and **add the slug to `matrix.tool`
in `.github/workflows/build.yml`** — otherwise CI silently ignores it.

---

## 7. Verification, and why it is not optional

* **`build/difftest.py`** runs the same inputs through the Python and through
  the exact JavaScript the site loads, comparing the **entire** result object:
  every selection field, capacity, part number, warning, adjustment, summary
  line, error message, and every cell of every capacity table. ~10,000 inputs
  per tool. Any difference fails the build.
* **`build/browser_test.js`** loads each real block in a headless browser and
  checks the rendered page against `fixtures.json`. 422 checks currently. As
  well as the sizing result it pins the cart link, the quantity box defaults,
  the account-pricing note and its position, the Items Needed layout and seat
  display names (`ITEMS_LAYOUT` lists the tools held to them — all eight), and
  the include-kit checkbox: present exactly when there is a kit, ticked to
  begin with, and removing only the kit from the cart when unticked. Many of
  these checks run inside an existing scenario, so the count does not move when
  one is added; when adding one, break the block on purpose and confirm it
  fails.
* **`build/fault_sweep.py`** walks each tool's input ranges looking for inputs
  the algorithm cannot answer (a spring colour missing from a table, and so on).
* **`fixtures.json`** pins exact expected output. CI fails if it is stale, which
  is what stops an accidental algorithm edit from silently changing what
  customers are told.

### Real bugs the differential test caught

Keep it in the pipeline. Every one of these was invisible by inspection:

* Python `list + list` concatenates lists; the naive JavaScript translation did
  string concatenation — wrong part numbers in one branch.
* `'N/A'['color']` raises `TypeError` in Python but silently returns `undefined`
  in JavaScript, producing a corrupted part number (`R.441-57S…None.I`) where
  Python correctly refused to size.
* `format(9.05, '.1f')` is `9.1` in Python; a scaled-rounding implementation
  gave `9.0`.
* `f"{x:,}"` keeps the decimal on a float (`5000.0` → `"5,000.0"`), which
  matters because model-121 computes min flow after the float conversion while
  other tools keep it an integer.
* `$GLOBALS` was hardcoded with the all-models global names, so a tool that did
  not inject a given global still reported it present via
  `'name' in globals()` — and then referenced an undefined variable. It is now
  generated per tool from `tool.json`.
* Computing the elevation reduction before validation made Python raise
  `ZeroDivisionError` when inlet equals outlet while JavaScript produced `NaN`.
  All eight tools had it; all now validate first.
* A bulk rename left "Model 461/122" in a user-facing message.
* Adding a parameter to `run_regulator_selection461` without updating its call
  site in `allmodels_selector` raised `TypeError` on every 461 selection. When
  changing a signature, grep for the call sites - there is one per tool.

---

## 8. The translator is a tool this team now owns

`build/transpile.py` (~600 lines) understands only the subset of Python the
algorithms currently use:

* `if`/`elif`/`else`, `for … in`, function definitions, assignment, augmented
  assignment, comparisons, arithmetic, f-strings, list/dict literals, slices,
  single-generator comprehensions
* builtins `abs`, `all`, `any`, `float`, `int`, `isinstance`, `len`, `list`,
  `max`, `min`, `round`, `sorted`, `str`, `globals`
* methods `.append`, `.get`, `.index`, `.items`, `.join`, `.keys`, `.lower`,
  `.strip`, `.startswith`, `.endswith`, `.upper`, `.values`

Anything else — `try`/`except`, `while`, classes, `import`, generators, sets —
**stops the build** with the offending line:

```
Unsupported stmt Try at line 2
```

That loud failure is deliberate: it can never emit questionable JavaScript.
When it happens, either rewrite that line within the subset or extend the
translator. Python semantics that had to be implemented carefully and should
not be "simplified": dicts become JS `Map`s (so numeric keys still sort
numerically), banker's rounding, value-preserving `and`/`or`, `.index()`
raising rather than returning `-1`, and subscript errors raising like Python's.

---

## 9. Known algorithm defects

Run `python3 build/fault_sweep.py` after any algorithm change. Current state:
**six of eight clean, one defect in two tools.**

### all-models and model-461: monitor sizing, 85–100 psi outlet (OPEN)

Both share `spring_57S()` / `spring_X57()`, so both carry it. `gen_match` sets a
monitor setpoint of `outlet_input + 15`; above 85 psi outlet that exceeds
100 psi, past the top of the 57S spring table, so `spring_57S()` returns the
string `'N/A'` and the next line subscripts it.

Reproduce in either tool: inlet 180 psi, outlet 90 psi, flow 800,000 CFH,
monitor protection. The page catches it and asks the customer to contact
Holland — safe but unhelpful.

**Left open deliberately: it needs a product decision, not a code fix.** The
57S series has no spring above 100 psi, so answering it means deciding what
monitor spring a 57S should use up there. Options, in the order we would
consider them:

1. **Reject the candidate**, so the selection loop falls through to
   `461-X57` / `441-X57`, whose table covers 75–250 psi. Safest, and probably
   what the logic intends.
2. **Borrow `spring_X57(monset)`** while keeping the 57S body. One line, but it
   asserts that spring fits that body — only USG can confirm.
3. **Leave it.** The window is narrow and the customer reaches a human.

Do **not** simply return `None` for the monitor spring: the tool would then
present a monitor selection with no monitor spring named, which is worse than
declining. Whichever you choose, apply it to **both**
`tools/all-models/algorithm.py` and `tools/model-461/algorithm.py` — they hold
separate copies. The input is pinned as an edge case in both.

### Fixed, for the record

* **all-models and model-121**: `hsc_pnc121()` built the diaphragm segment as
  `'8-HP'` where the part number wants `'8HP'`, so every `121-8-HP` came out as
  `R.121-8-HP.STD.…​.8-HP.…` instead of `…​.8HP.…`. Two copies again. Only a
  narrow band of inputs reaches a 121-8-HP at all — in all-models the sweep
  found none, because the 121/122 sits last in the priority order — so this was
  rare in the field and is thinly covered by tests. `model-121`'s
  `scenarios.json` pins one case; keep it.

* **all-models and model-461**: `diap_map` was keyed `'8" AL'` while the sizing
  code emits `'8" Al'`, so the lookup missed, `diap` fell through to `'EXTCON'`
  and the line that promotes the model to `461-8-S` never fired. Every 461-S on
  an 8" aluminium diaphragm came out as `R.461-S.…` instead of `R.461-8-S.…` —
  a wrong model segment in a part number, silent, and in **both** copies. Like
  the spring defect above, one character, fixed twice.
* **model-046**: `will_irv_work046()` looked the spring up with
  `spring_map[spring]`; `spring_046()` returns `Gray` above 125 psi outlet and
  `None` above 200, so it raised `KeyError` and broke **every** IRV request with
  an outlet above ~125 psi (568 inputs on the sweep grid). The data settles it —
  the Gray spring's range reads "cannot be used with 046-2", and the 046-2 *is*
  the IRV body — so it now answers `"No"`.
* **model-rpc**: `spring_RPC()` tested `elif op < 35` with no `else`, returning
  `None` at 35 and above. Broke plain sizing at exactly 35 psi outlet (which
  validation allows) and **all** monitor sizing at ≥32 psi outlet, since the
  setpoint is capped at 35. Changed to `<= 35`.
* **model-rpc**: `model_input` is `"RPC"` when no variant is pinned — an
  internal sentinel, not a model name — and it reached the output verbatim,
  giving `Model: RPC` and a part number of `R.RPC.…`. Now translated through the
  existing label map to `243-RPC`.
* **model-rpc**: `output['contorlline']` (letters transposed) in three places
  would have silently hidden the control line kit on that tool only.

---

## 10. Add to Cart

A result with a control line kit shows an **"Include control line kit"**
checkbox, ticked by default. Unticked, the kit leaves the cart URL and the
total, its quantity box locks (keeping its value) and its price dims. Lines are
tracked by position, so unticking the kit does not disturb the regulators'
quantities.

Each result renders an **Add to Cart** control pointing at a site endpoint that
takes matched `part[]` / `qty[]` pairs, adds each to the cart and redirects to
the cart page (or to a CMS "contact us" page if any part number is
unrecognised).

It is a bare `<button>` carrying the URL in `data-cart`, with a click handler
that navigates — not an `<a href>`. The button is deliberately unstyled so the
site theme's own button rules give it its colour, padding and radius and it
matches every other button on the site; the same arrangement as the 441
configurator. Adding any colour, border or padding rule for it in the block
would out-specify the theme, since every rule there is `#usg-sizing-tool`
scoped.

```
https://hollandsupplycompany.com/api/sizing-tool/add-to-cart?part[]=…&qty[]=1&part[]=…&qty[]=2
```

Rules the blocks implement:

* Regulators first (worker, then monitor), each at quantity 1, then the control
  line kit at its own `controllineqty` — which the customer can now change, see
  section 12.
* Values are `encodeURIComponent`'d and then `%2F` is **restored to `/`** —
  part numbers contain slashes (`R.143-1.3/4.16.11`) and the endpoint's
  documented example shows them unencoded. Spaces stay `%20` and the inch mark
  in `CONTROL LINE KIT - 441-1/2"` stays `%22`; both decode correctly.
* Pairs must alternate `part[],qty[]` so they line up server-side. The browser
  test parses the URL back apart and asserts this.

`hsc_pnc*` returns a dict: `worker`, optional `monitor`, optional `controlline`
and `controllineqty`. The kit appears on the page below the part numbers as
`CONTROL LINE KIT: 2` and in the cart, but **deliberately not in the PDF**.

### Open item: NetSuite reconciliation

A generated part number that is not in NetSuite cannot be added to the cart, and
the endpoint then redirects the whole attempt to the contact page — so one bad
part blocks an otherwise valid cart.

The tools can only emit a **finite** set: **1,358 distinct SKUs** (1,355
regulator part numbers plus 3 control line kits) as at the sweep below. That
figure is stale whenever an algorithm gains orifices or springs — the 143's
9/64" and 5/32" orifices added `R.143-2.{3/4,1}.{30,31}.{11,13,20}`, and the
`8" Al` fix turned some `R.461-S.*` numbers into `R.461-8-S.*`. The list was produced by
sweeping 12,000 randomised inputs per tool plus every pinned edge case, and
delivered as `usg-sizing-tool-skus.csv`. HSC is loading the missing ones into
NetSuite.

Check these three first — they are the only SKUs with spaces, one ends in an
inch mark, and they are the newest addition to the cart, so exact-string
matching is the likely failure:

```
CONTROL LINE KIT
CONTROL LINE KIT - 243-3/8
CONTROL LINE KIT - 441-1/2"
```

Caveats: the list is thorough but produced by sampling, not exhaustive
enumeration — a combination reachable only from a very narrow input window could
be missed. It should be regenerated after any algorithm change, since new
orifices or springs mean new part numbers. Worth promoting the ad-hoc script to
`build/list_skus.py`.

If gaps persist, the options considered were: a pre-flight validation endpoint
(best experience — fails before the click), an exception list shipped in the
bundle (no endpoint work, goes stale), and passing the attempted part numbers to
the contact page so it can show them and prefill a quote form.

---

## 11. Site configuration

Content Security Policy needs both CDNs:

```
script-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com;
```

`cdn.jsdelivr.net` serves the algorithms; `cdnjs.cloudflare.com` serves jsPDF
for the Download PDF Summary button. The old
`frame-src https://*.streamlit.app` entry from the iframe era is not needed.

`connect-src` matters too, for the lead time lookup (section 12). The policy
already carries `*.hsc.faxon.tech`, which covers the production endpoint at
`orchestrator.hsc.faxon.tech`. It does **not** cover the staging host
`orchestrator.hsc-staging.faxon.tech` — `hsc-staging` is a different label, so
the wildcard misses it and the browser refuses the request before it leaves,
with `Refused to connect` in the console and nothing on the page. Pointing the
blocks at staging therefore needs a CSP entry as well as a URL change. The
price endpoint is same-origin and needs nothing.

The repository **must stay public** — jsDelivr cannot read a private repo, and
neither can a visitor's browser.

The purge links and CI's purge step only matter for `@main` addresses. With
the blocks pinned to a commit (section 3) the purge is irrelevant, and a
release never waits on jsDelivr's cache.

---

## 12. Page layout conventions

All eight blocks follow the same shape, and the browser test pins the order:

1. Breadcrumb, `<h1>`, intro copy and notes (merged in from the old
   "text-only" blocks; the separate blocks were deleted from the pages)
2. Inputs (below)
3. Run Sizing
4. **Results**: Regulator Selection (model, sizes, seat, spring, capacity), then
   **Items Needed** — an Operating Regulator, a Monitor Regulator when one was
   sized, then the Control Line Kit, each a blue title with its part number
   underneath and its price and lead time below that — then the total, the
   account note and Add to Cart, then Download PDF Summary, capacity tables and
   Sizing Adjustments

### Inputs

| Section | Holds |
| --- | --- |
| **Pressures & Flow** | left: inlet, outlet and MAIP, each `label: [value] [units]`; right: max gas load/flow rate, then min (where the tool has one), then the gas load units |
| **Design Parameters** | pipe size, and the RPC model on the RPC. The 441/461 has none, so the heading is absent there |
| **Overpressure Protection** | required?, then partial IRV or the IRV-vs-monitor preference |
| **Load Type** | generator/boiler question and the % of load |
| **Gas Type** | gas type and specific gravity |
| **⚙️ Advanced Settings** | collapsible, closed to begin with: V-Port preference and 441/461-vs-121/122 priority (where present), the IRV limit (when applicable), oversize override, altitude and atmospheric pressure |

Pressures & Flow sits in the same two columns as the sections below, so the
gas load lines up with Load Type at every width. Each side is a grid with a
label column; pressure fields are 120 px, gas load fields 140 px, unit
dropdowns 110 px. Below 1,060 px wide each label moves above its fields — the
pressures side needs about 470 px to keep its longest label on one line.
Tools without a min gas load put the units on the second line; every tool has a
MAIP, so the pressures side always sets the section's height and the sections
below sit in the same place in every tool.

Advanced Settings is a native `<details>`, so it works by keyboard and screen
reader. Everything in it keeps its default and is sent whether or not the
section was opened; a value set and then closed away still applies, and shows
in the PDF's input summary. On the 441/461 it sits in the left column, under
Overpressure Protection.

The general tool's model question reads "Prioritize choosing 441/461 model or
121/122 model?" with **Model 441/461** the default; the options carry the values
`441/461` and `121/122`, mapping to the old No and Yes of "prefer combustion
regulator". The PDF summary still says "Combustion Regulator Preferred: Yes /
No".

### Price, lead time and quantity

Each part number on a result is followed by a panel holding its price and an
availability estimate. Both are fetched from the customer's own browser after
the result has rendered, so a slow or failing lookup never delays the sizing,
and both slots stay hidden when a lookup fails — the panel with them.

* **Price**: `GET /api/chatbot/products?sku=…`, one call per SKU, same-origin
  with `credentials: 'include'`. Without the session cookie the endpoint
  answers with list price rather than the customer's price, so the credentials
  are not optional.
* **Lead time**: `POST` to `LEAD_TIME_ENDPOINT`, one call for the whole
  selection (it takes 1-8 items; a selection is at most three). An estimate is
  quoted *for a quantity*, so it is cached against one and re-requested when
  the quantity changes, debounced by 500 ms. While the new estimate loads the
  old one dims rather than disappearing.
* Failures are silent to the customer and **loud in the console**, prefixed
  `[USG sizing]`. That is the only way to tell a blocked request from an empty
  answer; without it the page just shows nothing and says nothing.
* Neither figure reaches the PDF. Prices are session-specific and lead times
  move, so a saved file must not carry them — the same reasoning that keeps the
  control line kit out of the PDF.
* **Quantity** is an editable box, on the control line kit only. Regulators are
  one per selection and have no box. Changing it rewrites the cart URL in
  place, recomputes the line total and re-asks for the estimate. The boxes are
  keyed by **line position, not part number**: a monitor can carry the same
  part number as its worker, and keying on the SKU made the two lines share one
  quantity, with the last one on the page winning.

Item titles are the product-page blue (`rgb(49, 65, 122)`) at 24 px, regular
weight; part numbers sit under them at 16 px regular, the kit's at 14 px. Seats
are shown by their customer-facing names — Buna-N, Poly-U Tan, Poly-U Red — on
the page and in both PDF routes, while part numbers keep the algorithm's codes.

Details that were deliberate and are easy to undo by accident:

* Sizes are in **px**, not `rem`, with `!important` guards. The Concrete theme
  sets a non-16px root size and restyles headings, so rem-based sizing shrank
  the whole tool and the theme recoloured the headings.
* Number inputs have no +/- steppers and native spinners are suppressed.
* Info icons are a circled **i** with a custom tooltip (hover, tap, keyboard,
  auto-positioned so it never clips). The browser `title` attribute was useless
  on touch devices.
* Capacity tables scroll horizontally on narrow screens rather than squashing;
  Yes/No cells are colour-coded.
* The V-Port question is worded per tool: "Standard or V-Port orifice preferred
  if applicable?" on the general tool, which sizes every family, and "Standard
  or V-Port orifice preferred?" on the 121 and 441/461 tools. The (i) note is
  the same on all three. The PDF summary does not reuse the form wording — it
  says "Orifice Preference" — so relabelling the question is a block-only
  change, while the summary line is not.
* Each block's PDF and print-fallback subtitle must match its own `<h1>`. Three
  blocks once shipped with "Model 121 Sizing Tool" in the PDF heading because
  they were derived from that block; there is now a test for it.
* The PDF build is **reproducible** — no timestamp is embedded — so `dist/` only
  changes when sources change. A clock in there caused CI to republish every
  bundle on every push.

---

## 13. Open items

1. **The 85–100 psi monitor spring defect** (section 9) — awaiting a product
   decision from USG; apply to both all-models and model-461.
2. **NetSuite SKU reconciliation** (section 10) — HSC loading missing part
   numbers; verify the three control line kits first.
3. **Promote the SKU lister** to `build/list_skus.py` so regenerating the list
   is one command. More pressing now that two algorithms have gained part
   numbers.
4. **Confirm the workflow in GitHub is current.** Runs finish in about 46
   seconds, which is short for eight tools at ~10,000 cases each. Open a run:
   the current workflow shows eight "verify" jobs and a "publish" job. With the
   blocks pinned the purge no longer matters, but a workflow that verifies less
   than it should does.
5. **Quantity** is editable for the control line kit only; regulators are fixed
   at 1 each. Add boxes for them if customers should be able to order several.
6. **Lead time status vocabulary.** The integration guide documents
   `IN_STOCK`, `BUILD_TO_ORDER`, `INCOMING`, `PARTIAL`, `MADE_TO_ORDER`,
   `CONTACT` and `NOT_FOUND`; the orchestrator renames some of them and the
   blocks map what it actually sends (`AVAILABLE_TO_ORDER`,
   `PARTIAL_AVAILABILITY`, `CONTACT_US`). If a Suitelet status ever passes
   through unchanged it renders under a generic "Availability" heading, and
   `CONTACT` would not be recognised as a contact case, so the phone number and
   email would not appear. Map both vocabularies.
7. **No timeout on the lead time request.** The guide's own helper waits four
   seconds then shows a neutral "contact us" message. The blocks have no
   deadline, so a request that hangs leaves the panel hidden for good — quiet
   and safe, but the customer gets nothing where the guide would give them a
   phone number.
8. **The lead time endpoint is called from the browser**, which the integration
   guide advises against: a public URL in page source can be used to read the
   stock position part number by part number. There is no real alternative
   here, since the sizing tools compute their part numbers in the browser and
   have no PHP template to render a badge from, and the NetSuite Suitelet
   address does stay private behind the orchestrator. Worth confirming the
   orchestrator has origin restriction or rate limiting; if not, a same-origin
   proxy would be a one-line change to `LEAD_TIME_ENDPOINT`.
9. Optional: exhaustive SKU enumeration from the capacity tables rather than
   sampling.
10. **Decide whether a V-Port preference should exclude the 122** (section 6).
   It does today, as a side effect of the 122 having no V-Port variant.
11. **Five behaviours nothing pins**, so each could be reverted by a later edit
   without a test noticing. Inputs that reach them:
   * the 243 external control line body — inlet 25 psi, outlet 2 psi,
     18,000 CFH;
   * a 122 under a high-efficiency load in all-models — inlet 14 psi, outlet
     0.25 psi, 30,000 CFH, min flow 3,000, with a high-efficiency load;
   * a 121-8-HP part number in all-models;
   * a 496 inlet above 100 psi — 115 psi, 0.5 psi, 700 CFH;
   * a single 122 with no monitor — 121 tool, 3 psi, 0.5 psi, 1,000 CFH, min
     flow 300.
12. **Per-family IRV defaults on the general tool** (section 6). Decide whether
   one default should apply to every family in a run, so a 143 is not passed
   over for an 046 only because the 046's default is looser.
13. **psi MAIP truncation.** 60.9 psi is treated as 60, which admits an orifice
   rated to exactly 60 psi; the same pressure entered as 4.2 bar correctly rules
   it out. Keeping psi exact would close the gap.
14. **all-models `will_irv_work046()` lacks the Gray-spring fix** the 046 tool
   has (`spring_map.get()`). No swept input reaches it there, but the copies
   differ in a way that matters.
15. **The out-of-range warning** still names the inlet when it is the outlet
   that falls outside a table — and it is also what a customer sees for the
   143's deliberate low-inlet gap, where it reads as the tool being broken.

---

## 14. Things that bit us, in one list

* Pasting a block does nothing for an algorithm change — that lives in the CDN
  bundle. Check `USGSizing.versions`.
* `@main` jsDelivr URLs can serve the old bundle for hours even after a
  successful purge. The blocks are pinned to a commit for that reason
  (section 3).
* **Releasing a block before its bundle.** The IRV field started sending 0
  before the bundle that understands 0 was live, and every IRV request fell
  back to a monitor. Re-pin first, paste second.
* **Changing a data table without regenerating fixtures** fails CI, and it is
  easy to forget because the algorithm builds and difftests cleanly. A green
  build locally means nothing until `make_fixtures.py` has run and its diff has
  been read.
* **Files with the same name overwrite each other** when attached together —
  every tool's algorithm is `algorithm.py`. Rename before sending files for
  review, or one silently goes missing.
* `.github/` is a dot-folder: drag-and-drop upload skips it. Type the path in
  **Add file → Create new file** instead.
* Actions needs **Read and write** workflow permissions, or the build passes but
  never commits the rebuilt `dist/`.
* Editing `wrapper.js` without `reference.py` (or vice versa) fails the
  differential test — by design.
* Bulk find-and-replace across a block leaks the wrong tool's name into user
  copy. Check the PDF subtitle after any rename.
* Adding a tooltip changes the count that `form-map.js` asserts. The 121 is at
  8 since it gained the V-Port question.
* jsPDF cannot initialise under jsdom, so the browser tests verify the PDF's
  *data* but not its rendered layout. Download a real PDF after changing PDF
  layout.
* **A gap in a capacity table is not the same as a rule.** The 143 does not
  answer above a 2 psi outlet with an inlet below 10 psi, and that is enforced
  by the 6 psi outlet section of `data143` starting at a 10 psi inlet rather
  than by any code. It is deliberate, but it is invisible: the 143 tool reports
  "inlet pressure is out of range" (naming the inlet, which is fine), and
  all-models silently drops the family and lets the next one take the job, so a
  400 CFH load at 6 psi inlet / 2.5 psi outlet is answered with a 243 rather
  than a 143. The two outlet sections are otherwise identical, which is what
  makes capacity read flat from 2 to 6 psi; the 5 psi inlet row exists in the
  2 psi section as an interpolation endpoint and not as a sizing case, since
  validation already requires the outlet to be strictly below the inlet.
* **A flag threaded through a call that does not want it.** The 121's
  `result122` was interpolated with the same `vp` flag as the 121 maps. That was
  harmless while `vp` always started `False`, and became a 20% cut to every 122
  capacity the moment a V-Port-first pass existed — on the *standard* pass that
  follows a failed V-Port one. It is pinned to `False` now. When a variable
  stops being a constant, check every call it was passed to.
* Neither `difftest.py` nor `fault_sweep.py` would catch that change: the first
  compares JavaScript to Python, not new to old, and the second only looks for
  inputs that crash. A tool that politely declines looks healthy to both. When
  a data table changes, compare old and new answers over the affected pressure
  window directly.

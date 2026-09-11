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
      │  served by jsDelivr from GitHub
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
| `algorithm.py`, `wrapper.js` — sizing results, validation messages, **and everything in the PDF's Inputs table** | `dist/usg-*.js`, served by jsDelivr | push to GitHub, wait for CI, **purge the CDN**, hard-refresh |
| `block.html` — page markup, styling, PDF layout, page copy, form fields | the pasted block | re-paste the block; instant |

A `@main` jsDelivr URL is cached for up to 12 hours. CI has a purge step, but if
an older workflow is running, purge manually:

```
https://purge.jsdelivr.net/gh/my-usg/sizingtool@main/dist/usg-<tool>.js
```

**To check what a live page is actually running**, open its console and enter:

```js
USGSizing.versions
```

Compare the `algorithm` hash against the table in section 5. This is the
definitive answer and it settles the question in seconds.

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

| Tool | Page | Bundle | `algorithm` hash |
| --- | --- | --- | --- |
| all-models | `/resources/regulator-sizing-tools/general` | `usg-all-models.js` | `d04e6a174f6b` |
| model-046 | `…/model-046` | `usg-model-046.js` | `208e4323a736` |
| model-121 | `…/model-121-122` | `usg-model-121.js` | `81ddc8bad2ef` |
| model-143 | `…/model-143` | `usg-model-143.js` | `6df1df668d59` |
| model-243 | `…/model-243` | `usg-model-243.js` | `caffb09e8169` |
| model-461 | `…/model-441-461` | `usg-model-461.js` | `88ff4f73f9ed` |
| model-496 | `…/model-496` | `usg-model-496.js` | `f6502f86324b` |
| model-rpc | `…/model-243-rpc` | `usg-model-rpc.js` | `8bf4279e24d0` |

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
  `apply121` flag. Has a min-flow field.
* **model-461** entry takes the flows as **arguments**; tables come from the
  algorithm's own `build_standard_table()` / `build_vport_table()` with six
  columns including Qmax/Qmin. No pipe-size input. Has a **V-Port preference**
  input (`vp_preference`, `"standard"` or `"vport"`).
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
7. Push, wait for CI, purge that bundle, hard-refresh.

### Change the page, PDF layout or copy

Edit `tools/<tool>/block.html`, run `node build/browser_test.js <tool>`, then
re-paste the block. No push required for the site (push anyway to keep GitHub
honest).

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
  checks the rendered page against `fixtures.json`. 402 checks currently. As
  well as the sizing result it pins the cart link, the quantity box defaults,
  the account-pricing note and its position above the button.
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
for the Download PDF Summary button, and SheetJS for the all-models Excel
summary, which is why that one needed no policy change. The old
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

---

## 12. Page layout conventions

All eight blocks follow the same shape, and the browser test pins the order:

1. Breadcrumb, `<h1>`, intro copy and notes (merged in from the old
   "text-only" blocks; the separate blocks were deleted from the pages)
2. Inputs
3. Run Sizing
4. **Results**: Regulator Selection — model, sizes, spring, capacity, then
   `Part Number` and `Monitor Part Number` and the control line kit as fields,
   each followed by its live price and lead time — then Add to Cart, then
   Download PDF Summary, then capacity tables, then Sizing Adjustments, and on
   all-models only, Download Excel Summary at the foot of the page

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
* Neither figure reaches the PDF or the Excel summary. Prices are
  session-specific and lead times move, so a saved file must not carry them —
  the same reasoning that keeps the control line kit out of the PDF.
* **Quantity** is an editable box, on the control line kit only. Regulators are
  one per selection and have no box. Changing it rewrites the cart URL in
  place, recomputes the line total and re-asks for the estimate. The boxes are
  keyed by **line position, not part number**: a monitor can carry the same
  part number as its worker, and keying on the SKU made the two lines share one
  quantity, with the last one on the page winning.

Part numbers render in the product-page blue at 24px rather than as a
monospace chip, and the control line kit line matches them. That rule sits
immediately after the `.usg-field` rules it overrides: it is more specific, but
keeping it later as well means no cascade argument decides the colour.

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
* Each block's PDF and print-fallback subtitle must match its own `<h1>`. Three
  blocks once shipped with "Model 121 Sizing Tool" in the PDF heading because
  they were derived from that block; there is now a test for it.
* The PDF build is **reproducible** — no timestamp is embedded — so `dist/` only
  changes when sources change. A clock in there caused CI to republish every
  bundle on every push.
* The Excel summary (all-models only) writes **one sheet with fixed row
  positions**, matching the workbook it was modelled on: labels down column A,
  the run's values in column B. A value that does not apply leaves its cell
  empty rather than shifting the rows, so two downloads can be pasted side by
  side and compared line for line. Adding, removing or reordering a row breaks
  that. SheetJS loads from cdnjs on the first click rather than with the page;
  if it cannot be reached the same rows download as CSV.

---

## 13. Open items

1. **The 85–100 psi monitor spring defect** (section 9) — awaiting a product
   decision from USG; apply to both all-models and model-461.
2. **NetSuite SKU reconciliation** (section 10) — HSC loading missing part
   numbers; verify the three control line kits first.
3. **Promote the SKU lister** to `build/list_skus.py` so regenerating the list
   is one command. More pressing now that two algorithms have gained part
   numbers.
4. **Confirm the workflow in GitHub is current.** A run finishing in ~44s is a
   sign of an older workflow: the current one diff-tests ~10,000 inputs across
   eight tools and takes several minutes. An old workflow also lacks the
   automatic CDN purge, which makes algorithm changes appear not to work.
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

---

## 14. Things that bit us, in one list

* Pasting a block does nothing for an algorithm change — that lives in the CDN
  bundle. Check `USGSizing.versions`.
* `@main` jsDelivr URLs cache for 12 hours. Purge, or rely on CI's purge step.
* `.github/` is a dot-folder: drag-and-drop upload skips it. Type the path in
  **Add file → Create new file** instead.
* Actions needs **Read and write** workflow permissions, or the build passes but
  never commits the rebuilt `dist/`.
* Editing `wrapper.js` without `reference.py` (or vice versa) fails the
  differential test — by design.
* Bulk find-and-replace across a block leaks the wrong tool's name into user
  copy. Check the PDF subtitle after any rename.
* Adding a tooltip changes the count that `form-map.js` asserts.
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
* Neither `difftest.py` nor `fault_sweep.py` would catch that change: the first
  compares JavaScript to Python, not new to old, and the second only looks for
  inputs that crash. A tool that politely declines looks healthy to both. When
  a data table changes, compare old and new answers over the affected pressure
  window directly.

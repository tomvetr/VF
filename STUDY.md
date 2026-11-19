# Vegan filter study — how the study site works

Participant link: `https://tomvetr.github.io/VF/study.html`

Optional link settings:

| Setting | Example | Effect |
|---|---|---|
| `lang` | `?lang=zh` / `?lang=he` | Interface language (default English) |
| `pid` | `?pid=12345` | Participant ID from your panel, passed on to the survey |
| `group` | `?group=A` | Force a group (for testing only; normally random) |
| `reset` | `?reset=1` | Starts the study over on this device (clears saved progress). Add `&test=1` to also show a "Skip store" button in the bottom corner that jumps to the next store. |

Flow: intro → three stores (plain, vegan filter, and either label or category) in random order, each with its own shopping list → one question after each store → redirect to the Zoho survey.

During a task, adding a product that is not on the list is refused with a message that points to the list (which flashes); adding a non-vegan list item is refused with a "Not vegan" message, A store ends when the participant presses Checkout. When all four items are found, a message tells them to press Checkout; if they press it earlier, they are asked to confirm.

- Group A: plain store, vegan filter, vegan label (small tag on the product page).
- Group B: plain store, vegan filter, extra green "Plant-based" department.

## Fields sent to the survey

Every field arrives as a URL parameter. Create a Zoho variable with exactly this name for each one.

General: `pid`, `group` (A/B), `alt` (label/category), `order` (e.g. `fca` = filter first, then plain, then alternative), `lang`, `total` (seconds on the website).

Full parameter list and recommended survey questions: see `ZOHO_SETUP.md`.

Per store, with prefix `c_` (plain store), `f_` (vegan filter) and `a_` (label or category):

| Field | Meaning |
|---|---|
| `list` | Which shopping list (1–3) |
| `pos` | Position in the order (1–3) |
| `time` | Seconds from entering the store until the fourth item is added |
| `clicks` | Clicks during the task |
| `pages` | Product pages opened |
| `search` | Searches made |
| `feature` | Filter: times turned on. Category: visits to the Plant-based department. Label: vegan product pages viewed (label seen) |
| `items` | Distinct products in the cart |
| `found` | List items covered by a vegan product (0–4) |
| `nonvegan` | Attempts to add a non-vegan product (mistakes). These are refused with a message, so the cart only ever holds vegan products |
| `offlist` | Attempts to add a product that is not on the shopping list (refused with a message pointing to the list) |
| `ease` | "How easy was it to find the items?" (1–5) |
| `cart` | OSOG product IDs in the cart, separated by `-` |

Example: `c_time`, `f_time`, `a_time`.

# Vegan filter study — how the study site works

Participant link: `https://tomvetr.github.io/VF/study.html`

Optional link settings:

| Setting | Example | Effect |
|---|---|---|
| `lang` | `?lang=zh` / `?lang=he` | Interface language (default English) |
| `pid` | `?pid=12345` | Participant ID from your panel, passed on to the survey |
| `group` | `?group=A` | Force a group (for testing only; normally random) |
| `reset` | `?reset=1` | Start over on this device (for testing) |

Flow: intro → three stores (plain, vegan filter, and either label or category) in random order, each with its own shopping list → one question after each store → redirect to the Zoho survey.

During a task, adding a non-vegan product is refused with a "Not vegan" message, and "Finish shopping" only works once all four list items are in the cart.

- Group A: plain store, vegan filter, vegan label (small tag on the product page).
- Group B: plain store, vegan filter, extra "Plant-based" department.

## Fields sent to the survey

Every field arrives as a URL parameter. Create a Zoho variable with exactly this name for each one.

General: `pid`, `group` (A/B), `alt` (label/category), `order` (e.g. `fca` = filter first, then plain, then alternative), `lang`.

Per store, with prefix `c_` (plain store), `f_` (vegan filter) and `a_` (label or category):

| Field | Meaning |
|---|---|
| `list` | Which shopping list (1–3) |
| `pos` | Position in the order (1–3) |
| `time` | Seconds from entering the store to finishing |
| `clicks` | Clicks during the task |
| `pages` | Product pages opened |
| `search` | Searches made |
| `feature` | Filter: times turned on. Category: visits to Plant-based. Label: vegan product pages viewed (label seen) |
| `items` | Distinct products in the cart |
| `found` | List items covered by a vegan product (0–4) |
| `nonvegan` | Attempts to add a non-vegan product (mistakes). These are refused with a message, so the cart only ever holds vegan products |
| `ease` | "How easy was it to find the items?" (1–5) |
| `cart` | OSOG product IDs in the cart, separated by `-` |

Example: `c_time`, `f_time`, `a_time`.

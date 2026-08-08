# The Vegan Filter — Interactive Survey Prototype

An interactive, game-tutorial style mock of an online supermarket app that
demonstrates the value of a **Vegan mode** filter. Built for a survey (Zoho)
to prove the concept before pitching it to supermarkets.

**One self-contained file: [`index.html`](index.html).** No build step, no
internet, no dependencies — just open it in any browser.

## The experience (version 2)

The participant shops for the **same 5 vegan items twice** and we compare the time:

1. **Round 1 — without the filter.** The 5 targets (Tofu, Soy sauce, Soy milk,
   a vegan bread, and vegan noodles) are hidden among **109 products** (22 vegan,
   87 non-vegan — a 4:1 ratio). A live **timer** and a **tap counter** run.
2. **Read the ingredients.** Tap any product to open its ingredient list. This
   matters most in two brutal aisles:
   - **Bread** — 15 identical-looking loaves 🍞, only **1 is vegan**. The others
     hide milk, butter, egg, lard, honey…
   - **Instant noodles** — 15 bowls 🍜, only **1 is vegan**; 9 contain meat/seafood
     and **5 look vegetarian but secretly contain "albumin" (egg white)** — the
     kind of trap a shopper would never catch.
3. **Round 2 — with Vegan mode ON.** The filter hides all 87 non-vegan products;
   each hard aisle collapses to its single vegan option. Same 5 items, found in
   seconds.
4. **The filter wins.** A results screen shows **time + taps for each round** and
   the speed-up (e.g. *"3.8× faster with Vegan mode"*) — a concrete before/after
   number for your survey.

Every vegan item has a **unique icon** (so with the filter on the targets pop out);
several non-vegan items **share a target's icon** (so they're hard to find without
it). All products are common in Chinese supermarkets.

**Version history:** the approved earlier build is preserved at
[`versions/v1.html`](versions/v1.html) (single-round, 100 products, no timer or
ingredient view). The live `index.html` is version 2.

## Bilingual (English / 中文)

Every product and every UI string is already translated. A language toggle
(top-right) switches the whole app between English and Chinese live, so the
Chinese version is ready when you need it — no code changes required.

## Using it in the Zoho survey

Pick whichever fits your Zoho form:

- **Embed inline (recommended).** Host `index.html` anywhere that serves a
  static file (GitHub Pages, Netlify, Vercel, S3, your own server) and drop an
  iframe into a Zoho Forms *"Add HTML"* / description field:

  ```html
  <iframe src="https://YOUR-HOST/index.html"
          style="width:100%;max-width:460px;height:900px;border:0;margin:auto;display:block;"
          title="Vegan Filter demo"></iframe>
  ```

- **External link.** Add a button/link in the survey that opens the hosted
  `index.html` in a new tab, then bring participants back to the form.

- **Fully offline.** The file needs no server at all — you can email it or
  hand it out for in-person sessions.

The **"Continue the survey →"** button on the final screen is a placeholder;
in the live survey, wire it (or simply instruct the participant) to move to
the next Zoho page.

## Customising

Everything lives in `index.html`:

- **Products** — edit the `P` array. Each row is
  `{e:emoji, en:"English", zh:"中文", p:price, u:"unit", v:vegan?1:0, t:target?1}`.
- **The 5 items to find** — mark them with `t:1` (they must also be `v:1`).
- **Colours / layout** — the CSS variables at the top of `<style>`.
- **Copy / translations** — the `T` (strings) and `UNIT` dictionaries.

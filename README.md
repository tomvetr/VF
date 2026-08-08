# The Vegan Filter — Interactive Survey Prototype

An interactive, game-tutorial style mock of an online supermarket app that
demonstrates the value of a **Vegan mode** filter. Built for a survey (Zoho)
to prove the concept before pitching it to supermarkets.

**One self-contained file: [`index.html`](index.html).** No build step, no
internet, no dependencies — just open it in any browser.

## The experience

1. **Welcome** — the participant is given a shopping list of **5 vegan items**
   to find (Tofu, Bok choy, Shiitake mushroom, Soy sauce, Rice).
2. **Shop the hard way** — the items are scattered among **121 products**
   (76 vegan, 45 non-vegan: meat, fish, eggs, dairy). Finding them means
   scrolling and reading labels. After they add 2 items — or after ~28s — a
   coach tip nudges them toward the filter.
3. **Turn on Vegan mode** — the toggle instantly hides all 45 non-vegan
   products, the UI turns green, and the remaining items are easy to find.
4. **Basket complete** — a summary screen drives the point home:
   *121 products to scan → 76 with the filter on.*

The items are common in Chinese supermarkets, matching the intended market.

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

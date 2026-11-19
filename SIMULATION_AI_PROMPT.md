Goal: build and run a synthetic-participant pilot of our "vegan filter" online supermarket study (shopping task + survey).

The purpose is PILOTING: find UX bugs, confusing instructions or survey items, broken survey logic, and test the analysis pipeline end to end. It is NOT to estimate what real people think. Design everything with that in mind.

# The study you are simulating

Study website: https://tomvetr.github.io/VF/study.html

What a participant does:
1. Reads an intro pop-up and clicks Start.
2. Shops in three versions of an online supermarket (about 1,000 real US products, with photos, prices and ingredient lists), in random order:
   - Group A: regular store, store with a vegan filter (a switch next to the search bar), store with vegan labels (a "Vegan" label under the ingredient list on the product page).
   - Group B: regular store, store with a vegan filter, store with a vegan category (a green "Plant-based" department).
3. In each store they get a different shopping list of 4 items (e.g. "Vegan milk, Vegan sausage, Vegan bread, Vegan chocolate") and must add one vegan product per item. The store refuses non-vegan products ("This product is not vegan") and products not on the list ("This product is not on your shopping list"). The store ends automatically when all 4 items are in the cart.
4. After each store: one question, "How easy was it to find the items on your list?" (1-5).
5. At the end, "Continue to the survey" opens the Zoho survey with all shopping data in the link (URL parameters such as pid, group, alt, order, lang, total, and per store c_/f_/a_ time, clicks, pages, search, feature, items, found, nonvegan, offlist, ease, cart).

Useful link settings (combine with &):
- reset=1: test mode. Starts fresh and shows a "Skip store" button in the bottom corner.
- group=A or group=B: force the group.
- lang=en, zh or he: interface language (English, Chinese, Hebrew).
- pid=XXXX: participant ID, passed on to the survey.
Example: https://tomvetr.github.io/VF/study.html?reset=1&group=B&lang=zh&pid=P07

Progress is saved in the browser's localStorage, so use a fresh browser context for every participant.

# Build

1. Personas: generate N = 30 first-person persona profiles, sampled from explicit distributions written in a config file: diet, age, digital literacy, online grocery shopping frequency, motivation for using a vegan filter, patience, device (phone 70% / desktop 30%), language. Include low-literacy, impatient and skeptical personas (minimum counts in the config). Keep each profile coherent (e.g. only vegans say "I'm vegan myself"). Give each persona realistic limits: what they know about ingredients (most people don't know that whey, casein, gelatin or albumin are animal-derived; only vegans reliably do) and how carefully they read (impatient or low-literacy people go by the name and picture and skim). Save as personas.json.

2. Task agent: a Playwright browser driven by an LLM, one fresh agent per participant. The agent receives ONLY its persona and the participant instructions, never code, files, hypotheses or this prompt. Give it a simple text view of the screen (pop-ups, top bar with the shopping list, notifications, search box, filter switch, menus, product cards with numbered clickable elements, product window with ingredients) and a small command set (look, click <number>, search <words>, back, home, skip_store, quit). Phone personas use a phone-sized viewport. Tell it to stay in character, use only the persona's knowledge, and skim, guess and make mistakes as that person would.
   - Enforce budgets: steps per store, total steps, total minutes. Allow skipping a store or quitting.
   - Log every step: action, page/state (store number, store version, phase), timestamp, notifications shown, errors, and task success or failure per store. Save screenshots on failed actions, page errors, repeated identical screens (stuck), skips, quits and budget stops.
   - Intercept the Zoho survey link (survey.zohopublic.eu) and record its URL parameters instead of opening the real survey.

3. Survey agent: a separate, fresh call per participant. Input = persona + a plain-language record of that participant's own actions (built from their log) + the survey items verbatim (below). Output strict JSON keyed by item ID with {"answer", "reason"} (one-line reason). Respect the display logic and required items. Never submit to the live Zoho survey or any real database; write to a separate synthetic store, every record flagged synthetic=true, together with the recorded URL parameters. Validate answers (types, ranges, required items, valid rankings).

4. Realism: vary sampling where the model allows it (current Claude models reject temperature; if so, rely on persona variety and say so). Run a subset (about 20%) on a second model to check model dependence.

# Survey items (verbatim)

Text in [square brackets] depends on alt: alt=label -> "vegan labels" / "Store with vegan labels"; alt=category -> "a vegan category" / "Store with a vegan category".

Q1 (required, single). At the same prices, which of the three stores you just used would you choose? Regular store | Store with a vegan filter | Store with [vegan labels / a vegan category] | No preference
Q2 (optional, text). Why?
Q3 (required, ranking 1-3). Rank the three stores from most convenient (1) to least convenient (3) for finding vegan products. Regular store | Store with a vegan filter | Store with [vegan labels / a vegan category]
Q4 (optional, matrix 1-5, 1 = strongly disagree, 5 = strongly agree; each row rated for "Vegan filter" and for "[Vegan labels / Vegan category]"):
  Q4a It makes it easier to find vegan products.
  Q4b It makes vegan shopping more convenient.
  Q4c It saves time and effort when shopping.
  Q4d It would make vegans more likely to shop at this supermarket.
Q5 (required, slider 0-100). Of all the things that make veganism inconvenient, how much would a vegan filter in a large supermarket chain's online store remove? (0% = none, 100% = all of it)
Q6 (optional, 1-5, 1 = not at all, 5 = a great deal). How much would a vegan filter help…
  Q6a someone trying vegan for the first time to get started?
  Q6b a new vegan stick with it through the first months?
  Q6c a long-term vegan stay vegan?
Q7 (optional, 1-5, 1 = very unlikely, 5 = very likely). How likely are you to turn on a vegan filter in the future, if your online supermarket had one?
Q8 (optional, single). If you turned on the vegan filter, which would you prefer? You can change this setting at any time. (Use the answer options from the live survey; if you don't have them, skip Q8 and report it.)
Q9 (optional, single). What best describes your diet? Omnivore (your diet includes meat) | Flexitarian (your diet includes meat, but in smaller quantities) | Vegetarian (no meat, fish or seafood, but eggs or dairy products) | Vegan (no meat, fish, seafood, eggs or dairy products) | Other (please specify)
Q10 (optional, single). Have you ever followed a vegan diet at some point in your life? Yes | No
Q11 (optional, single). How often do you buy groceries online? Never | Less than once a month | 1–3 times a month | Once a week or more
Q12 (optional, text). What is your gender?
Q13 (optional, number). What is your birth year?

# Run

- First a dry run with 3 varied personas (e.g. one low-literacy and impatient, one skeptical on the second model, one desktop). Show me the logs, list the bugs, and fix bugs in your own tooling before the full run. Do not change the study website; report website bugs to me instead.
- Then run all N, at most about 6 participants at a time.

# Report (markdown + CSVs)

- Task success rate, time (the site's own timer and steps) and step counts per store version; where agents got stuck, with screenshots.
- Within-person comparisons: filter vs regular and filter vs label/category on steps, mistakes and ease.
- Per survey item: response distribution, near-zero-variance items, contradictory answers (e.g. Q1 choice not ranked first in Q3; survey diet differing from persona; survey answers inconsistent with what the participant actually did), and free-text themes that suggest confusing wording.
- Bugs found in the website or the survey logic, ranked by severity, each with how to reproduce it.
- Confirmation that the analysis pipeline runs end to end on the synthetic data.
- An explicit limitations section: synthetic responses are low-variance, positivity-biased and not valid estimates of human attitudes; LLM agents read more carefully and make fewer mistakes than people; list which findings need a human pilot (n ≈ 10–20) to confirm.

Keep all code in one folder with one command to rerun everything. Ask me before anything that costs money beyond $5 of API calls, and give me a cost estimate after the dry run.

A previous implementation exists in the repository github.com/tomvetr/VF, folder simulation/ (persona generator, Playwright harness, survey pipeline, analysis script). You may reuse it if you have access, but check it still matches the current website.

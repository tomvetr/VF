Goal: simulate a realistic sample of people going through our online shopping study and its survey, and collect their behaviour and answers as a dataset. The aim is to estimate how people would respond, so every simulated participant must behave and answer like a real person of their type, not like a careful AI.

Study website: https://tomvetr.github.io/VF/study.html
- Add pid=<participant id> to the link, and lang=en, lang=zh or lang=he for the participant's language (English, Chinese, Hebrew).
- Use a fresh browser context for every participant (progress is saved in the browser).
- The site gives participants all their instructions. At the end, "Continue to the survey" opens the survey; record the URL and its parameters (they hold the participant's shopping data) instead of submitting the live survey.

# Who to simulate

N = 100 participants (I will tell you if we scale up after the first results). Sample from these distributions and write them in a config file:

Diet (the main grouping in the analysis):
- Long-term vegans (vegan for more than 1 year): 15%
- New vegans (vegan for less than 6 months): 25%. This is a key group: they are motivated but still learning, know the basic rules, often don't recognise hidden animal ingredients, and find shopping stressful.
- Vegetarians: 15%
- Flexitarians (eat meat, trying to eat less): 20%
- Meat eaters (no plans to change): 25%, including some who are openly skeptical of vegan products.

Demographics:
- Age: 18-24: 20%, 25-34: 30%, 35-49: 25%, 50-64: 15%, 65+: 10%
- Gender: about half women, half men, a few non-binary
- Language: English 50%, Chinese 35%, Hebrew 15%
- Device: phone 70%, laptop or desktop 30%
- Online grocery shopping: never 15%, less than monthly 25%, 1-3 times a month 35%, weekly or more 25%
- Digital literacy: low 20%, medium 50%, high 30%
- Patience: low 30%, medium 45%, high 25%
- Reason for interest in a vegan filter: own diet, shopping for a vegan friend or family member, curiosity about eating less meat, health, or no interest. Make it coherent with the diet; meat eaters are mostly "no interest" or "curious".

Keep each person coherent and specific: give them a name, a short life situation (job, household, why they are doing the study, how much time they have) and a few habits, written as a first-person profile.

# Reading ingredient lists must not be easy

Real people are bad at this. Build it into every persona:
- Knowledge depends on the person:
  - Long-term vegans know most hidden animal ingredients (whey, casein, caseinate, lactose, albumin, gelatin, carmine, shellac, lard, tallow, honey, isinglass), but still slip when tired or rushed.
  - New vegans know the basics (no meat, fish, milk, eggs, honey) but often miss hidden ones like whey, casein, albumin, gelatin or carmine. They are unsure about "natural flavors", sugar, mono- and diglycerides or vitamin D3, and sometimes over-reject products out of caution.
  - Vegetarians and flexitarians recognise milk and eggs but rarely the hidden names.
  - Meat eaters know only the obvious ("chicken", "milk") and have to guess the rest.
- Reading behaviour: most people do not read the whole list. They trust the product name and picture ("Veggie", "Dairy-free", "Plant-based" feel safe even when they aren't), glance at the first few ingredients, and miss small print. Impatient and low-literacy people skim even more. Long lists, chemical names and lists in a second language make it harder.
- Fatigue: attention drops over the three stores; mistakes become more likely later in the session.
- People make ordinary mistakes: tapping the wrong product, searching with the wrong word, giving up on an item, misreading the instructions.

# Build

1. Personas: generate the N first-person profiles from the distributions above (explicit in the config file). Save as personas.json.

2. Task agent: a Playwright browser driven by an LLM, one fresh agent per participant. The agent receives ONLY its persona and the participant instructions, never code, files, hypotheses or this prompt. Give it a simple text view of the screen (pop-ups, the shopping list, notifications, search box, switches, menus, product cards with numbered clickable elements, product window with ingredients) and a small command set (look, click <number>, search <words>, back, home, skip_store, quit). Phone personas use a phone-sized viewport. Tell it to stay in character, use only the persona's knowledge, and read, skim, guess and make mistakes as that person would.
   - Enforce budgets: steps per store, total steps, total minutes. Allow giving up on a store or quitting, as a real person might.
   - Log every step: action, page/state, timestamp, notifications shown, errors, and success or failure per store.
   - Do not submit the live survey; record the survey URL and its parameters.

3. Survey agent: a separate, fresh call per participant. Input = persona + a plain-language record of that participant's own experience (built from their log) + the survey items verbatim (below). Output strict JSON keyed by item ID with {"answer", "reason"} (one-line reason). Respect required items and the wording rule below. Never submit to the live survey or any real database; write to a separate store, every record flagged synthetic=true, together with the recorded URL parameters. Validate answers (types, ranges, required items, valid rankings).

4. Realism: vary sampling where the model allows it (if the model rejects temperature, rely on persona variety and say so). Run about 20% of participants on a second model and compare the results, to check that the answers don't depend on one model.

# Survey items (verbatim)

The participant used three stores. One of them is a regular store, one has a vegan filter, and the third has either vegan labels or a vegan category. Wherever [square brackets] appear, use the name of the third store this participant actually saw ("Store with vegan labels" / "Vegan labels", or "Store with a vegan category" / "Vegan category").

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
Q8 (optional, single). If you turned on the vegan filter, which would you prefer? You can change this setting at any time. (Use the answer options from the live survey; if you don't have them, skip Q8 and tell me.)
Q9 (optional, single). What best describes your diet? Omnivore (your diet includes meat) | Flexitarian (your diet includes meat, but in smaller quantities) | Vegetarian (no meat, fish or seafood, but eggs or dairy products) | Vegan (no meat, fish, seafood, eggs or dairy products) | Other (please specify)
Q10 (optional, single). Have you ever followed a vegan diet at some point in your life? Yes | No
Q11 (optional, single). How often do you buy groceries online? Never | Less than once a month | 1–3 times a month | Once a week or more
Q12 (optional, text). What is your gender?
Q13 (optional, number). What is your birth year?

# Run

- First a pilot of 5 varied participants (include a new vegan, a long-term vegan, a skeptical meat eater, a low-literacy person and a Chinese-language phone user). Show me their logs and answers, and fix problems in your own tooling before the main run. Do not change the study website; tell me about anything that looks broken.
- Then run all N, a few participants at a time.

# Results (markdown report + CSVs)

- The dataset: one row per participant (persona attributes, model, shopping data from the URL parameters, survey answers) and one row per participant per store.
- Behaviour per store type: completion rate, time (the site's timer), number of actions, mistakes (non-vegan products refused), off-list attempts, ease rating. Within-person comparisons: vegan filter vs regular store, and vegan filter vs the third store.
- Survey results: distribution, mean and 95% confidence interval for every item, overall and broken down by diet group (long-term vegans, new vegans, vegetarians, flexitarians, meat eaters), language and age group.
- Q5 in particular: the estimated share of the convenience barrier a vegan filter removes, overall and per diet group.
- Common themes in the open answers (Q2), with example quotes per diet group.
- Differences between the two models.
- A short methods section: how personas were sampled, what the agents saw, budgets, and how many participants finished, gave up or quit.
- A limitations section: these are simulated people, not survey respondents. Say which results should be checked against real participants before being reported as findings.

Keep all code in one folder with one command to rerun everything. Ask me before anything that costs money beyond $5 of API calls, and give me a cost estimate after the 5-participant pilot.

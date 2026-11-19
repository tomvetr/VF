Goal: simulate a realistic sample of people going through our online shopping study and its survey, and collect their behaviour and answers as a dataset. The aim is to estimate how people would respond, so every simulated participant must behave and answer like a real person of their type, not like a careful AI.

Study website: https://tomvetr.github.io/VF/study.html
- Add pid=<participant id> to the link, and lang=en, lang=zh or lang=he for the participant's language (English, Chinese, Hebrew).
- Every participant id must start with "sim-" (for example pid=sim-001), so simulated responses can always be told apart from real ones in the survey results.
- Use a fresh browser context for every participant (progress is saved in the browser).
- The site gives participants all their instructions. At the end, "Continue to the survey" opens the survey. Record that URL and its parameters (they hold the participant's shopping data), then fill in and submit the live survey in the same browser, as that participant.

# Who to simulate

N = 100 participants (I will tell you if we scale up after the first results). Sample from these distributions and write them in a config file.

Diet (the main grouping in the analysis):
- Long-term vegans (vegan for more than 1 year): 15%
- New vegans (vegan for less than 6 months): 25%. This is a key group: they are motivated but still learning, know the basic rules, often don't recognise hidden animal ingredients, and find shopping stressful.
- Vegetarians: 15%
- Flexitarians (eat meat, trying to eat less): 20%
- Meat eaters (no plans to change): 25%, including some who are openly skeptical of vegan products.

Demographics:
- Age: 18-24: 20%, 25-34: 30%, 35-49: 25%, 50-64: 15%, 65+: 10%
- Gender: about half women, half men, a few who answer "Other"
- Language: English 50%, Chinese 35%, Hebrew 15%
- Device: phone 70%, laptop or desktop 30%
- Online grocery shopping: never 15%, less than monthly 25%, 1-3 times a month 35%, weekly or more 25%
- Digital literacy: low 20%, medium 50%, high 30%
- Patience: low 30%, medium 45%, high 25%
- Reason for interest in a vegan filter: own diet, shopping for a vegan friend or family member, curiosity about eating less meat, health, or no interest. Make it coherent with the diet; meat eaters are mostly "no interest" or "curious".
- Some Chinese-speaking vegans follow a "pure vegan" diet (no five pungent spices); include a few.

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
   - Record the survey URL and its parameters before the survey opens.

3. Survey agent: a separate, fresh call per participant. Input = persona + a plain-language record of that participant's own experience (built from their log) + the survey items verbatim (below). Output strict JSON keyed by item ID with {"answer", "reason"} (one-line reason). Respect required items and the wording rule below. Validate answers (types, ranges, required items, valid rankings), then enter them in the live survey (opened from the recorded URL, so the hidden variables are saved) and submit it. Also keep a local copy of every record, flagged synthetic=true, with the URL parameters and the submission time.

4. Realism: vary sampling where the model allows it (if the model rejects temperature, rely on persona variety and say so). Run about 20% of participants on a second model and compare the results, to check that the answers don't depend on one model.

# Survey items (verbatim)

The participant used three stores. One of them is a regular store, one has a vegan filter, and the third has either vegan labels or a vegan category. Wherever [square brackets] appear, use the third store this participant actually saw: "Store with vegan labels" or "Store with a vegan category". The URL parameter alt tells you which (alt=label or alt=category).

Q1 (required, single). At the same prices, which of the three stores you just used would you choose?
Regular store | Store with a vegan filter | Store with [vegan labels / a vegan category] | No preference

Q2 (optional, text). Why?

Q3 (required, ranking 1-3). Rank the three stores from most convenient (1) to least convenient (3) for finding vegan products.
Regular store | Store with a vegan filter | Store with [vegan labels / a vegan category]

Q4 (required, matrix, 1 = strongly disagree … 5 = strongly agree, or "Not applicable"). If an online supermarket added a "vegan filter" so you only see vegan items across all categories, it would:
- Q4a Make vegans more likely to shop at this supermarket.
- Q4b Make vegans save time and effort when shopping.
- Q4c Make it easier for beginners to adopt a vegan lifestyle.
- Q4d Make it easier to find vegan products.
- Q4e Make it easier for existing vegans to maintain it over time.
- Q4f Make vegan shopping more convenient.

Q5 (optional, 1-5, 1 = not at all, 5 = a great deal). How much would a vegan filter help a new vegan stick with it through the first months?

Q6 (required, slider 0-100). Of all the things that make veganism inconvenient, how much would a vegan filter in a large supermarket chain's online store remove? (0% = none, 100% = all of it)

Q7 (required, single). Is it likely that you will activate the filter in the future?
Yes, absolutely | No, probably not

Q8 (optional, single). What best describes your diet?
Omnivore (your diet includes meat) | Flexitarian (your diet includes meat, but in smaller quantities) | Vegetarian (your diet does not include meat, fish, or seafood but does include eggs or dairy products) | Vegan (your diet does not include meat, fish, seafood, eggs, or dairy products) | Pure Vegan (your diet does not include meat, fish, seafood, eggs, dairy products or five pungent spices) | Other (please specify)

Q9 (optional, single). Have you ever followed a vegan diet at some point in your life?
Yes | No

Q10 (optional, single). How often do you buy groceries online?
Never | Less than once a month | 1–3 times a month | Once a week or more

Q11 (optional, single). What is your gender?
Man | Woman | Other

Q12 (optional, number). What is your birth year?

Skip the survey's optional contact section ("Want to get more involved with the vegan filter project?"). Simulated people must not leave names or contact details.

# Run

- First a pilot of 5 varied participants (include a new vegan, a long-term vegan, a skeptical meat eater, a low-literacy person and a Chinese-language phone user). Show me their logs and answers, confirm their responses appear in the live survey with the hidden variables saved, and fix problems in your own tooling before the main run. Do not change the study website; tell me about anything that looks broken.
- Then run all N, a few participants at a time.

# Results (markdown report + CSVs)

- The dataset: one row per participant (persona attributes, model, shopping data from the URL parameters, survey answers).
- A short methods section: how personas were sampled, what the agents saw, budgets, and how many participants finished, gave up or quit, and how many survey submissions succeeded.

Keep all code in one folder with one command to rerun everything. Ask me before anything that costs money beyond $5 of API calls, and give me a cost estimate after the 5-participant pilot.

You are editing an existing Zoho Survey: https://survey.zohopublic.eu/zs/9fCd5d

Please make the changes below. Where Zoho cannot do something exactly as described, choose the closest option and list what you changed at the end. Do not delete collected responses.

# Background

The survey is part of a research study about a "vegan filter" for online supermarkets.

Participants no longer play the old game. They now shop in a mock online supermarket website first. The website:

1. randomly puts each participant in group A or B,
2. has them shop in three versions of the store, in random order:
   - group A: a regular store, a store with a vegan filter, and a store with vegan labels
   - group B: a regular store, a store with a vegan filter, and a store with a vegan category ("Plant-based" department)
3. asks one question after each store ("How easy was it to find the items on your list?"),
4. then sends the participant to this survey, with all their shopping data in the link.

The survey therefore starts after the shopping. It should not explain the shopping task again, and it should not repeat the "how easy" question.

# 1. Hidden variables (URL parameters)

Create one hidden variable (URL variable) for each parameter below, with exactly these names (lowercase, with underscores). Store every value with the response. They arrive in the link like this:

https://survey.zohopublic.eu/zs/9fCd5d?pid=p123&group=A&alt=label&order=fca&lang=en&total=412&c_list=1&c_pos=2&c_time=95&...

General (6):
- pid: participant ID
- group: A or B
- alt: which third store the participant saw: "label" (group A) or "category" (group B)
- order: order of the three stores: c = regular, f = vegan filter, a = label or category (e.g. "fca")
- lang: language used on the website: en, zh or he
- total: total time on the website, in seconds

Per store (13 fields x 3 stores = 39). Each field below comes three times, with a prefix:
c_ = regular store, f_ = vegan filter store, a_ = label or category store.
For example: c_time, f_time, a_time.

- _list: which shopping list was used (1, 2 or 3)
- _pos: position of this store in the order (1, 2 or 3)
- _time: seconds spent shopping in this store
- _clicks: number of clicks
- _pages: number of product pages opened
- _search: number of searches
- _feature: use of the store's vegan tool (filter turned on / visits to the Plant-based department / vegan product pages viewed; always 0 in the regular store)
- _items: number of different products in the cart
- _found: how many of the 4 list items were found (0-4)
- _nonvegan: mistakes: attempts to add a non-vegan product
- _offlist: attempts to add a product that is not on the list
- _ease: answer to "How easy was it to find the items on your list?" (1-5)
- _cart: product IDs in the cart, separated by "-"

So the full list of variable names is:
pid, group, alt, order, lang, total,
c_list, c_pos, c_time, c_clicks, c_pages, c_search, c_feature, c_items, c_found, c_nonvegan, c_offlist, c_ease, c_cart,
f_list, f_pos, f_time, f_clicks, f_pages, f_search, f_feature, f_items, f_found, f_nonvegan, f_offlist, f_ease, f_cart,
a_list, a_pos, a_time, a_clicks, a_pages, a_search, a_feature, a_items, a_found, a_nonvegan, a_offlist, a_ease, a_cart

The old game variables (time_without, time_with, clicks_without, clicks_with, mistakes_without, mistakes_with, gave_up) are no longer sent. Keep them only if the survey still needs them for older responses; otherwise remove them.

# 2. Language

Make the survey available in English, Simplified Chinese and Hebrew (right-to-left). Show the language that matches the "lang" variable (en / zh / he); default to English. Translate every question and answer option below.

# 3. Questions

Replace the current questions about the vegan filter with the questions below, in this order. The demographic questions in part 3 can keep their current wording.

Text in [square brackets] depends on the "alt" variable (use display logic, or two versions of the question):
- alt = label: "vegan labels" / "Store with vegan labels"
- alt = category: "a vegan category" / "Store with a vegan category"

## Part 1 – Comparing the stores

Q1. At the same prices, which of the three stores you just used would you choose? (single choice, REQUIRED)
- Regular store
- Store with a vegan filter
- Store with [vegan labels / a vegan category]
- No preference

Q2. Why? (open text, optional)

Q3. Rank the three stores from most convenient (1) to least convenient (3) for finding vegan products. (ranking, REQUIRED)
- Regular store
- Store with a vegan filter
- Store with [vegan labels / a vegan category]

Q4. How much do you agree with each statement? (matrix, 1 = strongly disagree, 5 = strongly agree; optional)
Rows:
- It makes it easier to find vegan products.
- It makes vegan shopping more convenient.
- It saves time and effort when shopping.
- It would make vegans more likely to shop at this supermarket.
Columns (each row is answered for both): "Vegan filter" and "[Vegan labels / Vegan category]".

## Part 2 – The vegan filter and veganism

Q5. Of all the things that make veganism inconvenient, how much would a vegan filter in a large supermarket chain's online store remove? (slider 0-100%, labels: 0% = none, 100% = all of it; REQUIRED)

Q6. How much would a vegan filter help… (matrix, 1 = not at all, 5 = a great deal; optional)
- someone trying vegan for the first time to get started?
- a new vegan stick with it through the first months?
- a long-term vegan stay vegan?

Q7. How likely are you to turn on a vegan filter in the future, if your online supermarket had one? (1 = very unlikely, 5 = very likely; optional)

Q8. If you turned on the vegan filter, which would you prefer? You can change this setting at any time. (single choice, optional)
Keep the answer options this question already has in the current survey.

## Part 3 – About you

Q9. What best describes your diet?
- Omnivore (your diet includes meat)
- Flexitarian (your diet includes meat, but in smaller quantities)
- Vegetarian (no meat, fish or seafood, but eggs or dairy products)
- Vegan (no meat, fish, seafood, eggs or dairy products)
- Other (please specify)

Q10. Have you ever followed a vegan diet at some point in your life? (Yes / No)

Q11. How often do you buy groceries online?
- Never
- Less than once a month
- 1–3 times a month
- Once a week or more

Q12. What is your gender?

Q13. What is your birth year?

## Questions to remove

Remove these questions from the current survey (they are replaced by Q1–Q8 above):
- The six statements that begin "If an online supermarket added a 'vegan filter' so you only see vegan items across all categories, it would: …" (more likely to shop there / easier for beginners / easier to maintain / save time and effort / more convenient / easier to find vegan products).
- "Is it likely that you will activate the filter in the future?" (replaced by Q7).
- "At the same prices, which store would you choose? [with filter, without filter, no preference]" (replaced by Q1).
- Any question that asks how easy the shopping task was (already asked on the website).

# 4. Other settings

- Required: Q1, Q3 and Q5 only. All other questions are optional.
- Do not randomise the order of the stores in Q1 and Q3; keep the order shown.
- Keep the survey's existing consent and thank-you pages, but remove any intro text that explains the old game.
- If the survey's public link changes, report the new link, because the website must send participants to it.

# 5. When you are done

Report:
1. The final survey link.
2. The list of hidden variables you created, exactly as named.
3. Anything you could not do as described, and what you did instead.

To test, open https://tomvetr.github.io/VF/study.html?reset=1&group=A (and again with group=B), complete the shopping, and check that the survey opens, shows the right wording for that group, and saves the hidden variables with the response.

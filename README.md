# What 1,165 public reviews say about AI coworkers

Data and method behind the study published at **[heytobo.com/complaints](https://heytobo.com/complaints)**.

On November 10, 2026 we collected public reviews and discussions about seven AI coworkers (Viktor, Claude Tag, Slackbot, Lindy, Dust, Glean, Notion AI) from Reddit, Hacker News, Trustpilot, G2, Product Hunt, LinkedIn and review blogs. 1,165 unique items, 687 kept as relevant. We sorted the negative sentences into 20 complaint families.

| # | Complaint family | Threads |
|---|---|---|
| 1 | Bills nobody can predict | 76 |
| 2 | Bugs and instability | 49 |
| 3 | Hard to set up | 49 |
| 4 | Missing or weak integrations | 49 |
| 5 | Memory that is siloed and invisible | 40 |
| 6 | Limits and caps | 39 |
| 7 | Clients and outsiders left out | 35 |
| 8 | Security and permissions that are too wide | 31 |
| 9 | Wrong answers | 29 |
| 10 | Billing and cancellation | 22 |
| 11 | Everyone has their own AI | 20 |
| 12 | No control, no undo | 12 |
| 13 | It doesn't actually act | 11 |
| 14 | Black box | 10 |
| 15 | Slow, with no feedback | 8 |
| 16 | Unreachable support | 8 |
| 17 | Noise | 8 |
| 18 | Generic output | 5 |
| 19 | Needs babysitting | 3 |
| 20 | Reserved for big plans | 3 |

## What is in this repository

- `classify.py`: the sorting script. It splits each item into sentences, keeps the negative ones and matches them against one keyword pattern per family.
- `families.json`: the 20 families, their patterns and their counts.
- `sources.csv`: the 687 URLs we kept, with the product and the platform. No review text is redistributed here: follow the links.

## Method

- **Collection.** Eight search angles per product (honest reviews, switching away, missing features, G2, Product Hunt, Hacker News and more), plus twelve searches for unmet needs.
- **Counting.** A URL counts once per family. One URL can count in several families.

## Limits, stated plainly

- Keyword matching is crude. Read the counts as orders of magnitude, not as measurements. The small families (under 10 threads) are the least reliable.
- Public reviews are a small and noisy sample, and some comparison articles are written by competitors.
- We could not read X, and we read Reddit and G2 only through search excerpts.
- We build a product in this space ([Tobo](https://heytobo.com)), so we are not neutral. That is why the page links every quote to its source and why the script is public.

To rerun it on your own collection: `python3 classify.py reviews.json`, where `reviews.json` is a list of `{"url", "texte", "produit", "source"}`.

Code: MIT. Counts and URL list: CC BY 4.0. Corrections welcome through issues.

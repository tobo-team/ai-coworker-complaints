"""Sort negative sentences from public reviews into 20 complaint families.

Input : a JSON list of items {"url", "texte" (the review text), "produit", "source"}.
Output: families.json (threads per family) and sources.csv (the URLs used, without any review text).

Usage : python3 classify.py reviews.json

Counting rule: a URL counts once per family; one URL can count in several families.
Keyword matching is crude. Read the counts as orders of magnitude.
"""
import collections, csv, json, re, sys

FAMILIES = {
    "Bills nobody can predict": r"credit|pricing|price|expensive|cost|overage|token bill|per[- ]token|burn|\$\d",
    "Billing and cancellation": r"cancel|refund|charged|billing|invoice|credit card|scam|subscription",
    "Memory that is siloed and invisible": r"memory|forget|forgot|remember|context (is|was|gets)|siloed|per[- ]channel|amnesia|stale",
    "Wrong answers": r"hallucinat|wrong|inaccura|incorrect|made up|mistake|fabricat|unreliable answers",
    "Needs babysitting": r"babysit|supervis|double[- ]check|verify everything|can't trust|cannot trust|hand[- ]hold|micro-?manag|keep an eye",
    "Slow, with no feedback": r"\bslow\b|latency|takes (too )?long|minutes to|waiting for",
    "Bugs and instability": r"\bbug|broken|crash|down(time)?\b|unstable|fails?\b|failed|error|glitch|stuck|loop",
    "Hard to set up": r"learning curve|setup|set up|configur|onboard|complicated|complex|steep|confus",
    "Missing or weak integrations": r"integration|connector|mcp|api access|doesn't (support|connect)|not supported|missing (tool|feature)",
    "Security and permissions that are too wide": r"privacy|security|permission|data (leak|access|retention)|compliance|soc ?2|gdpr|access to (all|every)|over[- ]?permission",
    "Unreachable support": r"support (is|was|team|never|didn)|no response|unresponsive|customer service|ticket",
    "Limits and caps": r"limit|cap\b|quota|rate[- ]limit|messages per|per week|throttl",
    "Reserved for big plans": r"enterprise only|enterprise plan|team plan|minimum seats|sales call|contact sales|not available|waitlist",
    "Clients and outsiders left out": r"client|guest|external|outside (the )?(company|org)|slack connect|vendor|contractor",
    "Black box": r"can't see|cannot see|no visibility|black box|opaque|don't know what|invisible|transparen",
    "It doesn't actually act": r"can't (do|act|take)|read[- ]only|just (a )?chat|only (answers|search|summar)|doesn't actually|glorified|wrapper",
    "Noise": r"spam|noisy|noise|too many (messages|notifications)|annoying|verbose|chatty",
    "Everyone has their own AI": r"duplicate|twice|same (email|task|work)|who (did|is doing|owns)|each (teammate|person) (has|had)|individual|not shared|shared (memory|context)",
    "Generic output": r"generic|mediocre|shallow|low quality|slop|not useful|useless|underwhelm|disappoint",
    "No control, no undo": r"undo|revert|rollback|irreversib|deleted|sent (an|the) email|without asking|approval|went rogue|destruct",
}
NEGATIVE = re.compile(r"\b(but|however|unfortunately|problem|issue|hate|annoy|frustrat|disappoint|worse|worst|can't|cannot|doesn't|didn't|won't|not|no |never|lack|missing|wish|too|only|fail|broke|bug|slow|expensive|scam|wrong|cancel|refund|limit)\b", re.I)


def main(path):
    items = json.load(open(path, encoding="utf-8"))
    urls = collections.defaultdict(set)
    for it in items:
        text = (it.get("texte") or "").replace("\n", " ")
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            sentence = sentence.strip()
            if not (40 <= len(sentence) <= 260) or not NEGATIVE.search(sentence):
                continue
            for name, pattern in FAMILIES.items():
                if re.search(pattern, sentence, re.I):
                    urls[name].add(it["url"])
    out = sorted(({"family": n, "threads": len(urls[n]), "pattern": FAMILIES[n]} for n in FAMILIES), key=lambda x: -x["threads"])
    json.dump(out, open("families.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    with open("sources.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["url", "product", "source"])
        for it in sorted(items, key=lambda x: (x.get("produit") or "", x["url"])):
            w.writerow([it["url"], {"BESOIN": "unmet need (no product)"}.get(it.get("produit"), it.get("produit")), it.get("source")])
    for row in out:
        print(f"{row['threads']:>4}  {row['family']}")


if __name__ == "__main__":
    main(sys.argv[1])

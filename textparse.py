msg = """
Fidelity International | B. Tech CSE related | 1-Year internship (Apprentice) | 2027 POB ||

Monthly Stipend - INR 35,000 ( INR 3780 to be deducted as Provident Fund)
Internship Duration - 12 Months
Tentative DOJ - 31st Aug 2026
Additional Benefits - Free Meals (Lunch & Dinner), Medical Plan, Life Insurance, Accidental Insurance, Subsidised Transport, Leaves, Relocation assistance is provided for students who live outside Delhi/NCR or transport coverage.

Note:
Students from relevant branches as mentioned can apply, however, the final shortlisting of branches / disciplines is at company's discretion.
Students who are eligible & interested should apply through haveloc on or before 09:00AM of 07 May 2026.
"""

import re
msg = msg.lower()

# Ignore common titles
titles = [
    "dr.", "mr.", "ms.", "mrs.", "engg.", "sr.", "jr.", "phd.",
    "b.tech.", "b.tech", "b. tech", "b. tech.",
    "m.tech.", "m.tech", "m. tech", "m. tech.",
    "b.arch.", "b.arch", "b. arch", "b. arch.",
    "m.arch.", "m.arch", "m. arch", "m. arch.",
    "b.des.", "b.des", "b. des", "b. des.",
    "m.des.", "m.des", "m. des", "m. des.",
    "b.engg.", "b.engg", "b. engg", "b. engg.",
    "m.engg.", "m.engg", "m. engg", "m. engg.",
    "f.i."
]

# Sort titles by length (longest first)
titles.sort(key=len, reverse=True)

# Replace . with <DOT> in the titles
for title in titles:
    if "." in title:
        safe_title = title.replace(".", "<DOT>")
        msg = msg.replace(title, safe_title)

# Split the string using a regular expression for separators: . \n ; ? ! || |
segments = re.split(r'\.|\n|;|\?|!|\|\||\|', msg)

# Clean up the segments and restore the periods
res = []
for segment in segments:
    clean_segment = segment.replace("<DOT>", ".").strip()
    
    # Only add non-empty segments
    if clean_segment:
        res.append(clean_segment)

print(res)
        

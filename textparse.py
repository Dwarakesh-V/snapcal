from typing import List
import re

def split_text(msg: str) -> List[str]:
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

    return res

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

print(split_text(msg))

time_examples = """
    Meeting tomorrow
    Meeting day after tomorrow
    Meeting on May 10
    Meeting on 10th May
    Meeting on 10 May
    Meeting on 10/05/2026
    Meeting at 10:00 AM
    Meeting at 10 
    We have a meeting. It's on 10 May at 10 AM
    I have a meeting with him on 10th may at 10am
    Let's catch up at 10am on Monday
    Exam starts next week Friday
    The interview is on 10/05/2026 10:00 AM
    We have to go to college. Tomorrow and the day after
    Let's have a presentation tomorrow at 10am
    I will call you back on Monday
    She said she will call me back on Monday
    Let's meet on Monday
    Test on 3rd, Interview on 5th, Hackathon on 10th
    Final interview on May 10th at 10:30 AM.
    He is the 1st in class
    The 10:00am slot is full
    Free food is provided. The hackathon days are scheduled to be 10,11 and 12 May. Ashwin is the 1st in class. 
"""
    

#!/usr/bin/env python3
"""
clean_leads.py (v2.2) - Ultra-Clean Lead Formatting
- Fixes compound email prefix collisions (elite -> Eli, tomball -> Tom, georgetown -> George, elizabeth -> Elizabeth)
- Strips SEO keyword stuffing from company names (-- or commas)
- Blocks font/template emails (typedesign)
Input: verified_shops.csv
Output: campaign_ready_leads.csv
"""

import os
import re
import csv

INPUT_FILE = "verified_shops.csv"
OUTPUT_FILE = "campaign_ready_leads.csv"

LEGAL_SUFFIXES = [
    r",?\s*\bL\.?L\.?C\.?\b",
    r",?\s*\bINC\.?\b",
    r",?\s*\bCORP\.?\b",
    r",?\s*\bCORPORATION\b",
    r",?\s*\bLTD\.?\b",
    r",?\s*\bLIMITED\b",
    r",?\s*\bP\.?L\.?L\.?C\.?\b",
    r",?\s*\bP\.?C\.?\b",
    r",?\s*\bCO\.?\b",
    r",?\s*\bCOMPANY\b",
]

CORPORATE_CHAINS = {
    "valvoline", "caliber collision", "service king", "firestone", "jiffy lube",
    "meineke", "midas", "pep boys", "ntb", "discount tire", "goodyear",
    "christian brothers", "gerber collision", "maaco", "aamco", "safelite",
    "texaco", "chevron", "sun auto service"
}

CITY_NAME_COLLISIONS = {
    "austin", "allen", "bryan", "tyler", "kyle", "victoria", "marshall",
    "taylor", "paris", "clyde", "brady", "clifton", "jasper", "kermit", "vernon",
    "tomball", "georgetown", "angelo", "houston", "dallas", "irving", "denton"
}

# যেসব শব্দের শুরুতে মানুষের নামের অক্ষর থাকে কিন্তু আসলে সেগুলো নাম নয় (যেমন: elite -> eli, tomball -> tom)
COMPOUND_COLLISIONS = (
    "elite", "tomball", "georgetown", "angelo", "jones", "davidson", "richardson",
    "anaheim", "anatire", "allready", "allstar", "allen", "austin", "bryan", "tyler",
    "christian", "christopher", "franklin", "jackson", "jefferson", "madison", "monroe",
    "washington", "hamilton", "lincoln", "garland", "harlingen", "rosenberg", "sherman",
    "raymondville", "stephenville", "robstown", "levelland", "marlin", "martindale"
)

KNOWN_FIRST_NAMES = {
    "aaron", "adam", "adrian", "alan", "albert", "alec", "alex", "alexander", "ali", "allen",
    "amanda", "amber", "amy", "ana", "andre", "andrea", "andrew", "andy", "angel", "angela",
    "anna", "anthony", "antonio", "arthur", "ashley", "austin", "barbara", "barry", "ben",
    "benjamin", "betty", "bill", "billy", "bob", "bobby", "brad", "bradley", "brandon",
    "brenda", "brian", "bruce", "bryan", "carlos", "carol", "carolyn", "cesar", "chad",
    "charles", "charlie", "cheryl", "chris", "christian", "christina", "christine",
    "christopher", "cindy", "clint", "cody", "corey", "craig", "crystal", "curtis", "cynthia",
    "dale", "damon", "dan", "dana", "daniel", "danny", "darrell", "darren", "dave", "david",
    "dawn", "dean", "deborah", "debra", "denise", "dennis", "derek", "devin", "diana", "diane",
    "don", "donald", "donna", "donny", "dorothy", "doug", "douglas", "dustin", "ed", "eddie",
    "edgar", "eduardo", "edward", "edwin", "eli", "elizabeth", "emily", "eric", "erick",
    "ernesto", "eugene", "evan", "eve", "evelyn", "fernando", "francisco", "frank", "fred",
    "freddy", "gabriel", "gary", "george", "gerald", "gilbert", "glenda", "glenn", "gloria",
    "gordon", "grace", "greg", "gregory", "gus", "hanna", "hannah", "harold", "harry",
    "harvey", "heather", "hector", "helen", "henry", "howard", "hugo", "ian", "isaac", "ivan",
    "jack", "jacob", "jacqueline", "jaime", "jake", "james", "jamie", "jane", "janet", "janice",
    "jared", "jason", "javier", "jay", "jean", "jeff", "jeffrey", "jennifer", "jeremy", "jerry",
    "jesse", "jess", "jessica", "jesus", "jill", "jim", "jimmy", "joan", "joe", "joel", "joey",
    "john", "johnny", "jon", "jonathan", "jordan", "jorge", "jose", "joseph", "josh", "joshua",
    "joyce", "juan", "judith", "judy", "julia", "julian", "julie", "julio", "justin", "karen",
    "katherine", "kathleen", "kathryn", "kathy", "katie", "keith", "kelly", "ken", "kenneth",
    "kevin", "kim", "kimberly", "kirk", "kurt", "kyle", "lance", "larry", "laura", "lauren",
    "lawrence", "lee", "leo", "leon", "leonard", "leslie", "lewis", "linda", "lindsey", "lisa",
    "lloyd", "logan", "lori", "louis", "luis", "luke", "lynn", "manuel", "marc", "marco",
    "marcos", "marcus", "margaret", "maria", "marie", "marilyn", "mario", "mark", "martha",
    "martin", "marty", "marvin", "mary", "matt", "matthew", "maurice", "max", "megan",
    "melissa", "melvin", "micah", "michael", "michelle", "miguel", "mike", "milton", "mitchell",
    "mohammed", "moises", "monica", "nancy", "nathan", "neil", "nelson", "newman", "nicholas",
    "nick", "nicole", "noah", "norma", "norman", "olivia", "omar", "oscar", "pamela",
    "patricia", "patrick", "paul", "paula", "pedro", "peggy", "perry", "pete", "peter", "phil",
    "philip", "phillip", "phyllis", "rachel", "rafael", "ralph", "ramon", "randall", "randy",
    "raul", "ray", "raymond", "rebecca", "rene", "ricardo", "rich", "richard", "rick", "ricky",
    "rita", "rob", "robert", "roberto", "robin", "rodney", "roger", "roland", "ron", "ronald",
    "ronnie", "rose", "ross", "roy", "ruben", "russell", "ruth", "ryan", "sam", "samantha",
    "samuel", "sandra", "sara", "sarah", "scott", "sean", "sergio", "seth", "shane", "shannon",
    "sharon", "shaun", "shawn", "shirley", "sidney", "stan", "stanley", "stephanie", "stephen",
    "steve", "steven", "stewart", "stuart", "susan", "tammy", "tanya", "ted", "teresa", "terry",
    "theresa", "thomas", "tiffany", "tim", "timothy", "tina", "todd", "tom", "tomas", "tommy",
    "tony", "tracy", "travis", "trevor", "troy", "tyler", "valerie", "vanessa", "vernon",
    "veronica", "victor", "victoria", "vincent", "virginia", "wade", "walter", "wanda",
    "warren", "wayne", "wendy", "wesley", "will", "willard", "william", "willie", "zach", "zachary"
}

BAD_EMAIL_DOMAINS = {
    "email.com", "example.com", "domain.com", "schedulista.com", "codelifter.com",
    "sentry.io", "wixpress.com", "cloudflare.com", "schema.org", "snowman.cn",
    "valvoline.com", "chevron.com", "nvmarketingco.com", "eyebytes.com", "lab6.com",
    "sansoxygen.com", "micahrich.com", "lowmaintenancelandscape.net", "richmondpm.ca"
}

BAD_EXACT_EMAILS = {
    "john@gmail.com", "test@gmail.com", "info@gmail.com", "admin@gmail.com",
    "user@gmail.com", "jonpinhorn.typedesign@gmail.com"
}

BAD_EMAIL_PREFIXES = {
    "your", "name", "example", "test", "sample", "user", "noreply", "no-reply"
}

GENERIC_EMAIL_PREFIXES = {
    "info", "contact", "marketing", "sales", "service", "support", "admin", "office",
    "billing", "manager", "management", "dispatch", "estimating", "estimator", "inquiry",
    "general", "customercare", "customerservice", "help", "hello", "mail", "repair",
    "parts", "feedback", "frontdesk", "inbox", "team", "care", "auto", "shop"
}

ACRONYMS = {"BMW", "USA", "ATX", "DFW", "HTX", "TX", "NW", "NE", "SW", "SE", "II", "III", "VIP", "PRO", "BBS", "MD", "AA", "JB", "JC", "JJ", "JR", "RV", "AC", "P3", "ASE", "GMR", "A1"}

def clean_company_name(raw_name):
    if not raw_name:
        return ""
    
    name = raw_name.strip()
    name = re.sub(r"[™®©]", "", name)
    # সাব-ব্রাঞ্চ, ডাবল হাইফেন (--), ডট বা লম্বা এসইও ট্যাগলাইন কেটে ফেলা
    name = re.split(r"\s+[-–|•:]\s+|--|\s*\(|\.\s*[A-Z]", name)[0].strip()

    for suffix_pat in LEGAL_SUFFIXES:
        name = re.sub(suffix_pat, "", name, flags=re.I).strip()

    # যদি নামের মধ্যে কমা থাকে এবং নাম অনেক বড় হয়, তবে কমার আগের অংশ নেওয়া
    if "," in name and len(name.split()) > 4:
        name = name.split(",")[0].strip()

    name = re.sub(r"[,.\s\-_]+$", "", name).strip()
    name = re.sub(r"\s+", " ", name)

    if name.isupper() or name.islower():
        words = []
        for w in name.split():
            w_clean = re.sub(r"[^A-Za-z0-9]", "", w).upper()
            if w_clean in ACRONYMS:
                words.append(w.upper())
            else:
                words.append(w.capitalize())
        name = " ".join(words)
        name = re.sub(r"['’]S\b", "'s", name)

    return name

def infer_first_name(company_name, email):
    # Strategy 1: সবার আগে ইমেইল প্রিফিক্স চেক করা
    if email and "@" in email:
        prefix = email.split("@")[0].lower()
        prefix_clean = re.sub(r"\d+", "", prefix).strip("._-")
        
        if not any(prefix_clean.startswith(gp) for gp in GENERIC_EMAIL_PREFIXES):
            # 1a. ডট, আন্ডারস্কোর বা হাইফেন দিয়ে আলাদা করা নাম (যেমন: "robert.johnson", "jess_bolyard")
            parts = re.split(r"[._\-]+", prefix_clean)
            cand = parts[0] if parts else ""
            if cand in KNOWN_FIRST_NAMES and cand not in CITY_NAME_COLLISIONS:
                return cand.capitalize()

            # 1b. একসাথে লেখা নাম (যেমন: "evehernandez" -> "Eve", "elizabeth" -> "Elizabeth")
            # তবে নিশ্চিত করা যে এটি "elite", "tomball", "georgetown", "angelo" ইত্যাদি শব্দ নয়
            if not any(prefix_clean.startswith(cc) for cc in COMPOUND_COLLISIONS):
                comp_first_word = re.split(r"[\s,'’&]+", company_name.lower())[0]
                # যদি ইমেইল প্রিফিক্সটি হুবহু কোম্পানির প্রথম শব্দের সমান না হয় (অথবা ৪+ অক্ষরের নাম হয়)
                for kn in sorted(KNOWN_FIRST_NAMES, key=len, reverse=True):
                    if len(kn) >= 4 and prefix_clean.startswith(kn):
                        if kn not in CITY_NAME_COLLISIONS and not comp_first_word.startswith(kn + "s"):
                            return kn.capitalize()
                    elif len(kn) == 3 and prefix_clean == kn:
                        if kn not in CITY_NAME_COLLISIONS:
                            return kn.capitalize()

    # Strategy 2: কোম্পানির নামে অ্যাপোস্ট্রফি ('s) থাকলে (যেমন: "Newman's Automotive" -> "Newman")
    possessive_match = re.match(r"^([A-Za-z]+)['’]s\b", company_name)
    if possessive_match:
        cand = possessive_match.group(1).lower()
        if cand in KNOWN_FIRST_NAMES and cand not in CITY_NAME_COLLISIONS:
            return cand.capitalize()

    # Strategy 3: কোম্পানির প্রথম শব্দ যদি মানুষের নাম হয় এবং শহরের নাম বা কলিশন শব্দ না হয়
    first_word = re.split(r"[\s,'’&]+", company_name)[0].lower()
    if (
        first_word in KNOWN_FIRST_NAMES 
        and first_word not in CITY_NAME_COLLISIONS 
        and not any(first_word.startswith(cc) for cc in COMPOUND_COLLISIONS)
    ):
        return first_word.capitalize()

    return ""

def clean_address(raw_address):
    if not raw_address:
        return ""
    addr = re.sub(r"\b(Open|Closed|Opens|Closes)\b.*$", "", raw_address, flags=re.I).strip()
    addr = re.sub(r"[,.\s\-_]+$", "", addr).strip()
    return addr

def is_valid_campaign_email(email, company_name):
    if not email or "@" not in email:
        return False
    if email in BAD_EXACT_EMAILS:
        return False
    prefix, domain = email.split("@", 1)
    if domain in BAD_EMAIL_DOMAINS or any(bad in domain for bad in BAD_EMAIL_DOMAINS):
        return False
    if prefix in BAD_EMAIL_PREFIXES:
        return False
    comp_lower = company_name.lower()
    if any(chain in comp_lower for chain in CORPORATE_CHAINS):
        return False
    return True

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file '{INPUT_FILE}' not found!")
        return

    clean_leads = []
    seen_emails = set()
    seen_websites = set()

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row.get("email", "").strip().lower()
            website = row.get("website", "").strip().lower()
            cleaned_company = clean_company_name(row.get("name", ""))

            if not is_valid_campaign_email(email, cleaned_company):
                continue
            if email in seen_emails or (website and website in seen_websites):
                continue

            first_name = infer_first_name(cleaned_company, email)
            cleaned_addr = clean_address(row.get("address", ""))

            lead = {
                "First Name": first_name,
                "Company Name": cleaned_company,
                "Email": email,
                "Website": row.get("website", "").strip(),
                "Phone": row.get("phone", "").strip(),
                "Address": cleaned_addr,
                "City": row.get("city", "").strip().title(),
                "State": row.get("state", "").strip().upper()
            }

            seen_emails.add(email)
            if website:
                seen_websites.add(website)
            clean_leads.append(lead)

    fieldnames = [
        "First Name", "Company Name", "Email", "Website", "Phone",
        "Address", "City", "State"
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for lead in clean_leads:
            writer.writerow(lead)

    fn_filled = sum(1 for l in clean_leads if l["First Name"])
    print("\n" + "=" * 55)
    print("✨ Cleaned Leads & Campaign Formatting Summary (v2.2):")
    print(f"   Input Verified Leads  : {INPUT_FILE}")
    print(f"   Campaign-Ready Leads  : {len(clean_leads)}")
    print(f"   Verified Human Names  : {fn_filled}")
    print(f"   Final CSV Output File : {OUTPUT_FILE}")
    print("=" * 55 + "\n")

if __name__ == "__main__":
    main()

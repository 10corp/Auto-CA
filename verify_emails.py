#!/usr/bin/env python3
"""
verify_emails.py - DNS & MX Record Email Verification
Validates syntax, checks disposable email domains, and checks DNS MX records.
Input: shops_with_emails.csv
Output: verified_shops.csv
"""

import os
import re
import csv
import dns.resolver

INPUT_FILE = "shops_with_emails.csv"
OUTPUT_FILE = "verified_shops.csv"

# Disposable / Temporary email domains
DISPOSABLE_DOMAINS = {
    "mailinator.com", "trashmail.com", "guerrillamail.com", "tempmail.com",
    "10minutemail.com", "yopmail.com", "sharklasers.com", "getairmail.com",
    "throwawaymail.com", "fakeinbox.com", "dispostable.com"
}

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# Cache to avoid duplicate DNS lookups for same domain
domain_cache = {}

def check_domain_mx(domain):
    domain = domain.lower().strip()
    if domain in domain_cache:
        return domain_cache[domain]

    if domain in DISPOSABLE_DOMAINS or any(ign in domain for ign in ("sentry", "wixpress", "cloudflare", "schema.org")):
        domain_cache[domain] = (False, "invalid_or_tracking_domain")
        return False, "invalid_or_tracking_domain"

    try:
        try:
            resolver = dns.resolver.Resolver()
        except Exception:
            resolver = dns.resolver.Resolver(configure=False)
            resolver.nameservers = ['8.8.8.8', '1.1.1.1', '8.8.4.4']
        
        if not getattr(resolver, 'nameservers', None):
            resolver.nameservers = ['8.8.8.8', '1.1.1.1', '8.8.4.4']

        resolver.timeout = 4.0
        resolver.lifetime = 4.0
        
        # 1. Lookup MX records
        try:
            answers = resolver.resolve(domain, "MX")
            if answers:
                mx_host = str(answers[0].exchange).rstrip(".")
                domain_cache[domain] = (True, f"mx_found:{mx_host}")
                return True, f"mx_found:{mx_host}"
        except (dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            pass

        # 2. RFC fallback: if no MX record, check A record
        try:
            answers_a = resolver.resolve(domain, "A")
            if answers_a:
                ip = str(answers_a[0].address)
                domain_cache[domain] = (True, f"a_record_fallback:{ip}")
                return True, f"a_record_fallback:{ip}"
        except Exception:
            pass

        domain_cache[domain] = (False, "no_mx_or_a_record")
        return False, "no_mx_or_a_record"

    except dns.resolver.NXDOMAIN:
        domain_cache[domain] = (False, "domain_does_not_exist")
        return False, "domain_does_not_exist"
    except dns.exception.Timeout:
        # Give benefit of doubt on timeout or treat as valid domain
        domain_cache[domain] = (True, "dns_timeout_assumed_valid")
        return True, "dns_timeout_assumed_valid"
    except Exception as e:
        domain_cache[domain] = (False, f"dns_error:{type(e).__name__}")
        return False, f"dns_error:{type(e).__name__}"

def verify_lead(lead):
    email = lead.get("email", "").strip()
    if not email:
        return False, "missing_email"

    if not EMAIL_REGEX.match(email):
        return False, "invalid_syntax"

    try:
        user_part, domain_part = email.rsplit("@", 1)
    except ValueError:
        return False, "malformed_email"

    is_valid, reason = check_domain_mx(domain_part)
    return is_valid, reason

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file '{INPUT_FILE}' not found!")
        return

    verified_leads = []
    seen_verified_emails = set()
    total = 0
    valid_count = 0
    invalid_count = 0

    # 1. Load previously verified leads
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as vf:
                r_prev = csv.DictReader(vf)
                for row_prev in r_prev:
                    clean_prev = {k: v for k, v in row_prev.items() if k is not None}
                    em = clean_prev.get("email", "").strip().lower()
                    if em and "@" in em and EMAIL_REGEX.match(em):
                        seen_verified_emails.add(em)
                        verified_leads.append(clean_prev)
            if verified_leads:
                print(f"📂 Loaded {len(verified_leads)} already verified leads from '{OUTPUT_FILE}'.")
        except Exception:
            pass

    print(f"🔍 Reading leads from '{INPUT_FILE}'...")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = [fn for fn in (reader.fieldnames or []) if fn is not None]
        for row in reader:
            clean_row = {k: v for k, v in row.items() if k is not None}
            email = clean_row.get("email", "").strip().lower()
            name = clean_row.get("name", "Unknown Shop")

            if not email or "@" not in email or not EMAIL_REGEX.match(email):
                continue

            if email in seen_verified_emails:
                continue

            total += 1
            is_valid, reason = verify_lead(clean_row)
            if is_valid:
                valid_count += 1
                clean_row["mx_status"] = "Valid"
                verified_leads.append(clean_row)
                seen_verified_emails.add(email)
                print(f"   ✅ [VALID] {name} -> {email} ({reason})")
            else:
                invalid_count += 1
                print(f"   ❌ [INVALID] {name} -> {email} ({reason})")

    # If all emails were invalid or empty (fallback safeguard), keep input rows with note
    if not verified_leads and total > 0:
        print("⚠️ Warning: No valid MX records found, retaining leads with unverified status.")
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean_row = {k: v for k, v in row.items() if k is not None}
                em = clean_row.get("email", "").strip().lower()
                if em and "@" in em and EMAIL_REGEX.match(em):
                    clean_row["mx_status"] = "Unverified"
                    verified_leads.append(clean_row)

    # Ensure fieldnames has mx_status
    out_fieldnames = [fn for fn in fieldnames if fn is not None]
    if "mx_status" not in out_fieldnames:
        out_fieldnames.append("mx_status")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames, extrasaction="ignore")
        writer.writeheader()
        for lead in verified_leads:
            clean_lead = {k: v for k, v in lead.items() if k is not None}
            writer.writerow(clean_lead)

    print("\n" + "=" * 50)
    print("📊 DNS & MX Verification Summary:")
    print(f"   Total Checked : {total}")
    print(f"   Valid / Active: {valid_count}")
    print(f"   Invalid / Dead: {invalid_count}")
    print(f"   Output File   : {OUTPUT_FILE} ({len(verified_leads)} records)")
    print("=" * 50)

if __name__ == "__main__":
    main()

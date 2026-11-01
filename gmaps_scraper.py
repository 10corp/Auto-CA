#!/usr/bin/env python3
"""
gmaps_scraper.py - Controlled Google Maps Auto Body Scraper
Features:
- Full IP Protection (Humanized random delays, webdriver masking, CAPTCHA detection)
- Resume from exact last record (completed_queries.txt)
- Controlled batch execution (--limit N)
"""

import os
import sys
import re
import csv
import time
import random
import argparse
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

OUTPUT_FILE = "shops.csv"
QUERIES_FILE = "queries.txt"
COMPLETED_QUERIES_FILE = "completed_queries.txt"

# Default configuration
DEFAULT_QUERIES = [
    "auto body shop in Austin TX",
    "auto body shop in Dallas TX",
    "auto body shop in Houston TX"
]
MAX_RESULTS_PER_QUERY = 120   # Maximum depth Google Maps can load per query
BATCH_SIZE = 3                # Batch grouping
DEFAULT_BATCH_DELAY = 60      # 1 minute (60s) pause between batches

def clean_text(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()

def extract_phone(text):
    if not text:
        return ""
    m = re.search(r"(\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})", text)
    return m.group(1).strip() if m else ""

def parse_city_state(query, address):
    city, state = "", "TX"
    m = re.search(r"\bin\s+([A-Za-z\s]+)\s+([A-Z]{2})\b", query, re.I)
    if m:
        city = m.group(1).strip().title()
        state = m.group(2).upper()
    elif address:
        m2 = re.search(r",\s*([A-Za-z\s]+),\s*([A-Z]{2})\b", address)
        if m2:
            city = m2.group(1).strip()
            state = m2.group(2).upper()
    return city, state

def load_completed_queries():
    if os.path.exists(COMPLETED_QUERIES_FILE):
        try:
            with open(COMPLETED_QUERIES_FILE, "r", encoding="utf-8") as f:
                return set(line.strip().lower() for line in f if line.strip())
        except Exception:
            pass
    return set()

def mark_query_completed(query):
    try:
        with open(COMPLETED_QUERIES_FILE, "a", encoding="utf-8") as f:
            f.write(query.strip() + "\n")
    except Exception:
        pass

def load_existing_shops():
    shops = []
    seen_websites = set()
    seen_names = set()
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    shops.append(r)
                    if r.get("website"):
                        seen_websites.add(r["website"].lower().strip())
                    if r.get("name"):
                        seen_names.add(r["name"].lower().strip())
        except Exception:
            pass
    return shops, seen_websites, seen_names

def save_shops(shops):
    fieldnames = ["name", "website", "phone", "address", "city", "state", "rating"]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in shops:
            writer.writerow(s)

def scrape_google_maps(queries, max_per_query=MAX_RESULTS_PER_QUERY, query_limit=None, batch_delay=DEFAULT_BATCH_DELAY):
    all_shops, seen_websites, seen_names = load_existing_shops()
    completed_queries = load_completed_queries()
    
    # Filter only uncompleted queries
    pending_queries = [q for q in queries if q.lower().strip() not in completed_queries]
    
    initial_count = len(all_shops)
    total_in_file = len(queries)
    already_done = len(completed_queries)

    print(f"\n📊 PIPELINE STATUS:")
    print(f"   • Total Queries in Plan : {total_in_file}")
    print(f"   • Completed Previously  : {already_done}")
    print(f"   • Remaining to Process  : {len(pending_queries)}")
    print(f"   • Total Unique Shops    : {initial_count}")

    if not pending_queries:
        print("\n🎉 All queries in queries.txt are already completed!")
        print("💡 Delete 'completed_queries.txt' if you want to restart from scratch.")
        return all_shops

    # Apply user-requested limit (e.g. run only 3 queries today)
    if query_limit and query_limit > 0:
        queries_to_run = pending_queries[:query_limit]
        print(f"🎯 Controlled Mode Active: Processing next {len(queries_to_run)} queries (out of {len(pending_queries)} remaining).")
    else:
        queries_to_run = pending_queries
        print(f"🎯 Full Mode: Processing all {len(queries_to_run)} remaining queries.")

    print(f"🛡️ Anti-Block Protection: Human jitter enabled | {batch_delay}s delay between 3-query batches\n")

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        context = browser.new_context(
            locale="en-US",
            user_agent=random.choice(user_agents),
            viewport={"width": 1366, "height": 768}
        )
        page = context.new_page()

        # Stealth: Hide webdriver flag
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        new_shops_added = 0

        for q_idx, query in enumerate(queries_to_run, 1):
            print(f"\n" + "=" * 60)
            print(f"[{q_idx}/{len(queries_to_run)}] 🔎 Searching: '{query}'")
            print("=" * 60)

            search_url = f"https://www.google.com/maps/search/{quote_plus(query)}?hl=en"
            
            try:
                page.goto(search_url, wait_until="domcontentloaded", timeout=45000)
            except Exception as e:
                print(f"⚠️ Page load error: {e}")
                continue

            # Anti-Block Check: Detect CAPTCHA or Unusual Traffic prompt
            current_url = page.url.lower()
            if "sorry/index" in current_url or "captcha" in current_url:
                print("\n" + "🛑" * 30)
                print("⚠️ GOOGLE RATE LIMIT / CAPTCHA DETECTED!")
                print("🛑 The scraper is stopping immediately to protect your IP.")
                print("💡 Recommendation: Wait 30-60 minutes or change your IP/VPN before resuming.")
                print("🛑" * 30 + "\n")
                break

            try:
                page.wait_for_selector("div.Nv2PK, div[role='feed']", timeout=15000)
            except Exception:
                print("⚠️ No listing cards found for this query.")
                mark_query_completed(query)
                continue

            feed = page.query_selector("div[role='feed']")
            
            # Slow, humanized continuous scrolling until "You've reached the end of the list."
            print("   📜 Scrolling slowly through results feed...")
            prev_count = 0
            stagnant_count = 0
            max_scrolls = 60

            for scroll_idx in range(1, max_scrolls + 1):
                if feed:
                    # Scroll down gradually in 1000px increments
                    page.evaluate("el => el.scrollBy(0, 1000)", feed)
                
                # Humanized pacing between scrolls
                time.sleep(random.uniform(1.2, 1.8))

                cards_now = len(page.query_selector_all("div.Nv2PK"))

                # Check if Google Maps displayed "You've reached the end of the list."
                reached_end = False
                try:
                    if page.locator("text=You've reached the end of the list").count() > 0:
                        reached_end = True
                    elif page.locator("span.HlvSq").count() > 0:
                        span_text = page.locator("span.HlvSq").first.inner_text().lower()
                        if "end of the list" in span_text:
                            reached_end = True
                    elif page.locator("div.PbZDve").count() > 0:
                        div_text = page.locator("div.PbZDve").first.inner_text().lower()
                        if "end of the list" in div_text:
                            reached_end = True
                except Exception:
                    pass

                if reached_end:
                    print(f"   🏁 Reached 'You\'ve reached the end of the list.' ({cards_now} cards found).")
                    break

                if max_per_query and cards_now >= max_per_query:
                    print(f"   🎯 Reached target limit ({cards_now} listings).")
                    break

                # Progress indicator
                if cards_now != prev_count:
                    stagnant_count = 0
                    print(f"   ↳ Loaded {cards_now} listings (scroll {scroll_idx})...")
                else:
                    stagnant_count += 1
                    # Give Google Maps enough time to load the next chunk (up to 6 stagnant scrolls)
                    if stagnant_count >= 6:
                        print(f"   🏁 Feed ended (no new cards after 6 scrolls, {cards_now} total cards).")
                        break

                prev_count = cards_now

            cards = page.query_selector_all("div.Nv2PK")
            print(f"   📥 Extracting data from {len(cards)} listing cards...")

            q_city, q_state = parse_city_state(query, "")
            query_new = 0

            for card in cards:
                if max_per_query and query_new >= max_per_query:
                    break

                try:
                    name_el = card.query_selector("div.qBF1Pd, div.fontHeadlineSmall")
                    name = clean_text(name_el.inner_text()) if name_el else ""
                    if not name or name.lower().strip() in seen_names:
                        continue

                    # Website link
                    website_el = card.query_selector(
                        "a.lcr4fd, a[data-value*='Website' i], a[aria-label*='website' i], a[href^='http']:not([href*='google.com']):not([href*='schedule']):not([href*='booking'])"
                    )
                    website = website_el.get_attribute("href") if website_el else ""
                    if website:
                        website = website.split("?")[0].strip()

                    if not website:
                        continue

                    website_clean = website.lower().strip()
                    if website_clean in seen_websites:
                        continue

                    # Skip social/directory duplicates
                    if any(d in website_clean for d in ("facebook.com", "instagram.com", "yelp.com", "yellowpages.com")):
                        continue

                    card_text = card.inner_text()
                    phone = extract_phone(card_text)

                    rating_el = card.query_selector("span.MW4etd")
                    rating = rating_el.inner_text().strip() if rating_el else ""

                    address = ""
                    divs = card.query_selector_all("div.W4Efsd")
                    for d in divs:
                        t = clean_text(d.inner_text())
                        if "·" in t:
                            parts = [p.strip() for p in t.split("·")]
                            for part in parts:
                                if re.search(r"\d+\s+[A-Za-z]+", part) and not extract_phone(part):
                                    address = part
                                    break
                        if address:
                            break

                    city, state = parse_city_state(query, address)
                    if not city:
                        city = q_city
                    if not state:
                        state = q_state

                    shop_record = {
                        "name": name,
                        "website": website,
                        "phone": phone,
                        "address": address,
                        "city": city,
                        "state": state,
                        "rating": rating
                    }

                    seen_names.add(name.lower().strip())
                    seen_websites.add(website_clean)
                    all_shops.append(shop_record)
                    query_new += 1
                    new_shops_added += 1
                    print(f"   ➕ [{query_new}] {name} | {website} | {phone}")

                except Exception:
                    continue

            print(f"   ✅ Saved {query_new} new unique shops from '{query}'.")

            # Save immediately and mark query completed
            save_shops(all_shops)
            mark_query_completed(query)

            # Random polite delay between individual queries
            time.sleep(random.uniform(3.0, 5.0))

            # Batch pause if more queries remaining in this run
            if q_idx % BATCH_SIZE == 0 and q_idx < len(queries_to_run):
                print("\n" + "☕" * 30)
                print(f"⏸️ [Safety Batch Pause] Completed {q_idx} queries.")
                mins_delay = batch_delay // 60
                delay_desc = f"{mins_delay} min" if mins_delay >= 1 and batch_delay % 60 == 0 else f"{batch_delay}s"
                print(f"⏳ Waiting {batch_delay}s ({delay_desc}) to protect IP from Google Maps...")
                print("☕" * 30)
                
                for remaining in range(batch_delay, 0, -5):
                    mins, secs = divmod(remaining, 60)
                    time_str = f"{mins:02d}:{secs:02d}"
                    sys.stdout.write(f"\r   ⏳ Next query starting in: {time_str} ({remaining}s)   ")
                    sys.stdout.flush()
                    time.sleep(5)
                
                print("\n\n🚀 Resuming next query batch...\n")

        browser.close()

    print(f"\n🎉 Session complete! Added {new_shops_added} new shops (Database Total: {len(all_shops)}).")
    return all_shops

def main():
    parser = argparse.ArgumentParser(description="Controlled Google Maps Auto Body Scraper")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of queries to run in this session")
    parser.add_argument("--delay", type=int, default=DEFAULT_BATCH_DELAY, help="Delay in seconds after every 3 queries")
    args, unknown = parser.parse_known_args()

    queries = []
    if os.path.exists(QUERIES_FILE):
        with open(QUERIES_FILE, "r", encoding="utf-8") as f:
            queries = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not queries:
        queries = DEFAULT_QUERIES

    scrape_google_maps(queries, max_per_query=MAX_RESULTS_PER_QUERY, query_limit=args.limit, batch_delay=args.delay)

if __name__ == "__main__":
    main()

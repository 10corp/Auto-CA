#!/usr/bin/env python3
"""
run_pipeline.py - Master Controller & Lead Generation Pipeline
Gives you 100% control over scraping batches, pausing, resuming, and anti-ban pacing.
"""

import os
import sys
import time
import argparse
import subprocess

# Ensure line-buffered stdout so tail -f shows live logs immediately under nohup
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(line_buffering=True)

COMPLETED_QUERIES_FILE = "completed_queries.txt"
QUERIES_FILE = "queries.txt"
SHOPS_FILE = "shops.csv"
NO_WEBSITE_FILE = "no-website.csv"
LEADS_FILE = "campaign_ready_leads.csv"

def print_banner(step_num, title):
    print("\n" + "=" * 65)
    print(f"🚀 STEP {step_num}: {title}")
    print("=" * 65 + "\n")

def run_command(command, expected_output_file, step_name):
    start_time = time.time()
    try:
        result = subprocess.run(command, check=True)
        elapsed = round((time.time() - start_time) / 60, 2)
        
        if os.path.exists(expected_output_file) and os.path.getsize(expected_output_file) > 0:
            print(f"\n✅ [{step_name}] সফলভাবে সম্পন্ন হয়েছে! (সময় লেগেছে: {elapsed} মিনিট)")
            print(f"📁 আউটপুট ফাইল: {expected_output_file}")
            return True
        else:
            print(f"\n⚠️ [{step_name}] রান হয়েছে, কিন্তু '{expected_output_file}' ফাইলটি খালি বা পাওয়া যায়নি!")
            return False

    except subprocess.CalledProcessError as e:
        print(f"\n❌ [{step_name}] চলাকালীন সময়ে একটি এরর হয়েছে (Exit Code: {e.returncode})।")
        return False
    except KeyboardInterrupt:
        print(f"\n🛑 ইউজার ম্যানুয়ালি [{step_name}] বন্ধ করেছেন। প্রগ্রেস সেভ রয়েছে।")
        sys.exit(0)

def get_stats():
    total_queries = 0
    if os.path.exists(QUERIES_FILE):
        with open(QUERIES_FILE, "r", encoding="utf-8") as f:
            total_queries = sum(1 for line in f if line.strip() and not line.startswith("#"))

    completed_queries = 0
    if os.path.exists(COMPLETED_QUERIES_FILE):
        with open(COMPLETED_QUERIES_FILE, "r", encoding="utf-8") as f:
            completed_queries = sum(1 for line in f if line.strip())

    shops_count = 0
    if os.path.exists(SHOPS_FILE):
        with open(SHOPS_FILE, "r", encoding="utf-8") as f:
            shops_count = max(0, sum(1 for _ in f) - 1)

    no_web_count = 0
    if os.path.exists(NO_WEBSITE_FILE):
        with open(NO_WEBSITE_FILE, "r", encoding="utf-8") as f:
            no_web_count = max(0, sum(1 for _ in f) - 1)

    leads_count = 0
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            leads_count = max(0, sum(1 for _ in f) - 1)

    next_query = "None (All finished)"
    if os.path.exists(QUERIES_FILE):
        done_set = set()
        if os.path.exists(COMPLETED_QUERIES_FILE):
            with open(COMPLETED_QUERIES_FILE, "r", encoding="utf-8") as f:
                done_set = set(line.strip().lower() for line in f if line.strip())
        with open(QUERIES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                q = line.strip()
                if q and not q.startswith("#") and q.lower() not in done_set:
                    next_query = q
                    break

    return {
        "total_queries": total_queries,
        "completed_queries": completed_queries,
        "remaining_queries": max(0, total_queries - completed_queries),
        "shops_count": shops_count,
        "no_web_count": no_web_count,
        "leads_count": leads_count,
        "next_query": next_query
    }

def print_dashboard():
    s = get_stats()
    pct = round((s['completed_queries'] / s['total_queries']) * 100, 1) if s['total_queries'] > 0 else 0
    print("\n" + "=" * 65)
    print("🎛️  LEAD GENERATION MASTER CONTROL PANEL")
    print("=" * 65)
    print(f"📊 Search Progress       : {s['completed_queries']} / {s['total_queries']} queries done ({pct}%)")
    print(f"⏳ Remaining Queries     : {s['remaining_queries']}")
    print(f"📍 Next Query in Queue   : '{s['next_query']}'")
    print(f"🏢 Shops with Website    : {s['shops_count']} in 'shops.csv' (for Cold Email)")
    print(f"📞 No-Website Leads      : {s['no_web_count']} in '{NO_WEBSITE_FILE}' (for Web Dev Calling)")
    print(f"🎯 Campaign-Ready Leads  : {s['leads_count']} in '{LEADS_FILE}'")
    print("=" * 65)

def run_pipeline(query_limit=None, enrich_only=False):
    total_start = time.time()
    python_exec = sys.executable

    print("\n" + "#" * 65)
    print("🔥 US AUTO SHOP LEAD GENERATION PIPELINE RUNNING 🔥")
    print("#" * 65)

    if not enrich_only:
        # Step 1: Scrape Google Maps with limit
        step_cmd = [python_exec, "-u", "gmaps_scraper.py"]
        if query_limit and query_limit > 0:
            step_cmd.extend(["--limit", str(query_limit)])

        print_banner(1, f"Google Maps Scraping (Target: {query_limit if query_limit else 'All'} queries)")
        if not run_command(step_cmd, "shops.csv", "Google Maps Scraper"):
            print("প্রথম ধাপ অসম্পূর্ণ থাকায় পাইপলাইন স্থগিত করা হয়েছে।")
            return
    else:
        print("\n⏩ [Enrichment Mode]: Skipping Google Maps scraping, using existing 'shops.csv'.")

    # Step 2: Scrapy Email Extraction
    print_banner(2, "Website Email Extraction (email_spider.py)")
    if not run_command([python_exec, "-m", "scrapy", "runspider", "email_spider.py"], "shops_with_emails.csv", "Scrapy Email Spider"):
        print("দ্বিতীয় ধাপ অসম্পূর্ণ থাকায় পাইপলাইন স্থগিত করা হয়েছে।")
        return

    # Step 3: Free DNS & MX Verification
    print_banner(3, "Free DNS & MX Email Verification (verify_emails.py)")
    if not run_command([python_exec, "-u", "verify_emails.py"], "verified_shops.csv", "Email Verifier"):
        print("তৃতীয় ধাপ অসম্পূর্ণ থাকায় পাইপলাইন স্থগিত করা হয়েছে।")
        return

    # Step 4: Lead Cleaning & Formatting
    print_banner(4, "Lead Cleaning & Formatting (clean_leads.py)")
    if not run_command([python_exec, "-u", "clean_leads.py"], "campaign_ready_leads.csv", "Lead Cleaner"):
        print("চতুর্থ ধাপ অসম্পূর্ণ থাকায় পাইপলাইন স্থগিত করা হয়েছে।")
        return

    # Summary
    total_time = round((time.time() - total_start) / 60, 2)
    s = get_stats()
    print("\n" + "🎉" * 32)
    print(f"সেশন সম্পন্ন হয়েছে! সময় লেগেছে: {total_time} মিনিট।")
    print(f"📊 বর্তমানে মোট ক্যাম্পেইন রেডি লিড: {s['leads_count']} টি")
    print(f"📁 ফাইল: '{LEADS_FILE}'")
    print("🎉" * 32 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Master Pipeline Controller")
    parser.add_argument("--batch", type=int, default=None, help="Number of batches (1 batch = 3 queries) to run and then stop")
    parser.add_argument("--queries", type=int, default=None, help="Number of queries to run and then stop")
    parser.add_argument("--continuous", action="store_true", help="Run all remaining queries continuously with 60-second pauses")
    parser.add_argument("--enrich-only", action="store_true", help="Skip Google Maps; only enrich/verify existing shops.csv")
    parser.add_argument("--status", action="store_true", help="Print current progress stats and exit")
    args = parser.parse_args()

    # CLI Direct Modes
    if args.status:
        print_dashboard()
        return

    if args.enrich_only:
        run_pipeline(enrich_only=True)
        return

    if args.batch:
        run_pipeline(query_limit=args.batch * 3)
        return

    if args.queries:
        run_pipeline(query_limit=args.queries)
        return

    if args.continuous:
        run_pipeline(query_limit=None)
        return

    # Check if running non-interactively (e.g. nohup, background redirect, or cron)
    is_interactive = False
    try:
        is_interactive = sys.stdin is not None and hasattr(sys.stdin, "isatty") and sys.stdin.isatty()
    except Exception:
        is_interactive = False

    if not is_interactive:
        print("\n🚀 [Non-Interactive / Background Mode Detected]")
        print("   Auto-starting Continuous Pipeline (60-second pauses between batches).")
        print("   Use 'python3 run_pipeline.py --status' to monitor progress anytime.\n", flush=True)
        run_pipeline(query_limit=None)
        return

    # Interactive Dashboard Menu
    while True:
        print_dashboard()
        print("\nকন্ট্রোল মেনু থেকে পছন্দ করুন:")
        print("  [1] 🛡️  Run 1 Batch (মাত্র ৩টি সার্চ রান করে থেমে যাবে - আপনার IP-র জন্য ১০০% নিরাপদ)")
        print("  [2] 🔢 Run Custom Queries (আপনার ইচ্ছেমতো নির্দিষ্ট সংখ্যক সার্চ রান করুন)")
        print("  [3] ⚡ Run Enrichment ONLY (গুগল ম্যাপে হাত না দিয়ে আগের শপগুলো থেকে ইমেইল বের ও ভেরিফাই করুন)")
        print("  [4] 🚀 Continuous Auto-Run (সব সার্চ বিরতি দিয়ে স্বয়ংক্রিয়ভাবে চলতে থাকবে)")
        print("  [5] 📊 Refresh Status")
        print("  [0] 🛑 Exit")
        
        try:
            choice = input("\nআপনার পছন্দ লিখুন [0-5]: ").strip()
        except (KeyboardInterrupt, EOFError, OSError):
            print("\nবাইরে চলে যাওয়া হয়েছে। প্রগ্রেস সংরক্ষিত আছে।")
            break

        if choice == "1":
            run_pipeline(query_limit=3)
        elif choice == "2":
            try:
                num = int(input("কতগুলো সার্চ রান করতে চান? (যেমন 1, 3, 6): ").strip())
                if num > 0:
                    run_pipeline(query_limit=num)
            except ValueError:
                print("⚠️ দয়া করে একটি সঠিক সংখ্যা লিখুন।")
        elif choice == "3":
            run_pipeline(enrich_only=True)
        elif choice == "4":
            confirm = input("⚠️ এটি সব সার্চ রান করবে (প্রতি ৩টিতে ৬০ সেকেন্ড বিরতিসহ)। শুরু করতে চান? (y/n): ").strip().lower()
            if confirm in ("y", "yes"):
                run_pipeline(query_limit=None)
        elif choice == "5":
            continue
        elif choice == "0":
            print("\nধন্যবাদ! আপনার প্রগ্রেস সংরক্ষিত আছে। যেকোনো সময় আবার রান করতে পারেন।\n")
            break
        else:
            print("⚠️ ভুল পছন্দ। ১ থেকে ৫-এর মধ্যে নির্বাচন করুন।")

if __name__ == "__main__":
    main()

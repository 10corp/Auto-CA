# 🚗 Texas Auto Body Lead Generation Master Pipeline (10,000+ Leads)

একটি সম্পূর্ণ স্বয়ংক্রিয় এবং ফুল-কন্ট্রোলযুক্ত B2B লিড জেনারেশন পাইপলাইন। এটি পুরো টেক্সাস (TX) রাজ্যের সব ইন্ডিপেন্ডেন্ট অটো বডি ও কলিশন রিপেয়ার শপের তথ্য Google Maps থেকে স্ক্র্যাপ করে, অফিশিয়াল ওয়েবসাইট থেকে ইমেইল বের করে, ডোমেইন ও MX রেকর্ড ভেরিফাই করে এবং **Instantly.ai** বা **Smartlead.ai**-তে কোল্ড ইমেইলিংয়ের উপযোগী ক্লিন CSV তৈরি করে।

---

## 🎯 লিড কোয়ালিটি ও ক্লিন ফিল্টার (v2.2 Ultra-Clean)

কোল্ড ইমেইলিংয়ে ১০০% হিউম্যান ফিলিং ও স্প্যাম স্কোর শূন্য রাখতে নিচের ফিল্টারগুলো সক্রিয় রয়েছে:

1. **কম্পাউন্ড সাবস্ট্রিং সংঘর্ষ রোধ (`COMPOUND_COLLISIONS`)**:
   - `elitebrosauto@...` থেকে ভুলবশত "Eli" হওয়া রোধ।
   - `tomballaseauto@...` থেকে শহরের নাম "Tom" হওয়া রোধ।
   - `georgetownmuffler@...` থেকে শহরের নাম "George" হওয়া রোধ।
   - `angelodentremoval@...` থেকে শহরের নাম "Angel" হওয়া রোধ।
   - `jonestire@...` থেকে "Jon" হওয়া রোধ।
2. **নিখুঁত ফিমেল ও ৪+ অক্ষরের নাম ডিটেকশন**:
   - `elizabeth@...` থেকে সঠিকভাবে **Elizabeth** সনাক্ত করা (পূর্বে ভুলবশত "Eli" আসত)।
   - ৩ অক্ষরের নামগুলো শুধুমাত্র হুবহু মিললে (Exact Match) নেওয়া হয়, যাতে কোনো বড় শব্দের অংশ হিসেবে ভুল নাম না বসে।
3. **এসইও কি-ওয়ার্ড স্টাফিং ক্লিন**:
   - ডাবল হাইফেন (`--`), ডট বা কমা দিয়ে ভরা লম্বা গুগল ম্যাপস ট্যাগলাইন স্বয়ংক্রিয়ভাবে ট্রিম করা হয়।
4. **টেমপ্লেট ও ডিজাইনার ইমেইল ব্লক**:
   - `jonpinhorn.typedesign@gmail.com`-এর মতো ফন্ট বা ওয়েবসাইট টেমপ্লেট ডিজাইনারদের ইমেইল ব্লক।
5. **টেক্সাসের শহরের নাম ফিল্টার (`CITY_NAME_COLLISIONS`)**:
   - Austin, Allen, Bryan, Tyler, Kyle, Victoria, Tomball, Georgetown, Angelo ইত্যাদি শহরের নাম কোম্পানিতে থাকলে সেগুলোকে মানুষের নাম ধরা **সম্পূর্ণ বন্ধ**।
6. **কর্পোরেট চেইন ফিল্টার ও ন্যাচারাল Title Case**:
   - Caliber Collision, Valvoline, Firestone, Meineke, Chevron, Texaco ইত্যাদি ন্যাশনাল চেইন বাদ।
   - ALL-CAPS কোম্পানির নামগুলোকে ন্যাচারাল Title Case-এ রূপান্তর।

---

## 🎛️ ফুল-কন্ট্রোল ড্যাশবোর্ড ও মেনু (Full Control Dashboard)

IP ব্লক এড়াতে এবং সম্পূর্ণ নিয়ন্ত্রণ আপনার হাতে রাখতে ইন্টারেক্টিভ কন্ট্রোল ড্যাশবোর্ড যোগ করা হয়েছে।

টার্মিনালে গিয়ে রান করুন:
```bash
cd /home/tuhin/Documents/Auto
python3 run_pipeline.py
```

### কন্ট্রোল মেনুর অপশনসমূহ:
- **[1] 🛡️ Run 1 Batch (৩টি সার্চ):** মাত্র ১টি ব্যাচ রান করে স্বয়ংক্রিয়ভাবে থেমে যাবে (IP সেফটির জন্য সেরা)।
- **[2] 🔢 Run Custom Queries:** নির্দিষ্ট সংখ্যক সার্চ রান করতে (যেমন: ১, ২, ৫টি)।
- **[3] ⚡ Run Enrichment ONLY:** গুগল ম্যাপে হাত না দিয়ে আগের স্ক্র্যাপ করা শপগুলো থেকে নতুন ইমেইল এক্সট্রাক্ট ও ভেরিফাই করতে।
- **[4] 🚀 Continuous Auto-Run:** প্রতি ৩টি সার্চ শেষে ৬০ সেকেন্ড (১ মিনিট) বিরতি দিয়ে স্বয়ংক্রিয়ভাবে চলতে থাকবে।
- **[5] 📊 Refresh Status:** বর্তমান অগ্রগতি ও স্ট্যাটাস রিফ্রেশ করে দেখাবে।
- **[0] 🛑 Exit:** প্রগ্রেস সেভ রেখে যেকোনো সময় নিরাপদে বের হয়ে যাওয়া।

---

## ⚡ কুইক কমান্ড শর্টকাট (CLI Flags)

```bash
# বর্তমান অগ্রগতি ও স্ট্যাটাস দেখতে
python3 run_pipeline.py --status

# মাত্র ১টি ব্যাচ (৩টি সার্চ) রান করে থেমে যেতে
python3 run_pipeline.py --batch 1

# ব্যাকগ্রাউন্ডে স্বয়ংক্রিয়ভাবে পুরো পাইপলাইন রান করে রাখতে (nohup)
nohup python3 run_pipeline.py > pipeline.log 2>&1 &

# ব্যাকগ্রাউন্ডের লাইভ লগ দেখতে
tail -f pipeline.log

# গুগল ম্যাপ ছাড়া শুধু ইমেইল কালেকশন ও ভেরিফিকেশন চালাতে
python3 run_pipeline.py --enrich-only
```

---

## 📁 পাইপলাইনের মূল ফাইলসমূহ

| ফাইল | ভূমিকা | আউটপুট |
|---|---|---|
| [run_pipeline.py](file:///home/tuhin/Documents/Auto/run_pipeline.py) | মাস্টার অর্কেস্ট্রেটর ও কন্ট্রোল ড্যাশবোর্ড | কনসোল ইন্টারফেস |
| [queries.txt](file:///home/tuhin/Documents/Auto/queries.txt) | ৩৪৮টি টেক্সাস সিটি ও কি-ওয়ার্ড তালিকা | ইনপুট কোয়ারি |
| [completed_queries.txt](file:///home/tuhin/Documents/Auto/completed_queries.txt) | সম্পন্ন হওয়া সার্চের লগ (রেজুমের জন্য) | ট্র্যাকিং ফাইল |
| [gmaps_scraper.py](file:///home/tuhin/Documents/Auto/gmaps_scraper.py) | ধাপ ১: ডিপ-স্ক্রলিং গুগল ম্যাপস স্ক্র্যাপার | `shops.csv` |
| [email_spider.py](file:///home/tuhin/Documents/Auto/email_spider.py) | ধাপ ২: ফিল্টারযুক্ত Scrapy ইমেইল এক্সট্রাক্টর | `shops_with_emails.csv` |
| [verify_emails.py](file:///home/tuhin/Documents/Auto/verify_emails.py) | ধাপ ৩: ফ্রি DNS ও MX রেকর্ড ইমেইল ভেরিফায়ার | `verified_shops.csv` |
| [clean_leads.py](file:///home/tuhin/Documents/Auto/clean_leads.py) | ধাপ ৪: v2.2 আল্ট্রা-ক্লিন লিড ফরম্যাটার | `campaign_ready_leads.csv` |
| [generate_tx_queries.py](file:///home/tuhin/Documents/Auto/generate_tx_queries.py) | ৩৪৮টি টেক্সাস সার্চ কোয়ারি জেনারেটর | `queries.txt` |
| [campaign_ready_leads.csv](file:///home/tuhin/Documents/Auto/campaign_ready_leads.csv) | চূড়ান্ত ভেরিফাইড ও ১০০% ক্লিন লিড তালিকা | প্রস্তুত আউটপুট |

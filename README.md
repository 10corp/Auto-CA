# 🚗 California Auto Body Lead Generation Master Pipeline (10,000+ Leads)

একটি সম্পূর্ণ স্বয়ংক্রিয় এবং ফুল-কন্ট্রোলযুক্ত B2B লিড জেনারেশন পাইপলাইন। এটি পুরো ক্যালিফোর্নিয়া (CA) রাজ্যের ১৯০টি প্রধান শহর ও মেট্রোপলিটন এলাকার (Los Angeles, Orange County, Bay Area, San Diego, Inland Empire, Central Valley, Central Coast) সব ইন্ডিপেন্ডেন্ট অটো বডি ও কলিশন রিপেয়ার শপের তথ্য Google Maps থেকে স্ক্র্যাপ করে এবং **টু-স্ট্রিম (Two-Stream)** আউটপুট তৈরি করে:

1. **📧 স্ট্রিম ১ (কোল্ড ইমেইলিং লিড):** যাদের অফিশিয়াল ওয়েবসাইট আছে তাদের ওয়েবসাইট থেকে ইমেইল বের করে, ডোমেইন ও MX রেকর্ড ভেরিফাই করে এবং **Instantly.ai** বা **Smartlead.ai**-তে সরাসরি আপলোড উপযোগী ক্লিন CSV তৈরি করে (`campaign_ready_leads.csv`)।
2. **📞 স্ট্রিম ২ (ওয়েব ডেভেলপমেন্ট সার্ভিস কোল্ড কলিং / FB এনরিচমেন্ট লিড):** গুগল ম্যাপসে যেসব অটো শপের কোনো ওয়েবসাইট নেই, তাদেরকে আলাদা ফাইলে সংরক্ষণ করে (`no-website.csv`), যাতে আপনার সেলস টিম সরাসরি ফোন করে ওয়েবসাইট তৈরি ও লোকাল এসইও (Web Development & SEO) সার্ভিস সেল করতে পারে, অথবা Outscraper / Scrap.io দিয়ে তাদের ফেসবুক পেজ থেকে ওনারের সরাসরি ইমেইল ও মোবাইল নম্বর বের করা যায়!

---

## 🗄️ পূর্ববর্তী স্টেটগুলোর ব্যাকআপ স্ট্যাটাস (Archive Data)

| স্টেট (State) | ব্যাকআপ ফোল্ডার | মোট কুয়েরি | ওয়েবসাইটযুক্ত শপ (`shops.csv`) | ওয়েবসাইটবিহীন লিড (`no-website.csv`) | ক্যাম্পেইন-রেডি লিড (`campaign_ready_leads.csv`) |
|---|---|---|---|---|---|
| **Florida (FL)** | [`fl_archive/`](file:///home/tuhin/Documents/Auto/fl_archive/) | 726 / 716 (100% Done) | **7,160 টি** | **5,064 টি** | **2,651 টি** |
| **Texas (TX)** | [`tx_archive/`](file:///home/tuhin/Documents/Auto/tx_archive/) | সম্পূর্ণ সম্পন্ন | সংরক্ষিত | সংরক্ষিত | সংরক্ষিত |

> [!NOTE]
> ফ্লোরিডা (FL)-এর সমস্ত স্ক্র্যাপড ডাটা, ভেরিফাইড ইমেইল এবং রিয়েল-টাইম লগ `fl_archive/` ডিরেক্টরিতে অক্ষত অবস্থায় ব্যাকআপ রাখা হয়েছে।

---

## 🏗️ টু-স্ট্রিম আর্কিটেকচার (California Pipeline Architecture)

```
                       [ 🔎 Google Maps Scraping ]
                       (১৯০টি ক্যালিফোর্নিয়া শহর x ৪ কি-ওয়ার্ড = ৭৬০ কুয়েরি)
                                   │
          ┌────────────────────────┴────────────────────────┐
          ▼                                                 ▼
[ 🌐 যাদের নিজস্ব ওয়েবসাইট আছে ]                   [ 📵 যাদের কোনো ওয়েবসাইট নেই ]
          │                                                 │
          ▼                                                 ▼
     shops.csv                                        no-website.csv
          │                                        (সরাসরি ওয়েব ডেভেলপমেন্ট সেলস কল
          ▼                                         বা Outscraper / Scrap.io দিয়ে
   email_spider.py (Scrapy ক্রলার)                   ফেসবুক পেজ এনরিচমেন্ট করার জন্য)
          │
          ▼
   verify_emails.py (DNS & MX ভেরিফিকেশন)
          │
          ▼
   clean_leads.py (v2.2 হিউম্যান নেইম & টাইটেল কেস)
          │
          ▼
🎯 campaign_ready_leads.csv
(Instantly.ai / Smartlead.ai-এর জন্য প্রস্তুত)
```

---

## 📁 আউটপুট ফাইল ও কলাম স্পেসিফিকেশন

### ১. `campaign_ready_leads.csv` (কোল্ড ইমেইল ক্যাম্পেইনের জন্য)
| কলাম | উদাহরণ | বিবরণ |
|---|---|---|
| **First Name** | *Carlos* | যাচাইকৃত হিউম্যান ফার্স্ট নেম (না থাকলে ব্ল্যাঙ্ক) |
| **Company Name** | *Pacific Coast Collision Center* | ন্যাচারাল Title Case ও এসইও ট্যাগলাইনমুক্ত নাম |
| **Email** | *carlos@pacificcoastcollision.com* | MX রেকর্ড ভেরিফাইড অ্যাক্টিভ বিজনেস ইমেইল |
| **Website** | *https://pacificcoastcollision.com* | শপের অফিশিয়াল ওয়েবসাইট |
| **Phone** | *+1 213-555-0144* | ইউএস ফরম্যাটের ফোন নম্বর |
| **Address** | *1200 S Figueroa St* | শপের ফিজিক্যাল ঠিকানা |
| **City** | *Los Angeles* | ক্যালিফোর্নিয়ার শহর |
| **State** | *CA* | স্টেট কোড |

### ২. `no-website.csv` (ওয়েব ডেভেলপমেন্ট কোল্ড কলিং ও ফেসবুক লিড এক্সট্রাকশনের জন্য)
| কলাম | উদাহরণ | কোল্ড কলিং / সার্ভিসে ব্যবহারের সুবিধা |
|---|---|---|
| **name** | *VALLEY AUTO BODY CRAFT* | শপের আসল নাম ধরে কল শুরু করার জন্য |
| **phone** | *+1 818-555-0199* | সরাসরি শপ ওনার বা ম্যানেজারের সাথে যোগাযোগের নম্বর |
| **address** | *7500 Sepulveda Blvd* | শপের লোকাল লোকেশন যাচাই করতে |
| **city / state** | *Van Nuys, CA* | লোকাল রেফারেন্স দিতে |
| **rating** | *4.8* | শক্তিশালী পিচিং পয়েন্ট: *"আপনার ৪.৮ স্টার রেটিং আছে, কিন্তু কোনো ওয়েবসাইট নেই!"* |
| **google_maps_url** | *https://www.google.com/maps/place/...* | ১ ক্লিকেই গুগল ম্যাপস প্রোফাইল, ফটো ও কাস্টমার রিভিউ দেখতে |

---

## 🎯 লিড কোয়ালিটি ও ক্যালিফোর্নিয়া ফিল্টারস

1. **নন-অটো স্প্যাম ফিল্টারিং (Spam / Clinic / Spa Blocker):**
   - "Auto Body"-র সাথে "Body" শব্দ মিলে যেসব ম্যাসাজ পার্লার, স্পা, নেইল সেলুন বা কসমেটিক ক্লিনিক আসে, সেগুলো স্ক্র্যাপার শুরুতেই ব্লক করে বাদ দেয়।
2. **ক্যালিফোর্নিয়া সিটির নাম সংঘর্ষ ফিল্টার (`CITY_NAME_COLLISIONS`):**
   - Tracy, Carson, Davis, Roseville, Bell, Stanton, Campbell, Dixon, Selma, Reedley, Patterson, Livingston, Ripon, Sanger, Lindsay, Fowler, Kerman, Anaheim, Pasadena, Burbank, Torrance, Glendale, Fremont, Modesto, Fresno, Clovis, Victorville, Corona, Ontario, Pomona, Salinas, Monterey, Napa, Irvine, Berkeley, Oakland, Vallejo, Fairfield, Hayward, Sunnyvale, Redwood, Richmond, Santee, Chino, Banning, Chico, Merced, Delano, Folsom, Lodi, Cypress, Manteca, Hemet, Eureka, Oxnard ইত্যাদি শহরের নাম কোম্পানিতে থাকলে সেগুলোকে মানুষের নাম ধরা **সম্পূর্ণ বন্ধ**।
3. **কর্পোরেট চেইন ফিল্টার:**
   - Caliber Collision, Service King, Gerber Collision, Valvoline, Firestone, Meineke, Midas, Pep Boys, Maaco ইত্যাদি বড় ন্যাশনাল চেইন বাদ।

---

## 🎛️ ফুল-কন্ট্রোল ড্যাশবোর্ড ও মেনু (Full Control Dashboard)

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
# ১. বর্তমান অগ্রগতি ও স্ট্যাটাস দেখতে
python3 run_pipeline.py --status

# ২. মাত্র ১টি ব্যাচ (৩টি সার্চ) রান করে থেমে যেতে
python3 run_pipeline.py --batch 1

# ৩. ব্যাকগ্রাউন্ডে স্বয়ংক্রিয়ভাবে পুরো পাইপলাইন রান করে রাখতে (nohup)
nohup python3 run_pipeline.py > pipeline.log 2>&1 &

# ৪. ব্যাকগ্রাউন্ডের লাইভ লগ রিয়েল-টাইমে দেখতে
tail -f pipeline.log

# ৫. গুগল ম্যাপ ছাড়া শুধু ইমেইল কালেকশন ও ভেরিফিকেশন চালাতে
python3 run_pipeline.py --enrich-only
```

---

## 📁 পাইপলাইনের মূল ফাইলসমূহ

| ফাইল | ভূমিকা | আউটপুট |
|---|---|---|
| [run_pipeline.py](file:///home/tuhin/Documents/Auto/run_pipeline.py) | মাস্টার অর্কেস্ট্রেটর ও কন্ট্রোল ড্যাশবোর্ড | কনসোল ইন্টারফেস |
| [queries.txt](file:///home/tuhin/Documents/Auto/queries.txt) | ৭৬০টি ক্যালিফোর্নিয়া সিটি ও কি-ওয়ার্ড তালিকা | ইনপুট কোয়ারি |
| [completed_queries.txt](file:///home/tuhin/Documents/Auto/completed_queries.txt) | সম্পন্ন হওয়া সার্চের লগ (রেজুমের জন্য) | ট্র্যাকিং ফাইল |
| [gmaps_scraper.py](file:///home/tuhin/Documents/Auto/gmaps_scraper.py) | ধাপ ১: ডিপ-স্ক্রলিং গুগল ম্যাপস স্ক্র্যাপার | `shops.csv` & `no-website.csv` |
| [no-website.csv](file:///home/tuhin/Documents/Auto/no-website.csv) | ওয়েবসাইটবিহীন শপ (ওয়েব সার্ভিস কোল্ড কলিং / FB এনরিচমেন্ট) | কোল্ড কলিং লিড |
| [email_spider.py](file:///home/tuhin/Documents/Auto/email_spider.py) | ধাপ ২: ফিল্টারযুক্ত Scrapy ইমেইল এক্সট্রাক্টর | `shops_with_emails.csv` |
| [verify_emails.py](file:///home/tuhin/Documents/Auto/verify_emails.py) | ধাপ ৩: ফ্রি DNS ও MX রেকর্ড ইমেইল ভেরিফায়ার | `verified_shops.csv` |
| [clean_leads.py](file:///home/tuhin/Documents/Auto/clean_leads.py) | ধাপ ৪: v2.2 আল্ট্রা-ক্লিন লিড ফরম্যাটার | `campaign_ready_leads.csv` |
| [generate_ca_queries.py](file:///home/tuhin/Documents/Auto/generate_ca_queries.py) | ৭৬০টি ক্যালিফোর্নিয়া সার্চ কোয়ারি জেনারেটর | `queries.txt` |
| [campaign_ready_leads.csv](file:///home/tuhin/Documents/Auto/campaign_ready_leads.csv) | চূড়ান্ত ভেরিফাইড ও ১০০% ক্লিন লিড তালিকা | প্রস্তুত কোল্ড ইমেইল আউটপুট |
| [fl_archive/](file:///home/tuhin/Documents/Auto/fl_archive/) | ফ্লোরিডা (FL) ক্যাম্পেইনের সমস্ত ফলাফল ব্যাকআপ (১৫,০০০+ লিড) | ব্যাকআপ ডিরেক্টরি |
| [tx_archive/](file:///home/tuhin/Documents/Auto/tx_archive/) | টেক্সাস (TX) ক্যাম্পেইনের সংরক্ষিত ফাইলসমূহ | ব্যাকআপ ডিরেক্টরি |

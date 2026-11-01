#!/usr/bin/env python3
"""
email_spider.py - Upgraded Scrapy spider to extract clean shop emails
Input: shops.csv
Output: shops_with_emails.csv
"""

import os
import re
import csv
from urllib.parse import urlparse
import scrapy

IGNORE_EXTENSIONS = (
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.css', '.js',
    '.woff', '.woff2', '.ttf', '.pdf', '.ico', '.mp4', '.avi', '.mov'
)

# ফিক্সড: সব প্লেসহোল্ডার, ওয়েব এজেন্সি এবং বুকিং টুল ডোমেইন ব্লক করা হয়েছে
IGNORE_DOMAINS = {
    'example.com', 'domain.com', 'yourdomain.com', 'email.com', 'test.com',
    'sentry.io', 'wixpress.com', 'wordpress.org', 'schema.org', 'cloudflare.com',
    'github.com', 'google.com', 'googleapis.com', 'schedulista.com', 'codelifter.com',
    'godaddy.com', 'squarespace.com', 'weebly.com', 'yelp.com', 'yellowpages.com',
    'facebook.com', 'instagram.com', 'latimes.com', 'snowman.cn'
}

# যেসব ফেক ইউজারনেম বা প্রিফিক্স থাকলে ইমেইল বাদ দেবে
BAD_EMAIL_PREFIXES = {
    'your', 'name', 'example', 'user', 'username', 'test', 'sample',
    'noreply', 'no-reply', 'donotreply', 'privacy', 'abuse', 'webmaster', 'postmaster'
}

EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b')

class EmailSpider(scrapy.Spider):
    name = "email_spider"
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_TIMEOUT': 12,
        'RETRY_TIMES': 1,
        'LOG_LEVEL': 'INFO',
        'CONCURRENT_REQUESTS': 16,
        'COOKIES_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'FEEDS': {
            'shops_with_emails.csv': {
                'format': 'csv',
                'encoding': 'utf8',
                'overwrite': True,
                'fields': ['name', 'email', 'website', 'phone', 'address', 'city', 'state']
            }
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_file = "shops.csv"
        self.output_file = "shops_with_emails.csv"
        self.found_emails = set()
        self.already_scraped_websites = set()
        self.existing_items = []
        self.shops_data = []

        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, "r", encoding="utf-8") as ef:
                    r = csv.DictReader(ef)
                    for row in r:
                        em = row.get("email", "").strip().lower()
                        web = row.get("website", "").strip().lower()
                        if em and self.is_clean_email(em):
                            self.found_emails.add(em)
                            if web:
                                self.already_scraped_websites.add(web)
                            self.existing_items.append(row)
            except Exception:
                pass

        if os.path.exists(self.input_file):
            with open(self.input_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    url = row.get("website", "").strip()
                    if url:
                        clean_url = url if url.startswith(("http://", "https://")) else "https://" + url
                        row["_clean_url"] = clean_url
                        self.shops_data.append(row)

    def is_clean_email(self, em):
        if not em or '@' not in em:
            return False
        em = em.lower().strip()
        if any(em.endswith(ext) for ext in IGNORE_EXTENSIONS):
            return False
        prefix, domain = em.split('@', 1)
        prefix_base = re.split(r'[._\-0-9]+', prefix)[0]
        if prefix in BAD_EMAIL_PREFIXES or prefix_base in BAD_EMAIL_PREFIXES:
            return False
        if domain in IGNORE_DOMAINS or any(ign in domain for ign in IGNORE_DOMAINS):
            return False
        if 'wix' in em or 'sentry' in em or 'u003e' in em:
            return False
        return True

    def generate_requests(self):
        for item in self.existing_items:
            yield item

        for shop in self.shops_data:
            web_clean = shop.get("website", "").strip().lower()
            if web_clean and web_clean in self.already_scraped_websites:
                continue

            yield scrapy.Request(
                url=shop["_clean_url"],
                callback=self.parse_homepage,
                errback=self.handle_error,
                meta={'shop': shop},
                dont_filter=True
            )

    async def start(self):
        for req in self.generate_requests():
            yield req

    def start_requests(self):
        for req in self.generate_requests():
            yield req

    def extract_emails_from_text(self, text):
        if not text:
            return []
        matches = set(EMAIL_REGEX.findall(text))
        valid_emails = [em.lower().strip() for em in matches if self.is_clean_email(em)]
        return sorted(valid_emails)

    def pick_best_email(self, emails, website_url):
        """ওয়েবসাইটের নিজস্ব ডোমেইনের ইমেইল বা জিমেইলকে অগ্রাধিকার দেবে"""
        site_domain = urlparse(website_url).netloc.lower().replace("www.", "")
        for em in emails:
            if site_domain and site_domain in em.split("@")[-1]:
                return em
        return emails[0]

    def parse_homepage(self, response):
        shop = response.meta['shop']
        shop_name = shop.get('name', '')
        
        emails = set(self.extract_emails_from_text(response.text))

        mailto_links = response.css('a[href^="mailto:"]::attr(href)').getall()
        for ml in mailto_links:
            clean_ml = ml.replace('mailto:', '').split('?')[0].strip().lower()
            emails.update(self.extract_emails_from_text(clean_ml))

        new_emails = [e for e in emails if e not in self.found_emails]
        if new_emails:
            best_email = self.pick_best_email(new_emails, shop.get('website', ''))
            self.found_emails.add(best_email)
            self.logger.info(f"📧 Found email for {shop_name}: {best_email}")
            yield {
                'name': shop.get('name', ''),
                'email': best_email,
                'website': shop.get('website', ''),
                'phone': shop.get('phone', ''),
                'address': shop.get('address', ''),
                'city': shop.get('city', ''),
                'state': shop.get('state', '')
            }
        else:
            contact_links = response.xpath(
                '//a[contains(translate(@href, "CONTACT", "contact"), "contact") or contains(translate(@href, "ABOUT", "about"), "about")]/@href'
            ).getall()

            visited_sublinks = set()
            count = 0
            for link in contact_links:
                sub_url = response.urljoin(link)
                if urlparse(sub_url).netloc == urlparse(response.url).netloc and sub_url not in visited_sublinks:
                    visited_sublinks.add(sub_url)
                    count += 1
                    yield scrapy.Request(
                        url=sub_url,
                        callback=self.parse_contact_page,
                        errback=self.handle_error,
                        meta={'shop': shop},
                        dont_filter=True
                    )
                    if count >= 2:
                        break

    def parse_contact_page(self, response):
        shop = response.meta['shop']
        emails = set(self.extract_emails_from_text(response.text))

        mailto_links = response.css('a[href^="mailto:"]::attr(href)').getall()
        for ml in mailto_links:
            clean_ml = ml.replace('mailto:', '').split('?')[0].strip().lower()
            emails.update(self.extract_emails_from_text(clean_ml))

        new_emails = [e for e in emails if e not in self.found_emails]
        if new_emails:
            best_email = self.pick_best_email(new_emails, shop.get('website', ''))
            self.found_emails.add(best_email)
            self.logger.info(f"📧 Found subpage email for {shop.get('name')}: {best_email}")
            yield {
                'name': shop.get('name', ''),
                'email': best_email,
                'website': shop.get('website', ''),
                'phone': shop.get('phone', ''),
                'address': shop.get('address', ''),
                'city': shop.get('city', ''),
                'state': shop.get('state', '')
            }

    def handle_error(self, failure):
        pass

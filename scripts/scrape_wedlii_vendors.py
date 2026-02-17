from __future__ import annotations
import os
import time
import uuid
from typing import List, Optional, Dict
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")
BASE_URL: str = "https://wedlii.com.au"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL or SUPABASE_SERVICE_KEY missing")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_html(url: str) -> Optional[str]:
    try:
        print(f"[FETCH] {url}")
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as exc:
        print(f"[ERROR] Request failed: {exc}")
        return None


def parse_vendor_urls(category_url: str) -> List[str]:
    html = fetch_html(category_url)
    if not html:
        print("[WARN] No HTML received for category page")
        return []

    soup = BeautifulSoup(html, "html.parser")

    links = [
        a["href"]
        for a in soup.find_all("a", href=True)
        if "/vendor" in a["href"]
    ]

    urls = list({BASE_URL + link for link in links})

    print(f"[DEBUG] Found {len(urls)} vendor URLs")
    return urls


def safe_text(soup: BeautifulSoup, selector: str) -> Optional[str]:
    el = soup.select_one(selector)
    return el.get_text(strip=True) if el else None


def parse_vendor_page(url: str) -> Optional[Dict]:
    html = fetch_html(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    name = safe_text(soup, "h1")

    if not name:
        print(f"[WARN] No vendor name found: {url}")
        return None

    category = safe_text(soup, "[class*=category]")
    city = safe_text(soup, "[class*=location]")
    price_text = safe_text(soup, "[class*=price]")

    if not price_text:
        print(f"[WARN] No price found for {name}")
        return None

    try:
        recommended_price = int("".join(filter(str.isdigit, price_text)))
    except ValueError:
        print(f"[WARN] Invalid price for {name}: {price_text}")
        return None

    style_tags = [
        el.get_text(strip=True)
        for el in soup.find_all(class_=lambda c: c and "style" in c.lower())
    ]

    vendor = {
        "id": str(uuid.uuid4()),
        "name": name,
        "category": (category or "unknown").lower(),
        "style_tags": style_tags,
        "city": (city or "unknown").lower(),
        "recommended_price": recommended_price,
        "availability": None,
        "source_url": url,
    }

    print(f"[PARSED] {vendor['name']} | {vendor['city']} | {vendor['recommended_price']}")
    return vendor


def upsert_vendor(vendor: Dict) -> None:
    response = (
        supabase
        .table("vendors")
        .upsert(vendor, on_conflict="source_url")
        .execute()
    )

    if response.data:
        print(f"[DB] Upserted: {vendor['name']}")
    else:
        print(f"[DB-WARN] No data returned for {vendor['name']}")


def main() -> None:
    category_pages = [
        f"{BASE_URL}/vendors/photographers",
        f"{BASE_URL}/vendors/venues",
        f"{BASE_URL}/vendors/florists",
    ]

    total_saved = 0

    for category_url in category_pages:
        print(f"\n[INFO] Scraping category: {category_url}")
        vendor_urls = parse_vendor_urls(category_url)

        for vendor_url in vendor_urls:
            vendor = parse_vendor_page(vendor_url)
            if vendor:
                upsert_vendor(vendor)
                total_saved += 1

            time.sleep(2)

    print(f"\n[DONE] Scraping finished. Vendors saved: {total_saved}")


if __name__ == "__main__":
    main()

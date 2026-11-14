
# Fetch a web page content
import streamlit as st
import requests
import json
from typing import Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader

def fetch_page_text(url: str) -> str:

    # fetch webpage detail
    loader = WebBaseLoader(url)
    document = loader.load()
    # st.write(document[0])
    # if not document or document[0].page_content.strip():
    #     raise ValueError("Page se content nahi mila")
    return document[0].page_content



HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
}

BAD_WORDS = ("logo", "icon", "sprite", "banner", "avatar",
             "placeholder", "pixel", "blank", "loader", "badge")
GOOD_WORDS = ("product", "main", "hero", "primary", "landing", "zoom", "gallery")


# ---------- Strategy 1: JSON-LD ----------
def _image_from_value(value) -> Optional[str]:
    """JSON-LD ka 'image' str, list ya {'url': ...} dict, kuch bhi ho sakta hai."""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return value.get("url") or value.get("contentUrl")
    if isinstance(value, list):
        for v in value:
            found = _image_from_value(v)
            if found:
                return found
    return None


def _product_nodes(data):
    """Nested / @graph ke andar se bhi Product nodes dhoondhta hai."""
    if isinstance(data, list):
        for d in data:
            yield from _product_nodes(d)
    elif isinstance(data, dict):
        t = data.get("@type")
        types = t if isinstance(t, list) else [t]
        if "Product" in types:
            yield data
        for v in data.values():
            if isinstance(v, (dict, list)):
                yield from _product_nodes(v)


def _from_json_ld(soup) -> Optional[str]:
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or script.get_text())
        except json.JSONDecodeError:
            continue
        for node in _product_nodes(data):
            found = _image_from_value(node.get("image"))
            if found:
                return found
    return None


# ---------- Strategy 2: meta tags ----------
def _from_meta(soup) -> Optional[str]:
    for attrs in (
        {"property": "og:image"},
        {"property": "og:image:secure_url"},
        {"name": "og:image"},
        {"name": "twitter:image"},
        {"property": "twitter:image"},
        {"name": "twitter:image:src"},
    ):
        tag = soup.find("meta", attrs=attrs)
        if tag and tag.get("content"):
            return tag["content"]

    link = soup.find("link", rel="image_src")
    if link and link.get("href"):
        return link["href"]

    tag = soup.find(attrs={"itemprop": "image"})
    if tag:
        return tag.get("content") or tag.get("src") or tag.get("href")
    return None


# ---------- Strategy 3: best <img> ----------
def _img_src(img) -> Optional[str]:
    # lazy-loading wale attributes pehle, kyunki 'src' aksar placeholder hota hai
    for attr in ("data-old-hires", "data-src", "data-lazy-src", "data-original"):
        if img.get(attr):
            return img[attr]
    srcset = img.get("srcset") or img.get("data-srcset")
    if srcset:
        return srcset.split(",")[-1].strip().split(" ")[0]   # aksar sabse badi
    return img.get("src")


def _to_int(value) -> int:
    try:
        return int(str(value).replace("px", "").strip())
    except ValueError:
        return 0


def _from_img_tags(soup) -> Optional[str]:
    best_src, best_score = None, -1
    for img in soup.find_all("img"):
        src = _img_src(img)
        if not src or src.startswith("data:") or src.lower().endswith((".svg", ".gif")):
            continue

        hints = " ".join([src, " ".join(img.get("class", [])),
                          img.get("id", ""), img.get("alt", "")]).lower()
        if any(w in hints for w in BAD_WORDS):
            continue

        score = sum(2 for w in GOOD_WORDS if w in hints)
        score += min(_to_int(img.get("width")) * _to_int(img.get("height")) / 10000, 5)

        if score > best_score:          # tie mein pehli image jeetegi
            best_src, best_score = src, score
    return best_src


# ---------- Main ----------
def fetch_productImage(url: str) -> Optional[str]:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for strategy in (_from_json_ld, _from_meta, _from_img_tags):
        found = strategy(soup)
        if found:
            # '//cdn.site.com/a.jpg' ya '/img/a.jpg' ko poora URL bana de
            return urljoin(response.url, found.strip())
    return None
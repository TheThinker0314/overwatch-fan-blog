
import os
import sys
import xml.etree.ElementTree as ET
import urllib.request
from datetime import datetime
import re
import subprocess
from newspaper import Article
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

RSS_URL = 'https://news.google.com/rss/search?q="Generative+AI"+when:7d&hl=en-US&gl=US&ceid=US:en'
POSTS_DIR = 'content/posts'

def get_ai_summary_and_tags(text):
    """
    Placeholder for a function that calls a GenAI model.
    For now, it returns a truncated summary and placeholder tags.
    """
    summary = (text[:400] + '...') if len(text) > 400 else text
    tags = ["AI", "Generative AI", "Tech"]
    # In a real scenario, this function would contain the API call to a model
    # like the one I am, to generate a summary and tags.
    # For example:
    # client = GenAIClient()
    # response = client.generate(prompt=f"Summarize this article and suggest 5 tags: {text}")
    # return response.summary, response.tags
    return summary, tags

def sanitize_filename(title):
    """Sanitizes a string to be used as a filename."""
    if not title:
        return f"post-{int(datetime.now().timestamp())}"
    s = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    return s.strip().replace(' ', '-').lower()[:60]

def process_rss_feed():
    """Fetches RSS feed, parses articles, and creates new posts."""
    try:
        req = urllib.request.urlopen(RSS_URL)
        xml_data = req.read()
        root = ET.fromstring(xml_data)
        channel = root.find('channel')
        items = channel.findall('item')
        
        if not items:
            logging.info("No items found in RSS feed.")
            return

        new_posts_created = 0
        for item in items:
            google_news_link = item.find('link').text
            
            # Create an Article object. This will handle redirects from Google News.
            article = Article(google_news_link)
            
            try:
                article.download()
                article.parse()
            except Exception as e:
                logging.error(f"Could not download/parse article from {google_news_link}. Error: {e}")
                continue

            # Check if parsing was successful and we have content
            if not article.text or not article.title:
                logging.warning(f"Skipping article, no text or title found for {article.source_url}")
                continue

            # Sanitize filename
            filename = f"{sanitize_filename(article.title)}.md"
            filepath = os.path.join(POSTS_DIR, filename)
            
            if os.path.exists(filepath):
                # logging.info(f"Post already exists: {filename}")
                continue

            # We have a new article, process it
            logging.info(f"Processing new article: {article.title}")

            # Generate AI summary and tags
            summary, tags = get_ai_summary_and_tags(article.text)

            # Prepare front matter
            date_str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            
            front_matter = f"""---
title: "{article.title.replace('"', '')}"
date: {date_str}
draft: false
summary: "{summary.replace('"', '')}"
tags: {tags}
categories: ["News Digest"]
featured_image: "{article.top_image}"
source_url: "{article.source_url}"
---

{summary}

[Read the original article at {article.meta_data.get('og', {}).get('site_name', 'the source')} »]({article.source_url})
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(front_matter)
            
            logging.info(f"Created post: {filename}")
            new_posts_created += 1

            # Let's process a few articles per run, not just one.
            if new_posts_created >= 5:
                break

    except Exception as e:
        logging.error(f"An error occurred in process_rss_feed: {e}")

def main():
    logging.info("Starting article processing script.")
    process_rss_feed()
    logging.info("Article processing script finished.")

if __name__ == '__main__':
    main()

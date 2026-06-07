
import requests                      
from bs4 import BeautifulSoup        
import pandas as pd                  
import time                          



def scrape_finance_news():
    """
    This function scrapes the latest finance headlines.
    Think of it like reading a newspaper, but automatically!
    """
    
    print("📡 Connecting to the website...")
    
    # The website URL we want to scrape
    url = "https://www.moneycontrol.com/news/business/markets/"
    
    # Headers make our request look like it's coming from a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # Send a GET request to the website (like visiting the page)
    response = requests.get(url, headers=headers, timeout=10)
    
    # Check if the request was successful (200 = OK)
    print(f"✅ Response Status: {response.status_code}")
    
    # Parse the HTML content using BeautifulSoup
    # 'html.parser' is a built-in Python tool to read HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all news articles on the page
    # We look for specific HTML tags that contain the news
    articles = soup.find_all('li', class_='clearfix')
    
    # Store our collected data here
    news_data = []
    
    print(f"\n📰 Found {len(articles)} articles. Extracting data...\n")
    
    for article in articles[:15]:  # Limit to 15 articles
        try:
            # Extract the headline text
            title_tag = article.find('a')
            title = title_tag.get_text(strip=True) if title_tag else "N/A"
            
            # Extract the link
            link = title_tag['href'] if title_tag and title_tag.has_attr('href') else "N/A"
            
            # Extract the date/time if available
            time_tag = article.find('span')
            publish_time = time_tag.get_text(strip=True) if time_tag else "N/A"
            
            # Only add if we have a real title
            if title and title != "N/A" and len(title) > 10:
                news_data.append({
                    'Headline': title,
                    'Published': publish_time,
                    'Link': link
                })
                print(f"  ✔ {title[:60]}...")  # Show first 60 chars
                
        except Exception as e:
            # Skip articles that cause errors
            continue
    
    return news_data


# ============================================
# PART B: Scrape Quotes from a Practice Website
# (Safe to use - designed for scraping practice)
# ============================================

def scrape_quotes():
    """
    Scrapes quotes from quotes.toscrape.com
    This is a website made for practicing web scraping - totally safe and legal!
    """
    
    print("\n📡 Scraping quotes from practice website...")
    
    all_quotes = []
    page = 1
    
    while page <= 3:  # Scrape first 3 pages
        url = f"http://quotes.toscrape.com/page/{page}/"
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all quote blocks on the page
        quote_blocks = soup.find_all('div', class_='quote')
        
        # If no quotes found, stop
        if not quote_blocks:
            break
        
        for block in quote_blocks:
            # Extract quote text (remove the quotation marks)
            text = block.find('span', class_='text').get_text(strip=True)
            
            # Extract author name
            author = block.find('small', class_='author').get_text(strip=True)
            
            # Extract tags (topics of the quote)
            tags = [tag.get_text() for tag in block.find_all('a', class_='tag')]
            
            all_quotes.append({
                'Quote': text,
                'Author': author,
                'Tags': ', '.join(tags),
                'Page': page
            })
        
        print(f"  ✔ Page {page} scraped - {len(quote_blocks)} quotes found")
        
        time.sleep(1)  # Wait 1 second between pages (good practice!)
        page += 1
    
    return all_quotes


# ============================================
# MAIN PROGRAM - Run everything
# ============================================

if __name__ == "__main__":
    
    print("=" * 55)
    print("   WEB SCRAPING - DATA SCIENCE INTERNSHIP TASK 1")
    print("=" * 55)
    
    # ---------- SCRAPE QUOTES (Safe Practice Site) ----------
    print("\n🔷 SECTION 1: Scraping Quotes Data")
    print("-" * 40)
    
    quotes = scrape_quotes()
    
    if quotes:
        # Convert to DataFrame (like an Excel table)
        df_quotes = pd.DataFrame(quotes)
        
        # Save to CSV file
        df_quotes.to_csv('quotes_data.csv', index=False)
        
        print(f"\n✅ Successfully scraped {len(quotes)} quotes!")
        print("\n📊 Sample Data Preview:")
        print(df_quotes[['Author', 'Quote']].head(5).to_string(index=False))
        print(f"\n💾 Data saved to: quotes_data.csv")
    
    # ---------- SCRAPE FINANCE NEWS ----------
    print("\n\n🔷 SECTION 2: Scraping Finance News")
    print("-" * 40)
    
    try:
        news = scrape_finance_news()
        
        if news:
            df_news = pd.DataFrame(news)
            df_news.to_csv('finance_news.csv', index=False)
            
            print(f"\n✅ Successfully scraped {len(news)} news articles!")
            print(f"💾 Data saved to: finance_news.csv")
        else:
            print("⚠️ No news data found. Website may have changed its structure.")
            
    except Exception as e:
        print(f"⚠️ Could not scrape finance news: {e}")
        print("   (This is normal - some sites block scrapers)")
    
    print("\n" + "=" * 55)
    print("   SCRAPING COMPLETE! Check your CSV files.")
    print("=" * 55)
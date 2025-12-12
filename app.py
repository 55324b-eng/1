import requests, re, time, os

# Settings
S, E = 1, 1     # Page range to scrape
U = 'https://hentaidad.com/page/'
SL = 2              # Sleep time
SUFF = '-1'
DATA_FILE = 'data.json' # File name where data is stored

def clean_url(u, s):
    # Remove thumb suffix and handle webp replacement
    u = re.sub(r'([-_]thumb)(?=\.webp)', '', u, flags=re.I)
    return u if re.search(r'-\d+\.\w+$', u) else u.replace('.webp', f'{s}.webp')

def get_existing_data():
    """Reads existing URLs from the file to avoid deletion"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract URLs inside quotes
            return re.findall(r'"(https?://[^"]+)"', content)
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def scrape(p):
    try:
        from bs4 import BeautifulSoup
        r = requests.get(U + str(p), headers={'User-Agent':'Mozilla/5.0'}, timeout=15)
        if r.status_code != 200: return []
        
        soup = BeautifulSoup(r.content, 'html.parser')
        # Find all images with data-src
        images = [clean_url(el.get('data-src'), SUFF) for el in soup.find_all(attrs={'data-src':True}) if el.get('data-src')]
        return images
    except Exception as e:
        print(f"Error scraping page {p}: {e}")
        return []

# --- MAIN LOGIC ---

# 1. Load OLD data first
all_data = get_existing_data()
print(f"Old data loaded: {len(all_data)} items")

seen_urls = set(all_data) # Use set for fast duplicate checking

# 2. Scrape NEW data
print(f"Scraping pages {S} to {E}...")
for p in range(S, E + 1):
    new_urls = scrape(p)
    if new_urls:
        count = 0
        for url in new_urls:
            if url not in seen_urls:
                all_data.append(url)
                seen_urls.add(url)
                count += 1
        print(f"Page {p}: Found {len(new_urls)}, Added {count} new.")
    time.sleep(SL)

# 3. Save MERGED data (Old + New)
formatted_body = ',\n'.join(f'"{u}"' for u in all_data)
# Javascript variable format
file_content = f'const data =[\n{formatted_body}\n];'

# Writing directly to file (No stdout/print needed)
with open(DATA_FILE, 'w', encoding='utf-8') as f:
    f.write(file_content)

print(f"Done! Total entries saved: {len(all_data)}")
import requests, re, time

S, E = 1, 500
U = 'https://hentaidad.com/page/'
SL = 2
SUFF = '-1'
RTH = r'([-_]thumb)(?=\.webp)'
RSF = r'-\d+\.\w+$'
A = []

def clean_url(u, s):
    u = re.sub(RTH, '', u, flags=re.I)
    return u if re.search(RSF, u) else u.replace('.webp', f'{s}.webp')

def scrape(p):
    try:
        from bs4 import BeautifulSoup
        r = requests.get(U + str(p), headers={'User-Agent':'Mozilla/5.0'}, timeout=15)
        r.raise_for_status()
        return [clean_url(el.get('data-src'), SUFF) for el in BeautifulSoup(r.content, 'html.parser').find_all(attrs={'data-src':True}) if el.get('data-src')]
    except:
        return None

for p in range(S, E + 1):
    L = scrape(p)
    if L: A.extend(L)
    time.sleep(SL) 

formatted_body = ',\n'.join(f'"{u}"' for u in A)
final_output = f'const data =[\n{formatted_body}\n];'

print(final_output)

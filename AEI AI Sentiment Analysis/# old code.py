# old code

# Extracting main meta tags:
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to fetch the page at {url}")


soup = BeautifulSoup(response.content, 'html.parser')
metadata = {}       
for main_tag in main_tags:
    tags = soup.find_all('meta', attrs = {'property': main_tag})
    if tags:
        tag = tags[0]
        metadata[main_tag] = tag['content']
# Extracting keywords
tags = soup.find_all('meta', attrs={'name': 'keywords'})
if tags:
    tag = tags[0]
    if 'content' in tag.attrs:
        metadata['keywords'] = tag['content']
    else:
        metadata['keywords'] = 'N/A
# Extract Open Graph tags
og_tags = ['og:title', 'og:description', 'og:type', 'og:url', 'og:site_name', 'og:locale']
for og_tag in og_tags:
    tags = soup.find_all('meta',attrs = {'property':og_tag})
    if tags:
        tag = tags[0]
        if 'content' in tag.attrs:                    
            metadata[og_tag] = tag['content']
        else:
            metadata[og_tag] = 'N/A
# Extract Twitter Card tags
twitter_tags = ['twitter:card', 'twitter:site', 'twitter:title', 'twitter:description']
for twitter_tag in twitter_tags:
    tags = soup.find_all('meta',attrs={'name':twitter_tag})
    if tags:
        tag = tags[0]
        if 'content' in tag.attrs:                    
            metadata[twitter_tag] = tag['content']
        else:
            metadata[twitter_tag] = 'N/A
# Extract Schema.org markup
for tag in soup.find_all('script', type='application/ld+json'):
    try:
        json_data = json.loads(tag.string)
        if '@context' in json_data and 'schema.org' in json_data['@context']:
            metadata.update(json_data)
    except json.JSONDecodeError:
        continu
# Extract article type & sections
article_tags = ['article.type', 'article.section', 'article.summary']
for article_tag in article_tags:
    tags = soup.find_all('meta', attrs={'name':article_tag})
    if tags:
        tag=tags[0]
        if 'content' in tag.attrs:                    
            metadata[article_tag] = tag['content']
        else:
            metadata[article_tag] = 'N/A'
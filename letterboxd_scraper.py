from bs4 import BeautifulSoup
import requests
import json

# Function to fetch movie data from a given URL
def fetch_movie_data(url):
    # Define headers to mimic a real browser request
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'referer': 'https://google.com',
    }

    # Send a GET request to the URL
    r = requests.get(url, headers=headers)
    # Parse the content of the response with BeautifulSoup
    soup = BeautifulSoup(r.content, 'lxml')

    # Dictionary to store movie data
    item = {}

    # Extract movie title
    title_meta = soup.find('meta', {'property': 'og:title'})
    if title_meta:
        item['title'] = title_meta.get('content')
    else:
        print(f"Title not found for URL: {url}")

    # Extract release year
    year_small = soup.find('small', {'class': 'number'})
    if year_small:
        item['release year'] = year_small.text.strip()
    else:
        print(f"Year not found for URL: {url}")

    # Extract directors
    directors = soup.find_all('span', {'class': 'prettify'})
    item['director(s)'] = [director.text.strip() for director in directors] if directors else []

    # Extract cast
    cast = soup.find_all('a', {'class': 'text-slug tooltip'})
    item['cast'] = [actor.text.strip() for actor in cast] if cast else []

    # Extract rating
    rating_meta = soup.find('meta', {'name': 'twitter:data2'})
    if rating_meta:
        item['rating'] = rating_meta.get('content')
    else:
        print(f"Rating not found for URL: {url}")

    # Extract genres
    genres_div = soup.find('div', {'class': 'text-sluglist capitalize'})
    if genres_div:
        item['genres'] = [genre.text.strip() for genre in genres_div.find_all('a', {'class': 'text-slug'})]
    else:
        print(f"Genres not found for URL: {url}")

    # Extract producers
    producers_div = soup.find_all('div', {'class': 'text-sluglist'})[2] if len(soup.find_all('div', {'class': 'text-sluglist'})) > 2 else None
    item['producer(s)'] = [producer.text.strip() for producer in producers_div.find_all('a')] if producers_div else []

    # Extract writers
    writers_div = soup.find_all('div', {'class': 'text-sluglist'})[3] if len(soup.find_all('div', {'class': 'text-sluglist'})) > 3 else None
    item['writer(s)'] = [writer.text.strip() for writer in writers_div.find_all('a')] if writers_div else []

    # Extract additional statistics
    movie_id = url.split('/')[-2]
    stats_url = f'https://letterboxd.com/esi/film/{movie_id}/stats/'
    r_stats = requests.get(stats_url, headers=headers)
    soup_stats = BeautifulSoup(r_stats.content, 'lxml')

    # Extract watched by count
    watched_by = soup_stats.find('a', {'class': 'has-icon icon-watched icon-16 tooltip'})
    if watched_by:
        item['watched by'] = watched_by.text.strip()
    else:
        item['watched by'] = 'Data not available'
        print(f"Watched by data not available for URL: {url}")

    # Extract listed by count
    listed_by = soup_stats.find('a', {'class': 'has-icon icon-list icon-16 tooltip'})
    if listed_by:
        item['listed by'] = listed_by.text.strip()
    else:
        item['listed by'] = 'Data not available'
        print(f"Listed by data not available for URL: {url}")

    # Extract liked by count
    liked_by = soup_stats.find('a', {'class': 'has-icon icon-like icon-liked icon-16 tooltip'})
    if liked_by:
        item['liked by'] = liked_by.text.strip()
    else:
        item['liked by'] = 'Data not available'
        print(f"Liked by data not available for URL: {url}")

    return item

# Function to scrape a list of movies from a given URL
def scrape_movie_list(list_url):
    # Define headers to mimic a real browser request
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'referer': 'https://google.com',
    }

    # Send a GET request to the list URL
    r = requests.get(list_url, headers=headers)
    # Parse the content of the response with BeautifulSoup
    soup = BeautifulSoup(r.content, 'lxml')

    # Extract links to individual movies
    movie_links = soup.find_all('a', {'class': 'poster film-poster'})

    movie_urls = []
    # Construct full URLs for each movie
    for link in movie_links:
        movie_url = link.get('href')
        if movie_url.startswith('/film/'):
            full_movie_url = f'https://letterboxd.com{movie_url}'
            movie_urls.append(full_movie_url)

    movie_data = []
    # Fetch data for each movie URL
    for url in movie_urls:
        print(f"Fetching data for URL: {url}")
        data = fetch_movie_data(url)
        movie_data.append(data)

    return movie_data

# URL of the list of popular movies from the 2020s
list_url = 'https://letterboxd.com/films/popular/decade/2020s/'
movies_data = scrape_movie_list(list_url)

# Save fetched data to a file
with open('movies_data.txt', 'w') as f:
    for movie in movies_data:
        f.write(json.dumps(movie, indent=4))
        f.write('\n\n')

print("Data has been saved to movies_data.txt")

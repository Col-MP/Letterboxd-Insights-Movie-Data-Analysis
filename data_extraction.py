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
    item['title'] = title_meta.get('content') if title_meta else 'Title not found'

    # Extract release year
    year_small = soup.find('small', {'class': 'number'})
    item['release year'] = year_small.text.strip() if year_small else 'Year not found'

    # Extract directors
    directors = soup.find_all('span', {'class': 'prettify'})
    item['director(s)'] = [director.text.strip() for director in directors] if directors else []

    # Extract cast
    cast = soup.find_all('a', {'class': 'text-slug tooltip'})
    item['cast'] = [actor.text.strip() for actor in cast] if cast else []

    # Extract rating
    rating_meta = soup.find('meta', {'name': 'twitter:data2'})
    item['rating'] = rating_meta.get('content') if rating_meta else 'Rating not found'

    # Extract genres
    genres_div = soup.find('div', {'class': 'text-sluglist capitalize'})
    item['genres'] = [genre.text.strip() for genre in genres_div.find_all('a', {'class': 'text-slug'})] if genres_div else []

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
    item['watched by'] = watched_by.text.strip() if watched_by else 'Data not available'

    # Extract listed by count
    listed_by = soup_stats.find('a', {'class': 'has-icon icon-list icon-16 tooltip'})
    item['listed by'] = listed_by.text.strip() if listed_by else 'Data not available'

    # Extract liked by count
    liked_by = soup_stats.find('a', {'class': 'has-icon icon-like icon-liked icon-16 tooltip'})
    item['liked by'] = liked_by.text.strip() if liked_by else 'Data not available'

    return item

# Function to process a list of movie URLs
def process_movie_urls(file_path):
    # Read URLs from a file
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]

    movie_data = []
    # Fetch data for each URL
    for url in urls:
        print(f"Fetching data for URL: {url}")
        data = fetch_movie_data(url)
        print(f"Fetched data: {data}")
        movie_data.append(data)

    # Save fetched data to a file
    with open('movies_data.txt', 'w') as f:
        for movie in movie_data:
            f.write(json.dumps(movie, indent=4))
            f.write('\n\n')

    print("Data has been saved to movies_data.txt")

# Run the process
process_movie_urls('final_movie_urls.txt')

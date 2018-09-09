
import urllib.request
from bs4 import BeautifulSoup
from collections import Counter

GENRE = 'Crime'
URL = 'https://www.imdb.com/search/title?genres=crime&sort=user_rating,desc&title_type=feature&num_votes=25000,&page=%d'
NPAGES = 1

def fetch_html(page_number):
	print('Fetching page', page_number, '...')
	ufile = urllib.request.urlopen(URL % page_number)
	html = str(ufile.read().decode('utf-8'))
	return html

def get_movie_soups(html):
	soup = BeautifulSoup(html)
	# print(soup.prettify())
	movie_soups = soup.find_all(class_='lister-item')
	return movie_soups

def extract_movie_info(movie_soup):
	title = movie_soup.find('h3').find('a').get_text()
	year = int(movie_soup.find(class_='lister-item-year').get_text()[-5:-1])
	duration = int(movie_soup.find(class_='runtime').get_text()[:-4])
	genres = movie_soup.find(class_='genre').get_text().strip().split(', ')
	rating = float(movie_soup.find(class_='ratings-imdb-rating').get_text().strip())
	crew_soup = movie_soup.find_all('div', recursive=False)[-1].find_all('p')[-2]

	stars = list()
	director = None
	is_director = False
	is_star = False
	for child in crew_soup.children:
	    if "Director:" in str(child):
	        is_director = True
	        is_star = False
	        continue
	    if "Stars:" in str(child):
	        is_star = True
	        is_director = False
	        continue
	    if child.name == 'a':
	        if is_director:
	            director = child.get_text()
	        elif is_star:
	            stars.append(child.get_text())
	return {
		'title': title,
		'year': year,
		'duration': duration,
		'genres': genres,
		'rating': rating,
		'director': director,
		'stars': stars,
	}

def year_to_decade(year):
	return str((year // 10) * 10) + 's'

def print_statistics(counts, title, sort_by_value=False, limit=None):
	print('='*80)
	print(title)
	print('-'*80)

	if not sort_by_value:
		keys = sorted(counts.keys())
	else:
		keys = sorted(counts.keys(), key=counts.get, reverse=True)

	if limit:
		keys = keys[:limit]

	for key in keys:
		print('%40s %4d' % (key, counts[key]))

def run():
	htmls = [fetch_html(page_number) for page_number in range(1, NPAGES+1)]

	movie_infos = list()
	for html in htmls:
		for movie_soup in get_movie_soups(html):
			info = extract_movie_info(movie_soup)
			movie_infos.append(info)
	print(movie_infos[0])

	# titles
	for movie_info in movie_infos:
		print("%80s (%d) - Rating %.1f %s" % (movie_info['title'], movie_info['year'], movie_info['rating'], '*' * int(5.0 * movie_info['rating'])))

	# decades
	years = [movie_info['year'] for movie_info in movie_infos]
	decades = [year_to_decade(year) for year in years]
	decade_counts = Counter(decades)
	print_statistics(decade_counts, 'Number of movies by decade')

	# genres
	genres = [genre for movie_info in movie_infos for genre in movie_info['genres']]
	genre_counts = Counter(genres)
	del genre_counts[GENRE]
	print_statistics(genre_counts, 'Related genres', sort_by_value=True, limit=25)

	# directors
	directors = [movie_info['director'] for movie_info in movie_infos]
	director_counts = Counter(directors)
	print_statistics(director_counts, 'Top directors', sort_by_value=True, limit=25)

	# stars
	stars = [star for movie_info in movie_infos for star in movie_info['stars']]
	star_counts = Counter(stars)
	print_statistics(star_counts, 'Top stars', sort_by_value=True, limit=25)

run()

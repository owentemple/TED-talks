import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
from random import randint
import json


# Specify the urls of the talks metadata to gather by pasting in as a list
urls = [
    'https://www.ted.com/talks/gautam_bhan_a_bold_plan_to_house_100_million_people',
    'https://www.ted.com/talks/nadine_hachach_haram_how_augmented_reality_could_change_the_future_of_surgery'
    ]

# Writes scraped data with column names to csv
def write_it(data_so_far):
    # Open a csv file with append, so old data will not be erased
    with open('TED-metadata.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        # The for loop
        for comments, title, duration, event, film_date, languages, main_speaker, name, num_speaker, published_date, \
            ratings, related_talks, speaker_occupation, tags, description, url, views in data_so_far:
            writer.writerow([comments, title, duration, event, film_date, languages, main_speaker, name, num_speaker, published_date, \
                             ratings, related_talks, speaker_occupation, tags, description, url, views, datetime.now()])

# Collect variables from Beautiful Soup object and print results
def gather_metadata(urls):
    data = []
    counter = 0

    for pg in urls:
        # query the website and return the html to the variable ‘page’
        page = requests.get(pg)

        soup = BeautifulSoup(page.text, 'html.parser')
        s = soup.find_all('script')
        json_text = str(s[11])[27:-10]
        obj = json.loads(json_text)
        current = obj['__INITIAL_DATA__']
        comments = current['comments']['count']
        title = current['name']
        duration = current['talks'][0]['duration']
        event = current['event']
        film_date = current['talks'][0]['player_talks'][0]['filmed']
        languages = len(current['talks'][0]['player_talks'][0]['languages'])
        main_speaker = current['talks'][0]['player_talks'][0]['speaker']
        name = current['name']
        num_speaker = len(current['speakers'])
        published_date = current['talks'][0]['player_talks'][0]['published']
        ratings = current['talks'][0]['ratings']
        related_talks = current['talks'][0]['related_talks']
        speaker_occupation = current['talks'][0]['speakers'][0]['description']
        tags = current['talks'][0]['tags']
        description = current['description']
        url = current['url']
        views = current['viewed_count']

        print(comments, '\n')
        print(title, '\n')
        print(duration, '\n')
        print(event, '\n')
        print(film_date, '\n')
        print(languages, '\n')
        print(main_speaker, '\n')
        print(name, '\n')
        print(num_speaker, '\n')
        print(published_date, '\n')
        print(ratings, '\n')
        print(related_talks, '\n')
        print(speaker_occupation, '\n')
        print(tags, '\n')
        print(description, '\n')
        print(url, '\n')
        print(views, '\n')

        # Save the data in tuple
        data.append((comments, title, duration, event, film_date, languages, main_speaker, name, num_speaker, published_date, \
            ratings, related_talks, speaker_occupation, tags, description, url, views))
        # Writes data once three talks have been collected
        counter += 1
        if counter > 3:
            write_it(data)
            counter = 0
            data = []
        # Sleeps between requests to TED.com to prevent 429 "Too Many Requests" error
        time.sleep(randint(11, 16))

    write_it(data)

if __name__ == "__main__":
    gather_metadata(urls)
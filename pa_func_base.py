import requests
import re
from bs4 import BeautifulSoup
import os
import datetime
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import numpy as np


def dir_creation():
    time = str(datetime.datetime.now())
    file_ext = time[-2:]
    cwd = os.getcwd()
    print('The current working directory is: ', cwd)
    base_folder_name = 'lyrics_v' + file_ext
    base_folder_loc = cwd + '/' + base_folder_name + '/'
    try:
        os.mkdir(base_folder_loc)
    except OSError:
        print("Creation of the directory %s failed" % base_folder_loc)
    else:
        print("Successfully created the directory %s " % base_folder_loc)
    return base_folder_name, base_folder_loc


def input_format(base_folder_name, base_folder_loc):
    # Set general domain and base to get to artist pages
    domain = 'https://www.lyrics.com/'
    base = 'https://www.lyrics.com/lyrics/'

    # input verification
    bad_input = True
    num_input = True

    if bad_input == True:
        custom = input('Import custom artists? Please type Y, N will retrieve a standard list: ')
        custom = custom.capitalize()
        custom = custom[0]
        if custom == 'Y':
            a_list = input('Please Give in Artist Names Separated by a comma ')
            a_list = a_list.replace(', ', ':')
            a_list = a_list.replace(',', ':')
            separated = a_list.split(':')
            capped = [each.capitalize() for each in separated]
            space_format = [each.replace(' ', '%20') for each in capped]
            print(space_format)
            num_of_songs = input(
                'how many songs do you want to retrieve? Please enter a number and press Enter: ')

            while num_input == True:
                try:
                    n_songs = int(num_of_songs)
                    num_input = False
                except:
                    print('Could not convert input to an integer, reverting to a default of 10 songs per artist')
                    n_songs = 10
                    num_input = False

            print('Going to retrieve songs from the following artists: ', space_format)
            bad_input = False

        elif custom == 'N':
            capped = ['Eminem', 'Madonna', 'Drake', ]
            while num_input == True:
                num_of_songs = input(
                    'how many songs do you want to retrieve? Please enter a number and press Enter: ')

                num_input = False
            try:
                n_songs = int(num_of_songs)
                print('int conversion sucessful')
            except:
                print('Could not convert input to an integer, reverting to a default of 10 songs per artist')
                n_songs = 10
                input_given == False

            print('Retrieving Lyrics for the following artists: ', capped)
            space_format = [each.replace(' ', '%20') for each in capped]
            bad_input = False
        else:
            print('Input Error, please try again')
        return space_format, base, domain, n_songs, base_folder_name, base_folder_loc
    # Gets links to individual artist pages with all of their songs listed


def get_links_create_files(space_format, base, domain, n_songs, base_folder_name, base_folder_loc):
    cwd = os.getcwd()
    artist_name_corpus = []
    links_artist = []
    corpus_dict = {}
    for each in space_format:
        url = base + each
        result = requests.get(url)
        page_content = BeautifulSoup(result.content, 'html.parser')
        artist_tags = page_content.find_all(a, {'class': 'serp-flat-list'})
        if len(artist_tags) <= 1:
            print('Artist not found')
            continue
        art_tag = str(artist_tags[0])
        find_artist_link = r'<a href=\"([^\"]*)'
        artist_result = re.findall(find_artist_link, art_tag)
        artist_link = artist_result[0]
        print('Retrieved Artist Link for: ', each)
        links_artist.append(artist_link)

    # Gets links to all songs in the Artists discography
    for item in links_artist:
        pattern = '[A-Z]\w*'
        artist_name = str(re.findall(pattern, item))
        artist_name = artist_name.replace('[', '')
        artist_name = artist_name.replace(']', '')
        artist_name = artist_name.replace('\'', '')
        artist_name = artist_name.replace(' ', '')
        artist_name = artist_name.replace(',', '')
        print('formatted artist name is:', artist_name)
        get_r = requests.get(domain + item)
        page_content = BeautifulSoup(get_r.content, 'html.parser')
        text = page_content.prettify()
        pattern = 'href=\"(/lyric/[^\"]+)\">'
        links = re.findall(pattern, text)
        print('Found all songlinks for :', artist_name)

        # Goes through all of the songs for each artist
        # Creates an indivudial file for each song, with a formatted name
        # n_songs represents the amount of songs per artist

        for link in links[:n_songs]:
            clean_lyrics = []
            pattern = '/lyric/[0-9]*/[^/]*/(.+)'
            song_name_plus = str(re.findall(pattern, link))
            song_name = song_name_plus.replace('+', '_')
            song_name = song_name.replace('[', '')
            song_name = song_name.replace(']', '')
            song_name = song_name.replace('\'', '')

            song_artist_file = artist_name + '_' + song_name
            print('File name this song will be saved to will be called: ', song_artist_file)
            artist_name_corpus.append(song_artist_file)
            url = domain + link
            get_s = requests.get(url)
            song_content = BeautifulSoup(get_s.content, 'html.parser')
            lyric_bodies = song_content.find_all(attrs={'id': 'lyric-body-text'})
            songtext = lyric_bodies[0]
            stringson = str(songtext)
            remove_pre = '<pre[^>]*>'
            pre_removed = re.sub(remove_pre, '', stringson, re.DOTALL)
            rm_last_pre = '</pre>'
            no_pres = re.sub(rm_last_pre, '', pre_removed)

            rm_start_a = '<a[^>]*>'
            no_start_a = re.sub(rm_start_a, '', no_pres)
            rm_end_a = '<\/a>'
            clean = re.sub(rm_end_a, '', no_start_a)
            clean_lyrics.append(clean)
            artist_songstring = ' '.join(clean_lyrics)
            clean_lyrics = []
            corpus_dict[artist_name] = artist_songstring
            if len(song_name) <= 2:
                print('TITLE ERROR')
                continue
            artist_file = '$'.join(artist_name_corpus)
            print(artist_file)
            print('artist_name_corpus type is: ', type(artist_name_corpus))
            print('artist_file type is: ', type(artist_file))
            artist_filename = str('corpus_songlist')
            with open(f'{base_folder_loc}{song_artist_file}.txt', 'w') as f:
                f.write(artist_songstring)
        print(artist_file)
        with open(f'{base_folder_loc}{artist_filename}.txt', 'w') as f:
            f.write(artist_file)
        with open(f'{cwd}/Lyric_Predictor/corp_loc.txt', 'w') as f:
            f.write(base_folder_loc)
        print(f'Successfully saved corpus for {artist_name} as .txt')
    return print(f'Lyrics scraped successfully to {base_folder_loc}, ready to generate corpus')


def generate_corpus(base_folder_loc):
    corpus = []
    f = open(base_folder_loc + "corpus_songlist.txt", "r")
    filestring = f.read()
    labels = filestring.split('$')
    labels.sort()
    filenames = os.listdir(base_folder_loc)
    filenames.remove('corpus_songlist.txt')
    filenames.sort()
    for file in filenames:
        f = open(f'{base_folder_loc}{file}', 'r')
        x = f.read()
        corpus.append(x)
    print(f'length of corpus is {len(corpus)}')
    return corpus, labels


def tmp_flask(form_input):
    '''takes corpus as an array of strings in which each entry of the array is all the
    text for that artist, labels are the artist labels respective the index of the array'''
    cwd = os.getcwd()
    cwd = cwd + '/Lyric_Predictor'
    f = open(f'{cwd}/corp_loc.txt', "r")
    corpus_loc = f.read()
    corpus, labels = generate_corpus(corpus_loc)

    # Generate Youtube Link Dictionary for Results
    print('corpus loc from tmp flask is: ', corpus_loc)
    with open(cwd + "/YTDICT.txt") as f:
        file = f.read()
    splitted = file.split('$')
    if len(splitted[-1]) == 0:
        splitted.remove(splitted[-1])
    song_names = splitted[::2]
    song_links = splitted[1::2]
    link_dict = {}
    for name, link in zip(song_names, song_links):
        link_dict[name] = link

    # Naive Bayes Countvectorization
    cv = CountVectorizer(stop_words='english')
    vec = cv.fit_transform(corpus)
    tf = TfidfTransformer()
    vec2 = tf.fit_transform(vec)
    vec2 = vec2.todense()
    X = vec2
    y = labels
    m = MultinomialNB()
    fitted_model = m.fit(X, y)
    user_input = form_input
    user_input = user_input.split('$$')
    test_vec = cv.transform(user_input)
    test_vec = tf.transform(test_vec)
    predict_output = m.predict(test_vec)
    probs = m.predict_proba(test_vec)
    lprobs = probs.tolist()
    predict_output = predict_output.tolist()
    songs_formatted = []

    # Results formatting and Cleaning
    for item in predict_output:
        item = item.replace('_', ' ')
        item = item.replace('%2C', '')
        item = item.replace('C3A9', 'e')
        item = item.replace('%27', '')
        pattern = r'%[0-9]{2,}'
        item = re.sub(pattern, '', item, count=0, flags=0)
        pattern = r'%..'
        item = re.sub(pattern, '', item, count=0, flags=0)
        songs_formatted.append(item)
    print("SF is ", songs_formatted)
    result_links = [link_dict[x] for x in songs_formatted]
    if len(result_links) == 1:
        result_links.append('NOLINK')
        result_links.append('NOLINK')
        if len(result_links) == 2:
            result_links.append('NOLINK')
    test_results = list(zip(songs_formatted, user_input, result_links))
    return test_results

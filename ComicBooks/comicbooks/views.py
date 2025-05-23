from django.shortcuts import render, redirect
from .forms import ComicBookForm
from .models import comicbooks
from django.shortcuts import get_object_or_404
from bs4 import BeautifulSoup
import requests
import json
import os
import csv

# Create your views here.
def home(request):
    return render(request, 'comicbooks/home.html')

def about(request):
    return render(request, 'comicbooks/about.html')


def create_comic_book(request):
    if request.method == 'POST':
        form = ComicBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('comic_list')
    else:
        form = ComicBookForm()
    return render(request, 'comicbooks/create_comic_book.html', {'form': form})

def comic_list(request):
    comics = comicbooks.objects.all()
    return render(request, 'comicbooks/comic_list.html', {'comics': comics})
def comic_details(request, comic_id):
    comic = get_object_or_404(comicbooks, id=comic_id)
    return render(request, 'comicbooks/details.html', {'comic': comic})
def delete_comic(request, comic_id):
    comic = get_object_or_404(comicbooks, id=comic_id)
    comic.delete()
    return redirect('comic_list')

def edit_comic(request, comic_id):
    comic = get_object_or_404(comicbooks, pk=comic_id)
    if request.method == 'POST':
        form = ComicBookForm(request.POST, request.FILES, instance=comic)
        if form.is_valid():
            form.save()
            return redirect('comic_details', comic_id=comic.id)
    else:
        form = ComicBookForm(instance=comic)
    return render(request, 'comicbooks/edit_comic.html', {'form': form, 'comic': comic})

# Below is for step Connect to API
def superhero_api_view(request, hero_id):
    token= 'a099675f0f78d5b83244fa9d2cf60284' # number given by superhero api site
    url = f'https://superheroapi.com/api/{token}/{hero_id}'

    response = requests.get(url)  # Make API request
    if response.status_code == 200:
        data = response.json() # parse JSON data
        print(json.dumps(data, indent=4)) # print to terminal


        if 'full-name' in data.get('biography', {}):
            data['biography']['full_name'] = data['biography']['full-name']

        # pass data to display on web page
        return render(request, 'comicbooks/superhero_api.html', {'data': data})
    else:
        error_message = f"API request failed with status code {response.status_code}"
        print(error_message)
        return render(request, 'comicbooks/superhero_api.html', {'error_message': error_message})

def marvel_characters_scrape():

    if os.path.exists('comicbooks/static/comicbooks/marvel_characters_scrape.csv'):
        file = open('comicbooks/static/comicbooks/marvel_characters_scrape.csv', 'r')
        reader = csv.reader(file)
        characters = [{'name': row[0], 'link': row[1]} for row in reader]
    else:

        alphabet = ("A" , "B", "C", "D", "E","F", "G", "H", "I", "J","K" , "L", "M", "N", "O","P", "Q", "R", "S", "T","U" , "V", "W", "X", "Y","Z")
        characters = []
        for i in alphabet:
            url = 'https://en.wikipedia.org/wiki/List_of_Marvel_Comics_characters:_'+ i
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            print("--------- PAGE TITLE ----------")
            print(soup.title)



            # Find all h2 that have an id
            for header in soup.find_all('h2'):
                if header.has_attr('id'):
                    name = header.get_text().strip()
                    link = f"{url}#{header['id']}"
                    characters.append({'name': name, 'link': link})

            print(characters)
            with open('comicbooks/static/comicbooks/marvel_characters_scrape.csv', 'w') as file:
                [file.write('{0}, {1} \n'.format(item['name'], item['link'])) for item in characters]

    return characters




def marvel_scrape(request):
    characters = marvel_characters_scrape()
    return render(request, 'comicbooks/marvel_scrape.html', {'characters': characters})

def dc_characters_scrape(request):
    if os.path.exists('comicbooks/static/comicbooks/dc_characters_scrape.csv'):
        with open('comicbooks/static/comicbooks/dc_characters_scrape.csv', 'r') as file:
            reader = csv.reader(file)
            characters = [{'name': row[0], 'link': row[1]} for row in reader]
    else:
        url='https://en.wikipedia.org/wiki/List_of_DC_Comics_characters'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        characters = []
        content_div = soup.find_all('div', class_='mw-parser-output')

        for div in content_div:
            for li in content_div.find_all('li'):
                a_tag = li.find_all('a')
                if a_tag and a_tag.has_attr('href') and a_tag['href'].startswith('/wiki/'):
                    name = a_tag.get_text()
                    link = 'https://en.wikipedia.org' + a_tag['href']
                    characters.append({'name': name, 'link': link})

        with open('comicbooks/static/comicbooks/dc_characters_scrape.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for char in characters:
                writer.writerow([char['name'], char['link']])

    return characters

def dc_scrape(request):
    characters = dc_characters_scrape(request)
    return render(request,'comicbooks/dc_scrape.html', {'characters': characters})

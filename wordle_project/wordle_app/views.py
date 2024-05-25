# wordle_app/views.py
import random
import requests
from django.shortcuts import render, redirect

# Sample word list
WORDS = ['APPLE', 'BERRY', 'CHESS', 'DRIVE', 'EAGLE', 'FANCY', 'GIANT', 'HOUSE', 'INPUT', 'JOKER']

def is_valid_word(word):
    url = f"https://api.datamuse.com/words?sp={word.lower()}&max=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return len(data) > 0 and data[0]['word'] == word.lower()
    return False

def home(request):
    if request.method == 'POST':
        guess = request.POST['guess'].upper()
        if len(guess) != 5 or not is_valid_word(guess):
            grid = request.session.get('attempts', [[{'letter': '', 'color': ''} for _ in range(5)] for _ in range(6)])
            error_message = 'Word not in the dictionary' if len(guess) == 5 else 'Please enter a 5-letter word'
            return render(request, 'wordle_app/index.html', {'error': error_message, 'grid': grid})
        
        word = request.session.get('word')
        attempts = request.session.get('attempts', [])
        attempt = [{'letter': letter, 'color': ''} for letter in guess]
        
        for i, letter in enumerate(guess):
            if letter == word[i]:
                attempt[i]['color'] = 'green'
            elif letter in word:
                attempt[i]['color'] = 'yellow'
            else:
                attempt[i]['color'] = 'gray'
        
        attempts.append(attempt)
        request.session['attempts'] = attempts
        
        if guess == word or len(attempts) >= 6:
            return render(request, 'wordle_app/success.html', {'word': word, 'attempts': len(attempts)})

        grid = attempts + [[{'letter': '', 'color': ''} for _ in range(5)] for _ in range(6 - len(attempts))]
        return render(request, 'wordle_app/index.html', {'grid': grid})

    word = random.choice(WORDS)
    request.session['word'] = word
    request.session['attempts'] = []
    grid = [[{'letter': '', 'color': ''} for _ in range(5)] for _ in range(6)]
    return render(request, 'wordle_app/index.html', {'grid': grid})

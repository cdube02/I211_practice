from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

DINO_KEYS = ['slug', 'name', 'description', 'image', 'image-credit', 'source-url', 'source-credit']

with open('dinosaurs.csv', 'r') as csvfile:
    data = csv.DictReader(csvfile)
    dinosaurs = {row['slug']:{'name':row['name'],'description':row['description'],
'image':row['image'], 'image-credit':row['image-credit'], 'source-url':row['source-url'],
'source-credit':row['source-credit']} for row in data}


@app.route('/')
@app.route('/dino')
@app.route('/dino/<dino>')

def index(dino=None):
    dinosaurs=get_dinos()
    print(dino)
    if dino and dino in dinosaurs.keys():
        dinosaur = dinosaurs[dino]
        return render_template('dino.html', dinosaur=dinosaur)
    else:
        return render_template('index.html', dinosaurs=dinosaurs)

@app.route('/add-dino', methods=['GET', 'POST'])
def add_dino():
    if request.method == 'POST':
        dinosaurs = get_dinos()
        newDino={}
        newDino['slug'] = request.form['slug']       
        newDino['name'] = request.form['name']       
        newDino['description'] = request.form['description']       
        newDino['image'] = request.form['image']       
        newDino['image-credit'] = request.form['image-credit']
        newDino['source-url'] = request.form['source-url']       
        newDino['source-credit'] = request.form['source-credit']
        dinosaurs[request.form['name']] = newDino
        set_dinos(dinosaurs)
        return redirect(url_for('index'))   
    else:
        return render_template('add-dino.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dino-quiz', methods=['GET', 'POST'])
def dino_quiz():
    if request.method == 'POST':
        quizGuesses = {} 
        quizGuesses['q1'] = request.form['continents']
        quizGuesses['q2'] = request.form['eggs', 'false']
        quizGuesses['q3'] = request.form.getlist('herbivores')
        quizGuesses['q4'] = request.form['extinct']


        quizGuesses['Question 3'] == " and ".join(quizGuesses["Question 3"])

        quizAnswers = {
            'q1' : 'North America',
            'q2' : 'true',
            'q3' : 'Stegosaurus and Triceratops',
            'q4' : '66'
        }

        print(quizGuesses)

        return render_template('quiz-results.html', quizGuesses = quizGuesses, quizAnswers=quizAnswers)
        return redirect(url_for('index'))
    else:
        return render_template('dino-quiz.html')

def get_dinos():    
    with open('dinosaurs.csv', 'r') as csvfile:            
        data = csv.DictReader(csvfile)            
        dinosaurs = {}            
        for dino in data:                
            dinosaurs[dino['slug']] = dino    
    return dinosaurs

def set_dinos(dinosaurs):    
    with open('dinosaurs.csv', mode ='w', newline='') as csv_file:        
        writer = csv.DictWriter(csv_file, fieldnames=DINO_KEYS)        
        writer.writeheader()        
        for dino in dinosaurs.values():            
            writer.writerow(dino)
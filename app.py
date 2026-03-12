import os
from flask import Flask, render_template, request, redirect, url_for
from google.cloud import firestore

app = Flask(__name__)

# Initialize Firestore
db = firestore.Client()
notes_collection = db.collection('notes')

@app.route('/')
def index():
    notes = [doc.to_dict() | {'id': doc.id} for doc in notes_collection.stream()]
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    content = request.form.get('content')
    if content:
        notes_collection.add({'content': content})
    return redirect(url_for('index'))

@app.route('/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    notes_collection.document(note_id).delete()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

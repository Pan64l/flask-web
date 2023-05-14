# stored the route of all websites
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from . import database
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
#when you / route you will get the homepage
# return the homepage
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 2:
            flash('Please enter a note', category='error')
        else:
            new_note = Note(data=note, u_id = current_user.id)
            database.session.add(new_note)
            database.session.commit()
            flash('Note: %s' % note, category = 'success')
    return render_template('home.html', user = current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.u_id == current_user.id:
            database.session.delete(note)
            database.session.commit()

    return jsonify({})
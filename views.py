from flask import Blueprint, render_template, request
from contact_importer import ContactImporter

views_blueprint = Blueprint('views', __name__,)


@views_blueprint.route('/')
def index():
    return render_template('index.html', current_user={})


@views_blueprint.route('/exporter')
def export_runner():
    return render_template('exporter.html')


@views_blueprint.route('/create_batch', methods=['GET', 'POST'])
def create_batch():
    if request.method == 'POST':
        importer = ContactImporter()
        try:
            batch_id = importer.create_batch(request.files.get('file'))
            return render_template('create_batch.html', batch_id=batch_id)
        except:
            return render_template('create_batch.html')
    return render_template('create_batch.html')
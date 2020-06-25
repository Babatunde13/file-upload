from flask import Flask, render_template ,request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
# from flask_marshmallow import Marshmallow
import os
from io import BytesIO

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir, 'db.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='adsdnekj22WBKNMR'

db=SQLAlchemy(app)
# ma = Marshmallow(app)

class Form(FlaskForm):
    file = FileField('Upload File', 
                        validators=[DataRequired()])
    submit = SubmitField('Submit')

class FileStorage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    file=db.Column(db.LargeBinary)

    def __repr__(self):
        return f'<{self.name}>'

# class ProductSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'name' 'description', 'price', 'key')
    
# product_schema=ProductSchema(Strict=True)
# products_schema=ProductSchema(Strict=True, many=True)

@app.route('/', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = Form()
    if form.validate_on_submit():
        newfile=FileStorage(name=form.file.data.filename,
                            file=form.file.data.read())
        db.session.add(newfile)
        db.session.commit()
        return f'{form.file.data.filename} is saved to the database successfully'
    return render_template('index.html', form=Form())


@app.route('/downloads/<int:id>')
def download(id):
    file_data = FileStorage.query.get_or_404(id)
    return send_file(BytesIO(file_data.file), attachment_filename=file_data.name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
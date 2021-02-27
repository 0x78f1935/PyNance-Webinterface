from flask_classful import FlaskView, route
from flask import render_template

from backend import db, pynance

class HomePageView(FlaskView):
    
    decorators = [ ]

    def get(self):
        return render_template('index.html')
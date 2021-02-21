from flask_classful import FlaskView, route
from flask import render_template

class HomePageView(FlaskView):
    
    decorators = [ ]

    def get(self):
        return render_template('index.html')
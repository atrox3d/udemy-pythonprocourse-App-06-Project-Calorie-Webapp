from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request

from temperature import Temperature
from calorie import Calorie

app = Flask(__name__)


class HomePage(MethodView):
    template = 'index.html'

    def get(self):
        return render_template(self.template)


class CaloriesformPage(MethodView):
    template = 'calories_form_page.html'

    def get(self):
        return render_template(self.template, caloriesform=CaloriesForm())


class CaloriesForm(Form):
    country = StringField('Country: ', default='italy')
    city = StringField('City: ', default='turin')

    weight = StringField('Weight: ', default='95')
    height = StringField('Height: ', default='175')
    age = StringField('Age: ', default='50')

    button = SubmitField('Submit')


app.add_url_rule(
    '/',
    view_func=HomePage.as_view('home_page')
)
app.add_url_rule(
    '/calories_form',
    view_func=CaloriesformPage.as_view('calories_form_page')
)


app.run(debug=True)

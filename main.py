from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request

from temperature import Temperature
from calorie import Calorie

app = Flask(__name__)


class HomePage(MethodView):
    template = 'index.html'                                                     # set template html file

    def get(self):
        return render_template(self.template)                                   # render template for get request


class CaloriesformPage(MethodView):
    template = 'calories_form_page.html'                                        # set template html file

    def get(self):
        return render_template(
            self.template,
            caloriesform=CaloriesForm()                                         # new form with defaults
        )

    def post(self):
        caloriesform = CaloriesForm(request.form)                               # get form post data

        temperature = Temperature(                                              # instantiate Temperature
            country=caloriesform.country.data,
            city=caloriesform.city.data
        ).get()                                                                 # get value

        calorie = Calorie(                                                      # instantiate Calorie
            weight=float(caloriesform.weight.data),                             # converto to float
            height=float(caloriesform.height.data),                             # converto to float
            age=float(caloriesform.age.data),                                   # converto to float
            temperature=temperature
        )

        calories = calorie.calculate()                                          # get value

        return render_template(
                    self.template,
                    caloriesform=caloriesform,                                  # from post data
                    calories=calories,                                          # calories value
                    result=True                                                 # flag for output
        )


class CaloriesForm(Form):                                                       # set form fields
    country = StringField('Country: ', default='italy')
    city = StringField('City: ', default='turin')

    weight = StringField('Weight: ', default='95')
    height = StringField('Height: ', default='175')
    age = StringField('Age: ', default='50')

    button = SubmitField('Submit')


app.add_url_rule(                                                               # set / route
    '/',
    view_func=HomePage.as_view('home_page')
)
app.add_url_rule(                                                               # set /calories_form route
    '/calories_form',
    view_func=CaloriesformPage.as_view('calories_form_page')
)


app.run(debug=True)

from flask import Flask
from flask import render_template
import pygal
from pygal.style import Style
import random

app = Flask(__name__)

@app.route("/")
def chart():

    F = open('/var/www/FlaskApp/FlaskApp/templates/price_list.txt', 'r')
    rates_and_time = F.read().split('\n')
    rates_list = rates_and_time[0].split()
    rates = [float(i) for i in rates_list]
    times = rates_and_time[1].split()
    F.close()

    H = open('/var/www/FlaskApp/FlaskApp/templates/_data_.txt', 'r')
    twt_and_time = H.read().split('\n')
    positive = [int(i) for i in twt_and_time[0].split()]
    negitive = [int(i) for i in twt_and_time[1].split()]
    tim = twt_and_time[2].split()
    H.close()

    custom_style_0 = Style(colors=('#F59A00', '#F59A00'), background = 'transparent', plot_background = 'transparent')
    line_chart = pygal.StackedLine(x_label_rotation=35, interpolate='cubic', style = custom_style_0, height = 300)
    line_chart.x_labels = times
    line_chart.add('USD', rates)
    chart = line_chart.render(is_unicode=True)
    
    custom_style_1 = Style(colors=('#5EA9DD', '#EC164C'), background = 'transparent', plot_background = 'transparent')
    stackedbar_chart = pygal.StackedBar(x_label_rotation=35, style = custom_style_1, height = 300)
    stackedbar_chart.x_labels = tim
    stackedbar_chart.add('Pos', positive)
    stackedbar_chart.add('Neg', negitive)
    chart2 = stackedbar_chart.render(is_unicode=True)

    return render_template('index.html', chart2=chart2, chart=chart)


if __name__ == "__main__":
    app.run(debug=True)

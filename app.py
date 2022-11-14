import flask
import pickle
import pandas as pd

# Use pickle to load in the pre-trained model.
with open(f'model/model.pkl', 'rb') as f:
    model = pickle.load(f)

app = flask.Flask(__name__, template_folder='templates')
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return flask.render_template('main.html')
    if flask.request.method == 'POST':
        frequency = flask.request.form['frequency']
        angle_of_attack = flask.request.form['angle of attack']
        chord_length = flask.request.form['chord length']
        fsv = flask.request.form['free-stream velocity']
        ssdt = flask.request.form['suction side disp thick']
        input_variables = pd.DataFrame([[frequency, angle_of_attack, chord_length,fsv,ssdt]],
        columns=['Frequency', 'Angle of attack', 'Chord length','Free-stream velocity','Suction side disp thick'],dtype=float)
        prediction = round(model.predict(input_variables)[0],3)
        return flask.render_template('main.html',
                                     original_input={'Frequency': frequency,
                                                     'Angle of attack': angle_of_attack,
                                                     'Chord length': chord_length,
                                                     'Free-stream velocity': fsv,
                                                     'Suction side disp thick': ssdt},
                                     result=prediction,
                                     )
if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///diet.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

total_cal = 0


class diet(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(200), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    total_calories = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}"


class maint(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    my_gender = db.Column(db.String(200), nullable=False)
    my_weight = db.Column(db.Integer, nullable=False)
    my_height = db.Column(db.Integer, nullable=False)
    my_activity = db.Column(db.String(200), nullable=False)
    my_age = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    my_maint = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.my_gender}"

@app.route('/', methods=['GET', 'POST'])
def home():
    global total_cal
    if request.method == 'POST':
        f_name = request.form['title']
        cal = request.form['desc']
        total_cal=total_cal+int(cal)
        #total_cal = db.session.query(func.sum(diet.calories)).scalar()
        if f_name and cal:
            Diet = diet(food_name=f_name, calories=cal, total_calories=total_cal)
            db.session.add(Diet)
            db.session.commit()
    alldiet = diet.query.all()
    return render_template('index.html', alldiet=alldiet)


@app.route('/maintenance', methods=['GET', 'POST'])
def maintenance():
    if request.method == 'POST':
        m_gender = request.form['gender']
        m_age = request.form['age']
        m_weight = request.form['weight']
        m_height = request.form['height']
        m_activity = request.form['activity']
        if m_activity == "Sedentary":
            act_fact = 1.2
        if m_activity == "Moderately active":
            act_fact = 1.375
        if m_activity == "Vigorously active":
            act_fact = 1.55
        if m_activity == "Extremely active":
            act_fact = 1.725
        if m_gender == "Male":
            m_maint = round(
                ((10*int(m_weight))+(6.25*int(m_height))-(5*int(m_age)) + 5)*act_fact)
        elif m_gender == "Female":
            m_maint = round(
                ((10*int(m_weight))+(6.25*int(m_height))-(5*int(m_age)) - 161)*act_fact)

        Maint = maint(my_gender=m_gender, my_weight=m_weight, my_height=m_height,
                      my_activity=m_activity, my_age=m_age, my_maint=m_maint)
        db.session.add(Maint)
        db.session.commit()

    allmaint = maint.query.all()
    return render_template('calculateMaintenance.html', allmaint=allmaint)


@app.route('/blog')
def blog():
    alldiet = diet.query.all()
    return render_template('blog.html')


@app.route('/update/<int:sno>')
def update(sno):
    Diet = diet.query.filter_by(sno=sno).first()
    return render_template('update.html', Diet=Diet)


@app.route('/delete/<int:sno>')
def delete(sno):
    Diet = diet.query.filter_by(sno=sno).first()
    db.session.delete(Diet)
    db.session.commit()
    return redirect("/")


@app.route('/maintenance/delete/<int:sno>')
def maint_delete(sno):
    Maint = maint.query.filter_by(sno=sno).first()
    db.session.delete(Maint)
    db.session.commit()
    return redirect("/maintenance")


if __name__ == "__main__":
    app.run(debug=True, port=8000)

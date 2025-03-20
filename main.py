from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, text

app = Flask(__name__)
con_str = "mysql://root:cset155@localhost/boatsdb"
engine = create_engine(con_str, echo=True)
connection = engine.connect()

@app.route('/')
def greeting():
    return render_template('index.html')

@app.route('/boats')
def boats():
    search_query = request.args.get('search', '')
    if search_query:
        if search_query.isdigit():
            boats = connection.execute(text("SELECT * FROM boats WHERE id = :search"), {"search": int(search_query)}).fetchall()
        else:
            boats = connection.execute(text("SELECT * FROM boats WHERE name LIKE :search OR type LIKE :search"), {"search": f"%{search_query}%"}).fetchall()
    else:
        boats = connection.execute(text('SELECT * FROM boats ORDER BY id DESC LIMIT 10')).fetchall()
    return render_template('boats.html', boats=boats, search_query=search_query)

@app.route('/boatcreate', methods=['GET', 'POST'])
def createboat():
    if request.method == 'POST':
        try:
            connection.execute(text(
                'INSERT INTO boats (id, name, type, ouwner_id, rental_price) VALUES (:id, :name, :type, :ouwner_id, :rental_price)')
                , request.form)
            connection.commit()
            return redirect(url_for('boats'))
        except:
            return render_template("boat_create.html", error="Failed to add boat")
    return render_template("boat_create.html")

@app.route('/boatupdate/<int:boat_id>', methods=['GET', 'POST'])
def updateboat(boat_id):
    if request.method == 'POST':
        try:
            connection.execute(text(
                'UPDATE boats SET name=:name, type=:type, ouwner_id=:ouwner_id, rental_price=:rental_price WHERE id=:id')
                , {**request.form, 'id': boat_id})
            connection.commit()
            return redirect(url_for('boats'))
        except:
            return render_template("boat_create.html", error="Update failed", boat_id=boat_id)
    boat = connection.execute(text('SELECT * FROM boats WHERE id=:id'), {'id': boat_id}).fetchone()
    return render_template("boat_create.html", boat=boat)

@app.route('/boatdelete/<int:boat_id>', methods=['POST'])
def deleteboat(boat_id):
    try:
        connection.execute(text('DELETE FROM boats WHERE id=:id'), {'id': boat_id})
        connection.commit()
    except:
        pass
    return redirect(url_for('boats'))

if __name__ == '__main__':
    app.run(debug=True)
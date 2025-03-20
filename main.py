from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, text

app = Flask(__name__)
con_str = "mysql://root:cset155@localhost/boatsdb"
engine = create_engine(con_str, echo=True)
connection = engine.connect()

@app.route('/')
def greeting():
    return render_template('index.html')

@app.route('/boats', methods=['GET', 'POST'])
def boats():
    search_query = request.args.get('search', '').strip()
    boat_id = request.args.get('boat_id')
    edit_mode = request.args.get('edit_mode') == 'True'
    boat = None
    
    if request.method == 'POST':
        boat_id = request.form.get('id')
        name = request.form['name']
        type_ = request.form['type']
        ouwner_id = request.form['ouwner_id']
        rental_price = request.form['rental_price']

        try:
            if boat_id:  
                connection.execute(text(
                    "UPDATE boats SET name=:name, type=:type, ouwner_id=:ouwner_id, rental_price=:rental_price WHERE id=:id"
                ), {"id": boat_id, "name": name, "type": type_, "ouwner_id": ouwner_id, "rental_price": rental_price})
            else: 
                connection.execute(text(
                    "INSERT INTO boats (name, type, ouwner_id, rental_price) VALUES (:name, :type, :ouwner_id, :rental_price)"
                ), {"name": name, "type": type_, "ouwner_id": ouwner_id, "rental_price": rental_price})
            connection.commit()
        except Exception as e:
            print("Error adding/updating boat:", e)

        return redirect(url_for('boats'))  
    
   
    if edit_mode and boat_id:
        boat = connection.execute(text("SELECT * FROM boats WHERE id=:id"), {"id": boat_id}).fetchone()
   
    if search_query:
        if search_query.isdigit():
            boats = connection.execute(text("SELECT * FROM boats WHERE id = :search"), {"search": int(search_query)}).fetchall()
        else:
            boats = connection.execute(text("SELECT * FROM boats WHERE name LIKE :search OR type LIKE :search"), 
                {"search": f"%{search_query}%"}).fetchall()
    else:
        boats = connection.execute(text("SELECT * FROM boats ORDER BY id DESC LIMIT 10")).fetchall()

    return render_template('boats.html', boats=boats, search_query=search_query, edit_mode=edit_mode, boat=boat)

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

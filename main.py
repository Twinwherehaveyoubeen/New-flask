from flask import Flask, render_template, request 
from sqlalchemy import create_engine, text 

app = Flask(__name__)
#Connection string is in thr format 
con_str = "mysql://root:cset155@localhost/boatsdb"
engine= create_engine(con_str, echo=True )
conection = engine.connect()


@app.route('/')
def greeting():
    return render_template('index.html')  

@app.route('/boats')
def boats():
    boats = conection.execute(text('select * from boats')).all()
    return render_template('boats.html', boats=boats[:10])


@app.route('/boatcreate', methods = ['GET'])
def getboat():
    return render_template("boat_create.html")



@app.route('/boatcreate', methods = ['POST'])
def createboat():
    try:
        conection.execute(text('insert into boats values( :id, :name, :type, :owner_id, :rental_price )'), request.form)
        conection.commit()
        return render_template("boat_create.html", error = "failed", success = "Sucessful")
    except:
         return render_template("boat_create.html")


@app.route('/<name>')  
def greet(name):
    return render_template('User.html', user=name)  




if __name__ == '__main__':
    app.run(debug=True)



# @app.route('/hello')
# def hello():
#     return "Hello"


# @app.route('/hello/<int:name>')
# def serveCoffee(name):
#     return f"The next number is,  {name + 1}"

# @app.route('/donut')
# def serveDonut():
#     return "Here is your donut."


# if __name__ == '__main__':
#     app.run(debug=True)

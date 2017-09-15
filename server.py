from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'mydb')

app.secret_key = 'KeepItSecretKeepItSafe'

@app.route('/users')
def index():
   
    query = "SELECT id, CONCAT(first_name,' ',last_name) AS full_name, email,  DATE_FORMAT(created_at,'%M %e %Y') AS created_at FROM users"                          
    users = mysql.query_db(query)  
    return render_template('index.html', all_users=users)

@app.route('/users/<id>', methods=['GET'])
def show_user(id):
    data = {'id': id} 
    query = "SELECT id, first_name, last_name , email,  DATE_FORMAT(created_at,'%M %e %Y') AS created_at FROM users WHERE id=:id"
    result = mysql.query_db(query, data)   
    print 'result at show' , result
    return render_template('show_user.html', user=result)

@app.route('/users/<id>/edit', methods=['GET'])
def edit_user(id):
    data = {'id': id} 
    print "at edit page", data
    
    query = "SELECT id, first_name, last_name , email,  DATE_FORMAT(created_at,'%M %e %Y') AS created_at FROM users WHERE id=:id"
    result = mysql.query_db(query, data)   
    print 'result at show' , result
    return render_template('edit_user.html', user=result)

@app.route('/users/<id>', methods=['POST'])
def update(id):
    data = {'id': id,
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email']
    } 
    query = "UPDATE users SET  first_name=:first_name, last_name=:last_name , email=:email,  created_at = NOW() WHERE id=:id "
    mysql.query_db(query, data)   
    
    my_url='/users/'+id
    return redirect(my_url)

@app.route('/users/create', methods=['POST'])
def create_new_entry():
    data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email']
    } 

    query = "INSERT INTO users (first_name, last_name, email, created_at) VALUES (:first_name, :last_name, :email, NOW() ) "
    print 'query so far', query, data
    

    mysql.query_db(query, data)   
    query = "SELECT id FROM users ORDER BY created_at DESC LIMIT 1"
    result= mysql.query_db(query)
    print "result", result
    
    my_url='/users/'+str(result[0]['id'])
    print 'URL',my_url
    return redirect(my_url)

@app.route('/users/new')
def displayUpdate():
    return render_template('add_user.html')


@app.route('/users/<id>/destroy', methods=['GET'])
def delete(id):
    data = {
        'id':id
    }
    print "delete", data
    query = 'DELETE FROM users WHERE id=:id'
    mysql.query_db(query, data)  
    return redirect('/users')

app.run(debug=True)
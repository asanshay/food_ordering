from flask import Flask, render_template, request, redirect , url_for
import json

app = Flask(__name__)

foods = []
with open('food.txt','r') as f:
    content = f.readlines()
    for item in content:
        foods.append(item)



@app.route('/')
def home():
    return render_template('home.html',foods=foods)


@app.route('/add',methods=["GET","POST"])
def add():
    if request.method == 'POST':
        add_item = request.form.get('add_item')
        if add_item != None and add_item != '' and add_item not in foods:
            foods.append(add_item)
            with open('food.txt','a') as f:
                f.write(f'{add_item}\n')

    elif request.method == 'GET':
        dindex = request.args.get('dindex','None')   # Gets the delete index of a particular food item
        if dindex != 'None' and dindex != '':
            removefromtxt('food.txt',int(dindex))
            del foods[int(dindex)]
    return render_template('add.html',foods=foods)

@app.route('/order',methods=['POST','GET'])
def order():
    if request.method == 'POST':
        food = request.form.get('food_name')
        name = request.form.get('full_name')
        
        if food == '' or name == '':
            return redirect(url_for('home'))

        with open('orders.csv','a') as file:
            file.write(f"{name}, {food}\n")

    elif request.method == 'GET':
        if request.args.get('redirect') == "redirect":
            print(request.args.get('redirect'))
            return redirect(url_for('home'))

    return render_template('orders.html',food1=food,name1=name)

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        passwords = getjson('passwords.json') 

        username = request.form.get('username')
        password = request.form.get('password')
        users = passwords['users']

        if username in users:
            if username == users[username]['username'] and password == users[username]['password']: 
                return redirect(url_for('add'))

    return render_template('login.html')

@app.route('/sign-up',methods=["GET","POST"])
def signup():
    error = "Enter a password"
    if request.method == 'POST':
        if request.form.get('password') != request.form.get('password1'):
            error = "Passwords are not the same, try again"
            return render_template('sign.html',error=error)
        else:
            username = request.form.get('name')
            password = request.form.get('password')
            print(username,password)
            passwords = getjson('passwords.json')
            passwords['users'][username] = {"username":username,"password":password}

            with open('passwords.json','w') as f:
                json.dump(passwords,f)

            return redirect(url_for('login'))

    return render_template('sign.html',error=error) 

def removefromtxt(filename,index):
    with open(filename,'r') as f:
        lines = f.readlines()

    del lines[index]

    with open(filename,'w') as f:
        f.writelines(lines)
    
def getjson(filename):
    with open(filename,'r') as f:
        content = json.load(f)

    return content

if __name__ == '__main__':
    app.run(debug=True)


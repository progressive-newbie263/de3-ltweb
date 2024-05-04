from flask import Flask, render_template, request, redirect, flash, jsonify
import requests
import json

app = Flask(__name__)
app.secret_key = "11225450"
base_url = 'http://127.0.0.1:5500/Supplier'
sqldbname = "Shopping.db"

@app.route('/')
def index():
    # Get all department from web api
    response = requests.get(base_url)
    # Check if the response is successful
    if response.status_code == 200:
        # Parse the response as a JSON object
        suppliers = response.json()
        # Render the supplier.html templates with the users data
        return render_template('supplier.html', suppliers = suppliers)
    else:
        # display an error message
        flash('Somthing went wrong. Please try again later')
    return render_template('supplier.html')

@app.route('/delete/<int:SupplierID>', methods = ['GET', 'POST'])
def delete(SupplierID):
    if request.method == 'POST':
        # send a delete request to the web api to delete the supplier by id
        response = requests.delete(f'{base_url}/{SupplierID}')
        # Check if the response is successful
        if response.status_code == 200:
            # display successful message
            flash(f'Department {SupplierID} deleted successfully')
            # Redirect to the home page
            return redirect('/')
        else:
            # Display an error message
            flash('Something went wrong. please try again later')
            return render_template('delete.html')
    else:
        # send a GET request to the web api to get the supplier by id
        response = requests.get(f'{base_url}/{SupplierID}')
    # Check if the response is successful
    if response.status_code == 200:
        # parse the response as a JSON object
        supplier = response.json()
        # render the delete.html template with the department
        return render_template('delete.html', supplier=supplier)
    else:
        # display an error message
        flash('Department not found')
        return render_template('delete.html')
    
@app.route('/add', methods = ['GET', 'POST'])
def add():
    #check if the request method is POST
    if request.method == 'POST':
        SupplierName = request.json.get('SupplierName')
        EmailAddress = request.json.get('EmailAddress')
        Password = request.json.get('Password')
        Tel = request.json.get('Tel')
        TotalEmployee = request.json.get('TotalEmployee')

        # Check if Name, Account, Email, Password, Tel are valid
        if SupplierName and EmailAddress and Password and Tel and TotalEmployee:
            response = requests.post(base_url,
                                     json={'SupplierName': SupplierName,
                                           'EmailAddress': EmailAddress, 'Password': Password, 'Tel': Tel, 'TotalEmployee': TotalEmployee})
            # Check if the response is successful
            if response.status_code == 200:
                # parse the response as a JSON object
                supplier = response.json()
                # display a success message
                flash(f"Department {supplier['SupplierID']} added successfully")
                # redirect to the home page
                return redirect('/')
            else:
                # display an error message
                flash('something went wrong. please try again later')
                return render_template('add.html')
        else:
            # display an error message
            flash('Supplier are required')
    else:
        return render_template('add.html')

@app.route('/edit/<int:SupplierID>', methods = ['GET', 'POST'])
def edit(SupplierID):
    #check if request method is POST
    if request.method == 'POST':
        #GET the info from the form
        SupplierName = request.form.get('SupplierName')
        EmailAddress = request.form.get('EmailAddress')
        Password = request.form.get('Password')
        Tel = request.form.get('Tel')
        TotalEmployee = request.form.get('TotalEmployee')
        #Check if the SUPPLIER are valid
        if SupplierName and EmailAddress and Password and Tel and TotalEmployee:
            #SEND a PUT request to the web api with the Supplier as a JSON data
            response = requests.put(f'{base_url}/{SupplierID}',
                json = {
                    'SupplierName': SupplierName,
                    'EmailAddress': EmailAddress,
                    'Password': Password, 'Tel': Tel,
                    'TotalEmployee': TotalEmployee
                }
            )
            #check if the response is successful
            if response.status_code == 200:
                #display a success message
                flash(f'Supplier {SupplierID} updated successfully')
                #redirect to the home page
                return redirect('/')
            else:
                #display an error message
                flash('Something went wrong. Please try again later')
        else:
            flash('Department are required')
            return render_template('edit.html')
    else:
        #send a get request to the web api to get the department by id
        response = requests.get(f'{base_url}/{SupplierID}')
    #check if the response is successful
    if response.status_code == 200:
        #parse the response as a JSON object
        supplier = response.json()
        return render_template('edit.html', supplier = supplier)
    else:
        flash('department not found')
        return render_template('/Supplier/edit.html')

if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port = 5500)
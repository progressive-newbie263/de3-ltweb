from flask import Flask, request, jsonify, request
import sqlite3
import json

app = Flask(__name__)
sqldbname = 'Shopping.db'
# cau1
@app.route('/')
def index():
    student_info = '29_NguyenVinhQuang_03'
    return student_info

#2aa
@app.route('/Supplier', methods = ['GET'])
def get_suppliers():
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    # Query the db for all supplier
    cur.execute("SELECT * FROM Supplier")
    AllSupplier = cur.fetchall()
    # Convert the result to a list of dictionaries
    supplier_list = []
    for supplier in AllSupplier:
        supplier_list.append({
            'SupplierID': supplier[0], 
            'SupplierName': supplier[1],
            'EmailAddress': supplier[2], 
            'Password': supplier[3], 
            'Tel': supplier[4],
            'TotalEmployee': supplier[5]
        })
    # Return a list as a JSON response
    return jsonify(supplier_list)

@app.route('/Supplier/<int:SupplierID>', methods = ['GET'])
def get_supplier(SupplierID):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM Supplier WHERE SupplierID = ?",(SupplierID,))
    supplier = cur.fetchone()
    #Convert the result to a dictionaries
    if supplier:
        supplier_dict = {
            'SupplierID': supplier[0], 
            'SupplierName': supplier[1],
            'EmailAddress': supplier[2],
            'Password': supplier[3],
            'Tel': supplier[4],
            'TotalEmployee': supplier[5]
        }
        return jsonify(supplier_dict)
    else:
        return 'Department not found', 404

#2b
@app.route('/Supplier/<int:SupplierID>', methods = ['DELETE'])
def delete_supplier(SupplierID):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute('DELETE FROM Supplier WHERE SupplierID = ?',(SupplierID,))
    conn.commit()
    if cur.rowcount > 0:
        return jsonify({'Message': 'Supplier deleted successfully.'})
    else:
        return "Supplier not found", 404

#3a
@app.route('/Supplier', methods = ['POST'])
def add_Supplier():
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()

    SupplierName = request.json.get('SupplierName')
    EmailAddress = request.json.get('EmailAddress')
    Password = request.json.get('Password')
    Tel = request.json.get('Tel')
    TotalEmployee = request.json.get('TotalEmployee')
    
    if SupplierName and EmailAddress and Password and Tel and TotalEmployee:
        #insert the department into the db
        cur.execute("INSERT INTO Supplier (SupplierName, EmailAddress, Password, Tel, TotalEmployee) VALUES (?, ?, ?, ?, ?)",
            (SupplierName, EmailAddress, Password, Tel, TotalEmployee))

        conn.commit()
        #GET the id of inserted supplier
        SupplierID = cur.lastrowid
        #Return the id as a JSON response
        return jsonify({'DepartmentID': SupplierID})
    else:
        return 'Supplier, Account and Password are required', 400

#3b
@app.route('/Supplier/<int:SupplierID>', methods =['PUT'])
def update_supplier(SupplierID):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()

    SupplierName = request.json.get('SupplierName')
    EmailAddress = request.json.get('EmailAddress')
    Password = request.json.get('Password')
    Tel = request.json.get('Tel')
    TotalEmployee = request.json.get('TotalEmployee')
    if SupplierName and EmailAddress and Password and Tel and TotalEmployee:
        cur.execute("UPDATE Department SET SupplierName = ?, EmailAddress = ?,"
                    "Password = ?, Tel = ?, TotalEmployee WHERE SupplierID = ?",
                    (SupplierName,EmailAddress, Password, Tel, TotalEmployee,SupplierID))
        conn.commit()
        if cur.rowcount > 0:
            return jsonify({'message': 'Supplier update successfully.'})
        else:
            return 'Supplier not found', 404
    else:
        return 'SupplierName, EmailAddress, Password, Tel, TotalEmployee are required'

#4a
@app.route('/check_Supplier', methods = ['POST'])
def check_supplier():
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()

    EmailAddress = request.json.get('EmailAddress')
    Password = request.json.get('Password')

    cur.execute("SELECT * FROM Supplier WHERE EmailAddress = ? AND Password = ?", (EmailAddress, Password))
    department = cur.fetchone()
    #Kiem tra ton tai
    if department:
        department_info = {
            'DepartmentID': department[0],
            'DepartmentName': department[1],
            'AccountName': department[2],
            'EmailAddress': department[3],
            'Password': department[4],
            'Tel': department[5],
            'Location': department[6]
        }
        return jsonify({'message': 'Supplier co ton tai', 'Supplier_Info': department_info})
    else:
        return jsonify({'message': 'Supplier not found'})

#4b
@app.route('/search_Supplier', methods = ['POST'])
def search_supplier():
    search_query = request.json.get('search_query')
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    # Thuc thi truy van de tim kiem
    cur.execute("SELECT * FROM Supplier WHERE SupplierName LIKE ? OR AccountName LIKE ? OR EmailAddress LIKE ?",
                ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
    
    suppliers = cur.fetchall()
    # Chuyen doi ket qua thanh danh sach dic
    supplier_list = []
    for supplier in suppliers:
        department_info = {
            'DepartmentID': supplier[0],
            'DepartmentName': supplier[1],
            'EmailAddress': supplier[2],
            'Password': supplier[3],
            'Tel': supplier[4],
            'TotalEmployee': supplier[5]
        }
        supplier_list.append(department_info)
    return jsonify(supplier_list)

#4c
@app.route('/Supplier_product/<int:SupplierID>', methods = ['GET'])
def get_product(SupplierID):
    #ket noi db
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()

    #Truy van de lay danh sach san pham cua ncc
    cur.execute("SELECT * FROM Product WHERE SupplierID = ?",(SupplierID,))
    products = cur.fetchall()

    #Chuyen doi ket qua thanh danh sach dics
    product_list = []
    for product in products:
        product_info = {
            'ProductID': product[0],
            'SupplierID': product[1],
            'ProductName': product[2],
            'Price': product[3]
        }
        product_list.append(product_info)
    return jsonify(product_list)

#4d
@app.route('/add_Supplier', methods = ['POST'])
def add_Suppliers():
    #nhan danh sach nhung ncc tu JSON
    suppliers = request.get_json()
    #ket noi db
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    #lap tung ncc de them vao db
    for supplier in suppliers:
        cur.execute("INSERT INTO Department (SupplierName, EmailAddress, Password, Tel, TotalEmployee) VALUES (?, ?, ?, ?, ?)",
            (supplier['SupplierName'], supplier['EmailAddress'], supplier['Password'], supplier['Tel'], supplier['TotalEmployee']))
    conn.commit()
    
    return jsonify({'message': 'Suppliers added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
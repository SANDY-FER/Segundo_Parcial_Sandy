from flask import Flask, render_template, request, redirect, session, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key_for_sessions'

@app.before_request
def initialize_session():
    if 'products' not in session:
        session['products'] = []

@app.route('/')
def index():
    return render_template('index.html', products=session.get('products', []))

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_product = {
            'id': len(session['products']) + 1,
            'name': request.form['name'],
            'quantity': request.form['quantity'],
            'price': request.form['price'],
            'expiry_date': request.form['expiry_date'],
            'category': request.form['category']
        }
        products = session.get('products', [])
        products.append(new_product)
        session['products'] = products
        
        flash('Producto agregado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('form.html')

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    products = [p for p in session.get('products', []) if p['id'] != product_id]
    session['products'] = products
    flash('Producto eliminado correctamente.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

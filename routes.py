import os
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from app import app
from forms import QuoteRequestForm, AdminLoginForm, ProductForm
from data_store import data_store

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def index():
    products = data_store.get_all_products()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = data_store.get_product(product_id)
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('index'))
    return render_template('product_detail.html', product=product)

@app.route('/quote/<int:product_id>', methods=['GET', 'POST'])
def quote_request(product_id):
    product = data_store.get_product(product_id)
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('index'))
    
    form = QuoteRequestForm()
    
    if form.validate_on_submit():
        quote_data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'city': form.city.data,
            'state': form.state.data,
            'country': form.country.data,
            'vehicle_make': form.vehicle_make.data,
            'vehicle_year': int(form.vehicle_year.data),
            'vehicle_model': form.vehicle_model.data,
            'remarks': form.remarks.data,
            'product_id': product_id
        }
        
        quote = data_store.add_quote(quote_data)
        flash(f'Quote request submitted successfully! Reference ID: {quote.id}', 'success')
        return redirect(url_for('index'))
    
    return render_template('quote_request.html', form=form, product=product)

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    
    if form.validate_on_submit():
        if data_store.check_admin_credentials(form.username.data, form.password.data):
            session['admin_logged_in'] = True
            session['admin_username'] = form.username.data
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials.', 'error')
    
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the admin panel.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    products = data_store.get_all_products()
    quotes = data_store.get_all_quotes()
    return render_template('admin/dashboard.html', products=products, quotes=quotes)

@app.route('/admin/add_product', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    form = ProductForm()
    
    if form.validate_on_submit():
        # Handle file upload
        main_image_url = 'https://via.placeholder.com/600x600/ccc/333?text=No+Image'
        
        if form.main_image.data:
            file = form.main_image.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to avoid conflicts
                import time
                timestamp = str(int(time.time()))
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                main_image_url = f"/static/uploads/{filename}"
        
        # Parse sizes and widths
        sizes = [size.strip() for size in form.sizes.data.split(',') if size.strip()]
        widths = [width.strip() for width in form.widths.data.split(',') if width.strip()]
        
        product_data = {
            'name': form.name.data,
            'description': form.description.data,
            'price': form.price.data,
            'main_image': main_image_url,
            'additional_images': [],
            'bolt_pattern': form.bolt_pattern.data,
            'sizes': sizes,
            'widths': widths
        }
        
        product = data_store.add_product(product_data)
        flash(f'Product "{product.name}" added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/add_product.html', form=form)

@app.route('/admin/quotes')
@admin_required
def admin_quotes():
    quotes = data_store.get_all_quotes()
    return render_template('admin/quotes.html', quotes=quotes)

@app.route('/admin/quote/<int:quote_id>/status/<status>')
@admin_required
def update_quote_status(quote_id, status):
    if status in ['pending', 'contacted', 'completed']:
        if data_store.update_quote_status(quote_id, status):
            flash(f'Quote status updated to {status}.', 'success')
        else:
            flash('Quote not found.', 'error')
    else:
        flash('Invalid status.', 'error')
    
    return redirect(url_for('admin_quotes'))

@app.route('/admin/product/<int:product_id>/delete')
@admin_required
def admin_delete_product(product_id):
    if data_store.delete_product(product_id):
        flash('Product deleted successfully.', 'success')
    else:
        flash('Product not found.', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

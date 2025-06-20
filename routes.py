import os
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from app import app, db
from forms import QuoteRequestForm, AdminLoginForm, ProductForm
from models import Product, Quote, Admin

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/quote/<int:product_id>', methods=['GET', 'POST'])
def quote_request(product_id):
    product = Product.query.get_or_404(product_id)
    form = QuoteRequestForm()
    
    if request.method == 'POST':
        # Get form data directly from request
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()
        country = request.form.get('country', '').strip()
        vehicle_make = request.form.get('vehicle_make', '').strip()
        vehicle_year = request.form.get('vehicle_year', '').strip()
        vehicle_model = request.form.get('vehicle_model', '').strip()
        remarks = request.form.get('remarks', '').strip()
        
        # Basic validation
        if first_name and last_name and email and phone and city and state and country and vehicle_make and vehicle_year and vehicle_model:
            try:
                year_int = int(vehicle_year)
                if 1900 <= year_int <= 2030:
                    quote = Quote(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone,
                        city=city,
                        state=state,
                        country=country,
                        vehicle_make=vehicle_make,
                        vehicle_year=year_int,
                        vehicle_model=vehicle_model,
                        remarks=remarks,
                        product_id=product_id
                    )
                    
                    db.session.add(quote)
                    db.session.commit()
                    flash(f'Quote request submitted successfully! Reference ID: {quote.id}', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Please enter a valid vehicle year (1900-2030).', 'error')
            except ValueError:
                flash('Please enter a valid vehicle year.', 'error')
        else:
            flash('Please fill in all required fields.', 'error')
    
    return render_template('quote_request.html', form=form, product=product)

# Test route for debugging login
@app.route('/test-login')
def test_login():
    with open('test_login.html', 'r') as f:
        return f.read()

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if username and password:
            admin = Admin.query.filter_by(username=username).first()
            if admin and admin.check_password(password):
                session['admin_logged_in'] = True
                session['admin_username'] = username
                flash('Logged in successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password.', 'error')
        else:
            flash('Please enter both username and password.', 'error')
    
    form = AdminLoginForm()
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
    products = Product.query.all()
    quotes = Quote.query.all()
    return render_template('admin/dashboard.html', products=products, quotes=quotes)

@app.route('/admin/add_product', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    form = ProductForm()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '0')
        bolt_pattern = request.form.get('bolt_pattern', '').strip()
        sizes_data = request.form.get('sizes', '').strip()
        widths_data = request.form.get('widths', '').strip()
        
        # Validate required fields
        if name and description and price and bolt_pattern:
            try:
                price_float = float(price)
                if price_float > 0:
                    # Handle file upload - use local SVG image
                    main_image_url = '/static/images/wheel-placeholder.svg'
                    
                    # Parse sizes and widths
                    sizes = [size.strip() for size in sizes_data.split(',') if size.strip()]
                    widths = [width.strip() for width in widths_data.split(',') if width.strip()]
                    
                    product = Product(
                        name=name,
                        description=description,
                        price=price_float,
                        main_image=main_image_url,
                        additional_images=[],
                        bolt_pattern=bolt_pattern,
                        sizes=sizes,
                        widths=widths
                    )
                    
                    db.session.add(product)
                    db.session.commit()
                    flash(f'Product "{product.name}" added successfully!', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Price must be greater than 0.', 'error')
            except ValueError:
                flash('Invalid price format.', 'error')
        else:
            flash('Please fill in all required fields.', 'error')
    
    return render_template('admin/add_product.html', form=form)

@app.route('/admin/quotes')
@admin_required
def admin_quotes():
    quotes = Quote.query.all()
    return render_template('admin/quotes.html', quotes=quotes)

@app.route('/admin/quote/<int:quote_id>/status/<status>')
@admin_required
def update_quote_status(quote_id, status):
    if status in ['pending', 'contacted', 'completed']:
        quote = Quote.query.get(quote_id)
        if quote:
            quote.status = status
            db.session.commit()
            flash(f'Quote status updated to {status}.', 'success')
        else:
            flash('Quote not found.', 'error')
    else:
        flash('Invalid status.', 'error')
    
    return redirect(url_for('admin_quotes'))

@app.route('/admin/product/<int:product_id>/delete')
@admin_required
def admin_delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
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

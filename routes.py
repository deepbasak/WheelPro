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
    
    if form.validate_on_submit():
        quote = Quote(
            first_name=form.first_name.data or "",
            last_name=form.last_name.data or "",
            email=form.email.data or "",
            phone=form.phone.data or "",
            city=form.city.data or "",
            state=form.state.data or "",
            country=form.country.data or "",
            vehicle_make=form.vehicle_make.data or "",
            vehicle_year=int(form.vehicle_year.data or 2020),
            vehicle_model=form.vehicle_model.data or "",
            remarks=form.remarks.data or "",
            product_id=product_id
        )
        
        db.session.add(quote)
        db.session.commit()
        flash(f'Quote request submitted successfully! Reference ID: {quote.id}', 'success')
        return redirect(url_for('index'))
    
    return render_template('quote_request.html', form=form, product=product)

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
    
    if form.validate_on_submit():
        # Handle file upload
        main_image_url = 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=600&h=600&fit=crop&crop=center'
        
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
        sizes_data = form.sizes.data or ""
        widths_data = form.widths.data or ""
        sizes = [size.strip() for size in sizes_data.split(',') if size.strip()]
        widths = [width.strip() for width in widths_data.split(',') if width.strip()]
        
        product = Product(
            name=form.name.data or "",
            description=form.description.data or "",
            price=form.price.data or 0.0,
            main_image=main_image_url,
            additional_images=[],
            bolt_pattern=form.bolt_pattern.data or "",
            sizes=sizes,
            widths=widths
        )
        
        db.session.add(product)
        db.session.commit()
        flash(f'Product "{product.name}" added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
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

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

@app.route('/wheels')
def wheels():
    """Store page with filtering capabilities"""
    # Get filter parameters from request
    design_type = request.args.get('design_type')
    vehicle_type = request.args.get('vehicle_type')
    series = request.args.get('series')
    new_stock = request.args.get('new_stock')
    
    try:
        # Build the query
        query = Product.query
        
        # Apply filters - with try/except to handle case where columns might not exist
        if design_type:
            try:
                query = query.filter_by(design_type=design_type)
            except Exception:
                # Column might not exist yet - skip this filter
                pass
                
        if vehicle_type:
            try:
                query = query.filter_by(vehicle_type=vehicle_type)
            except Exception:
                # Column might not exist yet - skip this filter
                pass
                
        if series:
            try:
                query = query.filter_by(series=series)
            except Exception:
                # Column might not exist yet - skip this filter
                pass
                
        if new_stock:
            try:
                query = query.filter_by(is_new_stock=1)
            except Exception:
                # Column might not exist yet - skip this filter
                pass
        
        # Get products
        products = query.all()
        
        # Get all unique filter values from the database for dropdowns
        all_products = Product.query.all()
        
        # Try to get filter values from products, handle case where columns don't exist
        try:
            design_types = sorted(set(p.design_type for p in all_products if p.design_type))
        except Exception:
            design_types = []
            
        try:
            vehicle_types = sorted(set(p.vehicle_type for p in all_products if p.vehicle_type))
        except Exception:
            vehicle_types = []
            
        try:
            series_list = sorted(set(p.series for p in all_products if p.series))
        except Exception:
            series_list = []
        
        # Import filter constants for new entries
        from data_store import DESIGN_TYPES, VEHICLE_TYPES, WHEEL_SERIES
        
        # If we couldn't get values from products, use the constants
        if not design_types:
            design_types = DESIGN_TYPES
        if not vehicle_types:
            vehicle_types = VEHICLE_TYPES
        if not series_list:
            series_list = WHEEL_SERIES
    except Exception as e:
        # In case of any database error, show a message and return empty results
        flash(f"Database error: {str(e)}. Please run the migration script.", "error")
        products = []
        design_types = DESIGN_TYPES
        vehicle_types = VEHICLE_TYPES
        series_list = WHEEL_SERIES
    
    return render_template('wheels.html', 
                          products=products, 
                          design_types=DESIGN_TYPES, 
                          vehicle_types=VEHICLE_TYPES, 
                          series_list=WHEEL_SERIES,
                          selected_design=design_type,
                          selected_vehicle=vehicle_type,
                          selected_series=series,
                          new_stock=new_stock)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/quote/<int:product_id>', methods=['GET', 'POST'])
def quote_request(product_id):
    product = Product.query.get_or_404(product_id)
    form = QuoteRequestForm()
    
    # Pre-populate wheel preference fields if product has those attributes
    if product.design_type:
        form.design_type.default = product.design_type
    if product.vehicle_type:
        form.vehicle_type.default = product.vehicle_type
    if product.series:
        form.series.default = product.series
    form.process()  # Process the form to apply the defaults
    
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
        design_type = request.form.get('design_type', '').strip()
        vehicle_type = request.form.get('vehicle_type', '').strip()
        series = request.form.get('series', '').strip()
        remarks = request.form.get('remarks', '').strip()
        
        # Basic validation
        if first_name and last_name and email and phone and city and state and country and vehicle_make and vehicle_year and vehicle_model and design_type and vehicle_type and series:
            try:
                year_int = int(vehicle_year)
                if 1900 <= year_int <= 2030:
                    # Store wheel preference info in remarks field for now
                    # In the future, you might want to add these fields to the Quote model
                    full_remarks = f"Design Type: {design_type}\nVehicle Type: {vehicle_type}\nWheel Series: {series}\n\n"
                    if remarks:
                        full_remarks += remarks
                    
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
                        remarks=full_remarks,
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
        bolt_pattern = request.form.get('bolt_pattern', '').strip()
        sizes_data = request.form.get('sizes', '').strip()
        widths_data = request.form.get('widths', '').strip()
        
        # Set default price value (hidden from UI)
        price_float = 0.01
        
        # Validate required fields
        if name and description and bolt_pattern:
            # Handle file upload
            main_image_url = '/static/images/wheel-placeholder.svg'
            
            # Handle multiple file uploads
            uploaded_files = request.files.getlist('main_image')
            additional_images = []
            
            if uploaded_files and uploaded_files[0].filename != '':
                import time
                
                # Check if using Cloudinary or local storage
                if app.config.get('USE_CLOUDINARY', False):
                    from cloud_storage import upload_file
                    
                    for i, file in enumerate(uploaded_files):
                        if file and file.filename and file.filename != '' and allowed_file(file.filename):
                            # Upload to Cloudinary
                            folder = "wheelrpo/wheels"
                            upload_result = upload_file(file, folder=folder)
                            
                            if upload_result and 'secure_url' in upload_result:
                                image_url = upload_result['secure_url']
                                
                                if i == 0:
                                    main_image_url = image_url
                                else:
                                    additional_images.append(image_url)
                else:
                    # Fallback to local storage
                    for i, file in enumerate(uploaded_files):
                        if file and file.filename and file.filename != '' and allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            # Add timestamp to avoid conflicts
                            timestamp = str(int(time.time()))
                            filename = f"{timestamp}_{i}_{filename}"
                            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                            file.save(filepath)
                            image_url = f"/static/uploads/{filename}"
                            
                            if i == 0:
                                main_image_url = image_url
                            else:
                                additional_images.append(image_url)
            
            # Parse sizes and widths
            sizes = [size.strip() for size in sizes_data.split(',') if size.strip()]
            widths = [width.strip() for width in widths_data.split(',') if width.strip()]
            
            # Get new fields
            design_type = request.form.get('design_type', '').strip()
            vehicle_type = request.form.get('vehicle_type', '').strip()
            series = request.form.get('series', '').strip()
            is_new_stock = int(request.form.get('is_new_stock', '0'))
            
            product = Product(
                name=name,
                description=description,
                price=price_float,
                main_image=main_image_url,
                additional_images=additional_images,
                bolt_pattern=bolt_pattern,
                sizes=sizes,
                widths=widths,
                design_type=design_type,
                vehicle_type=vehicle_type,
                series=series,
                is_new_stock=is_new_stock
            )
            
            db.session.add(product)
            db.session.commit()
            flash(f'Product "{product.name}" added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Please fill in all required fields.', 'error')
    
    return render_template('admin/add_product.html', form=form)

@app.route('/admin/quotes')
@admin_required
def admin_quotes():
    quotes = Quote.query.all()
    products = Product.query.all()
    products_dict = {product.id: product for product in products}
    return render_template('admin/quotes.html', quotes=quotes, products_dict=products_dict)

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

@app.route('/embed')
def embed_options():
    """Serve the embed options page"""
    return app.send_static_file('embed_options.html')

@app.route('/embed-code')
def embed_code():
    """Serve the simple embed code page"""
    return app.send_static_file('embed_code.html')

@app.route('/badge')
def badge():
    """Serve the badge code page"""
    return app.send_static_file('wheel_badge.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

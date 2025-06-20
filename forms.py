from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, FloatField, SelectField, IntegerField, PasswordField, FieldList, FormField
from wtforms.validators import DataRequired, Email, NumberRange, Length
from data_store import VEHICLE_MAKES, VEHICLE_YEARS

class QuoteRequestForm(FlaskForm):
    # Customer information
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=50)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=50)])
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=50)])
    
    # Vehicle information
    vehicle_make = SelectField('Vehicle Make', choices=[(make, make) for make in VEHICLE_MAKES], validators=[DataRequired()])
    vehicle_year = SelectField('Vehicle Year', choices=[(str(year), str(year)) for year in reversed(VEHICLE_YEARS)], validators=[DataRequired()])
    vehicle_model = StringField('Vehicle Model', validators=[DataRequired(), Length(min=1, max=50)])
    
    # Additional information
    remarks = TextAreaField('Remarks', validators=[Length(max=500)])

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    main_image = FileField('Main Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    bolt_pattern = StringField('Bolt Pattern', validators=[DataRequired(), Length(min=3, max=20)])
    
    # Dynamic fields for sizes and widths
    sizes = StringField('Available Sizes (comma-separated)', validators=[DataRequired()])
    widths = StringField('Available Widths (comma-separated)', validators=[DataRequired()])

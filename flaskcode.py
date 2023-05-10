from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.sqlite'
app.secret_key = 'secret_key'

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column('product_id', db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Integer)
    image = db.Column(db.String(100))
    description = db.Column(db.String(50))
    long_description = db.Column(db.String(500))
    enviromental = db.Column(db.String(30))

class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)




@app.route('/basket')
def basket():
    basket = session.get('basket', {})

    basket_products = []

    return render_template('basket.html', basket=basket.values(), len=len)





@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/single_product_page/<product_id>')
def single_product_page(product_id):
    prod = Product.query.filter_by(id=product_id).first()
    return render_template('single_product_page.html', product=prod)



@app.route('/add-to-basket/<product_id>', methods=['GET', 'POST'])
def add_to_basket(product_id):
    if request.method == 'POST':
        # get the product from the database using product_id
        product = Product.query.filter_by(id=product_id).first()
        # add the product to the user's basket
        basket = session.get('basket', {})
        if str(product_id) in basket:
            basket[str(product_id)]['quantity'] += 1
        else:
            basket[str(product_id)] = {'name': product.name, 'price': product.price, 'quantity': 1}
        session['basket'] = basket
        print(session['basket'])
        # redirect to the basket page
        return redirect('/basket')
    

  








if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        if len(Product.query.all()) != 0:
            app.run(debug=True)
        else:
            cat1 = Product(name="Wizard cat", price=30, image="images/wizard_cat.jpeg", description="magic cat",  long_description="A cat of many tricks, a master in the arts of magic. Can also perform card tricks. Does not come with a wand.", enviromental="high")
            cat2 = Product(name="Karate cat", price=75, image="images/karate_cat.jpg", description="can do a backflip", long_description="A master of many martial arts with many back belts. Lives in the mountains.", enviromental="high")
            cat3 = Product(name="George", price=0, image="images/george_cat.png", description="please take him", long_description="A pathetic excuse of a cat. Causes destruction wherever he goes.", enviromental="cat a strophic")
            cat4 = Product(name="Orange cat", price=6, image="images/orange_cat.jpg", description="most normal orange cat", long_description="A very strange cat. Chaotic but affectionate.", enviromental="extremely high")
            cat5 = Product(name="Big cat", price=100, image="images/big_cat.jpeg", description="a rather large boi", long_description="An absolute unit. Forever bulking. Doesn't move much. A cat of very few words, his presence speaks for him", enviromental="very low")
            cat6 = Product(name="Catfish", price=2000, image="images/catfish.jpg", description="can swim", long_description="Not quite sure how this is a cat to be honest however its in the name. Is able to switch between cat and fish I think.", enviromental="low")
            db.session.add_all([cat1, cat2, cat3, cat4, cat5, cat6])
            db.session.commit()

            app.run(debug=True)
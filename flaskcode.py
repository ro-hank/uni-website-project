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
        product = Product.query.filter_by(id=product_id).first()
        basket = session.get('basket', {})
        if str(product_id) in basket:
            basket[str(product_id)]['quantity'] += 1
        else:
            basket[str(product_id)] = {'name': product.name, 'price': product.price, 'quantity': 1}
        session['basket'] = basket
        print(session['basket'])
        return redirect('/basket')
    

  








if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        if len(Product.query.all()) != 0:
            app.run(debug=True)
        else:
            cat1 = Product(name="Wizard cat", price=30, image="images/wizard_cat.jpeg", description="magic cat",  long_description="A cat of many tricks, a master in the arts of magic. Can also perform card tricks. Does not come with a wand. A feline sorcerer that. can conjure up purrfect spells with a flick of their paw. From mesmerizing disappearing acts to mind-boggling levitations, this enigmatic furball will leave you spellbound. Wizard Cat dazzle you with their magical prowess, but they also moonlight as a card trick connoisseur. Prepare to be amazed as they shuffle their paws with uncanny agility and reveal cards with unparalleled finesse", enviromental="high")
            cat2 = Product(name="Karate cat", price=75, image="images/karate_cat.jpg", description="can do a backflip", long_description="a fierce feline warrior with a black belt in every martial art you can think of! This nimble ninja kitty is a force to be reckoned with, possessing lightning-fast reflexes and paws that pack a powerful punch. From karate chops to high-flying kicks, this martial arts maven is always ready to defend their territory with a swift and mighty paw. With their graceful movements and cat-like agility, they can scale walls and perform acrobatic stunts that will leave you in awe. Join forces with this formidable feline and unleash your inner warrior as you embark on an adventure of self-discovery and martial arts mastery.", enviromental="high")
            cat3 = Product(name="George", price=0, image="images/george_cat.png", description="please take him", long_description="A pathetic excuse of a cat. Causes destruction wherever he goes.  the epitome of feline chaos and mayhem! This mischievous furball is not your typical cool cat. With an unmatched talent for causing havoc and destruction, George leaves a trail of chaos wherever he sets his paws. From knocking over priceless ornaments to unraveling balls of yarn with unmatched enthusiasm, he is a true master of creating pandemonium. Don't be fooled by his innocent gaze and adorable purrs. George is a force to be reckoned with, and you never know what kind of mischief he'll conjure up next. ", enviromental="cat a strophic")
            cat4 = Product(name="Orange cat", price=6, image="images/orange_cat.jpg", description="most normal orange cat", long_description="A very strange cat. This peculiar feline is a walking paradox, defying all expectations. With an aura of mystique surrounding its every move, this cat is a fascinating blend of chaos and affection. One moment, it's knocking over vases and causing mayhem, and the next, it's curled up in your lap, purring with undeniable warmth. Its unpredictable nature keeps you on your toes, never knowing what bizarre antics or surprising displays of love it will unleash. It's as if the laws of normal cat behavior simply don't apply to this vibrant orange enigma.", enviromental="extremely high")
            cat5 = Product(name="Big cat", price=100, image="images/big_cat.jpeg", description="a rather large boi", long_description="An absolute unit in the feline kingdom! This majestic creature is forever in a bulking phase, boasting an impressive physique that commands attention. With muscles that ripple beneath its fur, this cat is a sight to behold. Yet, despite its imposing stature, the Big Cat prefers to conserve its energy and conserve it does. It's a master of the art of stillness, rarely seen moving, as if every motion requires a Herculean effort. This silent giant is a cat of few words, yet its mere presence speaks volumes. Its commanding aura and imposing figure leave no room for doubt - this is a cat that demands respect. So, prepare to be awed by the sheer magnitude of the Big Cat, and let its silent power captivate your imagination.", enviromental="very low")
            cat6 = Product(name="Catfish", price=2000, image="images/catfish.jpg", description="can swim", long_description="A creature that defies conventional feline expectations. Mysterious and perplexing, this peculiar being blurs the line between cat and fish, leaving us pondering its true nature. With an uncanny ability to seamlessly switch between its feline and aquatic forms, the Catfish navigates the world with unmatched versatility. When it's in its cat form, it exhibits all the typical behaviors of a feline: purring, stretching, and playfully pouncing on unsuspecting prey. But don't be fooled, for when the mood strikes, it effortlessly transforms into a sleek and graceful fish, effortlessly gliding through the water with finned finesse.", enviromental="low")
            db.session.add_all([cat1, cat2, cat3, cat4, cat5, cat6])
            db.session.commit()

            app.run(debug=True)
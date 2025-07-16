from ecommerce import db
from ecommerce.models import Product
from faker import Faker
import random

fake = Faker()

# Run this once
def populate_products():
    for i in range(1, 26):  # 25 products
        product = Product(
            name=f"Product {i}",
            description=fake.paragraph(nb_sentences=2),
            price=random.randint(199, 999),
            image=f"product{i}.jpg"  # make sure this matches your image filenames
        )
        db.session.add(product)
    db.session.commit()
    print("✅ Added 25 products successfully.")

if __name__ == "__main__":
    populate_products()

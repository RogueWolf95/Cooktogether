import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# Instantiate a Faker object
fake = Faker()

# Establish connection with SQLite Database
conn = sqlite3.connect('src\discord\cogs\core\components\sql\core.db')
cursor = conn.cursor()

# List of ingredients to choose from
ingredients = ['Sugar', 'Salt', 'Pepper', 'Olive Oil', 'Garlic', 'Onion', 'Tomato', 'Potato', 'Chicken', 'Beef', 'Pork', 'Fish']

# Generate test data for "User" table
for _ in range(1000):
    DUID = _
    Handle = fake.user_name()
    RegDate = fake.date_between(start_date='-5y', end_date='today')
    Email = fake.email()
    is21 = bool(random.getrandbits(1))
    
    cursor.execute("INSERT INTO User VALUES (?, ?, ?, ?, ?)", (DUID, Handle, RegDate, Email, is21))

# Generate test data for "Ingredient" table
for i, ingredient in enumerate(ingredients):
    IngredientID = i
    IngredientName = ingredient
    
    cursor.execute("INSERT INTO Ingredient VALUES (?, ?)", (IngredientID, IngredientName))

# Generate test data for "Recipe" table
for _ in range(50):
    RecipeID = _
    RecipeName = fake.catch_phrase()
    RecipeDesc = fake.sentence()
    hasAlchohol = bool(random.getrandbits(1))
    
    cursor.execute("INSERT INTO Recipe VALUES (?, ?, ?, ?)", (RecipeID, RecipeName, RecipeDesc, hasAlchohol))

# Generate test data for "RecipeIngredient" table
for _ in range(200):
    RecipeID = random.randint(0, 49)
    IngredientID = random.randint(0, len(ingredients) - 1)
    Measurement = f"{random.randint(1,5)} {random.choice(['teaspoon', 'tablespoon', 'cup', 'g', 'kg', 'lb', 'oz'])}"
    
    try:
        cursor.execute("INSERT INTO RecipeIngredient VALUES (?, ?, ?)", (RecipeID, IngredientID, Measurement))
    except sqlite3.IntegrityError:
        pass  # Skip if the combination already exists

# Commit changes and close connection
conn.commit()
conn.close()

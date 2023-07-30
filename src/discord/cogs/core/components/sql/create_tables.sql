
-- Create table "User"
CREATE TABLE IF NOT EXISTS User(
    DUID INTEGER PRIMARY KEY,
    Handle TEXT NOT NULL,
    RegDate DATE NOT NULL,
    Email TEXT,
    is21 BOOLEAN
);

-- Create table "Ingredient"
CREATE TABLE IF NOT EXISTS Ingredient(
    IngredientID INTEGER PRIMARY KEY,
    IngredientName TEXT
);

-- Create table "Ingredient"
CREATE TABLE IF NOT EXISTS Recipe(
    RecipeID INTEGER PRIMARY KEY,
    RecipeName TEXT,
    RecipeDesc TEXT,
    hasAlchohol BOOLEAN
);

-- Create table "RecipeIngredient"
CREATE TABLE IF NOT EXISTS RecipeIngredient(
    RecipeID INTEGER,
    IngredientID INTEGER,
    Measurement TEXT,
    PRIMARY KEY (RecipeID, IngredientID),
    FOREIGN KEY (RecipeID) REFERENCES Recipe(RecipeID),
    FOREIGN KEY (IngredientID) REFERENCES Ingredient(IngredientID)
);
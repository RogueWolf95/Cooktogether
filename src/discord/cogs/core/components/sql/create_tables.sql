--User Table
CREATE TABLE User (
    user_id INTEGER PRIMARY KEY, 
    username TEXT,
    discord_user_id TEXT UNIQUE,
    avater_url TEXT
);

--Recipe Table
CREATE TABLE Recipe (
    recipe_id INTEGER PRIMARY KEY,
    title TEXT,
    image_url TEXT,
    description TEXT,
    rating REAL
);

-- Ingredient Table
CREATE TABLE Ingredient (
    ingredient_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT
);

-- Step Table
CREATE TABLE Step (
    step_id INTEGER PRIMARY KEY,
    recipe_id INTEGER,
    step_number INTEGER,
    instruction TEXT,
    FOREIGN KEY (recipe_id) REFERENCES Recipe (recipe_id)
);


-- Rating Table
CREATE TABLE Like (
    like_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    recipe_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES User (user_id),
    FOREIGN KEY (recipe_id) REFERENCES Recipe (recipe_id)
);


    
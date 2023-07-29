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
    
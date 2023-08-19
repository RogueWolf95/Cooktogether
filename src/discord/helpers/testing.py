
import json


TESTING = True


if TESTING:
    with open("src/recipes/Halloween_cookies.txt", "r") as fin:
        test_recipe_txt = fin.read()
    with open("src/recipes/test_dish.json", "r") as json_in:
        test_recipe_json = json.load(json_in)
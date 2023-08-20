import os
import json

def clean():
    for file in os.listdir("src/recipes"):
        if file.endswith(".txt"):
            os.remove(f"src/recipes/{file}")

def fix():
    fixes_total = 0
    for file in os.listdir("src/recipes"):
        if file.endswith(".json"):
            with open(f"src/recipes/{file}", "r") as json_in:
                json_file = json.load(json_in)

            if "name" not in json_file:
                fixes_total += 1
                    
            if "ingredients" not in json_file:
                fixes_total += 1
                    
            if "instructions" not in json_file:
                fixes_total += 1
                    
            if "description" not in json_file:
                fixes_total += 1
                    
            if "spice" not in json_file:
                fixes_total += 1
                json_file["spice"] = 0
                    
            if "rating" in json_file:
                fixes_total += 1
                del json_file["rating"]
                    
            if "ratings" not in json_file:
                fixes_total += 1
                json_file["ratings"] = {}
                    
            if "Fav_counts" not in json_file:
                fixes_total += 1
                json_file["Fav_counts"] = 0

            with open(f"src/recipes/{file}", "w") as json_out:
                json.dump(json_file, json_out, indent=4)
            
    print(fixes_total)


if __name__ == "__main__":
    clean()
    fix()
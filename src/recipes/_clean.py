import os

def clean():
    for file in os.listdir("src/recipes"):
        if file.endswith(".txt"):
            os.remove(f"src/recipes/{file}")

if __name__ == "__main__":
    clean()
from nextcord import Embed
import json

from src.discord.helpers import parser
from src.discord.helpers import colors



def get_spice_meter_img()->dict:
    with open(f"src/images/spice_meter/spice_meter.json", "r") as fin:
        return json.load(fin)


class RecipeEmbedding:
    spice_meter = get_spice_meter_img()

    def create_embeds(self, dish_name:str="Missing Name", message:dict=None) -> Embed:
        recipe_info = parser.recipe_parser(dish_name, message)
        title = f"Recipe for {dish_name}"


        r_embed = Embed(title=title, description=recipe_info["description_str"], color=colors.heat_color_scale(recipe_info["spice_int"]))
        r_embed.add_field(name="The Ingredients", value=recipe_info["ingredients_str"], inline=False)
        r_embed.set_thumbnail(url=self.spice_meter[f"spice_meter_{recipe_info['spice_int']}"])

        if len(recipe_info["instructions_str"]) > 1000:
            recipe_info["instructions_str"] = recipe_info["instructions_str"][:1000] + "\n\nOUTPUT TOO LONG\n..."
        i_embed = Embed(title=title, color=colors.heat_color_scale(recipe_info["spice_int"]))
        i_embed.add_field(name="The Instructions", value=recipe_info["instructions_str"], inline=False)
        i_embed.set_footer(text="Created by AI")


        return r_embed, i_embed

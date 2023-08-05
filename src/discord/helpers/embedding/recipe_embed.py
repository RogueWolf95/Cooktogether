from nextcord import Embed
import re
import json

from src.discord.helpers import parser
from src.discord.helpers import colors



def get_spice_meter_img()->dict:
    with open(f"src/images/spice_meter/spice_meter.json", "r") as fin:
        return json.load(fin)


class RecipeEmbedding:
    spice_meter = get_spice_meter_img()


    def create_embeds(self, title:str="title", message:dict=None) -> Embed:
        recipe_info = parser.recipe_parser()
        
        r_embed = Embed(title=title, description=part_3, color=colors.heat_color_scale(spice_rating))
        r_embed.add_field(name="The Ingredients", value=part_1, inline=False)
        r_embed.set_thumbnail(url=self.spice_meter[f"spice_meter_{spice_rating}"])

        if len(part_2) > 1000:
            part_2 = part_2[:1000] + "\n\nOUTPUT TOO LONG\n..."
        i_embed = Embed(title=title, color=colors.heat_color_scale(spice_rating))
        i_embed.add_field(name="The Instructions", value=part_2, inline=False)
        i_embed.set_footer(text="Created by AI")


        return r_embed, i_embed

from nextcord import Embed
import re
import json

from src.discord.helpers.colors import heat_color_scale
from src.discord.helpers.string_splitter import split_recipe_string


def get_spice_meter()->dict:
    with open(f"src/images/spice_meter/spice_meter.json", "r") as fin:
        return json.load(fin)



class RecipeEmbedding:
    spice_meter = get_spice_meter()

    def extract_spicy_integer(self, s:str):
        match = re.search(r'\d+', s)
        if match:
            spice_rating = int(match.group())
            if spice_rating == 0:
                return 1
            else:
                return spice_rating
        else:
            return 0
        
    def extract_section_pretext(self, s:str):
        s = s.split("\n")[1:]
        s = "\n".join(s)
        return s


    def create_embeds(self, title:str="title", message:dict=None) -> Embed:
        part_idx = split_recipe_string(message)

        part_1:str = self.extract_section_pretext(message[part_idx[0]:part_idx[1]-1])
        part_2:str = self.extract_section_pretext(message[part_idx[1]:part_idx[2]-1])
        part_3:str = self.extract_section_pretext(message[part_idx[2]:part_idx[3]-1])
        part_4:str = message[part_idx[3]:].strip("Part: 4")
        spice_rating = self.extract_spicy_integer(part_4)


        r_embed = Embed(title=title, description=part_3, color=heat_color_scale(spice_rating))
        r_embed.add_field(name="The Ingredients", value=part_1, inline=False)
        r_embed.set_thumbnail(url=self.spice_meter[f"spice_meter_{spice_rating}"])

        if len(part_2) > 1000:
            part_2 = part_2[:1000] + "\n\nOUTPUT TOO LONG\n..."
        i_embed = Embed(title=title, color=heat_color_scale(spice_rating))
        i_embed.add_field(name="The Instructions", value=part_2, inline=False)
        i_embed.set_footer(text="Created by AI")


        return r_embed, i_embed

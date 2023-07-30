import os
import openai

from nextcord.ext import commands
import nextcord
import datetime
from src.discord.helpers.embedding.recipe_embed import RecipeEmbedding
from src.discord.bot import DiscordBot

openai.organization = os.getenv("OPEN_AI_ORG")
openai.api_key = os.getenv("OPEN_AI_TOKEN")


class AICog(commands.Cog):
    def __init__(self, bot):
        self.recipe_embedding = RecipeEmbedding()
        self.bot: DiscordBot = bot
        self.name = "Admin Commands"
        print("AICog connected")


    def generate_response(self, messages:list[dict], token_limit:int) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Using GPT-3.5-turbo
            messages=messages,
            max_tokens=token_limit  # Maximum length of the output
        )

        return response['choices'][0]['message']['content']


    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="contains", description="type an ingredient or list of ingredients")
    async def contains(self, interaction: nextcord.Interaction, ingredient: str, allergies: str=None) -> None:
        print("INFO", f"{interaction.user.name} used AICog.contains at {datetime.datetime.now()}")
        """use AI to find recipes that contain certain ingredients"""
        await interaction.response.defer()

        user_message = f"Create a list of 5 recipe names that contain {ingredient}"
        if allergies:
            user_message += f" exclude recipes that contain {allergies}"

        messages = [
                {"role": "system", "content": "You are a helpful sous chef."},
                {"role": "user", "content":  user_message}
            ]

        response = self.generate_response(messages, 150)
        await interaction.followup.send(response)

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="get_recipe", description="use AI to find recipes that contain certain ingredients")
    async def get_recipe(self, interaction: nextcord.Interaction, dish_name: str, serving_count: int=2) -> None:
        print("INFO", f"{interaction.user.name} used AICog.contains at {datetime.datetime.now()}")
        """use AI to find recipes that contain certain ingredients"""
        await interaction.response.defer()
        messages = [
                {"role": "system", "content": f"You are a helpful sous chef preparing a concise recipe.\n===\nPart 1: List the Ingredients for {serving_count} servings\n- ingredient 1\n- ingredient 2\n===\nPart 2: Write concise Instructions\n1.\n2.\n3.\n===\nPart 3: short Description of dish\nPart 4: spice factor integer between one and ten"},
                {"role": "user", "content": f'Generate a step by step recipe for {dish_name}'}
            ]
        response = self.generate_response(messages, 1000)
        with open(f"src/recipes/{dish_name}.txt", "w") as fout:
            fout.writelines(response)

        r_embed, i_embed = self.recipe_embedding.create_embeds(title=f"Recipe for {dish_name}", message=response)

        await interaction.followup.send(embed=r_embed)
        await interaction.send(embed=i_embed)


def setup(bot: commands.Bot):
    bot.add_cog(AICog(bot))


import asyncio
import os
import openai
import inspect
from nextcord.ext import commands
import nextcord
import datetime
from src.discord.helpers.embedding.recipe_embed import RecipeEmbedding
from src.discord.bot import DiscordBot
from src.discord.helpers import parser
from src.discord.helpers import json_manager

openai.organization = os.getenv("OPEN_AI_ORG")
openai.api_key = os.getenv("OPEN_AI_TOKEN")


class AICog(commands.Cog):
    REACTIONS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

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
        print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """use AI to find recipes that contain certain ingredients"""
        await interaction.response.defer()
        
        embed = nextcord.Embed(title=f"Recipes that contain {ingredient}.")

        user_message = f"Create a list of 5 recipe names that contain {ingredient}"
        if allergies:
            embed.description = f"Excluding: {allergies}"
            user_message += f" exclude recipes that contain {allergies}"

        messages = [
                {"role": "system", "content": "You are a helpful sous chef."},
                {"role": "user", "content":  user_message}
            ]

        response = self.generate_response(messages, 150)

        embed.add_field("========", response)

        message = await interaction.followup.send(embed=embed)

        # Add reactions to the message
        for reaction in self.REACTIONS:
            await message.add_reaction(reaction)

        # Start a background task to watch for reactions
        self.bot.loop.create_task(self.wait_for_reaction(interaction, messages, response, message))
        

    async def wait_for_reaction(self, interaction, messages, response, message):
            def check(reaction, user):
                return user == interaction.user and str(reaction.emoji) in self.REACTIONS and reaction.message.id == message.id

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                await self.handle_reaction(interaction, messages, response, reaction)
            except asyncio.TimeoutError:
                # Handle the timeout, e.g., remove the reactions from the message
                for reaction in self.REACTIONS:
                    await message.remove_reaction(reaction, self.bot.user)


    async def handle_reaction(self, interaction, messages, response, reaction):
        """Handle the reaction pressed by the user"""
        response = response.split("\n")

        if str(reaction.emoji) == "1️⃣":
            # handle first recipe
            await self.get_recipe(interaction, response[0].replace("1. ", ""))
        elif str(reaction.emoji) == "2️⃣":
            # handle second recipe
            await self.get_recipe(interaction, response[1].replace("2. ", ""))
        elif str(reaction.emoji) == "3️⃣":
            # handle second recipe
            await self.get_recipe(interaction, response[2].replace("3. ", ""))
        elif str(reaction.emoji) == "4️⃣":
            # handle second recipe
            await self.get_recipe(interaction, response[3].replace("4. ", ""))
        elif str(reaction.emoji) == "5️⃣":
            # handle second recipe
            await self.get_recipe(interaction, response[4].replace("5. ", ""))







    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="get_recipe", description="use AI to find recipes that contain certain ingredients")
    async def get_recipe(self, interaction: nextcord.Interaction, dish_name: str, serving_count: int=1) -> None:
        print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """use AI to find recipes that contain certain ingredients"""
        
        try:
            await interaction.response.defer()
        except nextcord.errors.InteractionResponded:
            pass

        if f"{dish_name}.json" in os.listdir("src/recipes"):
            recipe_info = json_manager.open_json(f"src/recipes/{dish_name}.json")
        else:
            messages = [
                    {"role": "system", "content": f"You are a helpful sous chef preparing a concise recipe.\n===\nPart 1: List the Ingredients for {serving_count} servings\n- ingredient 1\n- ingredient 2\n===\nPart 2: Write concise Instructions\n1.\n2.\n3.\n===\nPart 3: short Description of dish\nPart 4: spice factor integer between one and ten"},
                    {"role": "user", "content": f'Generate a step by step recipe for {dish_name}'}
                ]
            response = self.generate_response(messages, 1000)
            recipe_info = parser.recipe_parser(dish_name, response)
            json_manager.save_json(f"src/recipes/{dish_name}.json", recipe_info)

        r_embed, i_embed = self.recipe_embedding.create_embeds(dish_name, recipe_info)


        await interaction.followup.send(embed=r_embed)
        await interaction.followup.send(embed=i_embed)


# =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="help", description="use AI to find solutions to your culinary problems")
    async def help(self, interaction: nextcord.Interaction, query:str) -> None:
        print("INFO", f"{interaction.user.name} used AICog.contains at {datetime.datetime.now()}")
        """use AI to find solutions to your culinary problems"""
        await interaction.response.defer()

        messages = [
                {"role": "system", "content": "You are a helpful sous chef. Please help me with my culinary problem. do not respond to non culinary questions"},
                {"role": "user", "content":  query + "do not respond to non culinary questions"}
            ]
        response = self.generate_response(messages, 500)

        embed = nextcord.Embed(title=query.capitalize(), description=response, color=nextcord.Color.blurple())

        await interaction.followup.send(embed=embed)



# =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="cuisine", description="use AI to find recipes of a certain cuisine")
    async def cuisine(self, interaction: nextcord.Interaction, cuisine_name: str, allergies: str=None) -> None:
        print("INFO", f"{interaction.user.name} used AICog.contains at {datetime.datetime.now()}")
        """use AI to find recipes of a certain cuisine"""
        await interaction.response.defer()

        user_message = f"Create a list of 5 recipe names that are a {cuisine_name} dish"
        if allergies:
            user_message += f" exclude recipes that contain {allergies}"

        messages = [
                {"role": "system", "content": "You are a helpful sous chef."},
                {"role": "user", "content":  user_message}
            ]

        response = self.generate_response(messages, 150)
        await interaction.followup.send(response)
        
        
# =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="get_nutrition", description="use AI to find nutrition facts for dish")
    async def get_nutrition(self, interaction: nextcord.Interaction, dish_name: str, serving_count: int=2) -> None:
        print("INFO", f"{interaction.user.name} used AICog.contains at {datetime.datetime.now()}")
        """use AI to find nutrition facts for dish"""
        await interaction.response.defer()
        messages = [
                {"role": "system", "content": f"You are a helpful sous chef preparing a concise recipe.\n===\nPart 1: List the Ingredients for {serving_count} servings\n- ingredient 1\n- ingredient 2\n===\nPart 2: Give nutrtional facts for calories, fats, carbohydrates, and protein\n1.\n2.\n3.\n===\nPart 3: short Description of dish\n"},
                {"role": "user", "content": f'Generate nutritional information for {dish_name}'}
            ]
        response = self.generate_response(messages, 500)

        r_embed, i_embed = self.recipe_embedding.create_embeds(title=f"Recipe for {dish_name}", message=response)

        await interaction.followup.send(embed=r_embed)
        await interaction.send(embed=i_embed)


def setup(bot: commands.Bot):
    bot.add_cog(AICog(bot))


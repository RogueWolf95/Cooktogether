import asyncio
import nextcord
from src.discord.helpers.save_pdf import create_recipe_doc, stamp_image_to_pdf


async def wait_for_idx_reaction(self, interaction, response, message):
    def check(reaction, user):
        return user == interaction.user and str(reaction.emoji) in self.IDX_REACTIONS and reaction.message.id == message.id

    try:
        reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=check)
        await self.handle_idx_reaction(interaction, response, reaction)
    except asyncio.TimeoutError:
        # Handle the timeout, e.g., remove the reactions from the message
        for reaction in self.IDX_REACTIONS:
            await message.remove_reaction(reaction, self.bot.user)


async def handle_idx_reaction(self, interaction, response, reaction):
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


async def wait_for_options_reaction(self, interaction, recipe_info, message):
        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in self.OPTIONS_REACTIONS and reaction.message.id == message.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=check)
            await self.handle_options_reaction(interaction, reaction, recipe_info)
        except asyncio.TimeoutError:
            # Handle the timeout, e.g., remove the reactions from the message
            for reaction in self.OPTIONS_REACTIONS:
                await message.remove_reaction(reaction, self.bot.user)


async def handle_options_reaction(self, interaction, reaction, recipe_info):
    print(reaction)
    output_path = f"src/temp/{recipe_info['name']}.pdf"
    if str(reaction.emoji) == "💾":
        # handle save file
        create_recipe_doc(recipe_info, output_path)
        stamp_image_to_pdf(output_path, output_path, self.LOGO_PATH)
        
        await interaction.user.send(file=nextcord.File(output_path))
        
    elif str(reaction.emoji) == "⭐":
        # handle rating
        pass
        
    elif str(reaction.emoji) == "♥️":
        # handle favorite
        pass
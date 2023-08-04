from nextcord.ui import Modal, TextInput
from nextcord import Interaction
from datetime import datetime
import json

class RegisterModal(Modal):
    list_num = 1
    def __init__(self):
        self.list_num = RegisterModal.list_num
        super().__init__("Register your email for our newsletter", timeout=5 * 60)

        self.email = TextInput( 
                label=f"Email (Optional)",
                custom_id=f"RegisterModal_{self.list_num}",
                min_length=5,
                max_length=50,
            )
        self.add_item(self.email)


    async def callback(self, interaction: Interaction) -> None:

        user_dict = {
            "handle": interaction.user.display_name,
            "duid": interaction.user.id,
            "email": self.email.value,
            "reg_date": str(datetime.now()),
            "fav_recipes": [],
            "allergies": []
        }

        with open(f"src/users/{interaction.user.id}.json", "w") as json_out:
            json.dump(user_dict, json_out, indent=4)

        await interaction.send("received")
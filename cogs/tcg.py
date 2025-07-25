class TCG:
    # Basic Info
    def __init__(self, data):
        self.id = data.id
        self.name = data.name
        self.supertype = data.supertype
        self.subtypes = data.subtypes
        self.hp = data.hp
        self.types = data.types
        self.evolvesFrom = data.evolvesFrom
        self.rarity = data.rarity
        self.flavorText = data.flavorText

        # Abilities and Attacks
        self.abilities = data.abilities
        self.attacks = data.attacks
        self.weaknesses = data.weaknesses
        self.resistances = data.resistances
        self.retreatCost = data.retreatCost
        
        # Images
        self.imagesLarge = data.images.large
        self.imagesSmall = data.images.small
        
        # TCG Info
        self.lastUpdated = data.tcgplayer.updatedAt
        self.prices = data.tcgplayer.prices
        
        # Set info
        self.set = data.set

    def general_info(self):
        general_info = ""
        general_info += (f"HP: {self.hp}\n")
        general_info += (f"Type(s): {', '.join(self.types)}\n")
        general_info += (f"Rarity: {self.rarity}\n")
        general_info += (f"Evolves From: {self.evolvesFrom if self.evolvesFrom else 'N/A'}\n")
        general_info += (f"Flavor Text: {self.flavorText}\n")
        
        return general_info

    def abilities_info(self):
        abilities_info = ""
        if self.abilities:
            abilities_info += ("Abilities:\n")
            for ability in self.abilities:
                abilities_info += (f"- {ability.get('name')}: {ability.get('text')}\n")
        return abilities_info

    def extra_info(self):
        extra_info = ""
        # Display Attacks
        if self.attacks:
            extra_info += ("\nAttacks:\n")
            for attack in self.attacks:
                extra_info += (f"- {attack.name} (Cost: {attack.convertedEnergyCost}): {attack.text}\n")

        # Display Weaknesses and Resistances
        if self.weaknesses:
            extra_info += ("\nWeaknesses:\n")
            for weakness in self.weaknesses:
                extra_info += (f"- {weakness.type} (x{weakness.value})\n")
        if self.resistances:
            extra_info += ("\nResistances:\n")
            for resistance in self.resistances:
                extra_info += (f"- {resistance.type} (-{resistance.value})\n")
        return extra_info

    def tcg_info(self):
        tcg_info = ""
        if self.prices:
            tcg_info += ("\nTCGPlayer info:")
            if self.prices.normal:
                tcg_info += (f"- Normal Market Price: ${self.prices.normal.market}")          
            if self.prices.holofoil:
                tcg_info += (f"- Holofoil Market Price: ${self.prices.holofoil.market}")                           
            if self.prices.reverseHolofoil:
                tcg_info += (f"- Reverse Holofoil Market Price: ${self.prices.reverseHolofoil.market}")                         
            if self.prices.firstEditionHolofoil:
                tcg_info += (f"- First Edition Holofoil Market Price: ${self.prices.firstEditionHolofoil.market}")           
            if self.prices.reverseHolofoil:
                tcg_info += (f"- Reverse Holofoil Market Price: ${self.prices.reverseHolofoil.market}")
            
        return tcg_info
    
    def set_info(self):
        set_info = ""
        if self.set:
            set_info += ("\nSet Info:")
            set_info += (f"- Set Id: {self.set.id}")
            set_info += (f"- Set Name: {self.set.name}")
            set_info += (f"- Set Series: {self.set.series}")
            set_info += (f"- Printed Total: {self.set.printedTotal}")
            set_info += (f"- Set Total: {self.set.total}")
        
        set_info += (f"\nImage URL: {self.imagesLarge}")
        
        return set_info
    
    def __str__(self):
        return f"{self.name} - {self.supertype} ({self.rarity})\nHP: {self.hp}\nType(s): {', '.join(self.types)}"
class CharacterInfoDto:
    def __init__(self,
                 id,
                 name,
                 level,
                 exp,
                 expNeed,
                 hp, 
                 minMeleeDmg,
                 maxMeleeDmg,
                 minRangeDmg,
                 maxRangeDmg,
                 minMagicDmg,
                 maxMagicDmg,
                 healPower,
                 armor,
                 elementalResistance):
        
        self.id=id
        self.name=name
        self.level=level
        self.exp=exp
        self.expNeed=expNeed
        self.hp=hp
        self.minMeleeDmg=minMeleeDmg
        self.maxMeleeDmg=maxMeleeDmg
        self.minRangeDmg=minRangeDmg
        self.maxRangeDmg=maxRangeDmg
        self.minMagicDmg=minMagicDmg
        self.maxMagicDmg=maxMagicDmg
        self.healPower=healPower
        self.armor=armor
        self.elementalResistance=elementalResistance
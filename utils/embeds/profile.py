
# Discord
from discord import Embed, Member
from discord.ext.commands import command, Cog
# Utils
import utils
#Additions
from math import floor
from random import choice

class ProfileEmbed(Embed):

    bot = None

    def __init__(self, *args, **kwargs):
        #Gets the varibles for the embed
        type_ = kwargs.pop('type', None)
        user = kwargs.pop('user', Member)
        staff = kwargs.pop('staff', False)
        guild = user.guild
        quick = kwargs.pop('quick', False)
        sona = kwargs.pop('sona', 1)

        # Make the embed
        super().__init__(*args, **kwargs)

        #! Guild Checks
        if guild.id == self.bot.config['guilds']['FurryRoyaleID']:
            patron = self.bot.config['royale_patreon']
        else:
            patron = self.bot.config['razi_patreon']

        #! Define Varibles
        lvl = utils.Levels.get(user.id) 
        ss = utils.Settings.get(user.id)
        # mod = utils.Moderation.get(user.id)
        st = utils.Staff_Track.get(user.id)
        c = utils.Currency.get(user.id)
        inte = utils.Interactions.get(user.id)
        # items = utils.Items.get(user.id)
        # rel = utils.Relations.get(user.id)

        ch = utils.Sonas.get(user_id=user.id, slot=sona)
        print(ch)

        #* Required EXP varibles (Cant await in embeds...)
        if lvl.level == 0:
            requiredexp = 10
        elif lvl.level < 5:
            requiredexp = lvl.level*25
        else:
            requiredexp = round(lvl.level**3.35)

        #* get user's rank
        sorted_level_rank = utils.Levels.sort_levels()
        rank = sorted_level_rank.index(utils.Levels.get(user.id))


        # if rel.mate_id:
        #     mate_s = f"❧ ❤️ **Mated to:** <@{rel.mate_id}>"
        # else: mate_s = f"❧ ❌ **Doesn't have a Mate!**"
        
        # if rel.bestfriend_id:
        #     bff_s = f"❧ 💛 **BFF to:** <@{rel.bestfriend_id}>"
        # else: bff_s = f"❧ ❌ **Doesn't have a BFF!**"
        
        # if rel.owner_id:
        #     owner_s = f"❧ 💙**Pet to:** <@{rel.owner_id}>"
        # elif rel.pet_id:
        #     owner_s = f"❧ 💙**Owner to:** <@{rel.pet_id}>"
        # else: owner_s = f"❧ ❌**Doesn't have a Owner or Pet!**"


        #* Add Interactions
        if inte.premium == False:
            interact_gived = f"❧ Pats: **{inte.pats_given:,}**\n❧ Hugs: **{inte.hugs_given:,}**\n❧ Kisses: **{inte.kisses_given:,}**\n❧ Licks: **{inte.licks_given:,}**\n\n💤 **No premium!**"
            interact_received = f"❧ Pats: **{inte.pats_received:,}**\n❧ Hugs: **{inte.hugs_received:,}**\n❧ Kisses: **{inte.kisses_received:,}**\n❧ Licks: **{inte.licks_received:,}**"
        else:
            interact_gived = f"❧ Pats: **{inte.pats_given:,}**\n❧ Hugs: **{inte.hugs_given:,}**\n❧ Kisses: **{inte.kisses_given:,}**\n❧ Licks: **{inte.licks_given:,}**\n❧ Boops: **{inte.boops_given}**\n❧ Bites: **{inte.bites_given}**\n❧ Stabs: **{inte.stabs_given}**\n❧ Flirts: **{inte.flirts_given}**"
            interact_received = f"❧ Pats: **{inte.pats_received:,}**\n❧ Hugs: **{inte.hugs_received:,}**\n❧ Kisses: **{inte.kisses_received:,}**\n❧ Licks: **{inte.licks_received:,}**\n❧ Boops: **{inte.boops_received}**\n❧ Bites: **{inte.bites_received}**\n❧ Stabs: **{inte.stabs_received}**\n❧ Flirts: **{inte.flirts_received}**"


        #* Add Color
        self.color = ss.color

        #* Emojis
        amethyst_e = "<:Amethyst:766123218732843019>"
        diamond_e = "<:Diamond:766123219609976832>"
        emerald_e = "<:Emerald:766123219731611668>"
        phel_e = "<:PhelStone:766123219781419020>"
        silver_e = "<:Silver:766123219761233961>"
        gold_e = "<:GoldIngot:766123219827949596>"
        sapphire_e = "<:Sapphire:766123220201635850>"
        ruby_e = "<:Ruby:766123219928481852>"

        #* Add author
        self.set_author(name=f"{user.name}'s {type_} Profile", icon_url=user.avatar_url, url=patron)

        #* Add the types feild
        if type_ == "Loading":
            self.add_field(name='Loading...', value=f":3", inline=True)

        if type_ == "Default":
            self.add_field(name='INFORMATION', value=f"❧ Level Rank: **#{rank+1}**\n❧ Level: **{lvl.level}**\n❧ Exp: **{floor(lvl.exp):,}/{requiredexp:,}**\n", inline=True)
            self.add_field(name='OVERVIEW', value=f"Work In Progress...\n", inline=True)
            self.set_footer(text=f"| ✨ Sona | 💸 Currency | 🔮 Interactions |")

        if type_ == "Staff-Track":
            self.add_field(name='STAFF', value=f"❧ Mutes: {st.mutes}\n❧ Memes: {st.memes}\n❧ Nsfws: {st.nsfws}\n❧ Sonas: {st.mail_sonas}", inline=True)
            self.add_field(name='TRACK', value=f"❧ Purges: {st.purges}\n❧ Messages: {st.messages}\n❧ Monthly Msgs: {st.messages_month}\n❧ Verified: {st.mail_verification}", inline=True)
            if quick == False:
                self.set_footer(text=f"| 🔷 Return |")

        if type_ == "Currency":
            emotes = choice([1, 2, 3])
            if emotes == 1:
                emote_1 = silver_e
                emote_2 = gold_e
            elif emotes == 2:
                emote_1 = gold_e
                emote_2 = emerald_e
            elif emotes == 3:
                emote_1 = emerald_e
                emote_2 = diamond_e
            self.description = f"**{emote_1} 100x = 1 {emote_2} Ect.**"
            self.add_field(name='CURRENCY', value=f"❧ {silver_e} : **{floor(c.silver):,}x**\n❧ {gold_e} : **{floor(c.gold):,}x**\n❧ {emerald_e} : **{floor(c.emerald):,}x**\n❧ {diamond_e} : **{floor(c.diamond):,}x**", inline=True)
            self.add_field(name='SPECIAL', value=f"❧ {ruby_e} : **{floor(c.ruby):,}x**\n❧ {sapphire_e} : **{floor(c.sapphire):,}x**\n❧ {amethyst_e} : **{floor(c.amethyst):,}x**\n❧ {phel_e} : **{floor(c.phelstone):,}x**", inline=True)
            if quick == False:
                self.set_footer(text=f"| 🔷 Return |")

        # if type_ == "Items":
        #     self.add_field(name='Items', value=f"❧ 🍭 Daily Increaser: **{items.daily_increaser:,}**\n❧ 🧤 Thief's Gloves: **{items.thief_gloves:,}**\n❧ {bunny_e} Luck: **{items.rabbit_luck:,}/100**\n❧ 🍒 Lottery Tickets: **{c.lot_tickets:,}**", inline=True)
        #     self.add_field(name='𝙋𝙖𝙜𝙚 ２', value=f"❧ 🎉Party Popper: **{items.party_popper:,}**", inline=True)
        #     if quick == False:
        #         self.set_footer(text=f"| 🔷 Return |")

        if type_ == "Interactions":
            self.add_field(name='Given', value=interact_gived, inline=True)
            self.add_field(name='Received', value=interact_received, inline=True)
            if quick == False:
                self.set_footer(text=f"| 🔷 Return |")

        # if type_ == "Relationships":
        #     self.add_field(name='𝙍𝙀𝙇𝘼𝙏𝙄𝙊𝙉𝙎𝙃𝙄𝙋𝙎', value=f"{mate_s}\n{bff_s}\n{owner_s}", inline=True)
        #     if quick == False:
        #         self.set_footer(text=f"| 🔷 Return |")

        if type_ == "Sona":
            if staff == True:
                self.add_field(name='Name', value=f"{ch.name}", inline=True)
                self.add_field(name='Gender', value=f"{ch.gender}", inline=True)
                self.add_field(name='Age', value=f"{ch.age}", inline=True)
                self.add_field(name='Species', value=f"{ch.species}", inline=True)
                self.add_field(name='Weight', value=f"{ch.weight}", inline=True)
                self.add_field(name='Height', value=f"{ch.height}", inline=True)
                self.set_footer(text=f"| {sona}_sona |")
                if ch.bio != None:
                    self.add_field(name='Bio', value=ch.bio, inline=False)
                if ch.image != None:
                    self.set_image(url=ch.image)
            elif ch.verified == True:
                self.add_field(name='Name', value=f"{ch.name}", inline=True)
                self.add_field(name='Gender', value=f"{ch.gender}", inline=True)
                self.add_field(name='Age', value=f"{ch.age}", inline=True)
                self.add_field(name='Species', value=f"{ch.species}", inline=True)
                self.add_field(name='Weight', value=f"{ch.weight}", inline=True)
                self.add_field(name='Height', value=f"{ch.height}", inline=True)
                if ch.bio != None:
                    self.add_field(name='Bio', value=ch.bio, inline=False)
                if ch.image != None:
                    self.set_image(url=ch.image)
                if quick == False:
                    self.set_footer(text=f"| 🔷 Return |")
            else:
                self.add_field(name='Nothing?', value=f"❧ You don't have a verified character!\n❧ Do `.setsona`", inline=True)
                if quick == False:
                    self.set_footer(text=f"| 🔷 Return |")


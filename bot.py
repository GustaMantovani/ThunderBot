import discord
from discord.ext import commands
import logging
import requests
import os
from dotenv import load_dotenv

#Realizando um primeiro request antes da aplicação inciar para melhorar o tempo de resposta do bot
#segundo a documentação oficial do prodeck, esse é o único endpoint necessário
requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php')

#funções
def proDeckAPI_request(params):
    url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def get_card_info_by_name_and_language_ProDeckAPI(lang,cardName):
    if(lang=='en'):
        params = {
            'name': cardName
        }
    else:
        params = {
            'name': cardName,
            'language': lang
        }
    return proDeckAPI_request(params)
    
def get_data_by_lang_and_cardId(lang,id):
    if(lang=='en'):
        params = {
            'id': id
        }
    else:
        params = {
            'id': id,
            'language': lang
        }

    return proDeckAPI_request(params)


def translate_name_ProDeckAPI(original_lang,originalCardName,translate_lang):
    data=get_card_info_by_name_and_language_ProDeckAPI(original_lang,originalCardName)
    if data:
        if 'data' in data and len(data['data']) > 0:

            id = data['data'][0]['id']
            return get_data_by_lang_and_cardId(translate_lang,id)

def search_by_string_and_lang(lang,name):
    if(lang=='en'):
        params = {
            'fname': name
        }
    else:
        params = {
            'fname': name,
            'language': lang
        }
    return proDeckAPI_request(params)

#
#instâncias
##bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

##channel
channel = discord.channel.TextChannel
#
#init
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
#
#Comandos

@bot.command()
async def card(ctx, lang, cardName):
    async with channel.typing(ctx):
        data = get_card_info_by_name_and_language_ProDeckAPI(lang,cardName)
        
        if data:
            card = data['data'][0]['card_images'][0]['image_url']
            await ctx.send(card)
        else:
            if lang == 'pt':
                await ctx.send('Não foi possível encontrar informações sobre essa carta.')
            elif lang == 'en':
                await ctx.send('Unable to find information about this card.')
            elif lang == 'de':
                await ctx.send('Es konnten keine Informationen zu dieser Karte gefunden werden.')
            elif lang == 'it':
                await ctx.send('Impossibile trovare informazioni su questa carta.')
            elif lang == 'fr':
                await ctx.send("Impossible de trouver des informations sur cette carte.")
    await channel.send('Done!')

@bot.command()
async def info(ctx, lang, cardName):
    async with channel.typing(ctx):
        data = get_card_info_by_name_and_language_ProDeckAPI(lang, cardName)
        
        if data:
            card_data = data['data'][0]
            
            # Extrair informações da carta
            ##informações independentes
            name = card_data['name']
            type = card_data['type']
            desc = card_data['desc']
            image_url = card_data['card_images'][0]['image_url']

            embed = discord.Embed(title=name, description=desc, color=0x7289da)
            embed.set_thumbnail(url=image_url)
            embed.add_field(name="Card-Type", value=type, inline=True)
            ##informações relativas (nem toda carta possui)
            if 'atk' in card_data: #uma carta ter ataque implica em ter defesa
                atk = card_data['atk']
                def_ = card_data['def']
                embed.add_field(name="ATK", value=atk, inline=True)
                embed.add_field(name="DEF", value=def_, inline=True)

            if 'level' in card_data:
                level = card_data['level']
                embed.add_field(name="LvL", value=level, inline=True)
            
            if 'attribute' in card_data:
                attribute = card_data['attribute']
                embed.add_field(name="Attribute", value=attribute, inline=True)
            
            if 'race' in card_data:
                race = card_data['race']
                embed.add_field(name="Type", value=race, inline=True)
            
            if 'archetype' in card_data:
                archetype = card_data['archetype']
                embed.add_field(name="Archetype", value=archetype, inline=True)

            await ctx.send(embed=embed)
        else:
            if lang == 'pt':
                await ctx.send('Não foi possível encontrar informações sobre essa carta.')
            elif lang == 'en':
                await ctx.send('Unable to find information about this card.')
            elif lang == 'de':
                await ctx.send('Es konnten keine Informationen zu dieser Karte gefunden werden.')
            elif lang == 'it':
                await ctx.send('Impossibile trovare informazioni su questa carta.')
            elif lang == 'fr':
                await ctx.send("Impossible de trouver des informations sur cette carte.")
    await channel.send('Done!')

@bot.command()
async def tr(ctx, original_lang, cardName, translate_lang):
    async with channel.typing(ctx):
        data = translate_name_ProDeckAPI(original_lang, cardName, translate_lang)
        
        if data:
            name = data['data'][0]['name']
            await ctx.send(name)
        else:
            if translate_lang == 'pt':
                await ctx.send('Não foi possível encontrar informações sobre essa carta.')
            elif translate_lang == 'en':
                await ctx.send('Unable to find information about this card.')
            elif translate_lang == 'de':
                await ctx.send('Es konnten keine Informationen zu dieser Karte gefunden werden.')
            elif translate_lang == 'it':
                await ctx.send('Impossibile trovare informazioni su questa carta.')
            elif translate_lang == 'fr':
                await ctx.send("Impossible de trouver des informations sur cette carte.")

    await channel.send('Done!')

@bot.command()
async def search(ctx, lang, cardName):
    async with channel.typing(ctx):
        data = search_by_string_and_lang(lang, cardName)
        
        if data:
            for i in range(0,6) :
                card_data = data['data'][i]
                name = card_data['name']
                type = card_data['type']
                desc = card_data['desc']
                image_url = card_data['card_images'][0]['image_url']

                embed = discord.Embed(title=name, description=desc, color=0x7289da)
                embed.set_thumbnail(url=image_url)
                embed.add_field(name="Card-Type", value=type, inline=True)

                if 'atk' in card_data: #uma carta ter ataque implica em ter defesa
                    atk = card_data['atk']
                    def_ = card_data['def']
                    embed.add_field(name="ATK", value=atk, inline=True)
                    embed.add_field(name="DEF", value=def_, inline=True)

                if 'level' in card_data:
                    level = card_data['level']
                    embed.add_field(name="LvL", value=level, inline=True)
                
                if 'attribute' in card_data:
                    attribute = card_data['attribute']
                    embed.add_field(name="Attribute", value=attribute, inline=True)
                
                if 'race' in card_data:
                    race = card_data['race']
                    embed.add_field(name="Type", value=race, inline=True)
                
                if 'archetype' in card_data:
                    archetype = card_data['archetype']
                    embed.add_field(name="Archetype", value=archetype, inline=True)

                await ctx.send(embed=embed)
        else:
            if lang == 'pt':
                await ctx.send('Não foi possível encontrar informações sobre essa carta.')
            elif lang == 'en':
                await ctx.send('Unable to find information about this card.')
            elif lang == 'de':
                await ctx.send('Es konnten keine Informationen zu dieser Karte gefunden werden.')
            elif lang == 'it':
                await ctx.send('Impossibile trovare informazioni su questa carta.')
            elif lang == 'fr':
                await ctx.send("Impossible de trouver des informations sur cette carte.")

    await channel.send('Done!')

@bot.command()
async def prices(ctx,lang,cardName):
    async with channel.typing(ctx):
        data=get_card_info_by_name_and_language_ProDeckAPI(lang,cardName)

        if data:
            embed = discord.Embed(title=cardName, color=0x7289da)
            
            prices = data['data'][0]['card_prices'][0]
            if 'cardmarket_price' in prices:
                cardmarket_price = f"${prices['cardmarket_price']}"
                embed.add_field(name="Cardmarket Price:", value=cardmarket_price, inline=True)

            if 'tcgplayer_price' in prices:
                tcgplayer_price = f"${prices['tcgplayer_price']}"
                embed.add_field(name="tcgplayer Price:", value=tcgplayer_price, inline=True)

            if 'ebay_price' in prices:
                ebay_price = f"${prices['ebay_price']}"
                embed.add_field(name="ebay Price:", value=ebay_price, inline=True)

            if 'amazon_price' in prices:
                amazon_price = f"${prices['amazon_price']}"
                embed.add_field(name="Amazon Price:", value=amazon_price, inline=True)

            if 'coolstuffinc_price' in prices:
                coolstuffinc_price = f"${prices['coolstuffinc_price']}"
                embed.add_field(name="Coolstuffinc Price:", value=coolstuffinc_price, inline=True)

            await ctx.send(embed=embed)

        else:
            if lang == 'pt':
                await ctx.send('Não foi possível encontrar informações sobre essa carta.')
            elif lang == 'en':
                await ctx.send('Unable to find information about this card.')
            elif lang == 'de':
                await ctx.send('Es konnten keine Informationen zu dieser Karte gefunden werden.')
            elif lang == 'it':
                await ctx.send('Impossibile trovare informazioni su questa carta.')
            elif lang == 'fr':
                await ctx.send("Impossible de trouver des informations sur cette carte.")

    await channel.send('Done!')
#
    
@bot.event
async def on_message(message):
    # Check if the message was sent by the bot to avoid loops
    if message.author == bot.user:
        return

    # Check if the message is specific
    if message.content == 'ThunderBot ajuda':
        # Embed message for Portuguese (Brazil)
        embed_pt = discord.Embed(title="Comandos disponíveis", description="Lista de comandos disponíveis para usar com o bot:", color=0x7289da)
        embed_pt.add_field(name="!card (lang) (cardName)", value="Retorna a imagem da carta especificada.", inline=False)
        embed_pt.add_field(name="!info (lang) (cardName)", value="Fornece informações detalhadas sobre a carta especificada.", inline=False)
        embed_pt.add_field(name="!tr (original_lang) (cardName) (translate_lang)", value="Traduz o nome da carta de um idioma para outro.", inline=False)
        embed_pt.add_field(name="!search (lang) (cardName)", value="Pesquisa cartas com base em uma sequência de caracteres.", inline=False)
        embed_pt.add_field(name="!prices (lang) (cardName)", value="Mostra os preços da carta especificada.", inline=False)  # Adicionando o comando prices
        await message.channel.send(embed=embed_pt)

    elif message.content == 'ThunderBot help':
        # Embed message for English
        embed_en = discord.Embed(title="Available Commands", description="List of available commands to use with the bot:", color=0x7289da)
        embed_en.add_field(name="!card (lang) (cardName)", value="Returns the image of the specified card.", inline=False)
        embed_en.add_field(name="!info (lang) (cardName)", value="Provides detailed information about the specified card.", inline=False)
        embed_en.add_field(name="!tr (original_lang) (cardName) (translate_lang)", value="Translates the name of the card from one language to another.", inline=False)
        embed_en.add_field(name="!search (lang) (cardName)", value="Searches cards based on a character sequence.", inline=False)
        embed_en.add_field(name="!prices (lang) (cardName)", value="Shows the prices of the specified card.", inline=False)  # Adding the prices command
        await message.channel.send(embed=embed_en)

    elif message.content == 'ThunderBot hilfe':
        # Embed message for German
        embed_de = discord.Embed(title="Verfügbare Befehle", description="Liste der verfügbaren Befehle, die mit dem Bot verwendet werden können:", color=0x7289da)
        embed_de.add_field(name="!card (lang) (Kartenname)", value="Gibt das Bild der angegebenen Karte zurück.", inline=False)
        embed_de.add_field(name="!info (lang) (Kartenname)", value="Gibt detaillierte Informationen zur angegebenen Karte zurück.", inline=False)
        embed_de.add_field(name="!tr (original_lang) (Kartenname) (translate_lang)", value="Übersetzt den Namen der Karte von einer Sprache in eine andere.", inline=False)
        embed_de.add_field(name="!search (lang) (Kartenname)", value="Sucht nach Karten anhand einer Zeichenfolge.", inline=False)
        embed_de.add_field(name="!prices (lang) (Kartenname)", value="Zeigt die Preise der angegebenen Karte an.", inline=False)  # Adding the prices command
        await message.channel.send(embed=embed_de)

    elif message.content == 'ThunderBot aiuto':
        # Embed message for Italian
        embed_it = discord.Embed(title="Comandi disponibili", description="Elenco dei comandi disponibili da utilizzare con il bot:", color=0x7289da)
        embed_it.add_field(name="!card (lang) (nomeCarta)", value="Restituisce l'immagine della carta specificata.", inline=False)
        embed_it.add_field(name="!info (lang) (nomeCarta)", value="Fornisce informazioni dettagliate sulla carta specificata.", inline=False)
        embed_it.add_field(name="!tr (original_lang) (nomeCarta) (translate_lang)", value="Traduce il nome della carta da una lingua all'altra.", inline=False)
        embed_it.add_field(name="!search (lang) (nomeCarta)", value="Cerca carte basate su una sequenza di caratteri.", inline=False)
        embed_it.add_field(name="!prices (lang) (nomeCarta)", value="Mostra i prezzi della carta specificata.", inline=False)  # Adding the prices command
        await message.channel.send(embed=embed_it)

    elif message.content == 'ThunderBot aide':
        # Embed message for French
        embed_fr = discord.Embed(title="Commandes disponibles", description="Liste des commandes disponibles à utiliser avec le bot:", color=0x7289da)
        embed_fr.add_field(name="!card (lang) (nomCarte)", value="Renvoie l'image de la carte spécifiée.", inline=False)
        embed_fr.add_field(name="!info (lang) (nomCarte)", value="Fournit des informations détaillées sur la carte spécifiée.", inline=False)
        embed_fr.add_field(name="!tr (original_lang) (nomCarte) (translate_lang)", value="Traduit le nom de la carte d'une langue à une autre.", inline=False)
        embed_fr.add_field(name="!search (lang) (nomCarte)", value="Recherche des cartes basées sur une séquence de caractères.", inline=False)
        embed_fr.add_field(name="!prices (lang) (nomCarte)", value="Affiche les prix de la carte spécifiée.", inline=False)  # Adding the prices command
        await message.channel.send(embed=embed_fr)
    # Call the default command processing after the on_message event
    await bot.process_commands(message)


#run 
load_dotenv()
disc_api_key = os.getenv('DISCORD_API_KEY')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
bot.run(disc_api_key, log_handler=handler, log_level=logging.DEBUG)
#
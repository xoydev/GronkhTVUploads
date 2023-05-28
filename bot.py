from util import Util
import discord
from discord.ext import commands, tasks
import secret_data

u = Util()

channelid = secret_data.channelid
streamid: int

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
	global streamid
	print(f'Eingeloggt als {bot.user.name} ({bot.user.id})')
	streamid = int(await u.read_file('streamid'))
	check_stream.start()

msg_before = '@everyone Neuer Stream!'

@tasks.loop(minutes=10)
async def check_stream():
	global streamid
	print("Checking stream "+str(streamid))
	try:
		channel = bot.get_channel(channelid)
		if await u.check_stream(streamid):
			await channel.send(msg_before+'\nhttps://gronkh.tv/streams/'+str(streamid))
			print('Found stream '+str(streamid))
			await u.write_file('streamid', str(streamid+1))
			streamid += 1
		else:
			print('Stream '+str(streamid)+' not found')
	except discord.NotFound:
		print('ERROR: Channel "'+str(channelid)+'" not found!')

bot.run(secret_data.api_key)
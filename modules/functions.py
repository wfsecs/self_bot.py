import discord_webhook as dwh
from scapy.all import *
from PIL import Image
import requests
import datetime
import base64
import json


def iplookup_func(arg):
    r = requests.get(f'http://ipwho.is/{arg}')

    a = json.loads(r.text)
    c = a['connection']
    t = a['timezone']


    ip_info = f'''```ansi
[1;37m+---------------------------------------+    

  [0;34m [Basic] [0m

  [1;37mIP:[0;32m {a["ip"]}
  [1;37mType:[0;32m {a["type"]}
  [1;37mContinent:[0;32m {a["continent"]}
  [1;37mCountry:[0;32m {a["country"]}
  [1;37mRegion:[0;32m {a["region"]}
  [1;37mCity:[0;32m {a["city"]}
  [1;37mPostal Code:[0;32m {a["postal"]}
  [1;37mCapital:[0;32m {a["capital"]}

  [0;34m [Connection] [0m

  [1;37mASN:[0;31m {c["asn"]}
  [1;37mISP:[0;31m {c["isp"]}
  [1;37mDomain:[0;31m {c["domain"]}

  [0;34m [Timezone] [0m

  [1;37mID:[0;35m {t["id"]}
  [1;37mUTC:[0;35m {t["utc"]}
  [1;37mCurrent Time:[0;35m {t["current_time"]}

[1;37m+---------------------------------------+     
```'''
    return ip_info


def repeat_to_length(s, wanted):
    return (s * (wanted//len(s) + 1))[:wanted]


def portscan_ip(arg):
    ss = 'Port scan:'
    PORTS = {21: 'FTP',  # Ports to scan
             22: 'SSH',
             23: 'TELNET',
             25: 'SMTP',
             53: 'DNS',
             79: 'FINGER',
             80: 'HTTP',
             88: 'KERBEROS',
             194: 'IRC',
             443: 'HTTPS',
             3306: 'MYSQL',
             3389: 'RDP',
             8080: 'ALT HTTP',
             7777: 'TERRARIA',
             25565: 'MINECRAFT',
             42806: 'DISCORD'}

    for port in PORTS:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Terminate connection if no response after 3 seconds
        result = s.connect_ex((arg, port))
        if result == 0:
            ss += f'''
[32;1m       [+][37;1m Port {port} is open on [{arg}] [33m[{port}/{PORTS[port]}][37;1m'''
    return ss


def get_discord_data(token, id):
    headers = {'Authorization': token}
    r = requests.get(f'https://discord.com/api/v9/users/{id}', headers=headers).text
    user = json.loads(r)
    user_id = user['id']
    user_name = user['username']
    user_tag = user['discriminator']
    user_banner_color = user['banner_color']

    message_bytes = user_id.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    half_token = base64_bytes.decode('ascii')

    user_info = f'''```ansi
[0;31mUsername:[0;36m {user_name}
[0;31mDiscriminator:[0;36m {user_tag}
[0;35mID:[0;36m {user_id}
[0;33mBanner color:[0;36m {user_banner_color}
[0;34mHalf token: {half_token}
```'''
    return user_info


def get_pfp(token, id):

    headers = {'Authorization': token}
    r = requests.get(f'https://discord.com/api/v9/users/{id}', headers=headers).text
    user = json.loads(r)
    avatar = user['avatar']
    id = user['id']

    filename = f'avatars/{user["username"]}{user["discriminator"]}'

    r = requests.get(f'https://cdn.discordapp.com/avatars/{id}/{avatar}.webp')
    open(f'{filename}.webp', 'wb').write(r.content)

    image = Image.open(f'{filename}.webp')
    image.save(f'{filename}.png', format="png")
    pfp = f'{filename}.png'

    return pfp


def get_time():
    x = datetime.datetime.now()
    timern = x.strftime('%x %X')

    return timern


def log_filename():
    x = datetime.datetime.now()
    lfilename = x.strftime('[%m-%d-%y]#%H-%M-%S')
    lfilename = f'logs/{lfilename}.txt'

    return lfilename


def log_event(webhook, info):
    try:
        embed = dwh.DiscordEmbed(color=0xf53d3d)
        embed.set_author(name='Made by wfsec',
                         icon_url='https://cdn.discordapp.com/attachments/1050426327683055616/1050432369062072352/loglo.png')
        embed.add_embed_field(name="***Command ran / Event***", value=f'```{info}```')
        embed.set_footer(text="self_bot")

        webhook.add_embed(embed)
        dwhr = webhook.execute(remove_embeds=True)
    except:
        print('    [WEBHOOK-LOGGER] Failed to log!')

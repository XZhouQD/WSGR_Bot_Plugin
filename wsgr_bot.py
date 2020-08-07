from nonebot import on_command, CommandSession, permission
from json import loads

"""
WSGR Info Bot
A Nonebot Plugin
use with Resources

Version:
0.1.0
"""

class BotCache:
    """The bot cache"""
    def __init__(self):
        self.cache = {'ship':{}, 'equip':{}}
        self.path = 'plugins/wsgr_bot/cn_archive/'
        
    def get_ship(self, ship_name: str):
        try:
            return self.cache['ship'][ship_name]
        except:
            with open(f'{self.path}ship/{ship_name}.json', 'r') as f:
                j = loads(f.read())
            self.cache['ship'][ship_name] = j['data']
            return self.cache['ship'][ship_name]

bot_cache = BotCache()

@on_command('ship', aliases=('舰娘'), permission=permission.GROUP_MEMBER, only_to_me=False)
async def ship(session: CommandSession):
    ship_name = session.get('name')
    user = session.event.user_id
    group = session.event.group_id
    result = await fetch_ship(ship_name, user)
    await session.send(result)
    
@ship.args_parser
async def ship_args_parser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    
    if session.is_first_run:
        if stripped_arg:
            session.state['name'] = stripped_arg
        return
        
async def fetch_ship(ship_name: str, user: int) -> str:
    result = bot_cache.get_ship(ship_name)
    return f'[CQ:at,qq={user}] {result}'


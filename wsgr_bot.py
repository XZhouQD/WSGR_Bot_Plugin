from nonebot import on_command, CommandSession, permission
from json import loads
from aiocqhttp import MessageSegment
from os import getcwd

"""
WSGR Info Bot
A Nonebot Plugin
use with Resources

Version:
0.4.0-Alpha
"""

class BotCache:
    """The bot cache"""
    def __init__(self):
        self.cache = {'ship':{}, 'equip':{}}
        self.path = 'plugins/wsgr_bot/cn_archive/'
        self.init_json = 'plugins/wsgr_bot/cn_init.json'
        self.init_id_dict()

    def get_ship(self, ship_name: str):
        try:
            return self.cache['ship'][ship_name]
        except:
            with open(f'{self.path}ship/{ship_name}.json', 'r') as f:
                j = loads(f.read())
            #img_seg = MessageSegment.image(f'{getcwd()}/{self.path}images/L_NORMAL_{j["picId"]}.png')
            self.cache['ship'][ship_name] = j['data']
            return self.cache['ship'][ship_name]

    def get_equip(self, equip_name: str):
        try:
            return self.cache['equip'][equip_name]
        except:
            with open(f'{self.path}equipment/{equip_name}.json', 'r') as f:
                j = loads(f.read())
            self.cache['equip'][equip_name] = j['data']
            return self.cache['equip'][equip_name]
    
    def init_id_dict(self):
        with open(self.init_json, 'r') as f:
            j = loads(f.read())
        nameCorrectionDic = {}
        nameCorrectionDic["列克星敦"] = "列克星敦16"
        nameCorrectionDic["拉菲"] = "拉菲(本森级)"
        nameCorrectionDic["欧根亲王"] = "欧根亲王(圣诞节)"
        nameCorrectionDic["华盛顿"] = "华盛顿(儿童节)"
        nameCorrectionDic["内华达"] = "内华达(圣诞节)"
        nameCorrectionDic["提尔比茨"] = "提尔比茨(儿童节)"
        nameCorrectionDic["狮"] = "狮(战巡)"
        nameDic = {}
        modifyDic = {}
        #divide into original and modified to avoid bug
        for ship in j["shipCardWu"]:
            if ship["cid"] < 11000000 and ship["cid"]%10 <= 3:
                nameDic[int(ship["cid"]/100)%100000] = ship["title"].replace("•","·").replace("·","-")
            elif ship["cid"] < 20000000 and ship["cid"]%10 <= 3:
                modifyDic[int(ship["cid"]/100)%100000] = ship["title"].replace("•","·").replace("·","-")
                try:
                    if modifyDic[int(ship["cid"]/100)%100000] == nameDic[int(ship["cid"]/100)%100000-10000]:
                        modifyDic[int(ship["cid"]/100)%100000] = modifyDic[int(ship["cid"]/100)%100000] + "改"
                except:
                    pass
        flipped = {}
        for key, value in nameDic.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                flipped[value].append(key)
                nameDic[key] = nameCorrectionDic[value]
        flipped = {}
        for key, value in modifyDic.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                flipped[value].append(key)
                modifyDic[key] = nameCorrectionDic[value]
        #merge into one dict
        nameDic.update(modifyDic)
        self.id_dict = nameDic
    
    def get_by_id(self, ship_id: int):
        return self.get_ship(self.id_dict[ship_id])


# initialise global cache dict class
bot_cache = BotCache()

# equipments
@on_command('equip', aliases=('装备'), permission=permission.GROUP_MEMBER, only_to_me=False)
async def equip(session: CommandSession):
    equip_name = session.get('name')
    user = session.event.user_id
    group = session.event.group_id
    result = await fetch_equip(equip_name, user)
    await session.send(result)
    
@equip.args_parser
async def equip_args_parser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    
    if session.is_first_run:
        if stripped_arg:
            session.state['name'] = stripped_arg
        return
        
async def fetch_equip(equip_name: str, user: int) -> str:
    result = bot_cache.get_equip(equip_name)
    return f'[CQ:at,qq={user}] {result}'

# ships
@on_command('ship', aliases=('舰娘'), permission=permission.GROUP_MEMBER, only_to_me=False)
async def ship(session: CommandSession):
    ship_name = session.get('name')
    user = session.event.user_id
    group = session.event.group_id
    result = fetch_ship(ship_name, user)
    await session.send(result)
    
@ship.args_parser
async def ship_args_parser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    
    if session.is_first_run:
        if stripped_arg:
            session.state['name'] = stripped_arg
        return
        
def fetch_ship(ship_name: str, user: int) -> str:
    try:
        result = bot_cache.get_by_id(int(ship_name))
    except:
        result = bot_cache.get_ship(ship_name)
    return f'[CQ:at,qq={user}] {result}'


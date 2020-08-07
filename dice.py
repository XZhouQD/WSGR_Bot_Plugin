from nonebot import on_command, CommandSession, permission
import random


@on_command('roll', aliases=('骰子'), permission=permission.GROUP_MEMBER, only_to_me=False)
async def roll(session: CommandSession):
    xdy = session.get('xdy')
    xdy_list = xdy.split('d')
    x = int(xdy_list[0])
    y = int(xdy_list[1])
    user = session.event.user_id
    group = session.event.group_id
    result = await dice(x, y, user)
    print(result, group)
    await session.send(result)

@roll.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['xdy'] = stripped_arg
        return

async def dice(x: int, y: int, user: int):
    if x < 1 or y < 1:
        return f'[CQ:at,qq={user}]{x}d{y}格式错误！'
    result = f'[CQ:at,qq={user}] {x}d{y} = '
    rolls = []
    num_sum = 0
    for i in range(x):
        z = random.choice(range(1, y+1))
        num_sum += z
        rolls.append(str(z))
    result = result + ','.join(rolls) + f', Sum = {num_sum}'
    return result

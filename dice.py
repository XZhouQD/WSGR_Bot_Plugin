from nonebot import on_command, CommandSession, permission
import random


@on_command('roll', aliases=('骰子'), permission=permission.GROUP_MEMBER, only_to_me=False)
async def roll(session: CommandSession):
    xdy_aSb = session.get('xdy+aSb')
    xdy_list = xdy_aSb.split('+')
    xdy = xdy_list[0].split('d')
    x = int(xdy[0])
    y = int(xdy[1])
    user = session.event.user_id
    group = session.event.group_id
    if len(xdy_list) > 1:
        aSb = xdy_list[1].split('S')
        try:
            a = int(aSb[0])
        except:
            a = 0
        try:
            b = int(aSb[1])
        except:
            b = 0
    else:
        a = 0
        b = 0

    result = dice(x, y, user, a, b)
    print(result, group)
    await session.send(result)


@roll.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['xdy+aSb'] = stripped_arg
        return


def dice(x: int, y: int, user: int, a: int, b: int):
    if x < 1 or y < 1:
        return f'[CQ:at,qq={user}]格式错误！使用/roll xdy+aSb'
    if a == 0 and b == 0:
        result = f'[CQ:at,qq={user}] {x}d{y} = '
    elif a != 0 and b == 0:
        result = f'[CQ:at,qq={user}] {x}d{y}+{a} = '
    elif a == 0 and b != 0:
        result = f'[CQ:at,qq={user}] {x}d{y}+S{b} = '
    else:
        result = f'[CQ:at,qq={user}] {x}d{y}+{a}S{b} = '
    rolls = []
    num_sum = 0
    for i in range(x):
        z = random.choice(range(1, y + 1)) + a
        num_sum += z
        rolls.append(str(z))
    if b == 0:
        result = result + ','.join(rolls) + f', Sum = {num_sum}'
    else:
        result = result + ','.join(rolls) + f', Sum = {num_sum} + {b} = {num_sum + b}'
    return result

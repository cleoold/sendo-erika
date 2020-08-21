import random

import aiosqlite

from utils_bot.datetime import TZ, datetime
from utils_bot.typing import AsyncContextManager, Tuple, Union


def today_to_str() -> str:
    return str(
        datetime.now(TZ).strftime('%m%d%Y')
    )


def generate_luck_num(sender_id: int) -> float:
    'a user has a luck number between 0 and 1 every day'
    senderId: int = sender_id
    timeStamp: int = int(today_to_str())
    seed: int = (senderId * 2) | (timeStamp * 333)
    random.seed(seed)
    res: float = random.random()
    random.seed()
    return res


def generate_luck_result(sender_id: int) -> str:
    'converts the luck number of a user to a suitable string'
    def return_luck_by_num(num: float) -> str:
        if 0.0 <= num < 0.1:
            return '极坏'
        elif 0.1 <= num < 0.4:
            return '坏'
        elif 0.4 <= num < 0.7:
            return '一般'
        elif 0.7 <= num < 0.9:
            return '好'
        else:
            return '极好'
    return return_luck_by_num(generate_luck_num(sender_id))


def user_score_to_user(i: int) -> float:
    "a user's score is stored in int, but the displayed value is that divided by 100 (by now)" 
    return i / 100


def format_score(s: float) -> str:
    'format the displayed score (好感度) by hearts'
    if s < 100:
        return str(s)
    else:
        # example: '4.44 ♥' means 104.44
        return f'{float(s % 100):.4} {"♥" * int(s // 100)}'


class SignInSession(AsyncContextManager):

    '''Table attributes:

    table name: sign

    identity (format: userid_groupid)(str), 
    last sign in time (str), 
    score (int),
    luck (not used)(str), 
    score2 (stores the sign in count)(int), 
    score3 (not used)(int)
    '''

    def __init__(self,  db_name: str,
                 user_id: Union[str, int],
                 group_id: Union[str, int]):

        self.conn = aiosqlite.connect(db_name)
        self.user_id: int = int(user_id)
        self.identity: str = f'{user_id}_{group_id}'

    async def searchall(self) -> list:
        cur = await self.conn.execute('select * from sign')
        res: list = await cur.fetchall() # type: ignore
        await cur.close()
        return res

    async def init_table(self):
        cur = await self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS sign
            (identity VARCHAR(30) PRIMARY KEY,
             lastsign VARCHAR(10),
             score INT,
             luck VARCHAR(10),
             score2 INT,
             score3 INT)'''
        )
        await cur.close()
        await self.conn.commit()

    async def init_user(self):
        'create one entry for a user who wants to sign in'
        cur = await self.conn.execute('''INSERT OR IGNORE INTO sign 
                        (identity, lastsign, score, luck, score2, score3) 
                        values (?, ?, ?, ?, ?, ?)''',
                        (self.identity, '0', 0, '', 0, 0))
        await cur.close()
        await self.conn.commit()

    async def user_sign_in(self) -> Tuple[bool, float, float]:
        '''after user initializing, signs in. one user signs in once a day. 
        returns the successfulness of the signing in. returns the score after signing in. returns the score added
        '''

        today: str = today_to_str()
        async with self.conn.execute('SELECT * FROM sign WHERE identity=?', (self.identity,)) as cur:
            currentEntry = await cur.fetchone()
            scoreBefore: int = currentEntry[2]
            # checks sign in time, refuses if already signed in
            if currentEntry[1] == today:
                return False, user_score_to_user(scoreBefore), 0

            scoreAdded: int = int(generate_luck_num(self.user_id) * 100)
            scoreAfter: int = scoreBefore + scoreAdded
            await cur.execute('UPDATE sign SET score=?, lastsign=?, score2=score2+1 WHERE identity=?',
                             (scoreAfter, today, self.identity))
            await self.conn.commit()
            return True, user_score_to_user(scoreAfter), user_score_to_user(scoreAdded)

    async def user_check(self) -> Tuple[float, int, str]:
        'returns the score, sign-in count, last sign-in time for the user'
        async with self.conn.execute('SELECT * FROM sign WHERE identity=?', (self.identity,)) as cur:
            currentEntry = await cur.fetchone()
            return user_score_to_user(currentEntry[2]), currentEntry[4], currentEntry[1]

    async def __aenter__(self) -> 'SignInSession':
        await self.conn
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.conn.close()

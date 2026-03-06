#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ════════════════════════════════════════════════════════════════════════════════
# 𝐄𝐗𝐔 𝐏𝐇𝐎𝐍𝐄 𝐒𝐓𝐘𝐋𝐄 𝐁𝐎𝐓 ───── 𝐅𝐔𝐋𝐋 𝐒𝐓𝐀𝐂𝐊 𝐕𝟏
# ════════════════════════════════════════════════════════════════════════════════

import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union, Tuple
from collections import deque
import math
import time
import re
import json
from pathlib import Path

# Telegram Core
from telethon import TelegramClient, events, Button, functions, types
from telethon.tl.types import (
    MessageMediaDocument, MessageMediaPhoto, InputPeerChannel,
    InputPeerUser, PeerChannel, User, Channel, Chat, Message,
    UpdateNewChannelMessage, UpdateNewMessage
)
from telethon.errors import (
    FloodWaitError, RPCError, AuthKeyUnregisteredError,
    PhoneNumberUnoccupiedError, SessionPasswordNeededError,
    UserAlreadyParticipantError, ChannelPrivateError
)
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from telethon.tl.functions.phone import JoinGroupCallRequest, LeaveGroupCallRequest
from telethon.tl.types import InputPhoneContact, InputPeerUser
from telethon import utils

# Optional Voice Libraries
try:
    from pytgcalls import PyTgCalls
    from pytgcalls.types import Update
    from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
    from pytgcalls.types.stream import StreamAudioEnded
    from pytgcalls.exceptions import NoActiveGroupCall, GroupCallNotFound
    PYTGCALLS_AVAILABLE = True
except ImportError:
    PYTGCALLS_AVAILABLE = False

# ════════════════════════════════════════════════════════════════════════════════
# [ 𝐂𝐎𝐍𝐅𝐈𝐆𝐔𝐑𝐀𝐓𝐈𝐎𝐍 ] ───── 𝐄𝐗𝐔 𝐏𝐇𝐎𝐍𝐄 𝐒𝐓𝐘𝐋𝐄
# ════════════════════════════════════════════════════════════════════════════════

# Telegram API Credentials
API_ID = 36811424  # Replace with your API ID
API_HASH = "f28edfab583936ea62d6b458f754a4bd"  # Replace with your API Hash
BOT_TOKEN = "8713105830:AAG7VD0axvjPjFUv2AwglAxGKQCwDBQ1hEU"  # Replace with your Bot Token
PHONE_NUMBER = "+01722253348"  # Replace with your phone number
OWNER_ID = 8469461108  # Replace with your Telegram user ID

# EXU Channels Configuration
CHANNELS = [
    "@exucoder1",
    "@funcodex",
    "@exucodx1"
]

LIVE_CHANNEL = "@exulive"  # Channel for live streams
STORAGE_CHANNEL = "@exufile"  # Channel for music storage

# Subscriber Milestones
MILESTONES = [
    100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000
]

# Music Settings
MAX_QUEUE_SIZE = 100
DEFAULT_VOLUME = 100
AUTO_LEAVE_EMPTY = 300  # seconds

# Admin Control
ADMIN_ONLY_MODE = True
ALLOW_DOWNLOAD = True
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Session file
SESSION_FILE = "exu_phone_session.session"

# ════════════════════════════════════════════════════════════════════════════════
# [ 𝐄𝐗𝐔 𝐏𝐇𝐎𝐍𝐄 𝐒𝐓𝐘𝐋𝐄 ] ───── 𝐓𝐄𝐑𝐌𝐈𝐍𝐀𝐋 𝐅𝐎𝐑𝐌𝐀𝐓𝐓𝐈𝐍𝐆
# ════════════════════════════════════════════════════════════════════════════════

class EXUPhone:
    """𝐄𝐗𝐔 𝐏𝐇𝐎𝐍𝐄 𝐒𝐓𝐘𝐋𝐄 𝐅𝐎𝐑𝐌𝐀𝐓𝐓𝐄𝐑"""
    
    @staticmethod
    def bold(text: str) -> str:
        """Convert text to 𝐄𝐗𝐔 𝐏𝐇𝐎𝐍𝐄 bold unicode"""
        bold_map = {
            'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆',
            'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍',
            'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔',
            'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
            'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠',
            'h': '𝐡', 'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧',
            'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭', 'u': '𝐮',
            'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳',
            '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒', '5': '𝟓', '6': '𝟔',
            '7': '𝟕', '8': '𝟖', '9': '𝟗', '.': '·', ':': '∶', '-': '−', '_': '̲',
            '[': '【', ']': '】', '(': '❨', ')': '❩', '{': '❴', '}': '❵',
            '|': '┃', '/': '╱', '\\': '╲', '=': '═', '+': '➕', '*': '✶'
        }
        result = ''
        for char in str(text):
            result += bold_map.get(char, char)
        return result
    
    @staticmethod
    def header(text: str) -> str:
        """Create EXU phone style header"""
        border = "══════════════════════════════════════════════════"
        return f"\n{EXUPhone.bold(border)}\n{EXUPhone.bold(text.center(50))}\n{EXUPhone.bold(border)}"
    
    @staticmethod
    def log(event: str, status: str = "✓", color: str = "") -> None:
        """Terminal log with EXU phone style"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{EXUPhone.bold(f'[{timestamp}]')} {EXUPhone.bold(status)} {EXUPhone.bold(event)}")

# Initialize style
EXU = EXUPhone()

# ════════════════════════════════════════════════════════════════════════════════
# [ 𝐃𝐀𝐓𝐀 𝐒𝐓𝐑𝐔𝐂𝐓𝐔𝐑𝐄𝐒 ] ───── 𝐐𝐔𝐄𝐔𝐄 & 𝐒𝐓𝐎𝐑𝐀𝐆𝐄
# ════════════════════════════════════════════════════════════════════════════════

class Track:
    """Music track information"""
    def __init__(self, title: str, duration: int, url: str, file_id: str, requested_by: int):
        self.title = title
        self.duration = duration
        self.url = url
        self.file_id = file_id
        self.requested_by = requested_by
        self.requested_time = time.time()

class MusicQueue:
    """Music queue management"""
    def __init__(self):
        self.queue = deque(maxlen=MAX_QUEUE_SIZE)
        self.current = None
        self.loop = False
        self.shuffle = False
        self.volume = DEFAULT_VOLUME
        self.paused = False
        
    def add(self, track: Track) -> int:
        self.queue.append(track)
        return len(self.queue)
    
    def next(self) -> Optional[Track]:
        if self.loop and self.current:
            return self.current
        if self.queue:
            self.current = self.queue.popleft()
            return self.current
        self.current = None
        return None
    
    def clear(self):
        self.queue.clear()
        self.current = None
    
    def remove(self, index: int) -> bool:
        try:
            self.queue = deque(list(self.queue)[:index] + list(self.queue)[index+1:])
            return True
        except:
            return False

# ════════════════════════════════════════════════════════════════════════════════
# [ 𝐂𝐋𝐈𝐄𝐍𝐓 𝐈𝐍𝐈𝐓𝐈𝐀𝐋𝐈𝐙𝐀𝐓𝐈𝐎𝐍 ] ───── 𝐓𝐄𝐋𝐄𝐓𝐇𝐎𝐍 + 𝐏𝐘𝐓𝐆𝐂𝐀𝐋𝐋𝐒
# ════════════════════════════════════════════════════════════════════════════════

class EXUBot:
    """𝐄𝐗𝐔 𝐏𝐇𝐎𝐍𝐄 𝐒𝐓𝐘𝐋𝐄 𝐌𝐀𝐈𝐍 𝐁𝐎𝐓"""
    
    def __init__(self):
        # Initialize clients
        self.client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
        self.bot = TelegramClient('exu_bot', API_ID, API_HASH)
        self.pytgcalls = None
        if PYTGCALLS_AVAILABLE:
            self.pytgcalls = PyTgCalls(self.client)
        
        # Data storage
        self.music_queue = MusicQueue()
        self.channel_stats = {}
        self.subscriber_count = {}
        self.active_call = None
        self.admin_only = ADMIN_ONLY_MODE
        self.start_time = time.time()
        
        # Track joined channels
        self.joined_channels = set()
        
    async def start(self):
        """Start the EXU bot"""
        print(EXU.header("𝐄𝐗𝐔 𝐏𝐇𝐎𝐍𝐄 𝐒𝐓𝐘𝐋𝐄 𝐁𝐎𝐓"))
        
        # Start user client
        EXU.log("𝐈𝐧𝐢𝐭𝐢𝐚𝐥𝐢𝐳𝐢𝐧𝐠 𝐮𝐬𝐞𝐫 𝐜𝐥𝐢𝐞𝐧𝐭...", "⚡")
        await self.client.start(phone=PHONE_NUMBER)
        me = await self.client.get_me()
        EXU.log(f"𝐋𝐨𝐠𝐠𝐞𝐝 𝐢𝐧 𝐚𝐬: {me.first_name} (@{me.username})", "✅")
        
        # Start bot client
        EXU.log("𝐈𝐧𝐢𝐭𝐢𝐚𝐥𝐢𝐳𝐢𝐧𝐠 𝐛𝐨𝐭 𝐜𝐥𝐢𝐞𝐧𝐭...", "⚡")
        await self.bot.start(bot_token=BOT_TOKEN)
        bot_me = await self.bot.get_me()
        EXU.log(f"𝐁𝐨𝐭 𝐫𝐞𝐚𝐝𝐲: @{bot_me.username}", "✅")
        
        # Start pytgcalls if available
        if self.pytgcalls:
            try:
                await self.pytgcalls.start()
                EXU.log("𝐕𝐨𝐢𝐜𝐞 𝐜𝐥𝐢𝐞𝐧𝐭 𝐫𝐞𝐚𝐝𝐲", "🎵")
            except Exception as e:
                EXU.log(f"𝐕𝐨𝐢𝐜𝐞 𝐜𝐥𝐢𝐞𝐧𝐭 𝐞𝐫𝐫𝐨𝐫: {str(e)}", "⚠️")
        
        # Join all channels
        await self.join_channels()
        
        # Setup event handlers
        self.setup_handlers()
        
        # Notify owner
        await self.notify_owner_start()
        
        EXU.log("𝐄𝐗𝐔 𝐁𝐎𝐓 𝐈𝐒 𝐑𝐔𝐍𝐍𝐈𝐍𝐆", "🚀")
        print(EXU.bold("══════════════════════════════════════════════════"))
        
        await asyncio.Event().wait()
    
    async def join_channels(self):
        """Join all configured channels"""
        EXU.log("𝐉𝐨𝐢𝐧𝐢𝐧𝐠 𝐄𝐗𝐔 𝐜𝐡𝐚𝐧𝐧𝐞𝐥𝐬...", "📡")
        
        all_channels = CHANNELS + [LIVE_CHANNEL, STORAGE_CHANNEL]
        
        for channel in all_channels:
            try:
                entity = await self.client.get_entity(channel)
                if hasattr(entity, 'participants_count'):
                    await self.client(JoinChannelRequest(channel))
                    self.joined_channels.add(str(entity.id))
                    EXU.log(f"𝐉𝐨𝐢𝐧𝐞𝐝: {channel} ({entity.participants_count} 𝐦𝐞𝐦𝐛𝐞𝐫𝐬)", "✅")
                else:
                    self.joined_channels.add(str(entity.id))
                    EXU.log(f"𝐀𝐜𝐜𝐞𝐬𝐬𝐢𝐛𝐥𝐞: {channel}", "📁")
            except UserAlreadyParticipantError:
                EXU.log(f"𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐢𝐧: {channel}", "✓")
            except Exception as e:
                EXU.log(f"𝐅𝐚𝐢𝐥𝐞𝐝: {channel} - {str(e)}", "❌")
    
    async def notify_owner_start(self):
        """Notify owner that bot is started"""
        try:
            uptime = time.time() - self.start_time
            text = f"""
{EXU.bold('𝐄𝐗𝐔 𝐏𝐇𝐎𝐍𝐄 𝐁𝐎𝐓 𝐎𝐍𝐋𝐈𝐍𝐄')}
═══════════════════════════════
{EXU.bold('𝐒𝐭𝐚𝐭𝐮𝐬:')} ✅ 𝐀𝐜𝐭𝐢𝐯𝐞
{EXU.bold('𝐔𝐩𝐭𝐢𝐦𝐞:')} {int(uptime)}𝐬
{EXU.bold('𝐂𝐡𝐚𝐧𝐧𝐞𝐥𝐬:')} {len(self.joined_channels)} 𝐣𝐨𝐢𝐧𝐞𝐝
{EXU.bold('𝐌𝐨𝐝𝐞:')} {'𝐀𝐝𝐦𝐢𝐧 𝐎𝐧𝐥𝐲' if self.admin_only else '𝐏𝐮𝐛𝐥𝐢𝐜'}
═══════════════════════════════
"""
            await self.bot.send_message(OWNER_ID, text)
        except:
            pass
    
    def setup_handlers(self):
        """Setup all event handlers"""
        
        # ─── 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐇𝐀𝐍𝐃𝐋𝐄𝐑 ───
        @self.client.on(events.ChatAction)
        async def welcome_handler(event):
            if event.user_added or event.user_joined:
                user = await event.get_user()
                chat = await event.get_chat()
                
                if chat.username in CHANNELS:
                    # Get member count
                    try:
                        full_chat = await self.client.get_entity(chat)
                        count = full_chat.participants_count
                        
                        # Track subscriber
                        EXU.log(f"𝐍𝐞𝐰 𝐦𝐞𝐦𝐛𝐞𝐫: {user.first_name} @{user.username or 'no username'} [{user.id}]", "👤")
                        EXU.log(f"𝐓𝐨𝐭𝐚𝐥: {count} 𝐢𝐧 {chat.username}", "📊")
                        
                        # Send welcome message
                        welcome_text = f"""
{EXU.bold('𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐄𝐗𝐔')}
═══════════════════════════════
{EXU.bold('𝐍𝐚𝐦𝐞:')} {user.first_name}
{EXU.bold('𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞:')} @{user.username or 'None'}
{EXU.bold('𝐈𝐃:')} {user.id}
{EXU.bold('𝐌𝐞𝐦𝐛𝐞𝐫:')} #{count}
═══════════════════════════════
{EXU.bold('𝐄𝐗𝐔 𝐂𝐎𝐌𝐌𝐔𝐍𝐈𝐓𝐘')}
"""
                        await event.reply(welcome_text)
                        
                        # Check milestones
                        if count in MILESTONES:
                            milestone_text = f"""
{EXU.bold('🎉 𝐌𝐈𝐋𝐄𝐒𝐓𝐎𝐍𝐄 𝐑𝐄𝐀𝐂𝐇𝐄𝐃 🎉')}
═══════════════════════════════
{EXU.bold('𝐂𝐡𝐚𝐧𝐧𝐞𝐥:')} {chat.username}
{EXU.bold('𝐌𝐞𝐦𝐛𝐞𝐫𝐬:')} {count}
═══════════════════════════════
"""
                            await self.bot.send_message(OWNER_ID, milestone_text)
                            EXU.log(f"𝐌𝐢𝐥𝐞𝐬𝐭𝐨𝐧𝐞 𝐫𝐞𝐚𝐜𝐡𝐞𝐝: {count}", "🎉")
                            
                    except Exception as e:
                        EXU.log(f"𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐞𝐫𝐫𝐨𝐫: {str(e)}", "⚠️")
        
        # ─── 𝐋𝐈𝐕𝐄 𝐒𝐓𝐑𝐄𝐀𝐌 𝐃𝐄𝐓𝐄𝐂𝐓𝐎𝐑 ───
        @self.client.on(events.Raw)
        async def live_stream_detector(event):
            try:
                if hasattr(event, 'call') and hasattr(event, 'peer'):
                    chat_id = utils.get_peer_id(event.peer)
                    chat = await self.client.get_entity(chat_id)
                    
                    if chat.username == LIVE_CHANNEL.replace('@', ''):
                        EXU.log(f"𝐋𝐢𝐯𝐞 𝐬𝐭𝐫𝐞𝐚𝐦 𝐝𝐞𝐭𝐞𝐜𝐭𝐞𝐝 𝐢𝐧 {LIVE_CHANNEL}", "🔴")
                        
                        # Announce in channel
                        await self.client.send_message(
                            LIVE_CHANNEL,
                            f"{EXU.bold('🔴 𝐋𝐈𝐕𝐄 𝐍𝐎𝐖')}\n{EXU.bold('𝐄𝐗𝐔 𝐬𝐭𝐫𝐞𝐚𝐦 𝐢𝐬 𝐚𝐜𝐭𝐢𝐯𝐞')}"
                        )
                        
                        # Auto-join voice chat
                        if self.pytgcalls:
                            try:
                                await self.pytgcalls.join_group_call(chat_id)
                                EXU.log(f"𝐀𝐮𝐭𝐨-𝐣𝐨𝐢𝐧𝐞𝐝 𝐥𝐢𝐯𝐞 𝐬𝐭𝐫𝐞𝐚𝐦", "🎤")
                            except:
                                pass
            except:
                pass
        
        # ─── 𝐌𝐔𝐒𝐈𝐂 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 ───
        @self.bot.on(events.NewMessage(pattern=r'^/play(?: (.+))?$'))
        async def play_command(event):
            if self.admin_only and event.sender_id != OWNER_ID:
                return
            
            if not event.pattern_match.group(1):
                await event.reply(f"{EXU.bold('𝐔𝐬𝐚𝐠𝐞:')} /play <𝐬𝐨𝐧𝐠 𝐧𝐚𝐦𝐞 𝐨𝐫 𝐔𝐑𝐋>")
                return
            
            query = event.pattern_match.group(1)
            await event.reply(f"{EXU.bold('🔍 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠:')} {query}")
            EXU.log(f"𝐏𝐥𝐚𝐲 𝐫𝐞𝐪𝐮𝐞𝐬𝐭: {query} 𝐟𝐫𝐨𝐦 {event.sender_id}", "🎵")
        
        @self.bot.on(events.NewMessage(pattern=r'^/stop$'))
        async def stop_command(event):
            if self.admin_only and event.sender_id != OWNER_ID:
                return
            await event.reply(f"{EXU.bold('⏹️ 𝐌𝐮𝐬𝐢𝐜 𝐬𝐭𝐨𝐩𝐩𝐞𝐝')}")
            EXU.log(f"𝐒𝐭𝐨𝐩 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐟𝐫𝐨𝐦 {event.sender_id}", "⏹️")
        
        @self.bot.on(events.NewMessage(pattern=r'^/skip$'))
        async def skip_command(event):
            if self.admin_only and event.sender_id != OWNER_ID:
                return
            await event.reply(f"{EXU.bold('⏭️ 𝐒𝐤𝐢𝐩𝐩𝐢𝐧𝐠 𝐭𝐨 𝐧𝐞𝐱𝐭')}")
            EXU.log(f"𝐒𝐤𝐢𝐩 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐟𝐫𝐨𝐦 {event.sender_id}", "⏭️")
        
        @self.bot.on(events.NewMessage(pattern=r'^/queue$'))
        async def queue_command(event):
            if self.admin_only and event.sender_id != OWNER_ID:
                return
            await event.reply(f"{EXU.bold('📜 𝐐𝐮𝐞𝐮𝐞 𝐢𝐬 𝐞𝐦𝐩𝐭𝐲')}")
        
        # ─── 𝐈𝐍𝐋𝐈𝐍𝐄 𝐂𝐎𝐍𝐓𝐑𝐎𝐋 𝐏𝐀𝐍𝐄𝐋 ───
        @self.bot.on(events.NewMessage(pattern=r'^/panel$'))
        async def control_panel(event):
            if event.sender_id != OWNER_ID:
                return
            
            buttons = [
                [Button.inline("🎵 𝐌𝐮𝐬𝐢𝐜 𝐂𝐨𝐧𝐭𝐫𝐨𝐥", b"music_panel")],
                [Button.inline("📊 𝐒𝐭𝐚𝐭𝐬", b"stats"),
                 Button.inline("⚙️ 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬", b"settings")],
                [Button.inline("📢 𝐂𝐡𝐚𝐧𝐧𝐞𝐥𝐬", b"channels"),
                 Button.inline("👥 𝐒𝐮𝐛𝐬", b"subscribers")],
                [Button.inline("🔄 𝐓𝐨𝐠𝐠𝐥𝐞 𝐌𝐨𝐝𝐞", b"toggle_mode"),
                 Button.inline("🔴 𝐋𝐢𝐯𝐞", b"live")]
            ]
            
            text = f"""
{EXU.bold('𝐄𝐗𝐔 𝐂𝐎𝐍𝐓𝐑𝐎𝐋 𝐏𝐀𝐍𝐄𝐋')}
═══════════════════════════════
{EXU.bold('𝐒𝐭𝐚𝐭𝐮𝐬:')} ✅ 𝐎𝐧𝐥𝐢𝐧𝐞
{EXU.bold('𝐌𝐨𝐝𝐞:')} {'𝐀𝐝𝐦𝐢𝐧' if self.admin_only else '𝐏𝐮𝐛𝐥𝐢𝐜'}
{EXU.bold('𝐂𝐡𝐚𝐧𝐧𝐞𝐥𝐬:')} {len(self.joined_channels)} 𝐣𝐨𝐢𝐧𝐞𝐝
═══════════════════════════════
"""
            await event.reply(text, buttons=buttons)
        
        # ─── 𝐈𝐍𝐋𝐈𝐍𝐄 𝐁𝐔𝐓𝐓𝐎𝐍 𝐇𝐀𝐍𝐃𝐋𝐄𝐑 ───
        @self.bot.on(events.CallbackQuery)
        async def callback_handler(event):
            if event.sender_id != OWNER_ID:
                await event.answer("𝐎𝐰𝐧𝐞𝐫 𝐨𝐧𝐥𝐲", alert=True)
                return
            
            data = event.data.decode()
            
            if data == "music_panel":
                buttons = [
                    [Button.inline("▶️ 𝐏𝐥𝐚𝐲", b"play"),
                     Button.inline("⏸️ 𝐏𝐚𝐮𝐬𝐞", b"pause"),
                     Button.inline("⏹️ 𝐒𝐭𝐨𝐩", b"stop")],
                    [Button.inline("⏭️ 𝐒𝐤𝐢𝐩", b"skip"),
                     Button.inline("🔁 𝐋𝐨𝐨𝐩", b"loop"),
                     Button.inline("🔀 𝐒𝐡𝐮𝐟𝐟𝐥𝐞", b"shuffle")],
                    [Button.inline("🔊 𝐕𝐨𝐥+", b"vol_up"),
                     Button.inline("🔉 𝐕𝐨𝐥-", b"vol_down"),
                     Button.inline("📜 𝐐𝐮𝐞𝐮𝐞", b"show_queue")],
                    [Button.inline("◀️ 𝐁𝐚𝐜𝐤", b"back_panel")]
                ]
                await event.edit(buttons=buttons)
                
            elif data == "stats":
                uptime = time.time() - self.start_time
                hours = int(uptime // 3600)
                minutes = int((uptime % 3600) // 60)
                
                text = f"""
{EXU.bold('𝐄𝐗𝐔 𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐂𝐒')}
═══════════════════════════════
{EXU.bold('𝐔𝐩𝐭𝐢𝐦𝐞:')} {hours}h {minutes}m
{EXU.bold('𝐂𝐡𝐚𝐧𝐧𝐞𝐥𝐬:')} {len(self.joined_channels)}
{EXU.bold('𝐐𝐮𝐞𝐮𝐞:')} {len(self.music_queue.queue)} 𝐬𝐨𝐧𝐠𝐬
{EXU.bold('𝐌𝐨𝐝𝐞:')} {'𝐀𝐝𝐦𝐢𝐧' if self.admin_only else '𝐏𝐮𝐛𝐥𝐢𝐜'}
═══════════════════════════════
"""
                await event.answer("📊", alert=False)
                await event.edit(text)
                
            elif data == "toggle_mode":
                self.admin_only = not self.admin_only
                mode = "𝐀𝐝𝐦𝐢𝐧 𝐎𝐧𝐥𝐲" if self.admin_only else "𝐏𝐮𝐛𝐥𝐢𝐜"
                await event.answer(f"𝐌𝐨𝐝𝐞: {mode}")
                EXU.log(f"𝐌𝐨𝐝𝐞 𝐭𝐨𝐠𝐠𝐥𝐞𝐝 𝐭𝐨: {mode}", "⚙️")
                
            elif data == "back_panel":
                buttons = [
                    [Button.inline("🎵 𝐌𝐮𝐬𝐢𝐜 𝐂𝐨𝐧𝐭𝐫𝐨𝐥", b"music_panel")],
                    [Button.inline("📊 𝐒𝐭𝐚𝐭𝐬", b"stats"),
                     Button.inline("⚙️ 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬", b"settings")],
                    [Button.inline("📢 𝐂𝐡𝐚𝐧𝐧𝐞𝐥𝐬", b"channels"),
                     Button.inline("👥 𝐒𝐮𝐛𝐬", b"subscribers")],
                    [Button.inline("🔄 𝐓𝐨𝐠𝐠𝐥𝐞 𝐌𝐨𝐝𝐞", b"toggle_mode"),
                     Button.inline("🔴 𝐋𝐢𝐯𝐞", b"live")]
                ]
                await event.edit(buttons=buttons)
            
            elif data in ["play", "pause", "stop", "skip", "loop", "shuffle", "vol_up", "vol_down"]:
                action_map = {
                    "play": "▶️ 𝐏𝐥𝐚𝐲𝐢𝐧𝐠",
                    "pause": "⏸️ 𝐏𝐚𝐮𝐬𝐞𝐝",
                    "stop": "⏹️ 𝐒𝐭𝐨𝐩𝐩𝐞𝐝",
                    "skip": "⏭️ 𝐒𝐤𝐢𝐩𝐩𝐞𝐝",
                    "loop": "🔁 𝐋𝐨𝐨𝐩",
                    "shuffle": "🔀 𝐒𝐡𝐮𝐟𝐟𝐥𝐞",
                    "vol_up": "🔊 𝐕𝐨𝐥𝐮𝐦𝐞 +",
                    "vol_down": "🔉 𝐕𝐨𝐥𝐮𝐦𝐞 -"
                }
                await event.answer(action_map[data])
                EXU.log(f"{action_map[data]} 𝐛𝐲 𝐨𝐰𝐧𝐞𝐫", "🎮")
        
        # ─── 𝐀𝐃𝐌𝐈𝐍 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 ───
        @self.bot.on(events.NewMessage(pattern=r'^/addchannel (@\w+)$'))
        async def add_channel(event):
            if event.sender_id != OWNER_ID:
                return
            channel = event.pattern_match.group(1)
            try:
                await self.client(JoinChannelRequest(channel))
                CHANNELS.append(channel)
                await event.reply(f"{EXU.bold('✅ 𝐀𝐝𝐝𝐞𝐝:')} {channel}")
                EXU.log(f"𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐚𝐝𝐝𝐞𝐝: {channel}", "➕")
            except Exception as e:
                await event.reply(f"{EXU.bold('❌ 𝐄𝐫𝐫𝐨𝐫:')} {str(e)}")
        
        @self.bot.on(events.NewMessage(pattern=r'^/delchannel (@\w+)$'))
        async def remove_channel(event):
            if event.sender_id != OWNER_ID:
                return
            channel = event.pattern_match.group(1)
            if channel in CHANNELS:
                CHANNELS.remove(channel)
                await event.reply(f"{EXU.bold('✅ 𝐑𝐞𝐦𝐨𝐯𝐞𝐝:')} {channel}")
                EXU.log(f"𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐫𝐞𝐦𝐨𝐯𝐞𝐝: {channel}", "➖")
            else:
                await event.reply(f"{EXU.bold('❌ 𝐍𝐨𝐭 𝐟𝐨𝐮𝐧𝐝')}")
        
        # ─── 𝐒𝐓𝐀𝐑𝐓 𝐂𝐎𝐌𝐌𝐀𝐍𝐃 ───
        @self.bot.on(events.NewMessage(pattern=r'^/start$'))
        async def start_command(event):
            text = f"""
{EXU.bold('𝐄𝐗𝐔 𝐏𝐇𝐎𝐍𝐄 𝐒𝐓𝐘𝐋𝐄 𝐁𝐎𝐓')}
═══════════════════════════════
{EXU.bold('𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:')}
/play <𝐧𝐚𝐦𝐞> - 𝐏𝐥𝐚𝐲 𝐦𝐮𝐬𝐢𝐜
/stop - 𝐒𝐭𝐨𝐩 𝐦𝐮𝐬𝐢𝐜
/skip - 𝐒𝐤𝐢𝐩 𝐭𝐫𝐚𝐜𝐤
/queue - 𝐒𝐡𝐨𝐰 𝐪𝐮𝐞𝐮𝐞
/panel - 𝐂𝐨𝐧𝐭𝐫𝐨𝐥 𝐩𝐚𝐧𝐞𝐥 (𝐨𝐰𝐧𝐞𝐫)
═══════════════════════════════
"""
            await event.reply(text)

# ════════════════════════════════════════════════════════════════════════════════
# [ 𝐌𝐀𝐈𝐍 𝐄𝐍𝐓𝐑𝐘 𝐏𝐎𝐈𝐍𝐓 ]
# ════════════════════════════════════════════════════════════════════════════════

async def main():
    """Main entry point"""
    bot = EXUBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        print(f"\n{EXU.bold('𝐄𝐗𝐔 𝐁𝐎𝐓 𝐒𝐇𝐔𝐓𝐓𝐈𝐍𝐆 𝐃𝐎𝐖𝐍')}")
    except Exception as e:
        print(f"{EXU.bold('𝐅𝐀𝐓𝐀𝐋 𝐄𝐑𝐑𝐎𝐑:')} {str(e)}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{EXU.bold('𝐁𝐎𝐓 𝐒𝐓𝐎𝐏𝐏𝐄𝐃')}")

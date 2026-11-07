#!/usr/bin/env python3
"""
CHECKERAI Telegram Bot (@CHECKERPOSTLARMATBOT)
Token: 9214353265:AAFbjASBSiCMD976kaQsiG-EawfM64uriKY
Admin: Sardarbek (@sardardww, 5649102659)
Target Channel: @qaraqalpaqshajanaliqlar (-1003987848482)

Features:
- Instant proofreading against 2016 Karakalpak Latin Orthography.
- Fixes rogue capital 'I', removes Uzbekisms, Kazakhisms, Russian calques.
- 1-Click publish to @qaraqalpaqshajanaliqlar.
"""

import html
import json
import logging
import os
import sys
import time
import urllib.request
import urllib.parse

from karakalpak_ai_master import (
    sanitize_and_proofread_post,
    evaluate_news_relevance,
    repair_rogue_capital_i,
    CHANNEL_FOOTER
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CHECKERAI_BOT")

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "9214353265:AAFbjASBSiCMD976kaQsiG-EawfM64uriKY").strip()
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "5649102659").strip()
TARGET_CHANNEL = os.environ.get("TARGET_CHANNEL", "-1003987848482").strip()

# In-memory storage for draft previews
draft_storage = {}

def call_tg(method: str, payload: dict) -> dict:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "User-Agent": "CHECKERAI"})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        logger.error(f"Telegram API {method} error: {exc}")
        return {"ok": False, "error": str(exc)}

def handle_update(update: dict):
    # 1. Handle Inline Keyboard button clicks
    cb = update.get("callback_query")
    if cb:
        cb_id = cb.get("id")
        user_id = str(cb.get("from", {}).get("id"))
        cb_data = cb.get("data", "")
        msg = cb.get("message", {})
        chat_id = msg.get("chat", {}).get("id")
        message_id = msg.get("message_id")

        if user_id != ADMIN_CHAT_ID:
            call_tg("answerCallbackQuery", {
                "callback_query_id": cb_id,
                "text": "Ruxsat berilmegen!",
                "show_alert": True
            })
            return

        if cb_data.startswith("pub:"):
            draft_key = cb_data.split(":", 1)[1]
            draft = draft_storage.get(draft_key)
            if not draft:
                call_tg("answerCallbackQuery", {
                    "callback_query_id": cb_id,
                    "text": "Post tabılmadı yamasa múddeti ótti.",
                    "show_alert": True
                })
                return

            # Publish to channel
            pub_res = call_tg("sendMessage", {
                "chat_id": TARGET_CHANNEL,
                "text": draft["cleaned_html"],
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            })

            if pub_res.get("ok"):
                pub_id = pub_res["result"]["message_id"]
                pub_url = f"https://t.me/qaraqalpaqshajanaliqlar/{pub_id}"
                call_tg("editMessageReplyMarkup", {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "reply_markup": {
                        "inline_keyboard": [
                            [{"text": f"✅ Kanalǵa shıǵarıldı (#{pub_id})", "url": pub_url}]
                        ]
                    }
                })
                call_tg("answerCallbackQuery", {
                    "callback_query_id": cb_id,
                    "text": "🚀 Post kanalǵa tabıslı shıǵarıldı!",
                    "show_alert": False
                })
            else:
                call_tg("answerCallbackQuery", {
                    "callback_query_id": cb_id,
                    "text": f"Qátelik: {pub_res.get('error', 'Belgisiz')}",
                    "show_alert": True
                })
            return

        if cb_data.startswith("del:"):
            call_tg("editMessageReplyMarkup", {
                "chat_id": chat_id,
                "message_id": message_id,
                "reply_markup": {
                    "inline_keyboard": [
                        [{"text": "❌ Biykar etildi", "callback_data": "none"}]
                    ]
                }
            })
            call_tg("answerCallbackQuery", {
                "callback_query_id": cb_id,
                "text": "❌ Post biykar etildi.",
                "show_alert": False
            })
            return

    # 2. Handle text messages
    msg = update.get("message")
    if not msg:
        return

    chat_id = msg.get("chat", {}).get("id")
    user_id = str(msg.get("from", {}).get("id"))
    text = msg.get("text", "") or msg.get("caption", "")

    if not text:
        return

    if text in ("/start", "/help"):
        welcome = (
            "🏛 <b>CHECKERAI — Qaraqalpaqsha 0-Qátelik Tekseriwshi Bot</b>\n\n"
            "Magan qálegen qaraqalpaqsha jańalıq yamasa tekst jiberiń:\n"
            "1. 2016-jılǵı rásmiy latın imla qaǵıydalarına tekseredi.\n"
            "2. Singarmonizm, nızamsız bas «I» háribin hám ózbekizmlerdi dúzetedi.\n"
            "3. Bir basıw menen @qaraqalpaqshajanaliqlar kanalına shıǵaradı!"
        )
        call_tg("sendMessage", {"chat_id": chat_id, "text": welcome, "parse_mode": "HTML"})
        return

    # Run complete proofreading
    is_rel, rel_reason = evaluate_news_relevance(text)
    cleaned_html = sanitize_and_proofread_post(text)

    draft_key = f"{chat_id}_{int(time.time()*1000)}"
    draft_storage[draft_key] = {
        "original": text,
        "cleaned_html": cleaned_html,
        "created_at": time.time()
    }

    # Clean old drafts from memory (> 1 hour)
    now = time.time()
    for k in list(draft_storage.keys()):
        if now - draft_storage[k]["created_at"] > 3600:
            draft_storage.pop(k, None)

    rel_badge = "✅ Dolzarb" if is_rel else f"⚠️ Dolzarbligi tómen ({rel_reason})"
    preview_msg = (
        f"<b>📊 Tekseriw nátiyjesi:</b> {rel_badge}\n\n"
        f"{cleaned_html}"
    )

    markup = {
        "inline_keyboard": [
            [
                {"text": "🚀 Kanalǵa shıǵarıw", "callback_data": f"pub:{draft_key}"},
                {"text": "❌ Biykar etiw", "callback_data": f"del:{draft_key}"}
            ]
        ]
    }

    call_tg("sendMessage", {
        "chat_id": chat_id,
        "text": preview_msg,
        "parse_mode": "HTML",
        "reply_markup": markup
    })

def main():
    logger.info("CHECKERAI Bot polling started...")
    last_update_id = 0
    # Remove webhook if any
    call_tg("deleteWebhook", {"drop_pending_updates": False})

    while True:
        try:
            res = call_tg("getUpdates", {"offset": last_update_id + 1, "timeout": 20})
            if res.get("ok"):
                for upd in res.get("result", []):
                    last_update_id = upd["update_id"]
                    handle_update(upd)
            else:
                time.sleep(2)
        except Exception as exc:
            logger.error(f"Polling loop error: {exc}")
            time.sleep(3)

if __name__ == "__main__":
    main()

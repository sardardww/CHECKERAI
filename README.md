# 🏛️ CHECKERAI — Qaraqalpaqsha 0-Qátelik AI Tekseriwshi Sisteması

Rasmiy 2016-jılǵı Qaraqalpaq latın imla qaǵıydaları, singarmonizm (unlilar uyg‘unligi), anti-o‘zbekizm, anti-qozoqizm va `@KARAKALPAK24` kanali tajribasiga asoslangan mukammal tekshiruvchi va nashr etuvchi tizim.

---

## 🚀 Imkoniyatlar:
1. **0 Xato Kafolati:** So‘z o‘rtasidagi noo‘rin bosh harf `I` muammosini, singarmonizm buzilishlarini va o‘zbekcha kalkalarni avtomatik tuzatadi.
2. **Rasmiy Manbalar Bilan Moslashtirilgan:** 1,344 ta o‘zak so‘zlik akademik lug‘at va rasmiy kanallar uslubi.
3. **1-Click Nashr Qilish:** Matnni tekshiradi va bitta tugma bilan `@qaraqalpaqshajanaliqlar` kanaliga chiqaradi.
4. **REST API & Telegram Bot:** Istalgan AI Studio, Render yoki skript bilan ulanish imkoniyati.

---

## 🛠️ Ishga Tushirish:

### 1. Telegram Bot (@CHECKERPOSTLARMATBOT):
```bash
pip install -r requirements.txt
python bot.py
```

### 2. REST API:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### 3. Python Kod Ichida Ishlatish:
```python
from karakalpak_ai_master import sanitize_and_proofread_post

clean_html = sanitize_and_proofread_post("Xom qoraqalpoqcha matn...")
print(clean_html)
```

---

## 🔑 Sozlamalar (Environment Variables):
- `TELEGRAM_BOT_TOKEN`: Bot tokeni (Default: `@CHECKERPOSTLARMATBOT`)
- `ADMIN_CHAT_ID`: Admin ID (Sardarbek: `5649102659`)
- `TARGET_CHANNEL`: Maqsadli kanal (`@qaraqalpaqshajanaliqlar`, ID: `-1003987848482`)

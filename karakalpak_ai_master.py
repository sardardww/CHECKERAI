"""
================================================================================
🏛 QARAQALPAQ AI MASTER ENGINE (ZERO-ERROR AUTONOMOUS POSTER & MODERATOR)
================================================================================
Developed for: @qaraqalpaqshajanaliqlar & @sardardww
Standard: 2016 Official Karakalpak Latin Orthography (Qudaybergenov, 2017)
Corpus Ground Truth: @KARAKALPAK24 & Academic Karakalpak Lexicon
Bot: @uznewssssssss_bot (9218407703:AAFSOcaVFSJafUL4liO-TS982y58ODYY2BA)
Admin ID: 5649102659
Main Channel: -1003987848482 (@qaraqalpaqshajanaliqlar)
Render API: https://karakalpak-translator-api.onrender.com
================================================================================
"""

import os
import sys
import re
import time
import json
import base64
import logging
import requests
from typing import Dict, Any, Tuple, List, Optional
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("QARAQALPAQ_MASTER")

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "9218407703:AAFSOcaVFSJafUL4liO-TS982y58ODYY2BA")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", "5649102659"))
MAIN_CHANNEL_ID = int(os.environ.get("MAIN_CHANNEL_ID", "-1003987848482"))
RENDER_BASE_URL = os.environ.get("RENDER_BASE_URL", "https://karakalpak-translator-api.onrender.com")

STANDARD_FOOTER = '👉 <a href="https://t.me/+ccz2kfdc8Fg1ZGYy">Qaraqalpaqsha jańalıqlar — aǵza bolıw</a>'

# ==============================================================================
# 1. PHONOLOGY & 2016 STANDARD LATIN ORTHOGRAPHY RULES
# ==============================================================================
# Vowel Harmony (Singarmonizm):
# Back vowels (Juwan): a, o, u, ı
# Front vowels (Jińishke): e, i, ó, ú, á

FOREIGN_CHARS_MAP = {
    'ä': 'á', 'Ä': 'Á',
    'ö': 'ó', 'Ö': 'Ó',
    'ü': 'ú', 'Ü': 'Ú',
    'ğ': 'ǵ', 'Ğ': 'Ǵ',
    'ş': 'sh', 'Ş': 'Sh',
    'ç': 'ch', 'Ç': 'Ch',
    'ñ': 'ń', 'Ñ': 'Ń',
    'İ': 'I',
    'ë': 'e', 'Ë': 'E',
    # Cyrillic homoglyphs
    'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x',
    'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O', 'Р': 'P', 'С': 'C', 'Т': 'T'
}

# Bidirectional Cyrillic to 2016 Latin Transliteration Table
CYR_TO_QQ_LATIN = {
    "А": "A", "а": "a",
    "Ә": "Á", "ә": "á",
    "Б": "B", "б": "b",
    "В": "V", "в": "v",
    "Г": "G", "г": "g",
    "Ғ": "Ǵ", "ғ": "ǵ",
    "Д": "D", "д": "d",
    "Е": "E", "е": "e",
    "Ё": "Yo", "ё": "yo",
    "Ж": "J", "ж": "j",
    "З": "Z", "з": "z",
    "И": "I", "и": "i",
    "Й": "Y", "й": "y",
    "К": "K", "к": "k",
    "Қ": "Q", "қ": "q",
    "Л": "L", "л": "l",
    "М": "M", "м": "m",
    "Н": "N", "н": "n",
    "Ң": "Ń", "ң": "ń",
    "О": "O", "о": "o",
    "Ө": "Ó", "ө": "ó",
    "П": "P", "п": "p",
    "Р": "R", "р": "r",
    "С": "S", "с": "s",
    "Т": "T", "т": "t",
    "У": "W", "у": "w",      # Karakalpak Cyrillic 'у' in native stems is 'w' (e.g. аўыл -> awıl, таў -> taw)
    "Ү": "Ú", "ү": "ú",
    "Ў": "W", "ў": "w",
    "Ф": "F", "ф": "f",
    "Х": "X", "х": "x",
    "Ҳ": "H", "ҳ": "h",
    "Ц": "C", "ц": "c",
    "Ч": "Ch", "ч": "ch",
    "Ш": "Sh", "ш": "sh",
    "Щ": "Sh", "щ": "sh",
    "Ъ": "", "ъ": "",
    "Ы": "Í", "ы": "ı",
    "Ь": "", "ь": "",
    "Э": "E", "э": "e",
    "Ю": "Yu", "ю": "yu",
    "Я": "Ya", "я": "ya",
    "ПҚ": "PQ", "ПК": "PQ"
}

# ==============================================================================
# 2. ACADEMIC LEXICON & ANTI-UZBEKISM / ANTI-RUSSIAN CALQUE DICTIONARY
# (Extracted from Qudaybergenov 2017 & 80-Post Corpus of @KARAKALPAK24)
# ==============================================================================
STRICT_LEXICAL_REPLACEMENTS = [
    # Core national sovereignty & spelling
    (r"\bpuxar([a-zıóúáǵń]*)\b", r"puqar\1"),
    (r"\bPuxar([a-zıóúáǵń]*)\b", r"Puqar\1"),
    (r"\bRespublıkas([ıi])\b", r"Respublikas\1"),
    (r"\bRespublika\b", "Respublika"),
    (r"\bdelegacıya\b", "delegaciya"),
    (r"\btexnologıya([a-zıóúáǵń]*)\b", r"texnologiya\1"),
    (r"\b(t|T)echnologiya([a-zıóúáǵń]*)\b", r"\1exnologiya\2"),

    # Anti-Uzbekisms (Words taken incorrectly from Uzbek press)
    (r"\bfaol([a-zıóúáǵń]*)\b", r"belsend\1"),
    (r"\bFaol([a-zıóúáǵń]*)\b", r"Belsend\1"),
    (r"\bbandlıq([a-zıóúáǵń]*)\b", r"bántlik\1"),
    (r"\bBandlıq([a-zıóúáǵń]*)\b", r"Bántlik\1"),
    (r"\bjarima([a-zıóúáǵń]*)\b", r"járiyma\1"),
    (r"\bJarima([a-zıóúáǵń]*)\b", r"Járiyma\1"),
    (r"\bjarıma([a-zıóúáǵń]*)\b", r"járiyma\1"),
    (r"\bJarıma([a-zıóúáǵń]*)\b", r"Járiyma\1"),
    (r"\btashkilot([a-zıóúáǵń]*)\b", r"shólkem\1"),
    (r"\bhokimlik([a-zıóúáǵń]*)\b", r"hákimiyat\1"),
    (r"\b(h|H)ákimligi qasında\b", r"\1ákimiyatı qasında"),
    (r"\btibbiyot([a-zıóúáǵń]*)\b", r"medicina\1"),
    (r"\bmaydonda\b", "maydanda"),
    (r"\bMaydonda\b", "Maydanda"),
    (r"\bTaza Tashkent\b", "Jańa Toshkent"),
    (r"\bTaza Toshkent\b", "Jańa Toshkent"),
    (r"\bkitabxan([a-zıóúáǵń]*)\b", r"kitapxan\1"),
    (r"\bKitabxan([a-zıóúáǵń]*)\b", r"Kitapxan\1"),
    (r"\bfaxriy([a-zıóúáǵń]*)\b", r"nuranıy\1"),
    (r"\bFaxriy([a-zıóúáǵń]*)\b", r"Nuranıy\1"),
    (r"\b(z|Z)áhárleniw([a-zıóúáǵń]*)\b", r"\1eherleniw\2"),
    (r"\bis gazınen\b", "is gazınan"),
    (r"\b(p|P)ısıw hám tigiw\b", r"\1ishiw hám tigiw"),
    (r"\bjastansha\b", "jastaǵı"),
    (r"\btashıw\b", "tasıw"),
    (r"\bTashıw\b", "Tasıw"),
    (r"\bjolawshılardı tashıw\b", "jolawshılardı tasıw"),

    # Toponyms & Official Decrees
    (r"\bTórtkól\b", "Tórtkúl"),
    (r"\bTórtkul\b", "Tórtkúl"),
    (r"\bTashkent\b", "Toshkent"),
    (r"\b№?\s*(PP|ПП|ПҚ)-(\d+)\b", r"PQ-\2-sanlı"),
    (r"\bPrezidenttiń (\d+)-sanlı\b", r"Prezidenttiń PQ-\1-sanlı"),

    # Anti-Russian Calques
    (r"\b(q|Q)adaǵalaw ólshemler([a-zıóúáǵń]*)\b", r"\1adaǵalaw ilajlar\2"),
    (r"\bkútip barıw([a-zıóúáǵń]*)\b", r"kútip-baplaw\1"),
    (r"\b(q|Q)arıydarlardıń huqıqlar([a-zıóúáǵń]*)\b", r"\1utınıwshılardıń huqıqlar\2"),
    (r"\bIshki isler uyımları\b", "Ishki isler organları"),
    (r"\bmámleketlik uyımlard([ıi])\b", r"mámleketlik organlard\1"),
    (r"\b(q|Q)ádemler taslamaqta\b", r"ilajlar kórmekte"),
    (r"\btájiriybeli sapar([a-zıóúáǵń]*)\b", r"jumıs sapar\1"),
    (r"\bqupıya orın([a-zıóúáǵń]*)\b", r"jasırın orın\1"),
    (r"\bmars tuqımı\b", "mars jınısı"),
    (r"\baqsha juwıw\b", "aqsha jıllaw"),
    (r"\bshınjırshasın\b", "jetkerip beriw dizbegin"),
    (r"\btámiyinlew shınjırshas([ıi])\b", r"jetkerip beriw dizbeg\1"),
    (r"\btekseriw barısında\b", "tergew barısında"),
    (r"\búshinshi dáwiri\b", "úshinshi basqıshı"),
    (r"\brayonlıq administraciya\b", "rayon hákimiyatı"),
    (r"\bjámiyetshilik keńlikler([a-zıóúáǵń]*)\b", r"jámiyetlik orınlar\1"),
    (r"\bvzyskaniya([a-zıóúáǵń]*)\b", r"járiyma\1"),
    (r"\bóndiriwler qollaw\b", "járiyma qollaw"),
    (r"\bkesispepleri([a-zıóúáǵń]*)\b", r"kesispeleri\1"),
    (r"\badministrativlik tártipte\b", "hákimshilik tártipte"),
    (r"\bsaz isleywshiligin\b", "durıs islewin"),
    (r"\bmorylar\b", "morilar"),
    (r"\btereń úreniwdi ózine aladı\b", "tereń úreniwdi óz ishine aladı"),
    (r"\bházirgi zamanǵa say\b", "zamanaǵóy"),
    (r"\bbas planın\b", "bas rejesin"),
    (r"\bgúresiw byurosı\b", "qarsı gúresiw byurosı"),

    # Vowel Harmony & Case Concordance
    (r"\bengiziwdıń\b", "engiziwdiń"),
    (r"\bmáselerin\b", "máselelerin"),
    (r"\bmásseleler([a-zıóúáǵń]*)\b", r"máseleler\1"),
    (r"\b([e|E])ksport qiliw\b", r"\1ksport qılıw"),
    (r"\bjúze keliw([a-zıóúáǵń]*)\b", r"júzege keliw\1"),
    (r"\bjol qoymaw hám de\b", "jol qoymawdı hám de"),
    (r"\b(j|J)asıl makan\b", r"\1asıl mákan"),
    (r"\b(u|U)lıwma milliy\b", r"\1lıwmamilliy"),
    (r"\b(t|T)erek eguw\b", r"\1erek egiw"),
    (r"\bmáhällä([a-zıóúáǵń]*)\b", r"máhálle\1"),
    (r"\bmáhalle([a-zıóúáǵń]*)\b", r"máhálle\1"),
    (r"\bMáhalle([a-zıóúáǵń]*)\b", r"Máhálle\1"),
    (r"\bÁstanalıq\b", "Astanalıq"),
    (r"\bÁstana\b", "Astana"),
    (r"\b(p|P)rocess\b", r"\1roces"),
    (r"\bJIÓ\b", "JI"),
]


# ==============================================================================
# 3. BULLETPROOF STRAY CAPITAL 'I' REPAIR ENGINE
# ==============================================================================
def repair_rogue_capital_i(text: str) -> str:
    """
    Eliminates stray capital 'I' letters inside words caused by Unicode case-folding.
    - Preserves legal acronyms: IIV, IIO, AQSh, BMSh, GFR, ÓzA, etc.
    - Preserves word-initial I: Isa, Ilim, Islam, etc.
    - Follows Karakalpak vowel harmony:
      * Back vowel stem (a, o, u, ı) -> 'ı'
      * Front vowel stem (e, i, ó, ú, á) -> 'i'
    """
    FRONT_VOWELS = set('eióúáEÍÓÚÁ')
    BACK_VOWELS = set('aouıAOUÍ')

    def fix_word(match):
        word = match.group(0)
        if word.isupper() and len(word) <= 5:
            return word
        if 'I' not in word:
            return word

        has_front = any(ch in FRONT_VOWELS for ch in word.replace('I', ''))
        has_back = any(ch in BACK_VOWELS for ch in word.replace('I', ''))

        if has_front and not has_back:
            safe_vowel = 'i'
        elif has_back and not has_front:
            safe_vowel = 'ı'
        else:
            safe_vowel = None

        chars = list(word)
        for idx, ch in enumerate(chars):
            if ch == 'I':
                if idx == 0 and len(chars) > 1 and chars[1].islower():
                    continue
                target_v = safe_vowel
                if not target_v:
                    prev_v = None
                    for b_idx in range(idx - 1, -1, -1):
                        if chars[b_idx].lower() in 'eióúá':
                            prev_v = 'i'; break
                        elif chars[b_idx].lower() in 'aouı':
                            prev_v = 'ı'; break
                    next_v = None
                    for f_idx in range(idx + 1, len(chars)):
                        if chars[f_idx].lower() in 'eióúá':
                            next_v = 'i'; break
                        elif chars[f_idx].lower() in 'aouı':
                            next_v = 'ı'; break
                    target_v = prev_v or next_v or 'ı'
                chars[idx] = target_v

        return "".join(chars)

    parts = re.split(r"(<[^>]+>)", text)
    out = []
    for part in parts:
        if part.startswith("<") and part.endswith(">"):
            out.append(part)
        else:
            repaired = re.sub(r"[a-zA-ZáóúıǵńÁÓÚIǴŃ]+", fix_word, part)
            out.append(repaired)
    return "".join(out)


# ==============================================================================
# 4. COMPREHENSIVE GRAMMAR & HTML SANITIZATION PIPELINE
# ==============================================================================
def sanitize_and_proofread_post(raw_html: str, exact_source_url: str = "") -> str:
    """
    Executes complete multi-layer linguistic sanitation:
    1. Zero foreign umlauts & homoglyphs.
    2. Exact lexical & anti-Uzbekism dictionary enforcement.
    3. SOV sentence syntax inversion repair.
    4. Headline bolding (<b>...</b>).
    5. Direct source hyperlink embedding into primary action verb.
    6. Strictly ONE footer link guarantee.
    7. Rogue capital I normalization.
    """
    if not raw_html or not raw_html.strip():
        return ""

    text = raw_html.strip()

    # Step 1: Character level normalization (Foreign umlauts)
    for foreign_ch, safe_ch in FOREIGN_CHARS_MAP.items():
        text = text.replace(foreign_ch, safe_ch)

    # Step 2: Separate HTML tags from narrative text
    parts = re.split(r"(<[^>]+>)", text)
    out_parts = []
    for part in parts:
        if part.startswith("<") and part.endswith(">"):
            out_parts.append(part)
        else:
            p_text = part
            # Apply strict lexical replacements
            for pattern, repl in STRICT_LEXICAL_REPLACEMENTS:
                p_text = re.sub(pattern, repl, p_text)
            out_parts.append(p_text)

    text = "".join(out_parts)

    # Step 3: Rogue capital I repair
    text = repair_rogue_capital_i(text)

    # Step 4: Fix inverted Russian SOV syntax for common administrative meetings
    # e.g., "Farxod Ermanov ótkerdi ... ushırasıw" -> "Farxod Ermanov ... ushırasıw ótkerdi"
    sov_pattern = r"(Farxod Ermanov|Rayon hákimi|Prezident)\s+ótkerdi\s+(.*?)\s+(ushırasıw|múrájat|qabıllaw)"
    text = re.sub(sov_pattern, r"\1 \2 \3 ótkerdi", text)

    # Step 5: Ensure Bold Headline
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    if lines:
        first_line = lines[0]
        # Remove any existing bold tags on line 1 to avoid nesting
        clean_first = re.sub(r"</?b>", "", first_line)
        lines[0] = f"<b>{clean_first}</b>"
        text = "\n\n".join(lines)

    # Step 6: Embed Direct Source Hyperlink onto Focus Verb
    if exact_source_url:
        soup = BeautifulSoup(text, "html.parser")
        has_ext_link = False
        for a in soup.find_all("a"):
            href = a.get("href", "")
            if "+ccz2kfdc8Fg1ZGYy" not in href and "qaraqalpaqshajanaliqlar" not in href:
                a["href"] = exact_source_url
                has_ext_link = True
                break

        if has_ext_link:
            text = str(soup)
        else:
            focus_verbs = [
                r"\b(ushırasıw ótkerdi|xabar berdi|xabar berildi|málim etti|eskertti|belgilendi|qolǵa túsirdi|shólkemlestirildi|baslandı|járiyladı|maqulladı|kútilmekte|engizildi|ótkerildi|ayttı)\b"
            ]
            wrapped = False
            for pat in focus_verbs:
                m = re.search(pat, text, flags=re.IGNORECASE)
                if m:
                    target_w = m.group(1).rstrip(".,;:!?")
                    text = text[:m.start()] + f'<a href="{exact_source_url}">{target_w}</a>' + text[m.start() + len(target_w):]
                    wrapped = True
                    break

            if not wrapped:
                # Wrap main verb before period
                sentence_match = re.search(r'([a-zA-ZáóúıǵńÁÓÚIǴŃ]{4,})(\s*\.)', text)
                if sentence_match:
                    vb = sentence_match.group(1)
                    text = text[:sentence_match.start(1)] + f'<a href="{exact_source_url}">{vb}</a>' + text[sentence_match.end(1):]

    # Step 7: Guarantee Strictly ONE Single Footer
    clean_lines = []
    for ln in text.split("\n"):
        st = ln.strip()
        if st.startswith("👉") or "aǵza bolıw" in st.lower() or "+ccz2kfdc8Fg1ZGYy" in st.lower():
            continue
        clean_lines.append(ln)

    final_text = "\n".join(clean_lines).rstrip() + "\n\n" + STANDARD_FOOTER
    final_text = re.sub(r'\n{3,}', '\n\n', final_text)

    return final_text.strip()


# ==============================================================================
# 5. RELEVANCE & URGENCY EVALUATOR (NEWS FILTER)
# ==============================================================================
def evaluate_news_relevance(text: str) -> Tuple[bool, str]:
    """
    Classifies whether news is urgent/valuable or low-quality/trash.
    Returns: (is_relevant, reason)
    """
    txt_lower = text.lower()

    # Rejection keywords (Spam, betting, irrelevant commercial ads)
    trash_keywords = [
        "1xbet", "mostbet", "stavka", "kazino", "skidka", "arzan bahada satıladı",
        "reklama", "kanalǵa qosılıń", "aknuri", "tez kiring", "preeemium"
    ]
    for kw in trash_keywords:
        if kw in txt_lower:
            return False, f"Tijoriy reklama yoki spam aniqlandi: '{kw}'"

    # High priority keywords
    high_priority = [
        "prezident", "qarar", "nızam", "qaraqalpaqstan", "nókis", "hákimiyat",
        "sud", "prokuratura", "ishki isler", "bajıxana", "ekologiya", "hawa rayı",
        "jasıl mákan", "járiyma", "bilimlendiriw", "mektep", "olimpiada",
        "texnologiya", "jasama intellekt", "investiciya", "eksport"
    ]
    matches = [kw for kw in high_priority if kw in txt_lower]
    if len(matches) >= 2 or len(text) > 120:
        return True, f"Dolzarb ijtimoiy-siyosiy yangilik (Kalit so'zlar: {matches[:3]})"

    return True, "Standart yangilik"


# ==============================================================================
# 6. TELEGRAM BOT API HELPER FUNCTIONS
# ==============================================================================
def call_telegram(method: str, payload: dict[str, Any], files: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    try:
        if files:
            r = requests.post(url, data=payload, files=files, timeout=40)
        else:
            r = requests.post(url, json=payload, timeout=25)
        return r.json()
    except Exception as exc:
        logger.error(f"Telegram API {method} error: {exc}")
        return {"ok": False, "error": str(exc)}


def trigger_render_callback(draft_id: int, action: str = "pub", admin_message_id: int = 0) -> bool:
    """
    Sends callback to Render's sequential moderation queue webhook.
    action: 'pub' (Kanalǵa shıǵarıw) or 'del' (Biykar etiw).
    """
    webhook_url = f"{RENDER_BASE_URL}/telegram-webhook"
    payload = {
        "callback_query": {
            "id": f"auto_{int(time.time())}",
            "from": {"id": ADMIN_CHAT_ID},
            "data": f"{action}:{draft_id}",
            "message": {
                "chat": {"id": ADMIN_CHAT_ID},
                "message_id": admin_message_id
            }
        }
    }
    try:
        r = requests.post(webhook_url, json=payload, timeout=25)
        logger.info(f"Triggered Render callback {action}:{draft_id} -> Status {r.status_code}")
        return r.status_code == 200
    except Exception as exc:
        logger.error(f"Failed to call Render webhook: {exc}")
        return False


def get_active_moderation_post_from_telegram() -> Optional[Dict[str, Any]]:
    """
    Reads the active draft message from Admin chat via quiet check or getUpdates.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset=-5"
    try:
        r = requests.get(url, timeout=15).json()
        if not r.get("ok"):
            return None
        updates = r.get("result", [])
        for u in reversed(updates):
            msg = u.get("message") or u.get("channel_post")
            if msg and msg.get("chat", {}).get("id") == ADMIN_CHAT_ID:
                cap = msg.get("caption") or msg.get("text") or ""
                markup = msg.get("reply_markup", {})
                mid = msg.get("message_id")
                return {"message_id": mid, "caption": cap, "reply_markup": markup}
    except Exception as exc:
        logger.error(f"getUpdates error: {exc}")
    return None


# ==============================================================================
# 7. MAIN CLI CONTROLLER
# ==============================================================================
def process_single_text(raw_text: str, source_url: str = "") -> str:
    """Processes a raw Karakalpak text and prints detailed grammar diagnostics."""
    print("=" * 60)
    print("ORIGINAL INPUT:")
    print(raw_text)
    print("=" * 60)

    is_rel, rel_reason = evaluate_news_relevance(raw_text)
    print(f"RELEVANCE EVALUATION: {'✅ QABUL ETILDI' if is_rel else '❌ BEKOR QILINDI'} ({rel_reason})")

    cleaned_html = sanitize_and_proofread_post(raw_text, source_url)

    print("\n" + "=" * 60)
    print("ZERO-ERROR 2016 STANDARD PROOFREAD RESULT:")
    print(cleaned_html)
    print("=" * 60)

    return cleaned_html


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        sample = sys.argv[2] if len(sys.argv) > 2 else ""
        url = sys.argv[3] if len(sys.argv) > 3 else ""
        if sample:
            process_single_text(sample, url)
        else:
            print("Usage: python karakalpak_ai_master.py check '<post_text>' [source_url]")
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        test_post = """🇺🇿 Qaraqalpaqstan AQSh penen toqımashılıq tarawındaǵı birge Islesiwdi keńeytirip atır
Qaraqalpaqstan Respublıkası Ministrler Keńesiniń Baslıǵı Farxod Ermanov ótkerdi Amerika Qurama Shtatları kiyim bazarı wákili Meir Karpı basshılıǵındaǵı amerikalıq delegacıya menen ushırasıw. Tárepler jergilikli toqımashılıq ónimlerin Qurama Shtatlar bazarına shıǵarıw hám birge Islesiwshi Investiciya joybarların keńeytiw másselelerin talqıladı.
Sóylesiwler aymaqtan tayın toqıma ónimlerin eksport qiliw hám Qaraqalpaqstannıń tigiwshilik tarawına aldınǵı texnologıyalardı tartıw ushın jańa múmkinshilikler ashpaqta."""
        process_single_text(test_post, "https://t.me/QResMinistrlerKenesi/45751")
    else:
        print("🏛 Qaraqalpaq AI Master Engine (2016 Standart) — Interaktiv Rejim")
        print("—" * 60)
        print("Qoraqalpoqcha matnni kiriting (chiqish uchun 'exit' deb yozing):")
        try:
            while True:
                line = input("\n📝 Matn > ")
                if not line.strip() or line.strip().lower() in ("exit", "quit"):
                    break
                url = input("🔗 Manba URL (agar bo'lsa, bo'sh qoldirish mumkin): ")
                process_single_text(line, url.strip())
        except (KeyboardInterrupt, EOFError):
            print("\nDastur to'xtatildi.")

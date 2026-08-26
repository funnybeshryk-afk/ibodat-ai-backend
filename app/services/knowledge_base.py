import json
import re
from pathlib import Path
from typing import List

from app.models.knowledge import KbItem

# Ma'lumotlar endi shu faylda: app/data/knowledge_base.json
# Yangi maqola qo'shish uchun kodni o'zgartirish shart emas — shu JSON faylga
# bitta yangi obyekt qo'shish yetarli (id, title, category, content, language,
# source, sourceReference maydonlari bilan).
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"

# Juda qisqa so'zlar ("va", "bu" va h.k.) qidiruvda hisobga olinmaydi.
# 3 harfdan boshlab olamiz — "ota", "duo", "ilm" kabi diniy-lug'atda muhim
# qisqa so'zlar shu yerga sig'ishi kerak.
MIN_KEYWORD_LEN = 3


class KnowledgeBaseService:
    def __init__(self):
        self._data: List[KbItem] = self._load_data()

    def _load_data(self) -> List[KbItem]:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            raw_items = json.load(f)
        return [KbItem(**item) for item in raw_items]

    def _words(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower(), flags=re.UNICODE)

    def _keywords(self, query: str) -> List[str]:
        return [w for w in self._words(query) if len(w) >= MIN_KEYWORD_LEN]

    def _matches(self, keyword: str, haystack_words: List[str]) -> bool:
        # Faqat bitta yo'nalishda: kalit so'z haystack so'zining PREFIKSI
        # bo'lishi kerak (masalan, "namoz" -> "namozning" mos keladi).
        # Teskarisini ("qil" -> "qilish" kabi) hisobga olmaymiz — aks holda
        # ko'p fe'l ildizlari tasodifan har qanday so'zga mos kelib qolardi.
        return any(w.startswith(keyword) for w in haystack_words)

    def search(self, query: str, language: str = "uz") -> List[KbItem]:
        keywords = self._keywords(query)
        if not keywords:
            return []

        scored: List[tuple[int, KbItem]] = []
        for item in self._data:
            if item.language != language:
                continue

            haystack_words = self._words(f"{item.title} {item.content} {item.category}")
            score = sum(1 for kw in keywords if self._matches(kw, haystack_words))
            if score > 0:
                scored.append((score, item))

        # Ko'proq kalit so'z mos kelgan maqolalar birinchi bo'lib qaytariladi
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [item for _, item in scored[:5]]


knowledge_base = KnowledgeBaseService()

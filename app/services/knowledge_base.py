from typing import List, Optional
from app.models.knowledge import KbItem

class KnowledgeBaseService:
    def __init__(self):
        # In-memory storage for testing, can be moved to JSON or DB later
        self._data: List[KbItem] = [
            # DUALAR
            KbItem(
                id="dua_ilm",
                title="Ilm ziyoda bo'lishi uchun duo",
                category="Ilm",
                content="رَبِّ زِدْنِي عِلْمًا - Robbi zidnii ilman. Ey Robbim, ilmimni ziyoda qil.",
                language="uz",
                source="Qur'on",
                sourceReference="Toha surasi, 114-oyat"
            ),
            KbItem(
                id="dua_parents",
                title="Ota-ona haqqiga duo",
                category="Ota-ona",
                content="رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا - Robbirhamhumaa kamaa robbayaanii sog'iiron. Ey Robbim, ular meni kichikligimda tarbiyalaganlaridek, Sen ham ularga rahm qil.",
                language="uz",
                source="Qur'on",
                sourceReference="Isro surasi, 24-oyat"
            ),
            # HADISLAR
            KbItem(
                id="hadith_niyat",
                title="Amallar niyatga bog'liq",
                category="Niyat",
                content="إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ - Albatta, amallar niyatlarga bog'liqdir. Har bir kishi niyat qilgan narsasiga erishadi.",
                language="uz",
                source="Sahih Buxoriy",
                sourceReference="1-hadis"
            ),
            # NAMOZ BASICS
            KbItem(
                id="namoz_tahorat",
                title="Tahorat olish tartibi",
                category="Namoz",
                content="Tahorat 8 bosqichdan iborat: Niyat, Qo'llarni yuvish, Og'iz chayish, Burun chayish, Yuzni yuvish, Qo'llarni tirsakkacha yuvish, Mash tortish, Oyoqlarni yuvish.",
                language="uz",
                source="Fiqhu-l-vazeh",
                sourceReference="Tahorat bobi"
            ),
            KbItem(
                id="namoz_shartlar",
                title="Namozning shartlari",
                category="Namoz",
                content="Namozning 6 ta sharti bor: Tahoratli bo'lish, Poklik, Avrat yopiqligi, Vaqt, Qibla, Niyat.",
                language="uz",
                source="Muxtasaru-l-viqoya",
                sourceReference="Namoz kitobi"
            ),
            # RUSSIAN SAMPLES
            KbItem(
                id="dua_ilm_ru",
                title="Дуа для увеличения знаний",
                category="Знания",
                content="Господи! Приумножь мои знания (Рабби зидни ильман).",
                language="ru",
                source="Коран",
                sourceReference="Сура Та Ха, аят 114"
            )
        ]

    def search(self, query: str, language: str = "uz") -> List[KbItem]:
        query = query.lower()
        results = []
        for item in self._data:
            if item.language == language:
                if query in item.title.lower() or query in item.content.lower() or query in item.category.lower():
                    results.append(item)
        return results

knowledge_base = KnowledgeBaseService()

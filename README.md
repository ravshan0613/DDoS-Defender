#  Flask asosida DDoS va Login Brute Force himoya dasturi

Bu dastur Flask yordamida yozilgan bo‘lib, quyidagi funksiyalarni bajaradi:

-  DDoS hujumlarga qarshi IP bo‘yicha so‘rov cheklovi
-  Kirish (login) bruteforce urinishlarini aniqlash va bloklash
-  Ishonchli IP manzillarni white-list orqali bloklanmasdan ushlab turish
-  Parol bilan himoyalangan admin panel
-  Kirish va bloklash loglari (`log.txt` faylida)
-  Oddiy veb-interfeys orqali kuzatuv paneli (admin panel)

---

##  Talablar (Dependencies)

Quyidagi kutubxonalar kerak bo‘ladi:

- Python 3.7+
- Flask

O‘rnatish:
```bash
pip install flask

# MySoqqa

MySoqqa - bu Django asosida ishlab chiqilgan byudjet boshqaruvi veb-ilovasi bo‘lib, foydalanuvchilarga daromad va xarajatlarni boshqarish, moliyaviy statistikani ko‘rish, kalendar orqali tranzaksiyalarni kuzatish va shaxsiy sozlamalarni o‘zgartirish imkonini beradi. Ilova foydalanuvchi autentifikatsiyasi, xavfsiz parol tiklash va boshqa funksiyalarni qo‘llab-quvvatlaydi.

## Xususiyatlar
MySoqqa quyidagi veb-sahifalar va funksiyalarni o‘z ichiga oladi:

- **Bosh sahifa (`/`)**: Ilovaga xush kelibsiz sahifasi.
- **Ro‘yxatdan o‘tish (`/signup/`)**:
  - Foydalanuvchilar elektron pochta orqali ro‘yxatdan o‘tadi.
  - Tasdiqlash kodi yuboriladi (10 daqiqa amal qiladi).
  - Foydalanuvchi ismi, familiyasi, afzal til va valyutani tanlaydi.
- **Tizimga kirish (`/login/`)**: Foydalanuvchilar elektron pochta va parol bilan tizimga kiradi.
- **Tizimdan chiqish (`/logout/`)**: Foydalanuvchi sessiyasini yakunlaydi.
- **Boshqaruv paneli (`/dashboard/`)**:
  - Foydalanuvchining barcha daromad va xarajatlari ro‘yxati.
  - Yangi daromad yoki xarajat qo‘shish imkoniyati.
- **Daromad qo‘shish/tahrirlash/o‘chirish (`/add_income/`, `/update_income/<id>/`, `/delete_income/<id>/`)**:
  - Miqdor, valyuta, sana, kategoriya va eslatma kiritish.
  - Mavjud daromadlarni tahrirlash yoki o‘chirish.
- **Xarajat qo‘shish/tahrirlash/o‘chirish (`/add_expense/`, `/update_expense/<id>/`, `/delete_expense/<id>/`)**:
  - Daromad bilan bir xil funksiyalar, lekin xarajatlar uchun.
- **Statistika (`/statistics/`)**:
  - Umumiy daromad, xarajat va sof balansni ko‘rsatadi.
  - Kategoriyalar bo‘yicha tahlil (daromad va xarajatlar).
  - Progress bar orqali foizli taqsimot.
- **Kalendar (`/calendar/`)**:
  - Oylik tranzaksiyalarni kunlik ko‘rinishda ko‘rsatadi.
  - Oylik daromad, xarajat va balans xulosasi.
- **Tarix (`/history/`)**:
  - Barcha tranzaksiyalarni (daromad va xarajat) filtrlar bilan ko‘rish.
  - Qidiruv, tur (daromad/xarajat), kategoriya va sana bo‘yicha filtrlar.
  - Sahifalarga bo‘lingan ro‘yxat (har sahifada 20 ta yozuv).
- **Sozlamalar (`/settings/`)**:
  - Profilni yangilash (ism, familiya, afzal til, valyuta).
  - Parolni o‘zgartirish (joriy parolni tasdiqlash talab qilinadi).
  - Hisobni o‘chirish.
- **Parolni tiklash (`/password_reset/`)**:
  - Elektron pochtaga tasdiqlash kodi yuboriladi.
  - Yangi parol o‘rnatish uchun kodni tasdiqlash.

## Xavfsizlik
- **Elektron pochta tasdiqlash**: Ro‘yxatdan o‘tish va parol tiklash uchun tasdiqlash kodi.
- **Parol xavfsizligi**: Parollar shifrlanadi, `check_password` funksiyasi orqali tekshiriladi.
- **HTTPS**: Render’da joylashtirilganda xavfsiz ulanish.

## Tizim talablari
- Python 3.8 yoki undan yuqori.
- Git (kodni GitHub’dan yuklash uchun).
- Render hisobi (deploiement uchun).
- Elektron pochta xizmati (tasdiqlash kodlari uchun, masalan, Gmail SMTP).

## Mahalliy sozlash
Loyihani mahalliy kompyuterda ishga tushirish uchun quyidagi qadamlarni bajaring:

1. **Repozitoriyani klonlash**:
   ```bash
   git clone https://github.com/sizning_foydalanuvchi_nomingiz/mysoqqa.git
   cd mysoqqa
   ```

2. **Virtual muhit yaratish va faollashtirish**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows uchun: venv\Scripts\activate
   ```

3. **Bog‘liqliklarni o‘rnatish**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ma‘lumotlar bazasini sozlash**:
   - Migratsiyalarni ishga tushiring:
     ```bash
     python manage.py migrate
     ```
   - Dastlabki valyuta yaratish (ro‘yxatdan o‘tish uchun talab qilinadi):
     ```bash
     python manage.py shell
     ```
     ```python
     from user.models import Currency
     Currency.objects.create(code="USD", name="US Dollar")
     ```

5. **Statik fayllarni yig‘ish**:
   ```bash
   python manage.py collectstatic
   ```

6. **Serverni ishga tushirish**:
   ```bash
   python manage.py runserver
   ```
   - Brauzerda `http://localhost:8000` ga o‘ting.

7. **Test qilish**:
   - **Bosh sahifa**: `http://localhost:8000/`.
   - **Ro‘yxatdan o‘tish**:
     - `http://localhost:8000/signup/` ga o‘ting.
     - Elektron pochta kiritib, tasdiqlash kodi orqali ro‘yxatdan o‘ting.
   - **Tizimga kirish**: `http://localhost:8000/login/` orqali kirib, `dashboard` ga o‘ting.
   - **Sozlamalar**: `http://localhost:8000/settings/` da parolni o‘zgartiring.
   - **Statistika/Kalendar/Tarix**: Tranzaksiyalarni qo‘shib, ushbu sahifalarni sinab ko‘ring.

## Render’ga joylashtirish
Loyihani Render platformasiga joylashtirish uchun quyidagi qadamlarni bajaring:

1. **Render hisobini yaratish**:
   - [Render](https://render.com) saytida ro‘yxatdan o‘ting va elektron pochtangizni tasdiqlang.

2. **Veb-xizmat yaratish**:
   - Render Dashboard’da “New” > “Web Service” ni bosing.
   - GitHub hisobingizni ulang va `mysoqqa` repozitoriyasini tanlang.
   - Sozlamalar:
     - **Name**: `mysoqqa-api`
     - **Environment**: Python
     - **Region**: Sizga eng yaqin (masalan, US East)
     - **Branch**: `main`
     - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
     - **Start Command**: `gunicorn mysoqqa.wsgi:application`
     - **Instance Type**: Free (sinov uchun).
   - **Advanced Settings**:
     - Disk qo‘shing:
       - Name: `sqlite3-disk`
       - Mount Path: `/opt/render/project/src`
       - Size: 1 GB (SQLite3 uchun).

3. **Atrof-muhit o‘zgaruvchilarini sozlash**:
   - Web Service sozlamalarida Environment > Environment Variables ga o‘ting va quyidagilarni qo‘shing:
     - `DJANGO_SECRET_KEY`: Quyidagi buyruq bilan yarating:
       ```bash
       python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
       ```
     - `DEBUG`: `False`
     - `ALLOWED_HOSTS`: `mysoqqa-api.onrender.com,localhost,127.0.0.1`
     - `EMAIL_HOST_USER`: Sizning elektron pochta manzilingiz (masalan, Gmail).
     - `EMAIL_HOST_PASSWORD`: Elektron pochta ilovasi paroli.
     - `SECURE_SSL_REDIRECT`: `True`

4. **Joylashtirish**:
   - “Create Web Service” ni bosing.
   - Build loglarini kuzating.
   - URL ni eslab qoling (masalan, `https://mysoqqa-api.onrender.com`).

5. **Ma‘lumotlar bazasini tekshirish**:
   - `db.sqlite3` GitHub orqali yuklangan bo‘lsa, diskda (`/opt/render/project/src/db.sqlite3`) mavjud.
   - Tekshirish uchun Render shell’dan foydalaning:
     - Dashboard > Web Service > Shell.
     - Quyidagilarni ishga tushiring:
       ```bash
       python manage.py shell
       ```
       ```python
       from user.models import Currency
       Currency.objects.all()
       ```
     - Agar bo‘sh bo‘lsa, valyuta yarating:
       ```python
       Currency.objects.create(code="USD", name="US Dollar")
       ```

6. **Foydalanuvchi yaratish**:
   - Brauzerda `https://mysoqqa-api.onrender.com/signup/` ga o‘ting va yangi foydalanuvchi ro‘yxatdan o‘tkazing.
   - Yoki Render shell’da admin yarating:
     ```bash
     python manage.py createsuperuser
     ```

7. **Sinov**:
   - **Bosh sahifa**: `https://mysoqqa-api.onrender.com/`.
   - **Sozlamalar**: `https://mysoqqa-api.onrender.com/settings/` da parolni o‘zgartiring.
   - **Statistika**: `https://mysoqqa-api.onrender.com/statistics/` da balansni ko‘ring.
   - **Parol tiklash**: `https://mysoqqa-api.onrender.com/password_reset/` orqali sinab ko‘ring.

## Muammolarni bartaraf etish
- **Build muvaffaqiyatsiz bo‘lsa**: Loglarda `requirements.txt` yoki kod xatolarini tekshiring.
- **Ma‘lumotlar bazasi xatolari**: `db.sqlite3` diskda mavjudligini va ruxsatlarini tekshiring (`chmod 664 db.sqlite3`).
- **Statik fayllar yuklanmasa**: `collectstatic` ishlaganligini tekshiring.
- **Elektron pochta xatolari**: `EMAIL_HOST_USER` va `EMAIL_HOST_PASSWORD` to‘g‘riligini tekshiring.
- **403/500 xatolar**: `ALLOWED_HOSTS` va `DEBUG=False` sozlamalarini tekshiring.

## Kelajakdagi qadamlar
- PostgreSQL ga o‘tish uchun Render ma‘lumotlar bazasidan foydalaning.
- Maxsus domen qo‘shish uchun Render Dashboard > Settings > Custom Domains ga o‘ting.
- Frontend yaxshilash yoki mobil ilova qo‘shish uchun qo‘shimcha yordam so‘rang.

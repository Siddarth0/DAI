# Digital Information Portal

This portal was developed for DAI Global to streamline SME registration, BDSP onboarding, and service access through a modular, multilingual web interface. It supports dynamic user flows, secure authentication, and responsive dashboards tailored to development sector needs.

## 🌐 Key Modules

- **SME Registration**: Multi-step form with OTP verification and profile setup
- **BDSP Onboarding**: Stepwise profiling and dashboard access
- **Login System**: Separate flows for SMEs and BDSPs with secure email-based OTP
- **Admin Dashboard**: Custom views for managing users, services, and events
- **Multilingual Support**: Language selector for inclusive access

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: Django templates, Tailwind CSS, JavaScript, Swiper.js
- **Database**: PostgreSQL

## 📦 Setup Instructions

```bash
git clone https://github.com/Siddarth0/DAI.git
cd DAI
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

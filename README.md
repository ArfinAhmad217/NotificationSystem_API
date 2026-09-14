# Notification System — StarClinch Backend Developer Assignment

A full-stack notification system that lets an admin manage triggers and
templates for WhatsApp, Email, and Web Push from one panel, and fires
notifications on real website events (Login / Logout).

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Frontend:** Next.js (React)
- **WhatsApp:** Twilio WhatsApp Sandbox
- **Email:** Brevo (free transactional email API)
- **Web Push:** OneSignal

## Admin Panel

Templates and triggers are managed through Django's built-in admin panel
(used instead of a custom admin UI to fit the project timeline).

- URL: `/admin/`
- Username: `admin`
- Password: `admin123`

From the admin panel you can:
- Add/edit **Triggers** (e.g. `login`, `logout`)
- Add/edit **Templates** per trigger per channel (WhatsApp / Email / Web Push)
- Toggle a template's `is_active` flag on/off directly from the list view

## Triggers Built

- **Login** — fires on simulated login from the demo frontend
- **Logout** — fires on simulated logout from the demo frontend

Each trigger has one template per channel (WhatsApp, Email, Web Push),
each with its own message text.

## How It Works

1. Frontend has "Simulate Login" / "Simulate Logout" buttons.
2. Clicking a button calls `POST /api/fire/<trigger_code>/` with the
   recipient's WhatsApp number, email, and/or OneSignal push subscription ID.
3. Backend looks up all **active** templates for that trigger and sends a
   message on each configured channel.

## Environment Variables

Backend `.env`:

```
# WhatsApp (Twilio Sandbox)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+1XXXXXXXXXX

# Email (Brevo)
BREVO_API_KEY=your_brevo_api_key
BREVO_FROM_EMAIL=your_verified_sender_email

# Web Push (OneSignal)
ONESIGNAL_APP_ID=your_onesignal_app_id
ONESIGNAL_REST_API_KEY=your_onesignal_rest_api_key
```

Frontend `.env.local`:

```
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000
NEXT_PUBLIC_ONESIGNAL_APP_ID=your_onesignal_app_id
```

## Setup (Local)

**Backend:**
```
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend:**
```
cd frontend
npm install
npm run dev
```

Open `https://notification-system-frontend-kappa.vercel.app/` for the demo site and
`https://notificationsystem-api.onrender.com/admin/` for the admin panel.

## Known Limitations / Notes

- **WhatsApp Cloud API (Meta) sandbox** could not be completed due to a
  persistent email-verification loop on Meta for Developers during
  registration (reproducible across multiple browsers, incognito mode,
  and networks). As a working alternative within the sandbox spirit of
  this assignment, **Twilio's WhatsApp Sandbox** was used instead — same
  integration pattern (a `send_whatsapp()` service function called from
  the shared `notify()` dispatcher), just a different provider.
- Twilio's sandbox requires outbound messages to reference an
  **approved Content Template** rather than arbitrary free text once
  outside a short session window; this is a provider-side policy,
  not a code limitation. The integration pattern (trigger → template →
  channel function) is otherwise identical to what the Meta Graph API
  integration would look like.
- Web Push requires the browser tab to have granted notification
  permission once (via the "Enable Web Push" button on the demo site)
  before a subscription ID is available to send to.

## Live URLs

- Backend (Render): (https://notificationsystem-api.onrender.com/admin/)
- Frontend (Vercel): https://notification-system-frontend-kappa.vercel.app/

## Walkthrough Video

_Link: TBD_
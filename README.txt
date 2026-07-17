ANGEL MANAGER AI VERSION 5 — ONLINE DATABASE EDITION

WHAT IS NEW
- Saves students, fees, attendance, staff, construction and inventory in Supabase.
- Data is available from phone and laptop.
- Falls back to local CSV files when Supabase secrets are not configured.
- Login username/password can be stored securely in Streamlit Secrets.

DEPLOYMENT
1. Upload all files in this folder to your GitHub repository.
2. In Supabase, open SQL Editor and run supabase_setup.sql.
3. In Streamlit: My apps > Angel Manager AI > Settings > Secrets.
4. Add SUPABASE_URL, SUPABASE_ANON_KEY, APP_USERNAME and APP_PASSWORD.
5. Save secrets and reboot the app.

IMPORTANT
- Do not place secret/service-role keys in GitHub.
- Use only the Supabase anon public key in Streamlit Secrets.

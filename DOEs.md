# DOEs.md 🚀

---

# 🌐 Self-Hosting Muse Observatory - Deployment Steps

---

## 🔧 1. System Preparation

* 🔄 Update system packages
* 💪 Install dependencies: `python3`, `python3-pip`, `git`, `postgresql`, `cloudflared` (already installed)

---

## 🔋 2. PostgreSQL Setup

* 🏛 Install PostgreSQL server
* ⏱ Enable & start PostgreSQL systemd service
* 🆓 Create database `muse`
* 🔑 Create role `museuser` with strong password
* 🌟 Grant privileges to `museuser` on `muse` DB
* 🔌 (Optional) Tune PostgreSQL memory (e.g. shared\_buffers, work\_mem)
* 🔄 Set PostgreSQL systemd service resource limits (e.g. `CPUQuota=100%`, `MemoryMax=100G`)

---

## 🕊 3. Application Installation

* 📚 Clone repository `https://github.com/osiom/muse-observatory.git`
* 🏠 Create Python virtual environment (`venv`)
* 📁 Install Python dependencies with `pip install -r requirements.txt`
* 🔐 Create `.env` file with:

  * `DATABASE_URL=postgresql://museuser:<password>@localhost/muse`
  * `TZ=Europe/Berlin`
* 🔒 Secure `.env` file permissions (`chmod 600`)

---

## 🌌 4. Schedule Cron Job for `generate_facts.py`

* ⏰ Create cron job to run `generate_facts.py` every day at midnight
* 🔄 Ensure cron job uses virtualenv & correct working directory
* 🔢 Redirect logs to file for debugging

Example crontab line:

```
0 0 * * * cd /home/youruser/muse-observatory && /home/youruser/muse-observatory/venv/bin/python3 generate_facts.py >> /home/youruser/muse-observatory/facts.log 2>&1
```

---

## 🚀 5. Create App Service with Uvicorn (systemd)

* 🔄 Create systemd service file `/etc/systemd/system/muse-observatory.service`
* 🌐 Run uvicorn with `--workers 3`, `--host 0.0.0.0`, `--port 5000`
* 🌬️ Assign CPU and RAM limits (e.g. `CPUQuota=100%`, `MemoryMax=512M`)
* ⏱ Enable & start the app service

---

## 🌐 6. Cloudflared Tunnel Update

* 🔧 Edit `cloudflared` config file (`config.yml`):

```yaml
ingress:
  - hostname: muse-observatory.xyz
    service: http://localhost:5000
  - service: http_status:404
```

* 🔄 Restart `cloudflared` systemd service

---

## 🔒 7. Final Checks & Hardening

* 👀 Verify all services running: `systemctl status ...`
* 🔍 Check logs via `journalctl -u ...`
* 🤐 Ensure file permissions are correct
* 🔢 Setup database backups regularly

---

# 🍻 Done!

Your Muse Observatory is now self-hosted, secured, and exposed via Cloudflare Tunnel 🚀

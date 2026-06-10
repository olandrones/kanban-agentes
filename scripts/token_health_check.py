#!/usr/bin/env python3
"""Token health check + OpenRouter credit/usage watchdog.

Runs every 6 hours (`0 */6 * * *`):
1. Telegram bot: getMe against the bot's token from .env
2. OpenRouter: GET /api/v1/auth/key — returns credit limit, usage, free credit
3. Writes a JSON report to state/token_report.json that the maintenance agent
   and the sustainability panel can consume
4. Loud alert on stdout if anything is broken

Cron schedule: every 6 hours (`0 */6 * * *`).
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ENV_PATH = Path(r"E:\00 - Hermes System\.env")
FLAG_PATH = Path(r"E:\00 - Hermes System\state\token_revoked.flag")
REPORT_PATH = Path(r"E:\00 - Hermes System\state\token_report.json")
LOG_PREFIX = "[token-health-check]"


def read_env_value(key_pattern):
    """Read a value from .env matching the given pattern (regex)."""
    content = ENV_PATH.read_text(encoding="utf-8")
    m = re.search(r"^" + key_pattern + r"=(.+)$", content, re.MULTILINE)
    return m.group(1).strip() if m else None


def read_telegram_token():
    content = ENV_PATH.read_text(encoding="utf-8")
    m = re.search(
        r"^[A-Z][A-Z0-9_]*=([0-9]{8,12}:[A-Za-z0-9_-]{30,})$", content, re.MULTILINE
    )
    if not m:
        raise SystemExit(f"{LOG_PREFIX} ERROR: no Telegram-shaped token in .env")
    return m.group(1)


def check_telegram(token):
    """Returns dict: {ok, username, id, error}"""
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/getMe",
        headers={"User-Agent": "hermes-token-health-check/1.0"},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        body = json.loads(resp.read().decode())
        if body.get("ok") is True:
            bot = body["result"]
            return {"ok": True, "username": bot.get("username"), "id": bot.get("id")}
        return {"ok": False, "error": f"body.ok=false: {body}"}
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}: {e.read().decode()[:200]}"}
    except urllib.error.URLError as e:
        return {"ok": False, "error": f"URLError: {e.reason}"}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def check_openrouter():
    """Returns dict: {ok, usage_usd, limit_usd, remaining_usd, limit_remaining, is_free_tier, error}

    OpenRouter /api/v1/auth/key returns:
      { "data": { "label": "...", "usage": 12.34, "limit": 50.0, "is_free_tier": false, ... } }
    """
    api_key = read_env_value(r"OPENROUTER_API_KEY")
    if not api_key:
        return {"ok": False, "error": "OPENROUTER_API_KEY not in .env"}
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/auth/key",
        headers={
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "hermes-token-health-check/1.0",
        },
    )
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        body = json.loads(resp.read().decode())
        data = body.get("data", {})
        usage = float(data.get("usage", 0))
        limit = float(data.get("limit", 0)) if data.get("limit") is not None else None
        if limit and limit > 0:
            remaining = max(0, limit - usage)
            pct = (usage / limit) * 100
        else:
            remaining = None
            pct = None
        return {
            "ok": True,
            "usage_usd": round(usage, 4),
            "limit_usd": limit,
            "remaining_usd": round(remaining, 4) if remaining is not None else None,
            "usage_pct": round(pct, 1) if pct is not None else None,
            "is_free_tier": data.get("is_free_tier", False),
            "label": data.get("label", "default"),
        }
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}: {e.read().decode()[:200]}"}
    except urllib.error.URLError as e:
        return {"ok": False, "error": f"URLError: {e.reason}"}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    report = {
        "checked_at": now,
        "telegram": {},
        "openrouter": {},
    }

    # 1. Telegram
    try:
        tg_token = read_telegram_token()
        report["telegram"] = check_telegram(tg_token)
    except SystemExit as e:
        report["telegram"] = {"ok": False, "error": str(e)}
    except Exception as e:
        report["telegram"] = {"ok": False, "error": f"{type(e).__name__}: {e}"}

    if not report["telegram"].get("ok"):
        FLAG_PATH.parent.mkdir(parents=True, exist_ok=True)
        FLAG_PATH.write_text(
            f"{now}\nbody={json.dumps(report['telegram'])}\n", encoding="utf-8"
        )
        print(f"{LOG_PREFIX} REVOKED {now} telegram broken", file=sys.stderr)
    else:
        if FLAG_PATH.exists():
            FLAG_PATH.unlink()
        print(
            f"{LOG_PREFIX} OK telegram bot=@{report['telegram'].get('username')} id={report['telegram'].get('id')}"
        )

    # 2. OpenRouter
    report["openrouter"] = check_openrouter()
    if report["openrouter"].get("ok"):
        or_ = report["openrouter"]
        if or_.get("remaining_usd") is not None and or_["remaining_usd"] < 5:
            print(
                f"🚨 ALERTA: OpenRouter com apenas ${or_['remaining_usd']:.2f} restantes (${or_['usage_usd']:.2f} de ${or_['limit_usd']:.2f})",
                file=sys.stderr,
            )
        print(
            f"{LOG_PREFIX} OK openrouter usage=${or_['usage_usd']:.4f} limit=${or_['limit_usd']} remaining=${or_['remaining_usd']:.4f} ({or_['usage_pct']:.1f}%)"
        )
    else:
        print(
            f"{LOG_PREFIX} WARN openrouter check failed: {report['openrouter'].get('error')}",
            file=sys.stderr,
        )

    # 3. Write consolidated report for maintenance agent + sustainability panel
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{LOG_PREFIX} report written to {REPORT_PATH}")

    # 4. Loud stdout line for cron channel (delivered to Telegram)
    tg_status = "✅" if report["telegram"].get("ok") else "❌"
    or_status = "✅" if report["openrouter"].get("ok") else "⚠️"
    or_line = ""
    if report["openrouter"].get("ok") and report["openrouter"].get("remaining_usd") is not None:
        or_line = f" · OpenRouter: ${report['openrouter']['remaining_usd']:.2f} restantes ({report['openrouter']['usage_pct']:.0f}%)"
    elif not report["openrouter"].get("ok"):
        or_line = f" · OpenRouter check falhou: {report['openrouter'].get('error', '?')[:50]}"

    print(f"🛡 token-check {now} TG:{tg_status}{or_line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

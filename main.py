import hashlib
import os
import random
import re
import secrets
import smtplib
import string
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import get_db, init_db

app = FastAPI(title="IT-Cube Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_pending_otps: dict[str, dict]   = {}
_admin_sessions: dict[str, dict] = {}

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    key  = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260_000)
    return f"{salt}:{key.hex()}"

def verify_password(password: str, stored: str) -> bool:
    try:
        salt, key_hex = stored.split(":")
        key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260_000)
        return key.hex() == key_hex
    except Exception:
        return False

def send_otp_email(to_email: str, code: str) -> None:
    smtp_host = os.environ.get("SMTP_HOST", "")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASS", "")
    smtp_from = os.environ.get("SMTP_FROM", smtp_user)

    if not smtp_host or not smtp_user:
        print(f"\n{'='*50}")
        print(f"[NYX ADMIN] OTP для {to_email}: {code}")
        print(f"(Настройте SMTP в .env для отправки email)")
        print(f"{'='*50}\n")
        return

    msg              = MIMEMultipart("alternative")
    msg["Subject"]   = f"Код входа в NYX Admin: {code}"
    msg["From"]      = smtp_from
    msg["To"]        = to_email

    body = (
        f"Ваш код двухфакторной аутентификации для NYX Admin Panel:\n\n"
        f"    {code}\n\n"
        f"Код действителен 5 минут.\n"
        f"Не передавайте его третьим лицам.\n"
    )
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as srv:
            srv.ehlo()
            srv.starttls()
            srv.login(smtp_user, smtp_pass)
            srv.sendmail(smtp_from, to_email, msg.as_string())
    except Exception as exc:
        print(f"[NYX ADMIN] Ошибка отправки email: {exc}. OTP для {to_email}: {code}")

def require_admin(authorization: str = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Требуется авторизация администратора")
    token   = authorization[7:]
    session = _admin_sessions.get(token)
    if not session or session["expires"] < datetime.utcnow():
        _admin_sessions.pop(token, None)
        raise HTTPException(401, "Сессия истекла — войдите заново")
    return session

class AdminLoginRequest(BaseModel):
    email: str
    password: str

class AdminTOTPVerify(BaseModel):
    pending_token: str
    code: str

class AdminCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    login: str
    password: str

class UserRegister(BaseModel):
    full_name: str
    age: int
    email: str | None = None
    phone: str | None = None
    password: str

class TeamCreate(BaseModel):
    name: str
    event_id: int
    case_id: int
    event_invite_code: str
    user_id: int

class TeamUpdate(BaseModel):
    user_id: int
    name: str | None = None
    case_id: int | None = None

class JoinByCodeRequest(BaseModel):
    team_code: str
    user_id: int

class InviteCodeCreate(BaseModel):
    code: str
    event_id: int

class EventCreate(BaseModel):
    title: str
    slug: str
    description: str | None = None
    location: str = "IT Cube"
    status: str = "planned"        # 'planned' | 'active' | 'inactive'
    start_date: str | None = None  # YYYY-MM-DD, shown for planned events

class CaseCreate(BaseModel):
    event_id: int
    title: str
    description: str | None = None
    limit_teams: int = 8

class NewsCreate(BaseModel):
    text: str

@app.on_event("startup")
def startup():
    init_db()
    _seed_default_admin()

def _seed_default_admin():
    db = get_db()
    if db.execute("SELECT COUNT(*) FROM admins").fetchone()[0] == 0:
        db.execute(
            "INSERT INTO admins (email, password, name) VALUES (?,?,?)",
            ("admin@nyx.local", hash_password("admin123"), "Администратор"),
        )
        db.commit()
        print("\n[NYX] Создан дефолтный администратор: admin@nyx.local / admin123\n")
    db.close()

@app.post("/admin/auth/login")
def admin_login(data: AdminLoginRequest):
    db    = get_db()
    row   = db.execute("SELECT * FROM admins WHERE email = ?", (data.email,)).fetchone()
    db.close()
    if not row or not verify_password(data.password, row["password"]):
        raise HTTPException(401, "Неверный email или пароль")

    code          = str(secrets.randbelow(900_000) + 100_000)
    pending_token = secrets.token_urlsafe(32)
    _pending_otps[pending_token] = {
        "admin_id": row["id"],
        "email":    row["email"],
        "name":     row["name"],
        "code":     code,
        "expires":  datetime.utcnow() + timedelta(minutes=5),
    }
    send_otp_email(data.email, code)
    return {"pending_token": pending_token, "email": data.email}

@app.post("/admin/auth/verify-totp")
def admin_verify_totp(data: AdminTOTPVerify):
    pending = _pending_otps.get(data.pending_token)
    if not pending:
        raise HTTPException(400, "Сессия подтверждения не найдена")
    if pending["expires"] < datetime.utcnow():
        _pending_otps.pop(data.pending_token, None)
        raise HTTPException(400, "Код истёк — запросите новый")
    if pending["code"] != data.code:
        raise HTTPException(400, "Неверный код")

    _pending_otps.pop(data.pending_token, None)

    session_token = secrets.token_urlsafe(48)
    _admin_sessions[session_token] = {
        "admin_id": pending["admin_id"],
        "email":    pending["email"],
        "name":     pending["name"],
        "expires":  datetime.utcnow() + timedelta(hours=8),
    }
    return {"token": session_token, "name": pending["name"], "email": pending["email"]}

@app.post("/admin/auth/resend-totp")
def admin_resend_totp(pending_token: str):
    pending = _pending_otps.get(pending_token)
    if not pending:
        raise HTTPException(400, "Сессия не найдена — войдите заново")
    code             = str(secrets.randbelow(900_000) + 100_000)
    pending["code"]    = code
    pending["expires"] = datetime.utcnow() + timedelta(minutes=5)
    send_otp_email(pending["email"], code)
    return {"message": "Код отправлен повторно"}

@app.get("/admin/auth/me")
def admin_me(session = Depends(require_admin)):
    return {"email": session["email"], "name": session["name"], "admin_id": session["admin_id"]}

@app.get("/admin/auth/admins")
def list_admins(session = Depends(require_admin)):
    db   = get_db()
    rows = db.execute("SELECT id, email, name, created_at FROM admins ORDER BY id").fetchall()
    db.close()
    return [dict(r) for r in rows]

@app.post("/admin/auth/create")
def create_admin_account(data: AdminCreate, session = Depends(require_admin)):
    if len(data.password) < 6:
        raise HTTPException(400, "Пароль должен содержать не менее 6 символов")
    db = get_db()
    try:
        db.execute(
            "INSERT INTO admins (email, password, name) VALUES (?,?,?)",
            (data.email, hash_password(data.password), data.name),
        )
        db.commit()
    except Exception:
        raise HTTPException(400, "Email уже используется")
    finally:
        db.close()
    return {"message": "Администратор создан"}

@app.delete("/admin/auth/admins/{admin_id}")
def delete_admin(admin_id: int, session = Depends(require_admin)):
    if admin_id == session["admin_id"]:
        raise HTTPException(400, "Нельзя удалить собственный аккаунт")
    db = get_db()
    db.execute("DELETE FROM admins WHERE id = ?", (admin_id,))
    db.commit()
    db.close()
    return {"message": "Администратор удалён"}

@app.get("/stats")
def get_stats():
    db = get_db()
    result = {
        "events":  db.execute("SELECT COUNT(*) FROM events WHERE status IN ('planned','active')").fetchone()[0],
        "cases":   db.execute("SELECT COUNT(*) FROM cases").fetchone()[0],
        "teams":   db.execute("SELECT COUNT(*) FROM teams").fetchone()[0],
        "members": db.execute("SELECT COUNT(*) FROM members").fetchone()[0],
    }
    db.close()
    return result

@app.get("/events")
def get_events(all: int = 0):
    db = get_db()
    where = "" if all else "WHERE e.status IN ('planned','active')"
    rows = db.execute(f"""
        SELECT e.*, COUNT(c.id) AS cases_count
        FROM events e
        LEFT JOIN cases c ON c.event_id = e.id
        {where}
        GROUP BY e.id
        ORDER BY e.id DESC
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]

@app.get("/events/{slug}")
def get_event(slug: str):
    db    = get_db()
    event = db.execute("SELECT * FROM events WHERE slug = ?", (slug,)).fetchone()
    if not event:
        raise HTTPException(404, "Мероприятие не найдено")
    cases = db.execute("""
        SELECT c.*, COUNT(t.id) AS registered
        FROM cases c
        LEFT JOIN teams t ON t.case_id = c.id
        WHERE c.event_id = ?
        GROUP BY c.id
    """, (event["id"],)).fetchall()
    db.close()
    return {**dict(event), "cases": [dict(c) for c in cases]}

@app.post("/login")
def login(data: UserLogin):
    db   = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE login = ? AND password = ?", (data.login, data.password)
    ).fetchone()
    db.close()
    if not user:
        raise HTTPException(401, "Неверный логин или пароль")
    result = dict(user)
    del result["password"]
    return result

@app.post("/users/register")
def register_user(data: UserRegister):
    db   = get_db()
    base = re.sub(r"[^a-zа-яёa-z0-9]", "", data.full_name.lower().split()[0])[:8]
    if not base:
        base = "user"
    login_str = base + "_" + "".join(random.choices(string.digits, k=4))
    try:
        db.execute(
            "INSERT INTO users (full_name, age, email, phone, login, password) VALUES (?,?,?,?,?,?)",
            (data.full_name, data.age, data.email, data.phone, login_str, data.password),
        )
        db.commit()
    except Exception:
        raise HTTPException(400, "Пользователь с такими данными уже существует")
    finally:
        db.close()
    return {"login": login_str, "message": "Регистрация прошла успешно!"}

@app.get("/users/{user_id}/teams")
def get_user_teams(user_id: int):
    db = get_db()
    rows = db.execute("""
        SELECT t.id, t.name, t.event_id, t.case_id, t.leader_id, t.team_code, t.created_at,
               e.title AS event_title, e.slug AS event_slug,
               c.title AS case_title, c.description AS case_description,
               (t.leader_id = ?) AS is_leader
        FROM members m
        JOIN teams t ON m.team_id = t.id
        LEFT JOIN events e ON t.event_id = e.id
        LEFT JOIN cases c ON t.case_id = c.id
        WHERE m.user_id = ?
        ORDER BY t.id DESC
    """, (user_id, user_id)).fetchall()

    result = []
    for row in rows:
        team    = dict(row)
        members = db.execute("""
            SELECT u.id, u.full_name, (t.leader_id = u.id) AS is_leader
            FROM members mem
            JOIN users u ON mem.user_id = u.id
            JOIN teams t ON mem.team_id = t.id
            WHERE mem.team_id = ?
        """, (team["id"],)).fetchall()
        team["members"] = [dict(m) for m in members]
        result.append(team)

    db.close()
    return result

def _gen_team_code(db) -> str:
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not db.execute("SELECT id FROM teams WHERE team_code = ?", (code,)).fetchone():
            return code

@app.post("/teams")
def create_team(data: TeamCreate):
    db = get_db()

    if not db.execute("SELECT id FROM users WHERE id = ?", (data.user_id,)).fetchone():
        db.close(); raise HTTPException(404, "Пользователь не найден")

    event = db.execute("SELECT * FROM events WHERE id = ? AND status = 'planned'", (data.event_id,)).fetchone()
    if not event:
        db.close(); raise HTTPException(404, "Мероприятие не найдено или регистрация закрыта")

    case = db.execute(
        "SELECT * FROM cases WHERE id = ? AND event_id = ?", (data.case_id, data.event_id)
    ).fetchone()
    if not case:
        db.close(); raise HTTPException(404, "Кейс не найден или не относится к этому мероприятию")

    if db.execute("SELECT COUNT(*) FROM teams WHERE case_id = ?", (data.case_id,)).fetchone()[0] >= case["limit_teams"]:
        db.close(); raise HTTPException(400, "Лимит мест в этом кейсе исчерпан")

    code = db.execute(
        "SELECT * FROM invite_codes WHERE code = ? AND event_id = ? AND is_used = 0",
        (data.event_invite_code, data.event_id),
    ).fetchone()
    if not code:
        db.close(); raise HTTPException(400, "Неверный или уже использованный код приглашения")

    if db.execute(
        "SELECT t.id FROM teams t JOIN members m ON m.team_id = t.id "
        "WHERE t.event_id = ? AND m.user_id = ?",
        (data.event_id, data.user_id),
    ).fetchone():
        db.close(); raise HTTPException(400, "Вы уже состоите в команде для этого мероприятия")

    team_code = _gen_team_code(db)
    db.execute(
        "INSERT INTO teams (name, event_id, case_id, leader_id, team_code) VALUES (?,?,?,?,?)",
        (data.name, data.event_id, data.case_id, data.user_id, team_code),
    )
    team_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.execute("INSERT INTO members (team_id, user_id) VALUES (?,?)", (team_id, data.user_id))
    db.execute("UPDATE invite_codes SET is_used = 1 WHERE code = ?", (data.event_invite_code,))
    db.commit()
    db.close()
    return {"id": team_id, "team_code": team_code}

@app.get("/teams/{team_id}")
def get_team(team_id: int):
    db   = get_db()
    team = db.execute("""
        SELECT t.*, e.title AS event_title, e.slug AS event_slug,
               c.title AS case_title, c.description AS case_description
        FROM teams t
        LEFT JOIN events e ON t.event_id = e.id
        LEFT JOIN cases c ON t.case_id = c.id
        WHERE t.id = ?
    """, (team_id,)).fetchone()
    if not team:
        db.close(); raise HTTPException(404, "Команда не найдена")
    result  = dict(team)
    members = db.execute("""
        SELECT u.id, u.full_name, (t.leader_id = u.id) AS is_leader
        FROM members m
        JOIN users u ON m.user_id = u.id
        JOIN teams t ON m.team_id = t.id
        WHERE m.team_id = ?
    """, (team_id,)).fetchall()
    result["members"] = [dict(m) for m in members]
    db.close()
    return result

@app.put("/teams/{team_id}")
def update_team(team_id: int, data: TeamUpdate):
    db   = get_db()
    team = db.execute("SELECT * FROM teams WHERE id = ?", (team_id,)).fetchone()
    if not team:
        db.close(); raise HTTPException(404, "Команда не найдена")
    if team["leader_id"] != data.user_id:
        db.close(); raise HTTPException(403, "Только лидер команды может редактировать её")

    new_name = data.name if data.name is not None else team["name"]
    new_case = team["case_id"]

    if data.case_id is not None and data.case_id != team["case_id"]:
        case = db.execute(
            "SELECT * FROM cases WHERE id = ? AND event_id = ?", (data.case_id, team["event_id"])
        ).fetchone()
        if not case:
            db.close(); raise HTTPException(404, "Кейс не найден")
        if db.execute(
            "SELECT COUNT(*) FROM teams WHERE case_id = ? AND id != ?", (data.case_id, team_id)
        ).fetchone()[0] >= case["limit_teams"]:
            db.close(); raise HTTPException(400, "Лимит мест в этом кейсе исчерпан")
        new_case = data.case_id

    db.execute("UPDATE teams SET name=?, case_id=? WHERE id=?", (new_name, new_case, team_id))
    db.commit(); db.close()
    return {"message": "Обновлено"}

@app.delete("/teams/{team_id}")
def delete_team(team_id: int, user_id: int):
    db   = get_db()
    team = db.execute("SELECT * FROM teams WHERE id = ?", (team_id,)).fetchone()
    if not team:
        db.close(); raise HTTPException(404, "Команда не найдена")
    if team["leader_id"] != user_id:
        db.close(); raise HTTPException(403, "Только лидер команды может удалить её")
    db.execute("DELETE FROM teams WHERE id=?", (team_id,))
    db.commit(); db.close()
    return {"message": "Команда удалена"}

@app.post("/teams/join-by-code")
def join_team_by_code(data: JoinByCodeRequest):
    db   = get_db()
    team = db.execute("SELECT * FROM teams WHERE team_code = ?", (data.team_code,)).fetchone()
    if not team:
        db.close(); raise HTTPException(400, "Команда с таким кодом не найдена")
    if not db.execute("SELECT id FROM users WHERE id = ?", (data.user_id,)).fetchone():
        db.close(); raise HTTPException(404, "Пользователь не найден")
    if db.execute(
        "SELECT t.id FROM teams t JOIN members m ON m.team_id = t.id "
        "WHERE t.event_id = ? AND m.user_id = ?",
        (team["event_id"], data.user_id),
    ).fetchone():
        db.close(); raise HTTPException(400, "Вы уже состоите в команде для этого мероприятия")
    try:
        db.execute("INSERT INTO members (team_id, user_id) VALUES (?,?)", (team["id"], data.user_id))
        db.commit()
    except Exception:
        db.close(); raise HTTPException(400, "Вы уже в этой команде")
    db.close()
    return {"message": "Вы вступили в команду", "team_id": team["id"]}

@app.delete("/teams/{team_id}/leave")
def leave_team(team_id: int, user_id: int):
    db   = get_db()
    team = db.execute("SELECT * FROM teams WHERE id = ?", (team_id,)).fetchone()
    if not team:
        db.close(); raise HTTPException(404, "Команда не найдена")
    if team["leader_id"] == user_id:
        db.close(); raise HTTPException(400, "Лидер не может покинуть команду — удалите команду")
    db.execute("DELETE FROM members WHERE team_id=? AND user_id=?", (team_id, user_id))
    db.commit(); db.close()
    return {"message": "Вы покинули команду"}

@app.get("/invite-codes")
def get_invite_codes(event_id: int | None = None):
    db = get_db()
    if event_id:
        rows = db.execute(
            "SELECT ic.*, e.title AS event_title FROM invite_codes ic "
            "LEFT JOIN events e ON ic.event_id = e.id WHERE ic.event_id = ?", (event_id,)
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT ic.*, e.title AS event_title FROM invite_codes ic "
            "LEFT JOIN events e ON ic.event_id = e.id"
        ).fetchall()
    db.close()
    return [dict(r) for r in rows]

@app.post("/invite-codes")
def create_invite_code(data: InviteCodeCreate, session = Depends(require_admin)):
    db = get_db()
    if not db.execute("SELECT id FROM events WHERE id = ?", (data.event_id,)).fetchone():
        db.close(); raise HTTPException(404, "Мероприятие не найдено")
    try:
        db.execute("INSERT INTO invite_codes (code, event_id) VALUES (?,?)", (data.code, data.event_id))
        db.commit()
    except Exception:
        raise HTTPException(400, "Код уже существует")
    finally:
        db.close()
    return {"code": data.code, "event_id": data.event_id, "is_used": 0}

@app.get("/admin/events")
def get_all_events(session = Depends(require_admin)):
    db   = get_db()
    rows = db.execute("""
        SELECT e.*, COUNT(c.id) AS cases_count
        FROM events e LEFT JOIN cases c ON c.event_id = e.id
        GROUP BY e.id ORDER BY e.id DESC
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]

@app.post("/events")
def create_event(data: EventCreate, session = Depends(require_admin)):
    db = get_db()
    is_active = 0 if data.status == 'inactive' else 1
    try:
        db.execute(
            "INSERT INTO events (title, description, slug, location, status, start_date, is_active) VALUES (?,?,?,?,?,?,?)",
            (data.title, data.description, data.slug, data.location, data.status, data.start_date, is_active),
        )
        db.commit()
        eid = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    except Exception:
        raise HTTPException(400, "Мероприятие с таким slug уже существует")
    finally:
        db.close()
    return {"id": eid, **data.model_dump()}

@app.put("/events/{event_id}")
def update_event(event_id: int, data: EventCreate, session = Depends(require_admin)):
    db = get_db()
    is_active = 0 if data.status == 'inactive' else 1
    db.execute(
        "UPDATE events SET title=?, slug=?, description=?, location=?, status=?, start_date=?, is_active=? WHERE id=?",
        (data.title, data.slug, data.description, data.location, data.status, data.start_date, is_active, event_id),
    )
    db.commit(); db.close()
    return {"message": "Обновлено"}

@app.delete("/events/{event_id}")
def delete_event(event_id: int, session = Depends(require_admin)):
    db = get_db()
    db.execute("DELETE FROM events WHERE id=?", (event_id,))
    db.commit(); db.close()
    return {"message": "Удалено"}

@app.get("/admin/cases")
def get_all_cases(session = Depends(require_admin)):
    db   = get_db()
    rows = db.execute("""
        SELECT c.*, e.title AS event_title, COUNT(t.id) AS registered
        FROM cases c
        LEFT JOIN events e ON c.event_id = e.id
        LEFT JOIN teams t ON t.case_id = c.id
        GROUP BY c.id
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]

@app.post("/cases")
def create_case(data: CaseCreate, session = Depends(require_admin)):
    db = get_db()
    db.execute(
        "INSERT INTO cases (event_id, title, description, limit_teams) VALUES (?,?,?,?)",
        (data.event_id, data.title, data.description, data.limit_teams),
    )
    db.commit()
    cid = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.close()
    return {"id": cid, **data.model_dump()}

@app.put("/cases/{case_id}")
def update_case(case_id: int, data: CaseCreate, session = Depends(require_admin)):
    db = get_db()
    db.execute(
        "UPDATE cases SET event_id=?, title=?, description=?, limit_teams=? WHERE id=?",
        (data.event_id, data.title, data.description, data.limit_teams, case_id),
    )
    db.commit(); db.close()
    return {"message": "Обновлено"}

@app.delete("/cases/{case_id}")
def delete_case_endpoint(case_id: int, session = Depends(require_admin)):
    db = get_db()
    db.execute("DELETE FROM cases WHERE id=?", (case_id,))
    db.commit(); db.close()
    return {"message": "Удалено"}

@app.get("/admin/teams")
def get_all_teams(session = Depends(require_admin)):
    db   = get_db()
    rows = db.execute("""
        SELECT t.id, t.name, t.team_code, t.created_at,
               u.full_name AS leader_name,
               e.title AS event_title,
               c.title AS case_title,
               COUNT(m.id) AS member_count
        FROM teams t
        LEFT JOIN users u ON t.leader_id = u.id
        LEFT JOIN events e ON t.event_id = e.id
        LEFT JOIN cases c ON t.case_id = c.id
        LEFT JOIN members m ON m.team_id = t.id
        GROUP BY t.id
        ORDER BY t.id DESC
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]

@app.get("/news")
def get_news():
    db   = get_db()
    rows = db.execute("SELECT * FROM news ORDER BY id DESC").fetchall()
    db.close()
    return [dict(r) for r in rows]

@app.post("/news")
def create_news(data: NewsCreate, session = Depends(require_admin)):
    if not data.text.strip():
        raise HTTPException(400, "Текст новости не может быть пустым")
    db = get_db()
    db.execute("INSERT INTO news (text) VALUES (?)", (data.text.strip(),))
    db.commit()
    nid = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    row = db.execute("SELECT * FROM news WHERE id = ?", (nid,)).fetchone()
    db.close()
    return dict(row)

@app.delete("/news/{news_id}")
def delete_news(news_id: int, session = Depends(require_admin)):
    db = get_db()
    db.execute("DELETE FROM news WHERE id = ?", (news_id,))
    db.commit()
    db.close()
    return {"message": "Удалено"}

@app.get("/admin/stats")
def get_admin_stats(session = Depends(require_admin)):
    db        = get_db()
    case_rows = db.execute("""
        SELECT c.id, c.title, c.limit_teams, COUNT(t.id) AS registered
        FROM cases c LEFT JOIN teams t ON t.case_id = c.id
        GROUP BY c.id
    """).fetchall()
    total_teams   = db.execute("SELECT COUNT(*) FROM teams").fetchone()[0]
    total_members = db.execute("SELECT COUNT(*) FROM members").fetchone()[0]
    db.close()
    return {
        "totalCases":   len(case_rows),
        "totalTeams":   total_teams,
        "totalMembers": total_members,
        "cases": [dict(r) for r in case_rows],
    }

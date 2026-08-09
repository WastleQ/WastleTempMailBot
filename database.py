
import aiosqlite
from config import DATABASE_PATH


async def init_db() -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                language TEXT DEFAULT 'ru',
                email TEXT,
                mail_id TEXT,
                mail_token TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                mail_created_at TIMESTAMP
            )
        """)
        async with db.execute("PRAGMA table_info(users)") as cursor:
            columns = [row[1] async for row in cursor]
            if "mail_created_at" not in columns:
                await db.execute("ALTER TABLE users ADD COLUMN mail_created_at TIMESTAMP")
        await db.commit()

async def get_user(user_id: int) -> tuple[str, str | None, str | None, str | None, str | None] | None:
    async with aiosqlite.connect(DATABASE_PATH) as db, db.execute(
        "SELECT language, email, mail_id, mail_token, mail_created_at FROM users WHERE user_id = ?",
        (user_id,)
    ) as cursor:
        return await cursor.fetchone()

async def get_all_active_users() -> list[tuple[int, str, str]]:
    async with aiosqlite.connect(DATABASE_PATH) as db, db.execute(
        "SELECT user_id, language, mail_token FROM users WHERE email IS NOT NULL AND mail_token IS NOT NULL"
    ) as cursor:
        return await cursor.fetchall()

async def set_user_language(user_id: int, language: str) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO users (user_id, language) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET language = excluded.language
            """,
            (user_id, language)
        )
        await db.commit()

async def set_user_mailbox(user_id: int, email: str, mail_id: str, mail_token: str) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO users (user_id, email, mail_id, mail_token, mail_created_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                email = excluded.email,
                mail_id = excluded.mail_id,
                mail_token = excluded.mail_token,
                mail_created_at = CURRENT_TIMESTAMP
            """,
            (user_id, email, mail_id, mail_token)
        )
        await db.commit()

async def clear_user_mailbox(user_id: int) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            UPDATE users SET email = NULL, mail_id = NULL, mail_token = NULL, mail_created_at = NULL WHERE user_id = ?
            """,
            (user_id,)
        )
        await db.commit()

import asyncio
import json
from pathlib import Path

from aiohttp import web
from database import clear_user_mailbox, get_user, set_user_mailbox
from email_parser import clean_html_to_text, extract_links
from mail_api import create_temp_mail, get_message_detail, get_messages

WEBAPP_DIR = Path(__file__).resolve().parent / "webapp"

async def index_handler(request: web.Request) -> web.FileResponse:
    return web.FileResponse(WEBAPP_DIR / "index.html")

async def api_get_user(request: web.Request) -> web.Response:
    user_id = int(request.match_info['user_id'])
    user_data = await get_user(user_id)
    if not user_data or not user_data[1]:
        return web.json_response({"email": None, "createdAt": None})
    return web.json_response({"email": user_data[1], "createdAt": user_data[4]})

async def api_create_mail(request: web.Request) -> web.Response:
    user_id = int(request.match_info['user_id'])
    result = await create_temp_mail()
    if not result:
        return web.json_response({"error": "Failed to create email"}, status=500)
    
    await set_user_mailbox(user_id, result["email"], result["mail_id"], result["token"])
    return web.json_response({"email": result["email"]})

async def api_delete_mail(request: web.Request) -> web.Response:
    user_id = int(request.match_info['user_id'])
    await clear_user_mailbox(user_id)
    return web.json_response({"success": True})

async def api_get_messages(request: web.Request) -> web.Response:
    user_id = int(request.match_info['user_id'])
    user_data = await get_user(user_id)
    if not user_data or not user_data[3]:
        return web.json_response([])

    token = user_data[3]
    messages = await get_messages(token)
    
    enriched_messages = []
    for msg in messages:
        msg_id = msg.get("id")
        detail = await get_message_detail(token, msg_id) if msg_id else None
        html_content = detail.get("html", "") if detail else ""
        text_content = detail.get("text", "") if detail else msg.get("intro", "")
        links = extract_links(str(html_content), str(text_content))
        
        enriched_messages.append({
            "id": msg_id,
            "from": msg.get("from"),
            "subject": msg.get("subject"),
            "intro": msg.get("intro"),
            "body": clean_html_to_text(html_content or text_content),
            "createdAt": msg.get("createdAt"),
            "links": links
        })
        
    return web.json_response(enriched_messages)

async def api_stream_messages(request: web.Request) -> web.StreamResponse:
    user_id = int(request.match_info['user_id'])
    
    response = web.StreamResponse()
    response.content_type = 'text/event-stream'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    
    await response.prepare(request)
    
    last_count = -1
    last_email = "__INIT__"
    try:
        while True:
            user_data = await get_user(user_id)
            current_email = user_data[1] if user_data else None
            token = user_data[3] if user_data else None
            
            messages = await get_messages(token) if token else []
            count = len(messages)
            
            if count != last_count or current_email != last_email:
                last_count = count
                last_email = current_email
                data = json.dumps({"count": last_count, "email": current_email})
                await response.write(f"data: {data}\n\n".encode())
                
            await asyncio.sleep(3)
    except asyncio.CancelledError:
        pass
    except Exception as e:  # noqa: BLE001
        print(f"SSE stream error: {e}")
    
    return response

def setup_webapp_routes(app: web.Application) -> None:
    app.router.add_get('/', index_handler)
    app.router.add_get('/api/user/{user_id}', api_get_user)
    app.router.add_post('/api/create/{user_id}', api_create_mail)
    app.router.add_post('/api/delete/{user_id}', api_delete_mail)
    app.router.add_get('/api/messages/{user_id}', api_get_messages)
    app.router.add_get('/api/stream/{user_id}', api_stream_messages)

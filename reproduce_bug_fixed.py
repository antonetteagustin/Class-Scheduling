import urllib.request
import urllib.parse
import json
import http.cookiejar

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# Login
login_url = "http://127.0.0.1:5000/login"
login_data = urllib.parse.urlencode({
    "username": "admin",
    "password": "admin",
    "role": "admin"
}).encode('utf-8')
opener.open(login_url, login_data)

# Edit Section
edit_url = "http://127.0.0.1:5000/admin/sections/edit/1"
# INCLUDE department this time
edit_data = urllib.parse.urlencode({
    "id": "1",
    "name": "Grapes_Fixed",
    "department": "JHS",
    "grade_level": "7",
    "adviser_id": "",
    "room_id": "",
    "track_select": "",
    "is_section_a": "0"
}).encode('utf-8')

req = urllib.request.Request(edit_url, data=edit_data)
req.add_header('X-Requested-With', 'XMLHttpRequest')

try:
    with opener.open(req) as response:
        print("Status:", response.status)
        print("Body:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("Error Status:", e.code)
    print("Error Body:", e.read().decode('utf-8'))
except Exception as e:
    print("Exception:", e)

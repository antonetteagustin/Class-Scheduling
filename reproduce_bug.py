import requests

url = "http://127.0.0.1:5000/login"
session = requests.Session()
session.post(url, data={"username": "admin", "password": "admin", "role": "admin"})

edit_url = "http://127.0.0.1:5000/admin/sections/edit/1"
data = {
    "id": "1",
    "name": "Grapes",
    "grade_level": "8",
    "adviser_id": "",
    "room_id": "",
    "track_select": "",
    "is_section_a": "0"
}
headers = {'X-Requested-With': 'XMLHttpRequest'}

resp = session.post(edit_url, data=data, headers=headers)
print("Response Status:", resp.status_code)
print("Response JSON:", resp.json())

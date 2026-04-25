import urllib.request
import urllib.parse
import http.cookiejar
import os

def test_word_export():
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

    # Login
    login_url = "http://127.0.0.1:5000/login"
    login_data = urllib.parse.urlencode({"username": "admin", "password": "admin123", "role": "admin"}).encode('utf-8')
    opener.open(login_url, login_data)

    # Test individual export
    # Assuming section ID 1 exists from previous context
    url = "http://127.0.0.1:5000/export_word/section/1"
    try:
        with opener.open(url) as response:
            print(f"Individual Export Status: {response.status}")
            print(f"Content Type: {response.info().get_content_type()}")
            if response.status == 200 and 'docx' in response.info().get('Content-Disposition', ''):
                print("SUCCESS: Individual Word export works.")
    except Exception as e:
        print(f"Individual Export FAILED: {e}")

    # Test bulk export
    url_bulk = "http://127.0.0.1:5000/export_word_bulk/section/All"
    try:
        with opener.open(url_bulk) as response:
            print(f"Bulk Export Status: {response.status}")
            if response.status == 200:
                print("SUCCESS: Bulk Word export works.")
    except Exception as e:
        print(f"Bulk Export FAILED: {e}")

if __name__ == "__main__":
    test_word_export()

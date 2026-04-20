from flask import Flask, jsonify
import requests
import re
import logging

app_flask = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_play_store_version(package_name):
    url = f"https://play.google.com/store/apps/details?id={package_name}&hl=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            raise Exception(f"Play Store returned {resp.status_code}")
        # البحث عن الإصدار الحالي في الصفحة
        match = re.search(r'\[\[\[\"([0-9.]+)\"\]\]', resp.text)
        if match:
            return match.group(1)
        # نمط احتياطي
        match2 = re.search(r'Current Version.+?>([0-9.]+)<', resp.text, re.DOTALL)
        if match2:
            return match2.group(1)
        raise Exception("Version not found in page")
    except Exception as e:
        logger.error(f"Failed to fetch version: {e}")
        # قيمة افتراضية إذا فشل الجلب
        return "1.108.1"

def AuToUpDaTE():
    # نجلب الإصدار من Play Store
    version = get_play_store_version("com.dts.freefireth")
    # طلب الخادم الخارجي
    r = requests.get(
        f'https://bdversion.ggbluefox.com/live/ver.php?version={version}&lang=ar&device=android&channel=android&appstore=googleplay&region=ME&whitelist_version=1.3.0&whitelist_sp_version=1.0.0&device_name=google%20G011A&device_CPU=ARMv7%20VFPv3%20NEON%20VMH&device_GPU=Adreno%20(TM)%20640&device_mem=1993',
        timeout=10
    ).json()
    return r['server_url'], r['latest_release_version'], version

def EnV(n):
    if n < 0: raise ValueError("non-negative only")
    o = []
    while True:
        b = n & 0x7F
        n >>= 7
        o.append(b | 0x80 if n else b)
        if not n: break
    return bytes(o)

def VFi(f, v):
    return EnV((f << 3) | 0) + EnV(v)

def LFi(f, v):
    b = v.encode() if isinstance(v, str) else v
    return EnV((f << 3) | 2) + EnV(len(b)) + b

def TerGeT(d):
    p = bytearray()
    for k, v in d.items():
        f = int(k)
        if isinstance(v, dict):
            p += LFi(f, TerGeT(v))
        elif isinstance(v, int):
            p += VFi(f, v)
        elif isinstance(v, (str, bytes)):
            p += LFi(f, v)
    return bytes(p)

@app_flask.route('/generate')
def generate():
    server_url, latest_release, play_version = AuToUpDaTE()
    
    fields = {
        3: "2025-11-26 01:51:28",
        4: "free fire",
        5: 1,
        7: play_version,
        8: "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)",
        9: "Handheld",
        10: "MTN/Spacetel",
        11: "WIFI",
        12: 1280,
        13: 720,
        14: "240",
        15: "x86-64 SSE3 SSE4.1 SSE4.2 AVX AVX2 | 2400 | 4",
        16: 3942,
        17: "Adreno (TM) 640",
        18: "OpenGL ES 3.2",
        19: "Google|625f716f-91a7-495b-9f16-08fe9d3c6533",
        20: "176.28.139.185",
        21: "ar",
        22: "4306245793de86da425a52caadf21eed",
        23: "4",
        24: "Handheld",
        25: "OnePlus A5010",
        29: "c69ae208fad72738b674b2847b50a3a1dfa25d1a19fae745fc76ac4a0e414c94",
        30: 1,
        41: "MTN/Spacetel",
        42: "WIFI",
        57: "1ac4b80ecf0478a44203bf8fac6120f5",
        60: 46901,
        61: 32794,
        62: 2479,
        63: 900,
        64: 34727,
        65: 46901,
        66: 34727,
        67: 46901,
        70: 4,
        73: 1,
        74: "/data/app/com.dts.freefireth-fpXCSphIV6dKC7jL-WOyRA==/lib/arm",
        76: 1,
        77: "e62ab9354d8fb5fb081db338acb33491|/data/app/com.dts.freefireth-fpXCSphIV6dKC7jL-WOyRA==/base.apk",
        78: 6,
        79: 1,
        81: "32",
        83: "2019119026",
        85: 3,
        86: "OpenGLES2",
        87: 255,
        88: 4,
        92: 16190,
        93: "3rd_party",
        94: "KqsHT8W93GdcG3ZozENfFwVHtm7qq1eRUNaIDNgRobozIBtLOiYCc4Y6zvvpcICxzQF2sOE4cbytwLs4xZbRnpRMpmWRQKmeO5vcs8nQYBhwqH7K",
        95: 111207,
        97: 1,
        98: 1,
        99: "4",
        100: "4",
        102: "\u0013R\u0011FP\u000eY\u0003IQ\u000eF\t\u0000\u0011XC9_\u0000[Q\u000fh[V\na\u0007Wm\u000f\u0003f"
    }
    
    payload = TerGeT(fields)
    
    return jsonify({
        "server_url": server_url,
        "latest_release": latest_release,
        "play_version": play_version,
        "payload_hex": payload.hex(),
        "open_id": fields[22],
        "access_token": fields[29]
    })

@app_flask.route('/')
def home():
    return jsonify({
        "status": "active",
        "usage": "Go to /generate to get payload data"
    })

def handler(event, context):
    return app_flask(event, context)

if __name__ == '__main__':
    app_flask.run(host='0.0.0.0', port=8000)
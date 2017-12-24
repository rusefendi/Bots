from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup

URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'


def draw_text(d, pos, color=(0, 0, 0), text='', size=20):
    fnt = ImageFont.truetype("data/arial.ttf", size)
    d.text(pos, fill=color, text=text, font=fnt)


def get_html(url):
    r = requests.get(url)
    return r.text


def get_image(name):
    url = 'https://coinmarketcap.com/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    image = soup.find('a', text=name).parent.parent.find('img').attrs['src']
    return image


# Здесь, первый параметр это тип картинки, может быть:
# 1 (черно-белый), L (монохромный, оттенки серого),
# RGB, RGBA (RGB с альфа каналом), CMYK, YCbCr, I (32 bit Integer pixels),
# F (32 bit Float pixels).
img = Image.new("RGBA", (320, 160), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

rq = requests.get(URL).json()[0]
_id = rq['id'][0].title() + rq['id'][1:]
print(_id)
price_usd = rq['price_usd']
rank = rq['rank']
symbol = rq['symbol']
market_cap_usd = rq['market_cap_usd']
volume_usd_24h = rq['24h_volume_usd']
percent_change_1h = rq['percent_change_1h']
percent_change_24h = rq['percent_change_24h']
percent_change_7d = rq['percent_change_7d']
img = Image.open(get_image(_id))

draw_text(draw, (10, 0), text=symbol, size=50)
draw_text(draw, (0, 0), text=rank)
draw_text(draw, (200, 18), text=price_usd)
draw_text(draw, (200, 80), text='1H  ' + percent_change_1h + '%')
draw_text(draw, (200, 100), text='24H ' + percent_change_24h + '%')
draw_text(draw, (200, 120), text='7D  ' + percent_change_7d + '%')
draw_text(draw, (100, 50), text='MC  ' + market_cap_usd + '$')
draw_text(draw, (100, 70), text='VOL  ' + market_cap_usd + '$')
draw.bitmap((50, 50), img.bitmap(), fill=None)

del draw
img.save("test.png", "PNG")
print(rq)

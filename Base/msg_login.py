import os
import json
import base64
from lxml import etree

import aiohttp
from PIL import Image

api_key = os.getenv("BD_KEY")
key_secret = os.getenv('BD_SECRET')
user = os.getenv("msg_username")
passwd = os.getenv("msg_password")


def gif2png(image_file: str) -> str:
    png_filename = "tmp.png"
    img = Image.open(image_file)

    def iter_frames(img):
        try:
            i = 0
            while 1:
                img.seek(i)
                imgframe = img.copy()
                if i == 0:
                    palette = imgframe.getpalette()
                else:
                    imgframe.putpalette(palette)
                yield imgframe
                i += 1
        except EOFError:
            pass

    for i, frame in enumerate(iter_frames(img)):
        frame.save(png_filename, **frame.info)
    return png_filename


async def get_code(gif_image: str) -> str:
    verify_code = ""
    _headers = {"Content-Type": "application/x-www-form-urlencoded"}
    png_image = gif2png(gif_image)
    ocr_fmt = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={}"
    token_fmt = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}"
    async with aiohttp.ClientSession() as session:
        async with session.get(token_fmt.format(api_key, key_secret)) as resp:
            if resp.status == 200:
                _resp = await resp.json()
                access_token = _resp.get('access_token', "")
            else:
                print(await resp.json())
                exit(10)
        with open(png_image, 'rb') as f:
            img_resp = f.read()
        img_data = base64.b64encode(img_resp).decode("utf8")
        data = {"image": img_data}
        async with session.post(ocr_fmt.format(access_token), data=data, headers=_headers) as resp:
            if resp.status == 200:
                _json = await resp.json()
                try:
                    verify_code = _json.get("words_result")[0].get("words")
                except Exception:
                    print(_json)
                    exit(10)
    return verify_code


def get_count(html: str) -> float:
    selector = etree.HTML(html)
    matches = selector.xpath("/html/body/div/div/div[1]/div/div[2]/div/div/ul/li[1]/a/p/cite[1]/text()")
    if isinstance(matches, list):
        return float(matches[0])


async def login(username: str, password: str):
    _headers = {"Content-Type": "application/x-www-form-urlencoded"}
    _index_url = "http://web.900112.com"
    _query_url = "{}/welcome.asp".format(_index_url)
    _image_url = "{}/public/safecode.asp".format(_index_url)
    _login_url = "{}/action/CheckLogin.asp".format(_index_url)
    imge_file = "code.gif"
    async with aiohttp.ClientSession() as session:
        async with session.get(_image_url) as img_resp:
            with open(imge_file, 'wb') as f:
                f.write(await img_resp.read())
        verify_code = await get_code(imge_file)
        data = {"loginname": username, "loginpwd": password, "VerifyCode": verify_code}
        async with session.post(_login_url, headers=_headers, data=data) as resp:
            dic_data = json.loads(await resp.text())
            if (resp.status != 200) or (dic_data.get("status", "false") == 'false'):
                # print("Login Failed")
                exit(10)
        async with session.get(_query_url) as resp:
            context = await resp.text()
        surplus = get_count(context)
        print(surplus)


if __name__ == '__main__':
    import asyncio
    asyncio.run(login(user, passwd))


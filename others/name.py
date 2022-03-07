import re
import time
import requests


find_base = "http://xh.5156edu.com/wx/shu.html"


class Result(object):
    def __init__(self, name: str, num: int, sc: str, base: str,  success: str, rj: str):
        self.name = name
        self.score = num
        self.sc = sc
        self.base = base
        self.success = success
        self.rj = rj

    def __repr__(self):
        return f"Result(name={self.name} score={self.score}, 三材={self.sc}, " \
               f"基础={self.base}, 成功={self.success}, 人际={self.rj})"


def get(url: str) -> list:
    words = list()
    reg = re.compile("[^\x00-\xff]")
    resp = requests.get(url)
    html = resp.text.encode("latin1").decode("gbk")
    for line in html.split():
        if not line.startswith("class"):
            continue
        matches = reg.findall(line)
        if len(matches) >= 1:
            words.append(matches[0])
    return words


def score(name: str) -> Result:
    score_num = 0
    results = list()
    url = "https://www.hmz.com/xmcs/程_{}远_男_2021_8_4_14_cm/".format(name)
    resp = requests.get(url)

    for line in resp.text.split():
        if line.startswith("<strong>"):
            newline = line.replace("<strong>", "")
            reg = re.compile(r"\d+")
            result = reg.match(newline)
            if result:
                score_num = int(result.group())
        elif line.endswith("</em>"):
            newline = line.replace("</em>", "").replace('">', " ")
            result = newline.split()[-1]
            results.append(result)
    return Result(name, score_num, results[0], results[1], results[2], results[3])


def main():
    good_names = list()
    for i in range(1, 7):
        if i == 1:
            url = find_base
        else:
            url = "http://xh.5156edu.com/wx/shu_{}.html".format(i)
        for word in get(url):
            name_result = score(word)
            print(word, name_result)
            if name_result.score >= 88 \
                    and name_result.sc != "凶" \
                    and name_result.base != "凶" \
                    and name_result.success != "凶":
                good_names.append(name_result)
            time.sleep(0.5)
        time.sleep(1)
    print("跑完了，查看结果")
    with open("name2.txt", "a") as f:
        for name in good_names:
            f.write(f'{str(name)}\n')


if __name__ == '__main__':
    main()
    # n = score("保")
    # print(str(n))

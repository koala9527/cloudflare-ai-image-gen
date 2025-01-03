from dotenv import load_dotenv
import os
import anthropic
import requests
import time
import json
load_dotenv()

def calude(answer):

    client = anthropic.Anthropic(
        api_key="sk-******************************************"
    )
    message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": answer}
    ]
)
    return message.model_dump_json(indent=2)




def getdown(prompt,fold):
    account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
    api_token = os.environ["CLOUDFLARE_API_TOKEN"]
    model='@cf/stabilityai/stable-diffusion-xl-base-1.0'
    headers = {
        "Authorization": f"Bearer {api_token}",
    }
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"

    response = requests.post(
        url,
        headers=headers,
        json={"prompt": prompt},
    )
    file_path = './images/'+fold+'/'
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    with open(file_path+str(time.time())+".png", "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

def main():
    styles = '卡通中国西游记孙悟空人物'
    style = '给你一下参考的词语：风格提示词：comic,anime artwork,3d model,line art drawing,cinematic photo,photographic,oil painting,illustration'
    quality = '质量提示词：best quality,masterpiece,ultra detailed,4K,8K,UHD,HDR'
    background = '你来充当一位有艺术气息的Stable Diffusion prompt 助理。Stable Diffusion是一款利用深度学习的文生图模型，支持通过使用 prompt 来产生新的图像，描述要包含或省略的元素。'
    command = '我用自然语言告诉你要生成的prompt的主题，你的任务是根据这个主题想象一幅完整的画面，然后转化成一份详细的、高质量的prompt，让Stable Diffusion可以生成高质量的图像。用来描述图像，由普通常见的单词构成,提示词以","分隔的每个单词或词组称为 tag，prompt是由系列由","分隔的tag组成的，下面我将说明 prompt 的生成步骤，这里的 prompt 可用于描述人物、风景、物体或抽象数字艺术图画。你可以根据需要添加合理的、但不少于5处的画面细节,这个非常重要。'


    world_prompt = background+command+style+quality+'现在帮我生成十个提示词prompt，帮我选择一个个别的风格，尽可能高质量的提示词，需要你发挥想象力随机自定义一些场景环境和一点光线的单词，  我现在选一个'+styles+'风格，你开始生成吧,十个提示词一行一个英文段落，不要有其他的内容文字,格式，不要带序号'
    print(world_prompt)
    res = calude(world_prompt)
    # print(res)
    res = json.loads(res)
    res = res['content'][0]['text']
    # print(res)
    for i in res.split('\n'):
        if i.strip()!='':
            print(i)
            getdown(i,'monkey')

main()
# https://hatui.s3.bitiful.net/mini/wallpaper/test/xl/type2/1a4db142a3cdeecef11ed260fb5c5e1e8067cbcfac7ac1728d4b327d.jpg

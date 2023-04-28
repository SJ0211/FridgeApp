import requests
from PIL import Image, ImageDraw, ImageFont

def headlines():
    #api response stuff
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "ca",
        "pageSize": 4,
        "apiKey": "<YOUR API KEY HERE>"
    }

    response = requests.get(url, params=params)
    data = response.json()
    # image with same color as the background. less work :)
    image = Image.new("RGB", (520, 550), color=(195, 195, 195))

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("arial.ttf", size=24)

    # Fitting text in the image
    y = 10
    for i, article in enumerate(data["articles"]):
        lines = []
        words = article["title"].split()
        line = words[0]
        for word in words[1:]:
            if font.getsize(line + " " + word)[0] > 480:
                lines.append(line)
                line = word
            else:
                line += " " + word
        lines.append(line)
        for line in lines:
            draw.text((50, y), line, font=font, fill=(0, 0, 0))
            y += 40
        y += 20

    # save the image as a PNG file
    image.save("headlines.png")

    print("Top 5 headlines saved to headlines.png")

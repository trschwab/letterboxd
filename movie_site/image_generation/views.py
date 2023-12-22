from django.shortcuts import render
# from src.main import main_generate
from src.utils.get_stats import generate_stats_string
from src.src.update_user import update_user, is_valid_username
from src.src.generate_topster import main_generate
import time
import asyncio
from multiprocessing import Process
import logging

def home(request):
    try:
        return render(request, "home.html", {})
    except Exception as e:
        logging.info(e)
        return render(request, f"error.html", {})

def about(request):
    try:
        return render(request, "about.html", {})
    except Exception as e:
        logging.info(e)
        return render(request, f"error.html", {})


def your_stats(request):
    try:
        filename = request.POST['receive_key-stats'].lower()
        logging.info("Stats view calls username: %s", filename)
        stats = generate_stats_string(filename)
        f = open(f'image_generation/templates/your-stats.html', "w") 
        f.write(f'''
    {{% load static %}}

    <link rel="stylesheet" href="{{% static 'css/style.css' %}}">

    <h1>{filename} Stats:</h1>
        <body>
        <div style="width:800px; margin:0 auto;">
        <p>This page is autogenerated</p>
        <br><br>
        <p>{stats}<p>
        </div>
        </body>
                ''')
        f.close()
        return render(request, f"your-stats.html", {})
    except Exception as e:
        logging.info(e)
        return render(request, f"error.html", {})

def your_topster(request):
    try:
        filename = request.POST['receive_key-name'].lower()
        logging.info("Topster view calls username: %s", filename)
        x = main_generate(filename)
        f = open(f'image_generation/templates/your-topster.html', "w") 
        f.write(f'''
    {{% load static %}}

    <link rel="stylesheet" href="{{% static 'css/style.css' %}}">

    <h1>{filename} Topster:</h1>
        <body>
        <div style="width:800px; margin:0 auto;">
        <p>This page and image are autogenerated</p>
        <img src="{{% static './media/{filename}.png' %}}" width="500" height="600">
        </div>
        </body>
                ''')
        f.close()
        return render(request, f"your-topster.html", {})
    except Exception as e:
        logging.info(e)
        return render(request, f"error.html", {})

async def your_update(request):
    try:
        filename = request.POST['receive_key-update'].lower()
        logging.info("Topster view calls username: %s", filename)
        if is_valid_username(filename) == False:
            logging.info("Invalid username %s has been called via update function", filename)
            return render(request, f"error.html", {})
        p = Process(target=update_user, args=(filename,))
        p.start()

        f = open(f'image_generation/templates/your-update.html', "w") 
        f.write(f'''
    {{% load static %}}

    <link rel="stylesheet" href="{{% static 'css/style.css' %}}">

    <h1>Generating Stats for {filename}...</h1>
        <body>
        <div style="width:800px; margin:0 auto;">
        <p>Thank you for submitting your username<br><br>
            We're extracting your information now which may take a few minutes.<br><br>
            Feel free to exit and return in some time to request your topster or stats</p>
            </div>
            </body>
                ''')
        f.close()
        return render(request, f"your-update.html", {})
    except Exception as e:
        logging.info(e)
        return render(request, f"error.html", {})

def error(request):
    return render(request, f"error.html", {})
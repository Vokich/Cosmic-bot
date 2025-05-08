import math
import random
from io import BytesIO
import datetime
import pytz

from PIL import Image, ImageDraw, ImageFont
import telebot
from telebot import types

TOKEN = "8050334935:AAHjnBLdw3NamG21cWMlrBAfgvvOBGMDoPA"
bot = telebot.TeleBot(TOKEN)
SPACE_FACTS = [
    "Солнце составляет 99.86% массы всей Солнечной системы.",
    "Один день на Венере длится дольше, чем один год на Земле.",
    "Космос полностью беззвучен, так как там нет атмосферы для передачи звука.",
    "На Луне есть следы, оставленные астронавтами, которые останутся там миллионы лет.",
    "Международная космическая станция (МКС) вращается вокруг Земли каждые 90 минут.",
    "В галактике Млечный Путь около 100-400 миллиардов звезд.",
    "Самая высокая гора в Солнечной системе - Олимп на Марсе, высотой 21.9 км.",
    "Если два куска одного и того же металла соприкоснутся в космосе, они навсегда соединятся.",
    "Земля - единственное место в Солнечной системе, где вода существует в трех состояниях.",
    "Свет от Солнца достигает Земли за 8 минут и 20 секунд."
]
CONSTELLATIONS = {
    "Орион": [
        (80, 100, "Бетельгейзе", "красный"),
        (180, 50, "Ригель", "голубой"),
        (150, 120, "Беллатрикс", "голубой"),
        (120, 90, "Альнитак", "голубой"),
        (130, 80, "Альнилам", "голубой"),
        (140, 70, "Минтака", "голубой"),
        (100, 110, "Саиф", "голубой")
    ],
    "Большая Медведица": [
        (50, 50, "Дубхе", "оранжевый"),
        (100, 60, "Мерак", "белый"),
        (150, 70, "Фекда", "белый"),
        (200, 80, "Мегрец", "белый"),
        (250, 90, "Алиот", "белый"),
        (300, 100, "Мицар", "белый"),
        (350, 110, "Алькаид", "белый")
    ],
    "Лебедь": [
        (100, 100, "Денеб", "голубой"),
        (150, 150, "Альбирео", "золотой"),
        (120, 120, "Садр", "голубой"),
        (180, 180, "Гиенах", "голубой")
    ]
}
PLANETS = {
    "Меркурий": {"size": 4, "color": "серый", "distance": 30, "speed": 4.1, "moons": 0},
    "Венера": {"size": 9, "color": "жёлтый", "distance": 50, "speed": 1.6, "moons": 0},
    "Земля": {"size": 10, "color": "синий", "distance": 70, "speed": 1, "moons": 1},
    "Марс": {"size": 7, "color": "красный", "distance": 90, "speed": 0.5, "moons": 2},
    "Юпитер": {"size": 20, "color": "оранжевый", "distance": 120, "speed": 0.08, "moons": 79},
    "Сатурн": {"size": 17, "color": "золотой", "distance": 150, "speed": 0.03, "moons": 82},
    "Уран": {"size": 12, "color": "голубой", "distance": 180, "speed": 0.01, "moons": 27},
    "Нептун": {"size": 11, "color": "тёмно-синий", "distance": 210, "speed": 0.006, "moons": 14}
}
user_states = {}

def generate_star_chart(lat: float, lon: float, time: datetime.datetime, width=400, height=400) -> BytesIO:
    """Генерирует звездное небо для заданных координат и времени"""
    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)
    time_factor = (time.hour + time.minute/60) / 24
    lat_factor = abs(lat) / 90
    lon_factor = (lon % 360) / 360
    num_stars = 200
    for _ in range(num_stars):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        star_type = random.random()
        if star_type < 0.7:
            color = (brightness, brightness, brightness)  # белый
        elif star_type < 0.85:
            color = (brightness, brightness//2, brightness//3)  # желтый
        elif star_type < 0.95:
            color = (brightness//3, brightness//3, brightness)  # голубой
        else:
            color = (brightness, brightness//4, brightness//4)  # красный
        
        draw.ellipse([x-size, y-size, x+size, y+size], fill=color)

    for constellation, stars in CONSTELLATIONS.items():
        for star in stars:
            x, y, name, color_name = star
            x = int(x * (0.7 + 0.3 * lon_factor))
            y = int(y * (0.7 + 0.3 * lat_factor))
            
            if color_name == "красный":
                color = (255, 50, 50)
            elif color_name == "голубой":
                color = (50, 50, 255)
            elif color_name == "оранжевый":
                color = (255, 165, 0)
            elif color_name == "золотой":
                color = (255, 215, 0)
            else:
                color = (255, 255, 255)
            
            size = random.randint(2, 4)
            draw.ellipse([x-size, y-size, x+size, y+size], fill=color)

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def generate_planet_system(planet_name: str, width=400, height=400) -> BytesIO:
    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("ARIAL.ttf", 15, encoding="utf-8")
    sun_radius = 30
    draw.ellipse([width//2-sun_radius, height//2-sun_radius, 
                  width//2+sun_radius, height//2+sun_radius], 
                 fill="yellow")
    # орбиты и планеты
    for name, data in PLANETS.items():
        distance = data["distance"]
        radius = data["size"]
        color = data["color"]
        draw.ellipse([width//2-distance, height//2-distance, 
                      width//2+distance, height//2+distance], 
                     outline="gray", width=1)
        # Планета
        now = datetime.datetime.now()
        angle = (now.second + now.microsecond/1000000) * data["speed"] * math.pi / 30
        x = width//2 + distance * math.cos(angle)
        y = height//2 + distance * math.sin(angle)
        planet_color = {
            "gray": (150, 150, 150),
            "yellow": (255, 255, 0),
            "blue": (0, 0, 255),
            "red": (255, 0, 0),
            "orange": (255, 165, 0),
            "gold": (255, 215, 0),
            "lightblue": (173, 216, 230),
            "darkblue": (0, 0, 139)
        }.get(color, (255, 255, 255))
        
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=planet_color)
        if name == planet_name:
            draw.text((x, y-radius-15), name, fill="white", font=font)
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def generate_constellation_image(constellation_name: str, width=400, height=400) -> BytesIO:
    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)
    if constellation_name not in CONSTELLATIONS:
        constellation_name = "Орион"
    stars = CONSTELLATIONS[constellation_name]

    star_coords = []
    for star in stars:
        x, y, name, color_name = star
        x = int(x * width / 400)
        y = int(y * height / 400)
        star_coords.append((x, y, name, color_name))
        
        if color_name == "красный":
            color = (255, 50, 50)
        elif color_name == "голубой":
            color = (50, 50, 255)
        elif color_name == "оранжевый":
            color = (255, 165, 0)
        elif color_name == "золотой":
            color = (255, 215, 0)
        else:
            color = (255, 255, 255)
        
        size = random.randint(3, 5)
        draw.ellipse([x-size, y-size, x+size, y+size], fill=color)

    if constellation_name == "Орион":
        lines = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,0)]
    elif constellation_name == "Большая Медведица":
        lines = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6)]
    else:
        lines = [(0,1), (1,2), (2,3), (3,0)] # Линии для Лебедя
    
    for i, j in lines:
        if i < len(star_coords) and j < len(star_coords):
            x1, y1, _, _ = star_coords[i]
            x2, y2, _, _ = star_coords[j]
            draw.line([x1, y1, x2, y2], fill="white", width=1)

    font = ImageFont.truetype("ARIAL.ttf", 15, encoding="utf-8")
    draw.text((10, 10), constellation_name, fill="white", font=font)
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    welcome_text = f"""
🚀 Добро пожаловать, {user.first_name}, в Cosmic! 🌌

Я - ваш гид по вселенной. Вот что я могу:

🔭 /stars - Показать звездное небо для вашего местоположения
🪐 /planets - Исследовать планеты Солнечной системы
✨ /constellations - Узнать о созвездиях
🌠 /fact - Получить случайный космический факт
🎯 /quiz - Проверить свои знания о космосе

Выберите одну из команд или нажмите на кнопки ниже!
"""
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('🔭 Звездное небо')
    btn2 = types.KeyboardButton('🪐 Планеты')
    btn3 = types.KeyboardButton('✨ Созвездия')
    btn4 = types.KeyboardButton('🌠 Космический факт')
    btn5 = types.KeyboardButton('🎯 Викторина')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['stars'])
def ask_location_for_stars(message):
    user_states[message.chat.id] = "waiting_location_stars"
    bot.send_message(message.chat.id, "📍 Пожалуйста, отправьте ваше местоположение (можно приблизительное) "
                                      "или введите координаты в формате 'широта,долгота' "
                                      "(например: 55.75, 37.62 для Москвы).")

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == "waiting_location_stars")
def process_location_for_stars(message):
    try:
        chat_id = message.chat.id
        if message.location:
            lat = message.location.latitude
            lon = message.location.longitude
        else:
            coords = message.text.split(",")
            lat = float(coords[0].strip())
            lon = float(coords[1].strip())
        
        now = datetime.datetime.now(pytz.utc)
        star_chart = generate_star_chart(lat, lon, now)
        
        bot.send_photo(chat_id, star_chart, caption=f"🌠 Звездное небо для координат: {lat:.2f}, {lon:.2f}\n"
                                                  f"🕒 Время: {now.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        del user_states[chat_id]
    
    except Exception as e:
        bot.reply_to(message, "❌ Не удалось обработать местоположение. Пожалуйста, попробуйте еще раз или "
                              "отправьте ваши координаты в формате 'широта,долгота'.")
        print(f"Error: {e}")


@bot.message_handler(commands=['planets'])
def show_planets_menu(message):
    markup = types.InlineKeyboardMarkup()
    for planet in PLANETS.keys():
        markup.add(types.InlineKeyboardButton(planet, callback_data=f"planet_{planet}"))

    bot.send_message(message.chat.id, "🪐 Выберите планету для изучения:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('planet_'))
def show_planet_info(call):
    planet_name = call.data.split('_')[1]
    planet_data = PLANETS.get(planet_name)

    if planet_data:
        planet_image = generate_planet_system(planet_name)
        description = f"""
🪐 *{planet_name}*

• Размер: {planet_data['size']} пикселей (относительно Земли)
• Цвет: {planet_data['color']}
• Расстояние от Солнца: {planet_data['distance']} усл. ед.
• Спутников: {planet_data['moons']}
"""
        description = (description.replace
                       ("(", "\\(").replace(")", "\\)").replace(".", "\\."))
        bot.send_photo(call.message.chat.id, planet_image, caption=description, parse_mode="MarkdownV2")
    else:
        bot.answer_callback_query(call.id, "Планета не найдена")

@bot.message_handler(commands=['constellations'])
def show_constellations_menu(message):
    markup = types.InlineKeyboardMarkup()
    for constellation in CONSTELLATIONS.keys():
        markup.add(types.InlineKeyboardButton(constellation, callback_data=f"constellation_{constellation}"))
    
    bot.send_message(message.chat.id, "✨ Выберите созвездие для изучения:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('constellation_'))
def show_constellation_info(call):
    constellation_name = call.data.split('_')[1]
    stars = CONSTELLATIONS.get(constellation_name)
    
    if stars:
        constellation_image = generate_constellation_image(constellation_name)
        description = f"""
✨ *{constellation_name}*

Количество ярких звезд: {len(stars)}
Главные звезды:
"""
        for star in stars[:3]:
            _, _, name, color = star
            description += f"• {name} ({color})\n"

        description = description.replace("(", "\\(").replace(")", "\\)").replace(".", "\\.")
        bot.send_photo(call.message.chat.id, constellation_image, caption=description, parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, "Созвездие не найдено")

@bot.message_handler(commands=['fact'])
def send_space_fact(message):
    fact = random.choice(SPACE_FACTS)
    bot.send_message(message.chat.id, f"🌌 *Космический факт:*\n\n{fact}", parse_mode="Markdown")

@bot.message_handler(commands=['quiz'])
def start_space_quiz(message):
    questions = [
        {
            "question": "Какая планета самая горячая в Солнечной системе?",
            "options": ["Меркурий", "Венера", "Марс", "Юпитер"],
            "answer": 1
        },
        {
            "question": "Сколько спутников у Марса?",
            "options": ["0", "1", "2", "4"],
            "answer": 2
        },
        {
            "question": "Как называется галактика, в которой находится Земля?",
            "options": ["Андромеда", "Треугольник", "Млечный Путь", "Сомбреро"],
            "answer": 2
        }
    ]
    
    user_states[message.chat.id] = {
        "quiz": True,
        "questions": questions,
        "current_question": 0,
        "score": 0
    }
    
    ask_quiz_question(message.chat.id)

def ask_quiz_question(chat_id):
    user_state = user_states.get(chat_id)
    if not user_state or not user_state.get("quiz"):
        return
    
    current = user_state["current_question"]
    questions = user_state["questions"]
    
    if current >= len(questions):
        score = user_state["score"]
        total = len(questions)
        bot.send_message(chat_id, f"🎯 Викторина завершена! Ваш результат: {score}/{total}")
        del user_states[chat_id]
        return
    
    question_data = questions[current]
    markup = types.InlineKeyboardMarkup()
    for i, option in enumerate(question_data["options"]):
        markup.add(types.InlineKeyboardButton(option, callback_data=f"quiz_{current}_{i}"))
    
    bot.send_message(chat_id, f"❓ Вопрос {current+1}/{len(questions)}:\n\n{question_data['question']}", 
                    reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('quiz_'))
def handle_quiz_answer(call):
    try:
        _, q_index, a_index = call.data.split('_')
        q_index = int(q_index)
        a_index = int(a_index)
        
        chat_id = call.message.chat.id
        user_state = user_states.get(chat_id)
        
        if not user_state or not user_state.get("quiz"):
            bot.answer_callback_query(call.id, "Викторина не активна")
            return
        
        question = user_state["questions"][q_index]
        if a_index == question["answer"]:
            user_state["score"] += 1
            bot.answer_callback_query(call.id, "✅ Правильно!")
        else:
            correct_answer = question["options"][question["answer"]]
            bot.answer_callback_query(call.id, f"❌ Неверно! Правильный ответ: {correct_answer}")

        user_state["current_question"] += 1
        ask_quiz_question(chat_id)
    
    except Exception as e:
        print(f"Error handling quiz answer: {e}")
        bot.answer_callback_query(call.id, "Произошла ошибка")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text.lower()
    
    if text in ['🔭 звездное небо', 'звездное небо', 'звезды']:
        ask_location_for_stars(message)
    elif text in ['🪐 планеты', 'планеты']:
        show_planets_menu(message)
    elif text in ['✨ созвездия', 'созвездия']:
        show_constellations_menu(message)
    elif text in ['🌠 космический факт', 'факт']:
        send_space_fact(message)
    elif text in ['🎯 викторина', 'викторина']:
        start_space_quiz(message)
    else:
        bot.reply_to(message, "🚀 Я не понял ваш запрос. Пожалуйста, используйте кнопки меню или команды.")

if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()
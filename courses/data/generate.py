#!/usr/bin/env python3
"""Генерирует наборы данных курсов (courses/data/*.csv). Данные вымышленные, созданы этим скриптом.

    .venv/bin/python courses/data/generate.py

Seed фиксирован: повторный запуск даёт те же файлы. Файлы хранятся в репозитории — уроки и их сохранённый
вывод зависят от них, поэтому перегенерировать стоит только вместе с проверкой курсов (--update).
Лицензия данных — CC0 1.0 (см. README.md рядом).
"""

from __future__ import annotations

import csv
import datetime as dt
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
YEAR_DAYS = [dt.date(2025, 1, 1) + dt.timedelta(days=i) for i in range(365)]


def write(name: str, header: list[str], rows: list[list]) -> None:
    with open(HERE / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    size = (HERE / name).stat().st_size
    print(f"{name}: {len(rows)} строк, {size / 1024:.0f} КБ")


# ─── Магазин «Кофейная лавка» ───────────────────────────────────────────────
# Нормализованные таблицы (products, customers, orders) и их соединение shop_orders — одни и те же покупки.

PRODUCTS = [
    # id, название, категория, цена, себестоимость
    ("P01", "Эспрессо-смесь 1 кг", "Кофе", 1450, 870),
    ("P02", "Колумбия 250 г", "Кофе", 690, 380),
    ("P03", "Эфиопия 250 г", "Кофе", 790, 430),
    ("P04", "Бразилия 1 кг", "Кофе", 1290, 780),
    ("P05", "Кофе без кофеина 250 г", "Кофе", 720, 410),
    ("P06", "Чёрный чай 100 г", "Чай", 350, 150),
    ("P07", "Зелёный чай 100 г", "Чай", 390, 170),
    ("P08", "Улун 100 г", "Чай", 540, 260),
    ("P09", "Травяной сбор 50 г", "Чай", 260, 100),
    ("P10", "Шоколад горький", "Сладости", 180, 90),
    ("P11", "Печенье овсяное", "Сладости", 150, 70),
    ("P12", "Миндаль в шоколаде", "Сладости", 320, 170),
    ("P13", "Зефир", "Сладости", 210, 100),
    ("P14", "Кружка 350 мл", "Посуда", 590, 250),
    ("P15", "Френч-пресс", "Посуда", 1890, 950),
    ("P16", "Турка медная", "Посуда", 2400, 1300),
    ("P17", "Чайник заварочный", "Посуда", 1350, 640),
    ("P18", "Кофемолка ручная", "Аксессуары", 3200, 1900),
    ("P19", "Фильтры бумажные", "Аксессуары", 240, 90),
    ("P20", "Термокружка", "Аксессуары", 1150, 560),
]
CITIES = ["Москва", "Санкт-Петербург", "Казань", "Новосибирск", "Екатеринбург"]
CITY_P = [0.38, 0.24, 0.14, 0.12, 0.12]
CHANNELS = ["сайт", "приложение", "маркетплейс"]
CHANNEL_P = [0.45, 0.30, 0.25]
FIRST = ["Анна", "Иван", "Мария", "Олег", "Елена", "Дмитрий", "Ольга", "Сергей", "Наталья", "Павел",
         "Ирина", "Алексей", "Татьяна", "Максим", "Юлия", "Андрей", "Светлана", "Никита", "Ксения", "Роман"]
LAST = "АБВГДЕЖЗИКЛМНОПРСТУФХЧШЭЮЯ"


def shop(rng: np.random.Generator) -> None:
    n_customers = 240
    customers = []
    for i in range(n_customers):
        city = CITIES[rng.choice(len(CITIES), p=CITY_P)]
        signup = dt.date(2023, 1, 1) + dt.timedelta(days=int(rng.integers(0, 900)))
        name = f"{FIRST[rng.integers(len(FIRST))]} {LAST[rng.integers(len(LAST))]}."
        segment = rng.choice(["новый", "постоянный", "оптовый"], p=[0.45, 0.45, 0.10])
        customers.append([f"C{i + 1:03d}", name, city, signup.isoformat(), str(segment)])
    write("customers.csv", ["customer_id", "name", "city", "signup_date", "segment"], customers)
    write("products.csv", ["product_id", "name", "category", "price", "cost"], [list(p) for p in PRODUCTS])

    # спрос по категориям меняется по сезону: чай — зимой, сладости — в декабре, посуда — к праздникам
    category_weight = {"Кофе": 5.0, "Чай": 2.4, "Сладости": 2.0, "Посуда": 1.0, "Аксессуары": 0.9}
    orders, joined = [], []
    order_id = 10000
    by_id = {c[0]: c for c in customers}
    activity = rng.gamma(1.2, 1.0, n_customers)
    activity /= activity.sum()
    for day in YEAR_DAYS:
        month = day.month
        weekend = day.weekday() >= 5
        n = rng.poisson(4.0 * (1.25 if weekend else 1.0) * (1.6 if month == 12 else 1.0) * (0.8 if month in (7, 8) else 1.0))
        for _ in range(n):
            order_id += 1
            cust = customers[rng.choice(n_customers, p=activity)]
            channel = CHANNELS[rng.choice(3, p=CHANNEL_P)]
            weights = []
            for p in PRODUCTS:
                w = category_weight[p[2]]
                if p[2] == "Чай" and month in (1, 2, 11, 12):
                    w *= 1.8
                if p[2] == "Сладости" and month == 12:
                    w *= 2.2
                if p[2] == "Посуда" and month in (3, 12):
                    w *= 1.8
                weights.append(w / (1 + p[3] / 2500))
            weights = np.array(weights) / sum(weights)
            for k in rng.choice(len(PRODUCTS), size=1 + rng.binomial(2, 0.3), replace=False, p=weights):
                p = PRODUCTS[k]
                qty = 1 + int(rng.poisson(0.35 if p[3] > 1000 else 1.0))
                if cust[4] == "оптовый" and p[2] in ("Кофе", "Чай"):
                    qty += int(rng.integers(2, 6))
                orders.append([order_id, day.isoformat(), cust[0], p[0], qty, channel])
                joined.append([order_id, day.isoformat(), cust[0], by_id[cust[0]][2], channel, p[2], p[1], p[3], qty])
    write("orders.csv", ["order_id", "date", "customer_id", "product_id", "quantity", "channel"], orders)
    write("shop_orders.csv", ["order_id", "date", "customer_id", "city", "channel", "category", "product", "price", "quantity"], joined)


# ─── Погода ─────────────────────────────────────────────────────────────────

WEATHER = {
    # город: средняя температура года, размах сезона, осадки в дождливый день, вероятность осадков
    "Москва": (6.5, 13.5, 4.0, 0.45),
    "Санкт-Петербург": (6.0, 12.0, 4.2, 0.52),
    "Казань": (5.5, 15.0, 3.8, 0.42),
    "Новосибирск": (2.0, 19.0, 3.2, 0.38),
    "Сочи": (15.0, 8.5, 7.5, 0.35),
}


def weather(rng: np.random.Generator) -> None:
    rows, moscow = [], []
    for city, (mean, amp, rain, p_rain) in WEATHER.items():
        noise = 0.0
        for i, day in enumerate(YEAR_DAYS):
            noise = 0.7 * noise + rng.normal(0, 2.2)  # погода «помнит» вчерашний день
            avg = mean - amp * np.cos(2 * np.pi * (i - 15) / 365) + noise
            spread = 4 + 3 * rng.random()
            tmin, tmax = round(avg - spread / 2, 1), round(avg + spread / 2, 1)
            precip = round(float(rng.exponential(rain)), 1) if rng.random() < p_rain else 0.0
            wind = round(float(np.clip(rng.gamma(3.0, 1.3), 0.5, 18)), 1)
            row = [day.isoformat(), city, tmin, tmax, precip, wind]
            if city == "Москва":
                moscow.append([i + 1, tmin, tmax, precip])  # без пропусков: первые уроки NumPy ещё не знают NaN
            if rng.random() < 0.012:  # датчик иногда не передаёт данные
                row[rng.integers(2, 6)] = ""
            rows.append(row)
    write("weather.csv", ["date", "city", "temp_min", "temp_max", "precip_mm", "wind_ms"], rows)
    write("moscow_2025.csv", ["day", "temp_min", "temp_max", "precip_mm"], moscow)


# ─── Оценки студентов ───────────────────────────────────────────────────────

SUBJECTS = ["Математика", "Физика", "Программирование", "История", "Английский"]


def grades(rng: np.random.Generator) -> None:
    rows, wide = [], []
    groups = ["ИТ-21", "ИТ-22", "ИТ-23"]
    for i in range(30):
        student = f"{FIRST[i % len(FIRST)]} {LAST[(i * 7) % len(LAST)]}."
        group = groups[i // 10]
        talent = rng.normal(0, 9)
        scores = []
        for s, subject in enumerate(SUBJECTS):
            bias = rng.normal(0, 7) + (4 if group == "ИТ-22" and s == 2 else 0)
            for term in (1, 2):
                score = int(np.clip(round(68 + talent + bias + rng.normal(0, 6) + (2 if term == 2 else 0)), 20, 100))
                rows.append([student, group, subject, term, score])
                if term == 1:
                    scores.append(score)
        wide.append([f"S{i + 1:02d}", *scores])
    write("grades.csv", ["student", "group", "subject", "term", "score"], rows)
    write("scores.csv", ["student_id", *["math", "physics", "programming", "history", "english"]], wide)


# ─── Метеостанции (NumPy, модуль 8) ─────────────────────────────────────────

STATIONS = {
    # файл: поправка к температуре, поправка к влажности, какие дни датчик температуры молчал подряд
    "station_center.csv": (1.6, -6, []),
    "station_airport.csv": (0.0, 0, [11, 12, 13]),
    "station_forest.csv": (-1.4, 5, []),
}


def stations(rng: np.random.Generator) -> None:
    """Три станции за февраль 2025 года (28 дней): числа с пропусками — пустыми полями."""
    base = -6.0 + np.cumsum(rng.normal(0, 1.6, 28)) * 0.8 + np.linspace(0, 4, 28)
    humid = 82 + rng.normal(0, 4, 28)
    temps_missing = np.zeros((3, 28), dtype=bool)
    for s, (name, (dt_, dh, outage)) in enumerate(STATIONS.items()):
        rows = []
        for d in range(28):
            temp = round(float(base[d] + dt_ + rng.normal(0, 0.6)), 1)
            hum = int(np.clip(round(humid[d] + dh + rng.normal(0, 3)), 40, 100))
            wind = round(float(np.clip(rng.gamma(2.5, 1.2) + (1.5 if s == 1 else 0), 0.3, 15)), 1)
            row = [d + 1, temp, hum, wind]
            gap_temp = d + 1 in outage or (rng.random() < 0.06 and not temps_missing[:, d].any())
            if gap_temp:
                row[1] = ""
                temps_missing[s, d] = True
            elif rng.random() < 0.05:
                row[rng.integers(2, 4)] = ""
            rows.append(row)
        write(name, ["day", "temp", "humidity", "wind"], rows)


if __name__ == "__main__":
    shop(np.random.default_rng(2025))
    weather(np.random.default_rng(7))
    grades(np.random.default_rng(42))
    stations(np.random.default_rng(28))

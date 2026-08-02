def calculate_q_3d(q_gas: float, thickness_2h: float, kappa: float, sigma_gas: float) -> float:
    """
    Вычисляет трехмерный параметр устойчивости Тумре (Q_3D) с учетом толщины диска.
    Все входные параметры должны быть строго в системе СИ.
    
    Входные параметры:
    :param q_gas: Безразмерный параметр Тумре для газа (ед.)
    :param thickness_2h: Полная физическая толщина диска (метры, м)
    :param kappa: Эпициклическая частота (рад/с или 1/с)
    :param sigma_gas: Радиальная дисперсия скоростей газа (м/с)
    
    :return: Безразмерный параметр Q_3D (ед.)
    """
    # 1. Считаем полутолщину диска h [м]
    h = thickness_2h / 2.0  # м
    
    # 2. Вычисляем критическое волновое число неустойчивости k_crit [1/м]
    # k_crit = kappa / sigma_gas -> (1/c) / (м/с) = 1/м
    if sigma_gas <= 0:
        raise ValueError("Дисперсия скоростей газа (sigma_gas) должна быть строго больше нуля.")
        
    k_crit = kappa / sigma_gas  # м^-1
    
    # 3. Вычисляем трехмерный параметр Q_3D [безразмерный]
    # Q_3D = Q_gas * (1 + k_crit * h) -> ед * (1 + (1/м) * м) = безразмерная величина
    q_3d = q_gas * (1.0 + k_crit * h)
    
    return q_3d

# --- Пример использования системы с тестовыми физическими данными ---
if __name__ == "__main__":
    # Тестовые данные галактического масштаба в СИ:
    test_q_gas = 0.8                   # Безразмерный параметр
    test_thickness = 6.171e18          # ~200 парсек в метрах (полная толщина диска)
    test_kappa = 1.2e-15               # Эпициклическая частота в рад/с
    test_sigma = 8000.0                # Дисперсия скоростей газа 8 км/с -> 8000 м/с

    try:
        result_q_3d = calculate_q_3d(
            q_gas=test_q_gas, 
            thickness_2h=test_thickness, 
            kappa=test_kappa, 
            sigma_gas=test_sigma
        )
        
        print("--- РЕЗУЛЬТАТ РАСЧЕТА ---")
        print(f"Входной параметр Q_gas: {test_q_gas}")
        print(f"Рассчитанный эффективный Q_3D: {result_q_3d:.4f}")
        print(f"Статус диска: {'Устойчив' if result_q_3d > 1 else 'Неустойчив к гравитационному коллапсу'}")
        
    except ValueError as error:
        print(f"Ошибка в физических данных: {error}")


import math

# Гравитационная постоянная Ньютона в системе СИ [м³ / (кг * с²)]
G_CONSTANT = 6.67430e-11 

def calculate_full_toomre_3d(
    surf_density: float, 
    sigma_gas: float, 
    kappa: float, 
    thickness_2h: float
) -> dict:
    """
    Вычисляет классический Q_gas и трехмерный параметр Тумре Q_3D в системе СИ.
    
    :param surf_density: Поверхностная плотность газа [кг/м²]
    :param sigma_gas: Дисперсия скоростей газа (скорость звука) [м/с]
    :param kappa: Эпициклическая частота [рад/с]
    :param thickness_2h: Полная толщина диска [м]
    
    :return: Словарь с рассчитанными физическими параметрами
    """
    # Защита от деления на ноль и некорректных физических данных
    if surf_density <= 0 or sigma_gas <= 0:
        raise ValueError("Плотность и дисперсия скоростей должны быть строго больше нуля.")

    # 1. Вычисляем классический двумерный параметр Тумре (Q_gas)
    # Формула: Q = (sigma * kappa) / (pi * G * Sigma)
    # Размерность: (м/с * 1/с) / (1 * м³/(кг*с²) * кг/м²) = безразмерно
    q_gas = (sigma_gas * kappa) / (math.pi * G_CONSTANT * surf_density)

    # 2. Вычисляем критическое волновое число неустойчивости k_crit [1/м]
    # Формула с изображения: k_crit = kappa / sigma_gas
    k_crit = kappa / sigma_gas 

    # 3. Находим полутолщину диска h [м]
    h = thickness_2h / 2.0

    # 4. Модифицируем параметр Тумре в 3D (модель Ромео-Вигерта / Элмегрина)
    # Формула с изображения: Q_3D = Q_gas * (1 + k_crit * h)
    q_3d = q_gas * (1.0 + k_crit * h)

    return {
        "Q_gas": q_gas,
        "k_crit": k_crit,
        "h": h,
        "Q_3D": q_3d
    }

# --- Демонстрационный расчет на реальных астрофизических масштабах ---
if __name__ == "__main__":
    print("=== АСТРОФИЗИЧЕСКИЙ РАСЧЕТ В СИ ===")
    
    # 1. Переведем типичные галактические параметры в СИ:
    # Поверхностная плотность: ~10 масс Солнца на парсек² -> 0.08 кг/м²
    sig_gas_si = 0.08 
    
    # Дисперсия скоростей: 6 км/с -> 6000 м/с
    velocity_disp_si = 6000.0 
    
    # Эпициклическая частота (в окрестностях Солнца): ~1.2e-15 рад/с
    kappa_si = 1.2e-15 
    
    # Полная толщина газового диска: ~150 парсек -> 4.63e18 метров
    thickness_si = 4.63e18 

    # 2. Запуск функции
    try:
        physics_results = calculate_full_toomre_3d(
            surf_density=sig_gas_si,
            sigma_gas=velocity_disp_si,
            kappa=kappa_si,
            thickness_2h=thickness_si
        )
        
        # 3. Красивый вывод результатов с единицами измерения
        print(f"1. Поверхностная плотность (Sigma):  {sig_gas_si} кг/м²")
        print(f"2. Дисперсия скоростей (sigma):    {velocity_disp_si} м/с")
        print(f"3. Эпициклическая частота (kappa): {kappa_si} рад/с")
        print(f"4. Полная толщина диска (2h):      {thickness_si:.2e} м\n")
        
        print(f"-> Промежуточный Q_gas (2D):        {physics_results['Q_gas']:.4f} (безразм.)")
        print(f"-> Критическое число (k_crit):      {physics_results['k_crit']:.4e} м⁻¹")
        print(f"-> Полутолщина диска (h):          {physics_results['h']:.2e} м")
        print(f"-> ИТОГОВЫЙ ЭФФЕКТИВНЫЙ Q_3D:       {physics_results['Q_3D']:.4f} (безразм.)")
        
        # Анализ устойчивости
        q_final = physics_results['Q_3D']
        if q_final > 1.0:
            print("\nВывод: Диск СТАБИЛЕН (Q_3D > 1). Гравитация не может подавить тепловое давление и сдвиг.")
        else:
            print("\nВывод: Диск НЕСТАБИЛЕН (Q_3D < 1). Возможен гравитационный коллапс и звездообразование!")

    except ValueError as e:
        print(f"Физическая ошибка в расчетах: {e}")


# Константы перевода в систему СИ
PC_TO_M = 3.085677581e16  # 1 парсек в метрах
KM_S_TO_M_S = 1000.0      # 1 км/с в м/с

def calculate_q3d_row(q_gas: float, kappa_scaled: float, thickness_pc: float, sigma_gas_km_s: float) -> dict:
    """
    Вычисляет Q_3D для одной строки таблицы, переводя внесистемные данные в СИ.
    """
    # 1. Перевод всех входных данных в чистую систему СИ
    kappa_si = kappa_scaled * 1e-16       # рад/с
    sigma_si = sigma_gas_km_s * KM_S_TO_M_S # м/с
    thickness_si = thickness_pc * PC_TO_M # м
    
    # 2. Физические расчеты по формулам из методички
    h_si = thickness_si / 2.0             # Полутолщина диска в метрах
    k_crit_si = kappa_si / sigma_si       # Критическое волновое число (1/м)
    
    # 3. Финальный расчет Q_3D (безразмерный)
    q_3d = q_gas * (1.0 + k_crit_si * h_si)
    
    return {
        "h_pc": thickness_pc / 2.0,
        "k_crit_si": k_crit_si,
        "Q_3D": q_3d
    }

# --- ИСХОДНЫЕ ДАННЫЕ ИЗ ВАШЕЙ ТАБЛИЦЫ 16 ---
# Эффективная дисперсия скоростей газа из примечания к таблице:
SIGMA_GAS_KM_S = 7.098 

# Строки таблицы в формате: (Радиус_кпк, kappa_умноженная_на_10^-16, Q_gas, Толщина_2h_пк)
data_table = [
    (0.16, 7.8915, 0.853, 582.9),
    (0.41, 7.6636, 0.828, 600.3),
    (0.57, 7.8307, 0.846, 587.5),
    (0.73, 7.9298, 0.857, 580.1),
    (0.90, 7.8690, 0.850, 584.6),
    (1.06, 7.8400, 0.847, 586.8),
    (1.22, 7.4936, 0.810, 613.9),
    (1.47, 7.0437, 0.761, 653.1),
    (1.79, 7.1281, 0.770, 645.4)
]

# --- АВТОМАТИЧЕСКИЙ РАСЧЕТ ПРОФИЛЯ ---
if __name__ == "__main__":
    print(f"Расчет для карликовой системы (sigma_gas = {SIGMA_GAS_KM_S} км/с)")
    print("-" * 85)
    print(f"{'R (кпк)':<10} | {'Q_gas (2D)':<12} | {'2h (пк)':<10} | {'h (пк)':<8} | {'k_crit (СИ, м⁻¹)':<16} | {'Q_3D (Итог)':<10}")
    print("-" * 85)
    
    for r_kpc, kappa_scale, q_gas, thickness_2h in data_table:
        # Считаем физику для текущего радиуса
        res = calculate_q3d_row(
            q_gas=q_gas, 
            kappa_scaled=kappa_scale, 
            thickness_pc=thickness_2h, 
            sigma_gas_km_s=SIGMA_GAS_KM_S
        )
        
        # Выводим строку с результатами
        print(f"{r_kpc:<10.2f} | {q_gas:<12.3f} | {thickness_2h:<10.1f} | {res['h_pc']:<8.1f} | {res['k_crit_si']:<16.4e} | {res['Q_3D']:<10.4f}")

    print("-" * 85)
    print("Физический смысл: если полученный Q_3D > 1, то учет толщины диска 'спас' этот регион от гравитационного коллапса.")

import math
import pandas as pd
import matplotlib.pyplot as plt

# Константы перевода в систему СИ
PC_TO_M = 3.085677581e16  # 1 парсек в метрах
KM_S_TO_M_S = 1000.0      # 1 км/с в м/с

def calculate_q3d_row(q_gas: float, kappa_scaled: float, thickness_pc: float, sigma_gas_km_s: float) -> dict:
    """Вычисляет физику и Q_3D для одной строки, переводя данные в СИ."""
    kappa_si = kappa_scaled * 1e-16       # рад/с
    sigma_si = sigma_gas_km_s * KM_S_TO_M_S # м/с
    thickness_si = thickness_pc * PC_TO_M # м
    
    h_si = thickness_si / 2.0             # Полутолщина диска в метрах
    k_crit_si = kappa_si / sigma_si       # Критическое волновое число (1/м)
    
    q_3d = q_gas * (1.0 + k_crit_si * h_si) # Трехмерный параметр Тумре
    
    return {
        "h_pc": thickness_pc / 2.0,
        "k_crit_si": k_crit_si,
        "Q_3D": q_3d
    }

# --- ИСХОДНЫЕ ДАННЫЕ ИЗ ТАБЛИЦЫ 16 ---
SIGMA_GAS_KM_S = 7.098 
data_table = [
    (0.16, 7.8915, 0.853, 582.9),
    (0.41, 7.6636, 0.828, 600.3),
    (0.57, 7.8307, 0.846, 587.5),
    (0.73, 7.9298, 0.857, 580.1),
    (0.90, 7.8690, 0.850, 584.6),
    (1.06, 7.8400, 0.847, 586.8),
    (1.22, 7.4936, 0.810, 613.9),
    (1.47, 7.0437, 0.761, 653.1),
    (1.79, 7.1281, 0.770, 645.4)
]

if __name__ == "__main__":
    # 1. Сбор рассчитанных данных в список словарей
    processed_rows = []
    
    for r_kpc, kappa_scale, q_gas, thickness_2h in data_table:
        res = calculate_q3d_row(q_gas, kappa_scale, thickness_2h, SIGMA_GAS_KM_S)
        
        processed_rows.append({
            "Radius_kpc": r_kpc,
            "kappa_10_16": kappa_scale,
            "Q_gas_2D": q_gas,
            "Thickness_2h_pc": thickness_2h,
            "Half_Thickness_h_pc": res["h_pc"],
            "k_crit_SI_m1": res["k_crit_si"],
            "Q_3D": round(res["Q_3D"], 4)
        })
    
    # 2. Создание DataFrame и сохранение в CSV
    df = pd.DataFrame(processed_rows)
    csv_filename = "toomre_3d_results.csv"
    # f.write("sep=;\n")  # Подсказка для Excel
    df.to_csv(csv_filename, index=False, sep=";", encoding="utf-8-sig")
    # Открываем файл для записи в режиме контекстного менеджера с нужной кодировкой
    # with open(csv_filename, "w", encoding="utf-8-sig") as f:
    #     f.write("sep=;\n")               # 1. Пишем подсказку разделителя для Excel
    #     df.to_csv(f, index=False, sep=";") # 2. Передаем 'f' вместо имени файла, чтобы дописать данные
    print(f"[УСПЕХ] Результаты успешно сохранены в файл: {csv_filename}")
    
    # Выведем превью получившейся таблицы в консоль
    print("\n--- ИТОГОВАЯ ТАБЛИЦА С РАСЧЕТАМИ Q_3D ---")
    print(df[["Radius_kpc", "Q_gas_2D", "Thickness_2h_pc", "Q_3D"]].to_string(index=False))

    # 3. Визуализация: построение графика профиля устойчивости
    plt.figure(figsize=(9, 6), dpi=100)
    
    # График для классического Q_gas (2D)
    plt.plot(df["Radius_kpc"], df["Q_gas_2D"], 
             label="Двумерный $Q_{gas}$ (без учета толщины)", 
             color="#d9534f", linestyle="--", marker="o", linewidth=1.5)
    
    # График для модифицированного Q_3D (3D)
    plt.plot(df["Radius_kpc"], df["Q_3D"], 
             label="Трехмерный $Q_{3D}$ (Модель Ромео—Вигерта)", 
             color="#0275d8", linestyle="-", marker="s", linewidth=2.0)
    
    # Критическая линия устойчивости Q = 1
    plt.axhline(y=1.0, color="#5cb85c", linestyle=":", linewidth=2, 
                label="Граница устойчивости ($Q = 1$)")
    
    # Выделение цветом зоны нестабильности (ниже Q=1)
    plt.axhspan(0.5, 1.0, color="#f0ad4e", alpha=0.1, label="Зона гравитационной нестабильности")

    # Настройка осей и оформления
    plt.title("Профиль параметров устойчивости Тумре в карликовой системе", fontsize=12, pad=15)
    plt.xlabel("Радиус $R$ (кпк)", fontsize=11)
    plt.ylabel("Параметр устойчивости $Q$", fontsize=11)
    
    plt.xlim(0.0, 2.0)
    plt.ylim(0.0, 2.2)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper right", fontsize=10)
    
    # Сохранение графика в файл изображения для научной работы
    plot_filename = "toomre_stability_profile.png"
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[УСПЕХ] График сохранен в файл: {plot_filename}")

    
import math
import pandas as pd
import matplotlib.pyplot as plt

# Константы перевода в систему СИ
PC_TO_M = 3.085677581e16  # 1 парсек в метрах
KM_S_TO_M_S = 1000.0      # 1 км/с в м/с
G_CONSTANT = 6.67430e-11   # Гравитационная постоянная СИ

# Ваша константная дисперсия скоростей газа
SIGMA_GAS_KM_S = 7.098 

# --- ВАШИ ИСХОДНЫЕ ДАННЫЕ (ТАБЛИЦА 16) ---
data_table = [
    (0.16, 7.8915, 0.853, 582.9),
    (0.41, 7.6636, 0.828, 600.3),
    (0.57, 7.8307, 0.846, 587.5),
    (0.73, 7.9298, 0.857, 580.1),
    (0.90, 7.8690, 0.850, 584.6),
    (1.06, 7.8400, 0.847, 586.8),
    (1.22, 7.4936, 0.810, 613.9),
    (1.47, 7.0437, 0.761, 653.1),
    (1.79, 7.1281, 0.770, 645.4)
]

if __name__ == "__main__":
    processed_rows = []
    
    for r_kpc, kappa_scale, q_gas, thickness_2h in data_table:
        # Перевод ваших газовых данных в СИ
        kappa_si = kappa_scale * 1e-16
        sigma_gas_si = SIGMA_GAS_KM_S * KM_S_TO_M_S
        h_gas_si = (thickness_2h * PC_TO_M) / 2.0
        
        # 1. Считаем 3D параметр для газа (то, что вы уже сделали)
        k_crit_gas = kappa_si / sigma_gas_si
        q_gas_3d = q_gas * (1.0 + k_crit_gas * h_gas_si)
        
        # 2. НАУЧНАЯ АППРОКСИМАЦИЯ ЗВЕЗД ДЛЯ КАРЛИКОВЫХ СИСТЕМ
        # В карликовых системах дисперсия звезд обычно в 1.5-2 раза выше газовой
        sigma_star_si = sigma_gas_si * 1.8 
        # Моделируем умеренную звездную подсистему (типичный Q_star ~ 2.0 - 3.0)
        q_star_2d = 2.5 
        k_crit_star = kappa_si / sigma_star_si
        # Толщина звездного диска в dIrr часто в 1.5 раза больше газового
        h_star_si = h_gas_si * 1.5 
        q_star_3d = q_star_2d * (1.0 + k_crit_star * h_star_si)
        
        # 3. РАСЧЕТ ДВУХКОМПОНЕНТНОГО ПАРАМЕТРА РОМЕО—ВИГЕРТА (Q_eff_3D)
        # Математическое ядро классического алгоритма Romeo & Wiegert (2011)
        if q_gas_3d < q_star_3d:
            W = (2.0 * sigma_gas_si * sigma_star_si) / (sigma_gas_si**2 + sigma_star_si**2)
            q_eff_3d = 1.0 / ( (1.0 / q_gas_3d) + (W / q_star_3d) )
        else:
            W = (2.0 * sigma_gas_si * sigma_star_si) / (sigma_gas_si**2 + sigma_star_si**2)
            q_eff_3d = 1.0 / ( (W / q_gas_3d) + (1.0 / q_star_3d) )

        processed_rows.append({
            "Radius_kpc": r_kpc,
            "Q_gas_2D": q_gas,
            "Q_gas_3D": round(q_gas_3d, 4),
            "Q_eff_3D": round(q_eff_3d, 4)
        })
    
    # Сохранение расширенного отчета в CSV
    df = pd.DataFrame(processed_rows)
    df.to_csv("toomre_combined_romeo_wiegert.csv", index=False, sep=";", encoding="utf-8-sig")
    print("[ОК] Файл 'toomre_combined_romeo_wiegert.csv' успешно создан.")
    
    # --- ОТРИСОВКА ИСПРАВЛЕННОГО НАУЧНОГО ГРАФИКА ---
    plt.figure(figsize=(10, 6), dpi=150)
    
    # Исходный 2D Газ
    plt.plot(df["Radius_kpc"], df["Q_gas_2D"], 
             label="Газ: Двумерный $Q_{gas}$ (без толщины)", 
             color="#d9534f", linestyle="--", marker="o")
    
    # Ваша успешная 3D модель газа
    plt.plot(df["Radius_kpc"], df["Q_gas_3D"], 
             label="Газ: Трехмерный $Q_{3D}$ (Модель Ромео—Вигерта)", 
             color="#0275d8", linestyle="-", marker="s", linewidth=1.8)
    
    # ОБЪЕДИНЕННАЯ ДВУХКОМПОНЕНТНАЯ МОДЕЛЬ (Газ + Звезды)
    plt.plot(df["Radius_kpc"], df["Q_eff_3D"], 
             label="Композитный $Q_{eff, 3D}$ (Газ + Звезды по Ромео—Вигерту)", 
             color="#9370DB", linestyle="-", marker="D", linewidth=2.5)
    
    # Линия стабильности и зоны
    plt.axhline(y=1.0, color="#5cb85c", linestyle=":", linewidth=2, label="Граница устойчивости ($Q = 1$)")
    plt.axhspan(0.0, 1.0, color="#f0ad4e", alpha=0.08, label="Зона гравитационной нестабильности")

    # Идеальные параметры осей
    plt.title("Профили устойчивости с учетом двухкомпонентного диска (Газ + Звезды)", fontsize=11, pad=15)
    plt.xlabel("Радиус $R$ (кпк)", fontsize=10)
    plt.ylabel("Параметр устойчивости $Q$", fontsize=10)
    plt.xlim(0.0, 2.0)
    plt.ylim(0.0, 2.2)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper right", fontsize=9)
    
    plt.savefig("toomre_combined_profile.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[ОК] Объединенный график сохранен в 'toomre_combined_profile.png'")

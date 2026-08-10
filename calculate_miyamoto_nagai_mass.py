import numpy as np

def calculate_miyamoto_nagai_mass(v_table, r_kpc, current_inc_deg, target_inc_deg, a_kpc, b_kpc):
    """
    Проверка массы удержания в 3D потенциале Миямото-Нагаи с учетом угла наклона диска.
    
    Параметры:
    v_table         : Скорость из каталога SPARC (км/с)
    r_kpc           : Радиус, на котором проверяем скорость (кпк)
    current_inc_deg : Угол наклона диска в каталоге SPARC (65.0 градусов)
    target_inc_deg  : Ваш новый пересчитанный угол наклона (17.0 градусов)
    a_kpc           : Радиальный масштаб диска CamB (из статьи Reff = 0.43 кпк)
    b_kpc           : Вертикальная толщина диска (flaring параметр h)
    """
    # G в астрофизических единицах: (км/с)^2 * кпк / M_sun
    G_astro = 4.30091e-3
    
    # 1. Снимаем проекцию SPARC (65 градусов) и получаем лучевую скорость
    v_los = v_table * np.sin(np.radians(current_inc_deg))
    
    # 2. Проецируем на ваш истинный угол наклона (17 градусов)
    v_rot_true = v_los / np.sin(np.radians(target_inc_deg))
    
    # 3. НАСТОЯЩАЯ ФОРМУЛА МИЯМОТО-НАГАИ:
    # Выражаем M из формулы V^2 = (G * M * R^2) / (R^2 + (a+b)^2)^(3/2)
    numerator = v_rot_true**2 * (r_kpc**2 + (a_kpc + b_kpc)**2)**(1.5)
    denominator = G_astro * r_kpc**2
    
    m_disk_needed = numerator / denominator
    return v_rot_true, m_disk_needed

# =====================================================================
# КРАШ-ТЕСТ НАШИХ ЦИФР ИЗ СТАТЬИ (Экстремальный радиус R = 1.79 кпк)
# =====================================================================
R_edge = 1.79
V_edge = 20.10
R_eff = 0.43  # Эффективный радиус CamB из таблицы 6 вашей статьи

# Проверяем для двух ваших геометрических треков толщины диска из раздела 1.2:
for h_over_r in [0.31, 0.39]:
    b_thick = h_over_r * R_edge # Истинная толщина диска b в кпк
    
    v_rot, m_needed = calculate_miyamoto_nagai_mass(
        v_table=V_edge, 
        r_kpc=R_edge, 
        current_inc_deg=65.0, 
        target_inc_deg=17.0,
        a_kpc=R_eff,
        b_kpc=b_thick
    )
    
    print(f"При h/R = {h_over_r}:")
    print(f"  -> Истинная скорость вращения: {v_rot:.2f} км/с")
    print(f"  -> Требуемая масса диска в 3D: {m_needed:.2e} M_sun")

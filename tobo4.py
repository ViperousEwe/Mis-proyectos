from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Credenciales
usuario = "ARODRIGUEZ"
clave = "ARO5432"

# Iniciar navegador
driver = webdriver.Chrome()
driver.maximize_window()

# Ir al login
driver.get("https://appv2.huntertrack.com.do")

# Espera explícita
wait = WebDriverWait(driver, 30)

# Login
wait.until(EC.presence_of_element_located((By.ID, "mat-input-0")))
driver.find_element(By.ID, "mat-input-0").send_keys(usuario)
driver.find_element(By.ID, "mat-input-1").send_keys(clave)

wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//button[contains(., "Iniciar sesión")]'))).click()

# Esperar redirección
wait.until(EC.presence_of_element_located(
    (By.XPATH, '//span[contains(text(), "Último Estado")]')))
time.sleep(2)

# Clic en "Más Administración"
mas_admin = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//span[contains(text(), "Más Administración")]')))
mas_admin.click()
time.sleep(2)

# Esperar vista de administración (FIX del paréntesis aquí 👇)
wait.until(EC.presence_of_element_located(
    (By.XPATH, '//h1[contains(text(), "Administración")]')))

# Clic en tarjeta "Tipo De Dispositivo"
device_type_option = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[contains(text(), "Tipo De Dispositivo")]')))
device_type_option.click()

# Esperar tabla
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.mat-table")))
time.sleep(2)

# Extraer filas
rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

# Mostrar resultados
if not rows:
    print("⚠️ No se encontraron dispositivos en la tabla.")
else:
    print(f"✅ Dispositivos encontrados: {len(rows)}\n")
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) > 2:
            device_id = cols[0].text.strip()
            hardware = cols[1].text.strip()
            name = cols[2].text.strip()
            print(f"ID: {device_id} | Hardware: {hardware} | Name: {name}")

# Cerrar navegador
driver.quit()

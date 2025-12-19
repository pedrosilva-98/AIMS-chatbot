from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options

def get_driver():
    chrome_options = Options()
    
    # --- AS 3 LINHAS OBRIGATÓRIAS PARA A CLOUD ---
    chrome_options.add_argument("--headless")  # Não abre janela visual
    chrome_options.add_argument("--no-sandbox") # Segurança do Linux
    chrome_options.add_argument("--disable-dev-shm-usage") # Evita falta de memória
    # ---------------------------------------------

    # Tenta usar o driver instalado pelo packages.txt
    service = Service(executable_path="/usr/bin/chromedriver")
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        # Plano B: Caso estejas a rodar no teu PC localmente
        driver = webdriver.Chrome(options=chrome_options)
        
    return driver

def scrape_horario(number, password):

    driver = get_driver()

    extracted_data = [] 
    try:

        print("🚀 [Bot] A iniciar browser...")
        driver.get('https://netpa.novaims.unl.pt/netpa/page?stage=difhomestage')
        
        try: WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "notificacoesNetpa_OK-btnEl"))).click()
        except: pass
        try: WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceitar todos')]"))).click()
        except: pass

        print("🔑 [Bot] Login...")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "loginregisterLink"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'utilizador')]"))).send_keys(str(number))
        driver.find_element(By.XPATH, "//input[contains(@placeholder, 'palavra-chave')]").send_keys(str(password))
        
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Entrar')]"))))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "menuItemLink")))
        
        print("📍 [Bot] A abrir Horário...")
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Horário')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        driver.execute_script("arguments[0].click();", link)

        print("⏳ [Bot] A ler grelha...")
        
        table_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "tabhorarionew"))
        )

        html_content = table_element.get_attribute('outerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')

        header_row = soup.find("tr", class_="days")
        days_list = []
        if header_row:
            headers = header_row.find_all("th")
            for h in headers:
                text = h.get_text(strip=True)
                if text and "navegacaohorario" not in str(h):
                    days_list.append(text)
        
        if not days_list:
            days_list = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

        skip_tracker = [0] * len(days_list)

        all_rows = soup.find_all("tr")
        
        for row in all_rows:
            time_cell = row.find("th", class_="time")
            if not time_cell:
                continue 
            
            current_time = time_cell.get_text(strip=True)

            cells = row.find_all("td")
            cell_index = 0

            for day_idx, day_name in enumerate(days_list):

                if skip_tracker[day_idx] > 0:
                    skip_tracker[day_idx] -= 1
                    continue 

                if cell_index < len(cells):
                    cell = cells[cell_index]
                    rowspan = int(cell.get("rowspan", 1))
                    if rowspan > 1:
                        skip_tracker[day_idx] = rowspan - 1
                    cell_text = cell.get_text(" ", strip=True)
                    if cell_text and len(cell_text) > 2:
                        extracted_data.append(f"Dia: {day_name} | Hora: {current_time} | Aula: {cell_text}")
                    
                    cell_index += 1

        print(f"[Bot] Extração concluída. {len(extracted_data)} aulas encontradas.")

    except Exception as e:
        msg = f"Erro: {str(e)}"
        print(msg)
        return [msg]
    
    finally:
        driver.quit()

    if not extracted_data:
        return ["O horário parece estar vazio (nenhuma aula detetada na grelha)."]

    return extracted_data

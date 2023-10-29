from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from os import chdir


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Desativar renderização de imagens
options.add_argument('--disable-logging') 
options.add_argument('--silent')
options.add_argument('--disable-logging')
options.add_argument('--disable-dev-shm-usage')



import chromedriver_autoinstaller
from selenium import webdriver
from time import sleep

chromedriver_autoinstaller.install()  # Isso fará o download do ChromeDriver automaticamente se necessário

robo = webdriver.Chrome()

robo.get('https://www.youtube.com.br')

elementos = robo.find_elements(By.XPATH,'//*[@id="video-title"]')

lista = []
for elemento in elementos:
    lista.append(elemento.text)

pd.DataFrame({'nome': lista}).to_excel('meu_excel.xlsx')



campo_email = robo.find_element(By.XPATH, '//*[@id="email"]')
campo_email.send_keys('gustavo')
campo_email.send_keys(Keys.TAB)

# Mover para o próximo campo e realizar outras ações, se necessário
campo_senha = robo.find_element(By.XPATH, '//*[@id="pass"]')
campo_senha.send_keys('22222')
sleep(0.5)
robo.switch_to.active_element.send_keys(Keys.TAB)
sleep(0.5)
robo.switch_to.active_element.send_keys(Keys.ENTER)
# wait = WebDriverWait(robo, )

ROOT_DIRECTORY = str(Path(__file__).parent.absolute())
chdir(ROOT_DIRECTORY)
directory_raw = ROOT_DIRECTORY + '/raw' # prod
directory_final = ROOT_DIRECTORY + '/base_final' # prod

if not os.path.exists(directory_raw):
# create folder
    os.makedirs(directory_raw)
else:
    for file in os.listdir(directory_raw):
        # delete all files from the folder
        os.remove('{}/{}'.format(directory_raw,file)) # prod
        # os.remove('{}\\{}'.format(directory_raw,file)) # local

if not os.path.exists(directory_final):
# create folder
    os.makedirs(directory_final)
  

lista = [vendido_por, Detalhes_e_ofertas_especiais,
         preco_do_item, preco_total, link_pagina]

lista_etapa_2 = [vendido_por_2, Detalhes_e_ofertas_especiais_2,
                 preco_do_item_lista_2, preco_total_2, link_pagina_2]

diretorio_atual_parquet = os.getcwd()+'\\arquivos_parquet'
from bs4 import BeautifulSoup

data_salvar = datetime.now().strftime("%d-%m-%Y")
# data_hora_salvar = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
codigo_erro = []

CODIGO = pd.read_excel('produtos.xlsx')['COD'].to_list()


for codigo in CODIGO:
    try:
        print(codigo)
        table_html = []
        link_google = []
        ir_pagina_j = []
        
        robo.get(Website)
        robo.find_element(By.XPATH, pesquisar).clear()
        robo.find_element(By.XPATH, pesquisar).send_keys(CODIGO[0], Keys.ENTER)
        try:
            robo.find_element(By.PARTIAL_LINK_TEXT, 'Comparar').click()
        except:
            sleep(3)
            continue 
        sleep(3)
        try:        
            produto = robo.find_element(By.XPATH, '//*[@id="sg-product__pdp-container"]').text.split('\n')[0].strip()
        except:
            produto = 'Não localizado'
            pass
        sleep(2)
        while True:
            if len(robo.find_elements(By.XPATH, clicar_comparar)) == 1:
                break
            elif len(robo.find_elements(By.XPATH, clicar_comparar_2)) == 1:
                break
            else:
                sleep(3)
            try:            
                table_element  = robo.find_elements(By.XPATH, '//tr[@jscontroller="d5bMlb"]')
                for i in table_element:
                    print(i.get_attribute("outerHTML"))
                    table_html.append(i.get_attribute("outerHTML"))        
            except:
                continue
                    
            try:
                if robo.find_elements(By.LINK_TEXT, 'Acessar o site'):
                    link_google.extend([w.get_attribute('href') for w in robo.find_elements(By.LINK_TEXT, 'Acessar o site')])
                elif robo.find_elements(By.LINK_TEXT, 'Access the website'):
                    link_google.extend([w.get_attribute('href') for w in robo.find_elements(By.LINK_TEXT, 'Access the website')]) 
                else:   
                    pass
            except:
                print("Erro link")
                for i in table_element:
                    link_google.extend("Erro_link")
                    pass
    
            rows = []
            for i in table_html:
                soup = (BeautifulSoup(i, "html.parser"))
                rows.append(soup.find_all("tr"))
            if len(robo.find_elements(By.LINK_TEXT, 'Next')) == 1 or len(robo.find_elements(By.LINK_TEXT, 'Próxima')) == 1:
                try:
                    print("indo para Próxima")
                    robo.find_element(By.LINK_TEXT, 'Próxima').click()
                    sleep(3)
                    continue
                except:
                    print("indo para Next")
                    robo.find_element(By.LINK_TEXT, 'Next').click()
                    sleep(3)
                    continue

            else:
                break

        

        df = pd.DataFrame(rows)


        nome_loja = []
        for i in df[0]:
            tamanho = len('target="_blank">')
            inicio = str(i).find('target="_blank">') + tamanho
            fim = str(i)[inicio:].find('<span')
            total = inicio + fim
            nome_loja.append(str(i)[inicio:total].strip())
            
        parcela_t = []
        valor_parcela = []
        for i in df[0]:
            tamanho = len('</span><div')
            inicio = str(i).find('</span><div') + tamanho
            if inicio <= 12:
                parcela_t.append("Não informado")
            fim = str(i)[inicio:].find("<")
            total = inicio + fim
            parcela_split = str(i)[inicio:total].split(' ')
            parcela_t.append(parcela_split[1].strip())
            if len(parcela_split) < 4:
                valor_parcela.append("Não informado")
            else:
                valor_parcela.append(parcela_split[3].strip())

        parcela = [str(i) for i in parcela_t if 'data-hveid' not in str(i)] 
        parcela = [i.split('>') for i in parcela]
        parcela = [int(i[1]) if len(i) > 1 else int(0) for i in parcela]

        valor_parcela = [str(i) if 'R$' in str(i) else '0' for i in valor_parcela]        
        valor_parcela = [(str(i).replace('R$\xa0','').strip().replace(',', '.')) for i in valor_parcela]
        valor_parcela = [float(p.replace(".", "").replace(",", "."))/100 for p in valor_parcela]

        preco_i = []
        for i in df[1]:
            tamanho = len('R$ ')
            inicio = str(i).find('R$') + tamanho
            fim = str(i)[inicio:].find('<')
            total = inicio + fim
            preco_i.append(str(i)[inicio:total].strip())     

        preco_item=[v.replace(',', '.') for v in preco_i]
        preco_item=[float(p.replace(".", "").replace(",", "."))/100 for p in preco_item]

        cobranca_frete = []
        for i in df[2]:
            tamanho = len('R$ ')
            if 'Ver site' in str(i):
                cobranca_frete.append("Sim, ver no site")
            else:
                cobranca_frete.append("Não")

        preco_t = []
        for i in df[4]:
            tamanho = len('R$ ')
            inicio = str(i).find('R$') + tamanho
            fim = str(i)[inicio:].find('<')
            total = inicio + fim
            preco_t.append(str(i)[inicio:total].strip())   

        preco_total=[v.replace(',', '.') for v in preco_t]
        preco_total=[float(p.replace(".", "").replace(",", "."))/100 for p in preco_total]
            
        preco_total_parcelado = nova_lista = [round(a * b, 2)for a, b in zip(valor_parcela, parcela)]

        len(nome_loja)
        lista_teste = [nome_loja , preco_item, cobranca_frete ,parcela, 
                    valor_parcela, preco_total_parcelado, link_google, preco_total]

        if len(link_google) > len(nome_loja):
            link_google = [i for i in link_google if i != None]


        for i in lista_teste:
            print(len(i))
            
        len_diff = len(nome_loja) - len(link_google)
        link_google.extend([None] * len_diff)
        data={'loja': nome_loja,
            'preco_item': preco_item,
            'tem_frete': cobranca_frete,
            'parcela': parcela,
            'valor_da_parcela': valor_parcela,
            'preco_total_parcelado' : preco_total_parcelado,
            'link_google_direciona': link_google,
            'preco_total': preco_total,
            'data_da_coleta': datetime.now().strftime('%Y-%m-%d'),
            'hora_da_coleta' : datetime.now().strftime('%H:%M:%S')
            }

        len_diff = len(nome_loja) - len(link_google)
        link_google.extend([None] * len_diff)
        
        df_completo = pd.DataFrame(data)
        df_completo['codigo'] = codigo
        df_completo['diferenca_prazo'] = (df_completo['preco_total_parcelado'] / df_completo['preco_item']) - 1
        df_completo['diferenca_prazo'] = df_completo['diferenca_prazo'].apply(lambda x: '{:.2%}'.format(x))
        df_completo['produto'] = produto

        df_completo['ordem_anuncio'] = df_completo.groupby('codigo')['codigo'].rank(method='first')        

        df_completo = df_completo[['data_da_coleta', 'hora_da_coleta', 'codigo', 'loja', 'produto','preco_item', 'tem_frete', 'parcela', 'valor_da_parcela',
            'preco_total_parcelado', 'preco_total', 'diferenca_prazo', 'link_google_direciona', 'ordem_anuncio']]               

        df_completo = df_completo.sort_values(by=['codigo','ordem_anuncio'], ascending=True)    
        df_completo.to_parquet(f'{directory_raw}\\{codigo}-{data_salvar}.parquet')
    except:
        codigo_erro.append(codigo)
        continue

if len(codigo_erro) == 0:
    pass
else:
    lista_erro = pd.DataFrame({'codigo': codigo_erro})    
    lista_erro.to_excel('base_erro.xlsx', index=False)     
               


# Obtém a lista de arquivos parquet no diretório atual e classifica-os pela data de modificação
arquivos = sorted((os.path.join(directory_raw, f) for f in os.listdir(directory_raw) if f.endswith('.parquet')),
                  key=os.path.getmtime)          
dfs = []               
for arquivo in arquivos:
    df = pd.read_parquet(arquivo)
    dfs.append(df)

df_final = pd.concat(dfs, ignore_index=True) 
columns = df_final.columns

df_final.to_excel(f'{directory_final}\\base-{data_salvar}.xlsx', index=False)       
df_final.to_parquet(f'{directory_final}\\base-{data_salvar}.parquet', index=False)            

total = 0
for i in arquivos:
    Dataframe =  pd.read_parquet(i)
    columns = Dataframe.columns
    Rows = dba.Insert_Automatico(columns, 'bi_compara_precos', '',Dataframe)
    total += Rows
    print(Rows)
print(total)
    



# Dataframe = pd.read_parquet(r"C:\Users\guilh\OneDrive\Área de Trabalho\coleta_sku\base_final\base-28-04-2023.parquet")    

# DF_2 = pd.read_excel(r"C:\Users\guilh\OneDrive\Área de Trabalho\EAN.xlsx")
# DF_2 = DF_2.rename(columns = {'COD':'codigo'})
# df.merge(DF_2)


# df_doido = df.merge(DF_2, how='inner', on='codigo')


# df_doido.to_parquet(f'{directory_raw}\\{codigo}-{data_salvar}.parquet')
# df_doido.to_parquet(f'{directory_final}\\base-{data_salvar}.parquet', index=False)    






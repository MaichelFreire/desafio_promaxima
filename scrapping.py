from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from methods_scrapping import methods as mt
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desafio_promaxima.desafio_promaxima.settings')
django.setup()

from desafio_promaxima.desafio_promaxima.models import DataSerch



url = 'https://licitacoes1.caixa.gov.br/sicve-web/public/view/visitante/visitante.jsf#'

chrome_options = webdriver.ChromeOptions()

driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()


# clickando no botao de licitacoes encerradas PE-Pregao Eletronico
mt.waiting_for_element_click(driver, '//*[@id="idEncerradoPECompradorCaixa"]')

# clickando no botao de modalidade - seleciona Pregoes Eletronico
mt.waiting_for_element_click(driver, '//*[@id="tipoModalidade"]/tbody/tr/td[1]/label')

# clickando no botao de Certame - selecionna pregoaos eletronicos
mt.waiting_for_element_click(driver, '//*[@id="tipoCertame"]/tbody/tr/td[1]/label')

# capturando o tamanho da tabela
table = WebDriverWait(driver, 100).until(ec.presence_of_element_located((By.XPATH, '//*[@id="tableVisitante:tb"]')))
rows = table.find_elements(By.TAG_NAME, 'tr')

data = {}

# itera sob a quantidade de linhas da tabela
for row in range(0, len(rows)):

    # usado para aguardar caso a pagina esteja carregando
    WebDriverWait(driver, 100).until(ec.presence_of_element_located((By.XPATH, f'//*[@id="tableVisitante:{row}:linkSituacao"]')))

    # coluna descricao do item
    data['descricao_licitacao'] = mt.transform_element_text(driver, f'//*[@id="tableVisitante:{row}:j_idt153"]/p/span')

    # coluna numero do certame
    data['n_certame'] = mt.transform_element_text(driver, f'//*[@id="tableVisitante:{row}:j_idt139"]')

    # coluna atividade
    data['atividade'] = mt.transform_element_text(driver, f'//*[@id="tableVisitante:{row}:j_idt159"]')

    # coluna modalidade
    data['modalidade'] = mt.transform_element_text(driver, f'//*[@id="tableVisitante:{row}:j_idt135"]')

    # coluna comprador
    data['comprador'] = mt.transform_element_text(driver, f'//*[@id="tableVisitante:{row}:ordenaComprador"]')

    try:
        
        # clica no botao de situacao
        WebDriverWait(driver, 100).until(ec.presence_of_element_located((By.XPATH, rf'//*[@id="tableVisitante:{row}:linkSituacao"]'))).click()
    
    except Exception as e:
        
        continue

    # captura a descrição resumida
    data['descricao'] = mt.transform_element_text(driver, '//*[@id="info_certame"]/tbody/tr[3]/td/table/tbody/tr[1]/td/span')

    # captura a unidade de medida
    data['unidade'] = mt.transform_element_text(driver, '//*[@id="tabLoteItem:0:j_idt391"]/span')

    # captura a quantidade de itens do pedido
    data['quantidade'] = mt.transform_element_text(driver, '//*[@id="info_certame"]/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[5]/td/span')

    # captura o valor estimado
    data['valor'] = mt.transform_element_text(driver, '//*[@id="info_certame"]/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[4]/td/span').replace('.', '').replace(',', '.')
                
    
    data_serch = DataSerch(
    descricao_licitacao = data['descricao_licitacao'],
    n_certame = data['n_certame'],
    atividade = data['atividade'],
    modalidade = data['modalidade'],
    comprador = data['comprador'],
    descricao = data['descricao'],
    unidade = data['unidade'],
    quantidade = data['quantidade'],
    valor = data['valor']
                            )

    # insere os dados no banco
    data_serch.save()

    # volta para a pagina anterior
    WebDriverWait(driver, 100).until(ec.presence_of_element_located((By.XPATH, '//*[@id="idVoltar"]'))).click()
    


print('webscraping finalizado!')



import os
import glob
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Caminho para a pasta contendo os arquivos XML
pasta_xml = 'G:\\QUALIDADE\\Códigos\\Leitura de Faturas Gás\\Códigos\\Gás Local novo modelo\\Faturas'

# Namespace do XML
namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

def extrair_informacoes(xml_root):
    # Extrair e formatar a data de emissão
    data_emissao_iso = xml_root.find('.//nfe:ide/nfe:dhEmi', namespace).text
    data_emissao = datetime.fromisoformat(data_emissao_iso)
    data_emissao_formatada = data_emissao.strftime('%d/%m/%Y')
    
    # Clonar a data de emissão para data_inicio
    data_inicio = data_emissao_formatada
    
    # Calcular o último dia do mês para data_fim
    next_month = data_emissao.replace(day=28) + timedelta(days=4)
    data_fim = (next_month - timedelta(days=next_month.day)).strftime('%d/%m/%Y')
    
    informacoes = {
        'cnpj': xml_root.find('.//nfe:dest/nfe:CNPJ', namespace).text,
        'numero_fatura': xml_root.find('.//nfe:ide/nfe:nNF', namespace).text,
        'valor_total': xml_root.find('.//nfe:total/nfe:ICMSTot/nfe:vNF', namespace).text,
        'volume_total': xml_root.find('.//nfe:det/nfe:prod/nfe:qCom', namespace).text,
        'data_emissao': data_emissao_formatada,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'correcao_pcs': xml_root.find('.//nfe:infAdic/nfe:infCpl', namespace).text.split('Fator de Correcao Poder Calorifico: ')[1].split(' ')[0],
        'icms': xml_root.find('.//nfe:total/nfe:ICMSTot/nfe:vICMS', namespace).text
    }
    return informacoes

# Iterar sobre todos os arquivos XML na pasta
for arquivo_xml in glob.glob(os.path.join(pasta_xml, '*.xml')):
    tree = ET.parse(arquivo_xml)
    root = tree.getroot()
    informacoes = extrair_informacoes(root)
    print(f'Informações do arquivo {arquivo_xml}: {informacoes}')
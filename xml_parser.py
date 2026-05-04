from lxml import etree

# Função universal para leitura de cabeçalho
def cabecalho(caminho):
    ns = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}
    tree = etree.parse(caminho)
    root = tree.getroot()

    # Informações de cabeçalho
    lote = root.find('.//ans:sequencialTransacao', namespaces=ns).text
    data_registro = root.find('.//ans:dataRegistroTransacao', namespaces=ns).text
    hr_registro = root.find('.//ans:horaRegistroTransacao', namespaces=ns).text
    cnpj_origem = root.find('.//ans:origem//ans:CNPJ', namespaces=ns).text
    cnpj_destino= root.find('.//ans:destino//ans:CNPJ', namespaces=ns).text
    
    return lote, data_registro, hr_registro, cnpj_origem, cnpj_destino




# Função para leitura da guia da Guia-Consulta
def guia_consulta(caminho):
    ns = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}
    tree = etree.parse(caminho)
    root = tree.getroot()
    guias = root.xpath('.//ans:guiaConsulta', namespaces=ns)

    # Informações da guia
    lista_dados = []
    for guia in guias:
        dados_guia = {
            "data_atendimento" : guia.find('.//ans:dataAtendimento', namespaces=ns).text,
            "guia_prestador" : guia.find('.//ans:numeroGuiaPrestador', namespaces=ns).text,
            "guia_operadora" : guia.find('.//ans:numeroGuiaOperadora', namespaces=ns).text,
            "carteira" : guia.find('.//ans:numeroCarteira', namespaces=ns).text,
            "tp_atendimento" : guia.find('.//ans:atendimentoRN', namespaces=ns).text,
            "nome_prof" : guia.find('.//ans:nomeProfissional', namespaces=ns).text,
            "cd_conselho" : guia.find('.//ans:conselhoProfissional', namespaces=ns).text,
            "nr_conselho" : guia.find('.//ans:numeroConselhoProfissional', namespaces=ns).text,
            "cd_uf" : guia.find('.//ans:UF', namespaces=ns).text,
            "cbos" : guia.find('.//ans:CBOS', namespaces=ns).text,
            "cd_tabela" : guia.find('.//ans:codigoTabela', namespaces=ns).text,
            "cd_proc" : guia.find('.//ans:codigoProcedimento', namespaces=ns).text,
            "vl_proc" : guia.find('.//ans:valorProcedimento', namespaces=ns).text
        }
        lista_dados.append(dados_guia)

    return lista_dados


lista1 = guia_consulta(r"C:\Users\Max\OneDrive\Documentos\Projeto\Portinari\00000440322026010000000090203\4020010000000090000000000263322302026010000044032001203.xml")
print(lista1[0])
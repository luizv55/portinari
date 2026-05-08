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

    return lista_dados, guias




# Função para leitura da guia de SP-SADT
def guia_sadt(caminho):
    tree = etree.parse(caminho)
    root = tree.getroot()
    ns = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}


    # Função para tratar dado tipo None
    def get_text(element, path, ns):
        el = element.find(path, namespaces=ns)
        return el.text if el is not None else None

    
    # Abrindo a tag procedimentoExecutado
    procedimentos_xml = root.xpath('//ans:procedimentoExecutado', namespaces=ns)

    # Para as guias de SP-SADT
    guias = root.xpath('.//ans:guiaSP-SADT', namespaces=ns)

    # Para as outras despesas de SP-SADT
    guias_outras_despesas = root.xpath('//ans:outrasDespesas/ans:despesa', namespaces=ns)

    # Informações da guia
    lista_dados = []
    for guia in guias:
        dados_guia = {
            "registro_ANS": get_text(guia, './/ans:registroANS', ns),
            "guia_prestador": get_text(guia, './/ans:numeroGuiaPrestador', ns),
            "guia_principal": get_text(guia, './/ans:guiaPrincipal', ns),
            "guia_operadora": get_text(guia, './/ans:numeroGuiaOperadora', ns),
            "data_autorizacao": get_text(guia, './/ans:dataAutorizacao', ns),
            "senha": get_text(guia, './/ans:senha', ns),
            "carteira": get_text(guia, './/ans:numeroCarteira', ns),
            "atendimento_rn": get_text(guia, './/ans:atendimentoRN', ns),
            "cnpj_contratado": get_text(guia, './/ans:cnpjContratado', ns),
            "contratado_solicitante": get_text(guia, './/ans:nomeContratadoSolicitante', ns),
            "nome_prof_solicitante":        get_text(guia, './/ans:profissionalSolicitante/ans:nomeProfissional', ns),
            "conselho_prof_solicitante":    get_text(guia, './/ans:profissionalSolicitante/ans:conselhoProfissional', ns),
            "nr_conselho_prof_solicitante": get_text(guia, './/ans:profissionalSolicitante/ans:numeroConselhoProfissional', ns),
            "UF_conselho_prof_solicitante": get_text(guia, './/ans:profissionalSolicitante/ans:UF', ns),
            "CBOS_conselho_prof_solicitante": get_text(guia, './/ans:profissionalSolicitante/ans:CBOS', ns),
            "carater_atendimento": get_text(guia, './/ans:caraterAtendimento', ns),
            "indicacao_clinica": get_text(guia, './/ans:indicacaoClinica', ns),
            "codigo_prestador_operadora": get_text(guia, './/ans:codigoPrestadorNaOperadora', ns),
            "CNES": get_text(guia, './/ans:CNES', ns),
            "tipo_atendimento": get_text(guia, './/ans:tipoAtendimento', ns),
            "indicacao_acidente": get_text(guia, './/ans:indicacaoAcidente', ns),
            "regime_atendimento": get_text(guia, './/ans:regimeAtendimento', ns),

            # Valor total
            "valor_tot_proc": get_text(guia, './/ans:valorTotal/ans:valorProcedimentos', ns),
            "valor_tot_diarias": get_text(guia, './/ans:valorTotal/ans:valorDiarias', ns),
            "valor_tot_tx_alugueis": get_text(guia, './/ans:valorTotal/ans:valorTaxasAlugueis', ns),
            "valor_tot_material": get_text(guia, './/ans:valorTotal/ans:valorMateriais', ns),
            "valor_tot_medicamento": get_text(guia, './/ans:valorTotal/ans:valorMedicamentos', ns),
            "valor_tot_OPME": get_text(guia, './/ans:valorTotal/ans:valorOPME', ns),
            "valor_tot_gases": get_text(guia, './/ans:valorTotal/ans:valorGasesMedicinais', ns),
            "valor_tot_geral": get_text(guia, './/ans:valorTotal/ans:valorTotalGeral', ns),
            

            # Lista de procedimentos por guia
            "procedimentos": [{
                "sequencial_item": get_text(proc, './/ans:sequencialItem', ns),
                "data_execucao": get_text(proc, './/ans:dataExecucao', ns),
                "hora_inicial": get_text(proc, './/ans:horaInicial', ns),
                "hora_final": get_text(proc, './/ans:horaFinal', ns),
                "codigo_tabela": get_text(proc, './/ans:codigoTabela', ns),
                "cd_procedimento": get_text(proc, './/ans:codigoProcedimento', ns),
                "desc_procedimento": get_text(proc, './/ans:descricaoProcedimento', ns),
                "qtd_executada": get_text(proc, './/ans:quantidadeExecutada', ns),
                "via_acesso": get_text(proc, './/ans:viaAcesso', ns),
                "tecnica_utilizada": get_text(proc, './/ans:tecnicaUtilizada', ns),
                "reducao_acrescimo": get_text(proc, './/ans:reducaoAcrescimo', ns),
                "valor_unitario": get_text(proc, './/ans:valorUnitario', ns),
                "valor_total": get_text(proc, './/ans:valorTotal', ns),
                "grau_part": get_text(proc, './/ans:grauPart', ns),
                "cpf_contratado_equipe": get_text(proc, './/ans:cpfContratado', ns),
                "nome_prof_equipe": get_text(proc, './/ans:nomeProf', ns),
                "conselho_equipe": get_text(proc, './/ans:conselho', ns),
                "nr_conselho_prof_equipe": get_text(proc, './/ans:numeroConselhoProfissional', ns),
                "UF_conselho_prof_equipe": get_text(proc, './/ans:UF', ns),
                "CBOS_conselho_prof_equipe": get_text(proc, './/ans:CBOS', ns)
            }
            for proc in guia.findall('.//ans:procedimentoExecutado', ns)
                             ]

            # Lista de outras despesas por guia
            ,"outras_despesas": [{
                "sequencial_item2" : get_text(proc, './/ans:sequencialItem', ns),
                "codigo_despesa" : get_text(proc, './/ans:codigoDespesa', ns),
                "data_execucao2": get_text(proc, './/ans:dataExecucao', ns),
                "hora_inicial2": get_text(proc, './/ans:horaInicial', ns),
                "hora_final2": get_text(proc, './/ans:horaFinal', ns),
                "codigo_tabela2": get_text(proc, './/ans:codigoTabela', ns),
                "codigo_procedimento2": get_text(proc, './/ans:codigoProcedimento', ns),
                "qtd_executada2": get_text(proc, './/ans:quantidadeExecutada', ns),
                "unidade_medida2": get_text(proc, './/ans:unidadeMedida', ns),
                "reducao_acrescimo2": get_text(proc, './/ans:reducaoAcrescimo', ns),
                "valor_unitario2": get_text(proc, './/ans:valorUnitario', ns),
                "valor_total2": get_text(proc, './/ans:valorTotal', ns),
                "desc_proc2": get_text(proc, './/ans:descricaoProcedimento', ns)
            }
            for proc in guia.findall('.//ans:outrasDespesas/ans:despesa', ns)
            ]

            
        }
        lista_dados.append(dados_guia)
    return lista_dados, guias, guias_outras_despesas
    
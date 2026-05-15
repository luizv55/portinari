import flet as ft
import xml.etree.ElementTree as ET
import json
from xml_parser import cabecalho, guia_consulta, guia_sadt

# Extraindo as informações de especialidades
with open("src/CBOS.json", "r", encoding="utf-8") as f:
    tabela_cbos = json.load(f)

# Extraindo informações de conselho
with open("src/conselho.json", "r", encoding="utf-8") as f:
    tabela_conselho = json.load(f)

# Extraindo informações de UF do conselho
with open("src/UF.json", "r", encoding="utf-8") as f:
    tabela_conselho_UF = json.load(f)

# Extraindo as informações de caraterAtendimento:
with open("src/caraterAtendimento.json", "r", encoding="utf-8") as f:
    tabela_caraterAtendimento = json.load(f)

# Extraindo as informações de regimeAtendimento:
with open("src/regimeAtendimento.json", "r", encoding="utf-8") as f:
    tabela_regimeAtendimento = json.load(f)

# Extraindo as informações de tipoAtendimento:
with open("src/tipoAtendimento.json", "r", encoding="utf-8") as f:
    tabela_tipoAtendimento = json.load(f)

# Extraindo as informações de indicacaoAcidente
with open("src/indicacaoAcidente.json", "r", encoding="utf-8") as f:
    tabela_indicacaoAcidente = json.load(f)

# Extraindo as informações de tecnicaUtilizada
with open("src/tecnicaUtilizada.json", "r", encoding="utf-8") as f:
    tabela_tecnicaUtilizada = json.load(f)

# Extraindo as informações de viaAcesso
with open("src/viaAcesso.json", "r", encoding="utf-8") as f:
    tabela_viaAcesso = json.load(f)



def main(page: ft.Page):
    page.title = "Visualizador de Documento XML"
    page.bgcolor = ft.Colors.GREY_100
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


#=======Estado de aplicação=============
    lista_dados = []
    guias_consulta = []
    guias_sadt = []
    guias_outras = []
    lote = ""
    data_registro = ""
    hr_registro = ""
    cnpj_origem = ""
    cnpj_destino = ""


    nome_arquivo = ""
    caminho_arquivo = ""
    def on_file_picked(e: ft.FilePickerResultEvent):
        nonlocal nome_arquivo, caminho_arquivo, lista_dados, guias_consulta, guias_sadt, guias_outras, lote, data_registro, hr_registro, cnpj_origem, cnpj_destino
        if e.files:
            nome_arquivo = e.files[0].name
            caminho_arquivo = e.files[0].path

            if caminho_arquivo != '':
                # Extraindo as informações do cabeçalho
                res_cab = cabecalho(caminho_arquivo)
                lote, data_registro, hr_registro, cnpj_origem, cnpj_destino = res_cab

                lista_dados, guias_consulta = guia_consulta(caminho_arquivo)
                if len(guias_consulta) == 0:
                    lista_dados, guias_sadt, guias_outras = guia_sadt(caminho_arquivo)

                d = data_registro
                txt_tipo_guia.value = 'GUIA CONSULTA' if len(guias_consulta) > 0 else 'GUIA SP/SADT'
                txt_info_registro.value = f"ID do Registro: {lote} | Data: {d[8:10]}/{d[5:7]}/{d[0:4]}"
                txt_cnpj_origem.value = cnpj_origem
                txt_cnpj_destino.value = cnpj_destino

            # para fechar e aparecer o documento
            tela_upload.visible = False
            tela_documento.visible = True
            documento.visible = True
            page.update()
            atualizar_card()







    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    icone = ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, size=64, color=ft.Colors.BLUE_600)

    texto_caminho = ft.Text(
        "Nenhum arquivo selecionado",
        size=13,
        color=ft.Colors.GREY_500,
        max_lines=1,
        overflow=ft.TextOverflow.ELLIPSIS,
        width=220,
        text_align=ft.TextAlign.CENTER,
    )

    botao = ft.ElevatedButton(
        text="Selecione um arquivo",
        icon=ft.Icons.FOLDER_OPEN_OUTLINED,
        on_click=lambda e: file_picker.pick_files(),
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.symmetric(horizontal=24, vertical=14),
        ),
    )

    container = ft.Container(
        width=300,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=16,
        padding=ft.padding.symmetric(horizontal=24, vertical=32),
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            [
                icone,
                ft.Text(
                    "Carregar arquivo",
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.GREY_800,
                ),
                ft.Container(height=8),
                botao,
                ft.Container(height=4),
                texto_caminho,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        ),
    )





    # Paginação
    pagina_atual = {"index": 0}


    # Função para a criação das boxes personalizadas
    def field_box(label, value, icon, col=None):
        return ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(icon, size=16, color=ft.Colors.BLUE_700), ft.Text(label, size=12, weight="bold", color=ft.Colors.BLUE_GREY_400)]),
                ft.Text(value, size=16, weight="w500", color=ft.Colors.BLACK, selectable=True),
            ], spacing=2),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            expand=col,
        )

    # Controles de paginação
    lbl_pagina = ft.Text("", size=14, color=ft.Colors.WHITE, weight='bold')
    btn_anterior = ft.ElevatedButton(
        '◀  Anterior',
        on_click=lambda e: navegar(-1),
        disabled=True,
    )
    btn_proximo = ft.ElevatedButton(
        'Próximo ▶',
        on_click=lambda e: navegar(1),
    )

    card_container = ft.Column(
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )



    def atualizar_card():
        card_container.controls.clear()

        dados_filtrados = obter_dados_filtrados()
        total = len(dados_filtrados)

        if total == 0:
            card_container.controls.append(
                ft.Container(
                    content=ft.Text(
                        "Nenhuma guia encontrada",
                        color=ft.Colors.GREY_500,
                        size=16,
                    ),
                    padding=40,
                    alignment=ft.alignment.center
                )
            )

            lbl_pagina.value = '0 / 0'
            btn_anterior.disabled = True
            btn_proximo.disabled = True

        else:
            pagina_atual['index'] = max(0, min(pagina_atual['index'], total - 1))
            dados = dados_filtrados[pagina_atual['index']]

            if len(guias_consulta) > 0:
                card_container.controls.append(criar_card_consulta(dados))
            else:
                card_container.controls.append(criar_card_sadt(dados))

            lbl_pagina.value = f"{pagina_atual['index'] + 1} / {total}"
            btn_anterior.disabled = pagina_atual['index'] == 0
            btn_proximo.disabled = pagina_atual['index'] == total - 1
        
        page.update()

    def navegar(direcao: int):
        pagina_atual["index"] += direcao
        atualizar_card()

    termo_busca = {"valor": ""}


    def obter_dados_filtrados():
        termo = termo_busca["valor"].strip()
        if not termo:
            return lista_dados
        return [c for c in lista_dados if termo in str(c.get("guia_prestador", ""))]



    def limpar_pesquisa():
        search_field.value = ""
        filtrar_guias("")

    # Função para gerar um container para cada guia de consulta
    def criar_card_consulta(dados):
        if guias_consulta != 0:
            # Formatação de data
            d = str(dados.get('data_atendimento', ''))
            data_br = f"{d[8:10]}/{d[5:7]}/{d[0:4]}"

            # Pega o código CBOS do XML
            codigo_cbo = str(dados['cbos'])
            # Buscando a profissão
            nome_especialidade = tabela_cbos.get(codigo_cbo, 'Especialidade não identificada')

            # Pega o código do conselho
            codigo_conselho = str(dados['cd_conselho'])
            # Buscando pelo conselho
            nome_conselho = tabela_conselho.get(codigo_conselho, 'Conselho não identificado')

            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("INFORMAÇÕES BÁSICAS", weight="bold", color=ft.Colors.BLUE_800)
                    ]),
                    ft.Row([
                        field_box("Guia Prestador", dados['guia_prestador'], ft.Icons.ASSIGNMENT, col=True),
                        field_box("Guia Operadora", dados['guia_operadora'], ft.Icons.BUSINESS, col=True),
                        field_box("Carteira", dados['carteira'], ft.Icons.CONTACT_EMERGENCY, col=True)
                    ]),

                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

                    ft.Row([
                        ft.Text('INFORMAÇÕES DO PROFISSIONAL', weight="bold", color=ft.Colors.BLUE_800)
                    ]),
                    ft.Row([
                        field_box("Nome do Profissinal", dados['nome_prof'], ft.Icons.MEDICAL_SERVICES, col=True),
                        field_box("CBOS", f"{dados['cbos']} - {nome_especialidade}", ft.Icons.WORK_HISTORY, col=True)
                    ]),
                    ft.Row([
                        field_box("Códido do Conselho", f"{dados['cd_conselho']} - {nome_conselho}", ft.Icons.ACCOUNT_BALANCE, col=True),
                        field_box("Número do Conselho", dados['nr_conselho'], ft.Icons.FINGERPRINT, col=True),
                        field_box("UF", dados['cd_uf'], ft.Icons.MAP, col=True)]),
                    
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),


                    ft.Row([
                        ft.Text('INFORMAÇÕES DO PROCEDIMENTO', weight='bold', color=ft.Colors.BLUE_800)
                    ]),
                    ft.Row([
                        field_box("Data do Atendimento", data_br, ft.Icons.CALENDAR_MONTH, col=True),
                        field_box("Tipo do Atendimento", dados['tp_atendimento'], ft.Icons.CATEGORY, col=True),
                    ]),
                    ft.Row([
                        field_box("Código do Procedimento", dados['cd_proc'], ft.Icons.NUMBERS, col=True),
                        field_box("Código da Tabela", dados['cd_tabela'], ft.Icons.TABLE_CHART, col=True),
                        field_box("Valor do Procedimento", f"R$ {dados['vl_proc']}", ft.Icons.ATTACH_MONEY, col=True),
                    ])
                ]),
                margin=ft.margin.only(top=10, bottom=10),
                padding=40,
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
                width=800,
            )
        return ft.Container()
# ====================================================================================================================
    # Container com as informações da guia SP-SADT
    def criar_card_sadt(dados):
        if guias_sadt != 0:
            # Pega o código CBOS do XML
            codigo_cbo = str(dados.get('CBOS_conselho_prof_solicitante', ''))
            # Buscando a profissão
            nome_especialidade = tabela_cbos.get(codigo_cbo, 'Especialidade não identificada')

            # Pega o código do conselho
            codigo_conselho = str(dados.get('conselho_prof_solicitante', ''))
            # Buscando pelo conselho
            nome_conselho = tabela_conselho.get(codigo_conselho, 'Conselho não identificado')
            # Pega a UF do conselho
            codigo_UF = str(dados.get('UF_conselho_prof_solicitante', ''))
            codigo_UF1 = tabela_conselho_UF.get(codigo_UF, 'UF não identificado')

            # Pega as informações sobre o caracter de atendimento
            codigo_carater = str(dados.get('carater_atendimento', ''))
            codigo_carater1 = tabela_caraterAtendimento.get(codigo_carater, 'Carácter de atendimento não identificado')

            # Pega as informações sobre o tipo de atendimento
            codigo_tp_atendimento = str(dados.get('tipo_atendimento', ''))
            codigo_tp_atendimento1 = tabela_tipoAtendimento.get(codigo_tp_atendimento, 'Tipo de atendimento não identificado')

            # Pega as informações sobre a indicacao de acidente
            codigo_indicacaoAcidente = str(dados.get('indicacao_acidente', ''))
            codigo_indicacaoAcidente1 = tabela_indicacaoAcidente.get(codigo_indicacaoAcidente, 'Tipo de indicação acidente não identificado')

            # Pega as informações sobre regime de atendimento
            codigo_regimeAtendimento = str(dados.get('regime_atendimento', ''))
            codigo_regimeAtendimento1 = tabela_regimeAtendimento.get(codigo_regimeAtendimento, 'Tipo de regime de atendimento não identificado')


            # Data de autorização
            d = str(dados.get('data_autorizacao', ''))

            # Função interna para cada card de procedimento
            def criar_card_procedimento(proc):
                # Formatação de data
                d = str(proc.get('data_execucao', ''))
                data_br = f"{d[8:10]}/{d[5:7]}/{d[0:4]}" if d else '-'

                hora_inicial = str(proc.get('hora_inicial', '-') or '-')[:5]
                hora_final = str(proc.get('hora_final', '-') or '-')[:5]

                # Pega as informações sobre via de acesso
                codigo_viaAcesso = tabela_viaAcesso.get(str(proc.get('via_acesso', '-')), 'Ausente')

                # Pega as informações sobre tecnica utilizada
                codigo_tecnicaUtilizada = tabela_tecnicaUtilizada.get(str(proc.get('tecnica_utilizada', '-')), 'Ausente')

                # Pega as informações sobre codigo de conselho
                codigo_conselho10 = tabela_conselho.get(str(proc.get('conselho_equipe', '-')), '') 

                # Pega as informações sobre UF
                codigo_UF10 = tabela_conselho_UF.get(str(proc.get('UF_conselho_prof_equipe', '-')), '')

                # Pega as informações sobre CBOS
                codigo_CBOS10 = tabela_cbos.get(str(proc.get('CBOS_conselho_prof_equipe', '-')), '')

                return ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"PROCEDIMENTO EXECUTADO - {proc.get('sequencial_item', '-')}", weight="bold", color=ft.Colors.BLUE_800)
                        ]),
                        ft.Row([
                            field_box('Data de Execução', data_br, ft.Icons.CALENDAR_MONTH, col=True),
                            field_box('Hora Inicial', hora_inicial, ft.Icons.ACCESS_TIME, col=True),
                            field_box('Hora Final', hora_final, ft.Icons.ACCESS_TIME_FILLED, col=True)]),
                        ft.Row([
                            field_box('Codigo da Procedimento', proc.get('cd_procedimento'), ft.Icons.ASSIGNMENT, col=True),
                            field_box('Codigo da Tabela', proc.get('codigo_tabela'), ft.Icons.ASSIGNMENT, col=True),
                        ]),
                        ft.Row([
                            field_box('Descrição do Procedimento', proc.get('desc_procedimento'), ft.Icons.ASSIGNMENT, col=True)
                        ]),
                        ft.Row([
                            field_box('Quantidade Executada', proc.get('qtd_executada'), ft.Icons.ASSIGNMENT, col=True),
                            field_box('Via de Acesso', f"{proc.get('via_acesso') or ''}  {codigo_viaAcesso}", ft.Icons.ASSIGNMENT, col=True),
                            field_box('Técnica Utilizada', f"{proc.get('tecnica_utilizada') or ''} {codigo_tecnicaUtilizada}", ft.Icons.ASSIGNMENT, col=True)
                        ]),
                        ft.Row([
                            ft.Text("VALORAÇÃO", weight="bold", color=ft.Colors.BLUE_800)
                        ]),
                        ft.Row([
                            field_box('Valor Unitário', f"R$ {proc.get('valor_unitario')}", ft.Icons.ASSIGNMENT, col=True),
                            field_box('Valor Total', f"R$ {proc.get('valor_total')}", ft.Icons.ASSIGNMENT, col=True),
                            field_box('Redução de Acrescimo', f"{proc.get('reducao_acrescimo')}", ft.Icons.ASSIGNMENT, col=True)
                        ]),
                        ft.Row([
                            ft.Text("PROFISSIONAL", weight="bold", color=ft.Colors.BLUE_800),
                        ]),
                        ft.Row([
                            field_box('Nome', f"{proc.get('nome_prof_equipe') or '-'}", ft.Icons.ASSIGNMENT, col=True),
                            field_box('CPF Contratado', f"{proc.get('cpf_contratado_equipe') or '-'}", ft.Icons.ASSIGNMENT, col=True)
                        ]),
                        ft.Row([
                            field_box('Código do Conselho', f"{proc.get('conselho_equipe') or ''} - {codigo_conselho10}", ft.Icons.ASSIGNMENT, col=True),
                            field_box('Número do Conselho', f"{proc.get('nr_conselho_prof_equipe') or '-'}", ft.Icons.ASSIGNMENT, col=True),
                            field_box('UF do Conselho', f"{proc.get('UF_conselho_prof_equipe') or ''} - {codigo_UF10}", ft.Icons.ASSIGNMENT, col=True),
                        ]),
                        ft.Row([
                            field_box('CBOS', f"{proc.get('CBOS_conselho_prof_equipe') or ''} - {codigo_CBOS10}", ft.Icons.ASSIGNMENT, col=True)
                        ])
                    ]),
                    margin=ft.margin.only(top=10),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.BLUE_100),
                )
        
            # Função interna para criar card de outras despesas
            def card_outras_despesas(proc):
                if guias_outras != 0:
                    # Formatação de data
                    d2 = str(proc.get('data_execucao2', ''))
                    data_br2 = f"{d2[8:10]}/{d2[5:7]}/{d2[0:4]}" if d2 else '-'

                    # Formatação de hora
                    hora_inicial = str(proc.get('hora_inicial2', '-') or '-')[:5]
                    hora_final = str(proc.get('hora_final2', '-') or '-')[:5]

                    return ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"SERVIÇO EXECUTADO - {proc.get('sequencial_item2', '-')}", weight="bold", color=ft.Colors.BLUE_800),
                            ]),
                            ft.Row([
                                field_box('Data de Execução', data_br2, ft.Icons.CALENDAR_MONTH, col=True),
                                field_box('Hora Inicial', hora_inicial, ft.Icons.ACCESS_TIME, col=True),
                                field_box('Hora Final', hora_final, ft.Icons.ACCESS_TIME_FILLED, col=True)
                            ]),
                            ft.Row([
                                field_box('Código do Procedimento', proc.get('codigo_procedimento2'), ft.Icons.ASSIGNMENT, col=True),
                                field_box('Código da Tabela', proc.get('codigo_tabela2'), ft.Icons.ASSIGNMENT, col=True)
                            ]),
                            ft.Row([
                                field_box('Descrição do Procedimento', proc.get('desc_proc2'), ft.Icons.ASSIGNMENT, col=True)
                            ]),
                            ft.Row([
                                field_box('Quantidade Executada', proc.get('qtd_executada2'), ft.Icons.ASSIGNMENT, col=True),
                                field_box('Código de Despesa', proc.get('codigo_despesa'), ft.Icons.ASSIGNMENT, col=True),
                            ]),
                            ft.Row([
                                ft.Text("VALORAÇÃO", weight="bold", color=ft.Colors.BLUE_800)
                            ]),
                            ft.Row([
                                field_box('Valor Unitário', f"R$ {proc.get('valor_unitario2')}", ft.Icons.ASSIGNMENT, col=True),
                                field_box('Valor Total', f"R$ {proc.get('valor_total2')}", ft.Icons.ASSIGNMENT, col=True),
                                field_box('Redução Acréscimo', proc.get('reducao_acrescimo2'), ft.Icons.ASSIGNMENT, col=True),
                            ])
                        ]),
                        margin=ft.margin.only(top=10),
                        padding=ft.padding.all(20),
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                        border=ft.border.all(1, ft.Colors.BLUE_100),
                    )
                return ft.Container()


            # Gera os cards de procedimento
            procedimentos = dados.get('procedimentos', [])
            cards_procedimentos = [criar_card_procedimento(p) for p in procedimentos]

            # gera os cards de outras despesas
            outras_despesas = dados.get('outras_despesas', [])
            card_despesas = [card_outras_despesas(p) for p in outras_despesas]


            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("INFORMAÇÕES BÁSICAS", weight="bold", color=ft.Colors.BLUE_800),
                        ft.Text(f"Senha: {dados['senha']} | Data Autorização: {d[8:10]}/{d[5:7]}/{d[0:4]}", color=ft.Colors.GREY_800)
                        
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        field_box("Registro ANS", dados['registro_ANS'], ft.Icons.ASSIGNMENT, col=True),
                        field_box("Guia Prestador", dados['guia_prestador'], ft.Icons.ASSIGNMENT, col=True),
                        field_box("Guia Operadora", dados['guia_operadora'], ft.Icons.ASSIGNMENT, col=True),
                        field_box("Carteirinha", dados['carteira'], ft.Icons.ASSIGNMENT, col=True),
                    ]),
                    ft.Row([
                        ft.Text("DADOS DO SOLICITANTE", weight='bold', color=ft.Colors.BLUE_800),
                    ]),
                    ft.Row([
                        field_box('Nome', dados['contratado_solicitante'][:13], ft.Icons.ASSIGNMENT, col=True),
                        field_box('CNPJ', dados['cnpj_contratado'], ft.Icons.ASSIGNMENT, col=True)
                    ]),
                    ft.Row([
                        field_box('Nome do Profissional', dados['nome_prof_solicitante'], ft.Icons.ASSIGNMENT, col=True),
                        field_box("CBOS", f"{dados['CBOS_conselho_prof_solicitante']} - {nome_especialidade}", ft.Icons.WORK_HISTORY, col=True),
                    ]),
                    ft.Row([
                        field_box("Código do Conselho", f"{dados['conselho_prof_solicitante']} - {nome_conselho}", ft.Icons.ACCOUNT_BALANCE, col=True),
                        field_box('Número do Conselho', dados['nr_conselho_prof_solicitante'], ft.Icons.ASSIGNMENT, col=True),
                        field_box("UF do Conselho", f"{dados['UF_conselho_prof_solicitante']} - {codigo_UF1}", ft.Icons.WORK_HISTORY, col=True),
                    ]),
                    ft.Row([
                        ft.Text("ATENDIMENTO", weight='bold', color=ft.Colors.BLUE_800)
                    ]),
                    ft.Row([
                        field_box('Caráter de Atendimento', f"{dados['carater_atendimento']} - {codigo_carater1}", ft.Icons.ACCOUNT_BALANCE, col=True),
                        field_box('Indicação', dados['indicacao_clinica'], ft.Icons.ASSIGNMENT, col=True),
                    ]),
                    ft.Row([
                        field_box('Tipo de Atendimento', f"{dados['tipo_atendimento']} - {codigo_tp_atendimento1}", ft.Icons.ACCOUNT_BALANCE, col=True),
                        field_box('Indicação de Acidente', f"{dados['indicacao_acidente']} - {codigo_indicacaoAcidente1}", ft.Icons.ACCOUNT_BALANCE, col=True),
                        field_box('Regime de Atendimento', f"{dados['regime_atendimento']} - {codigo_regimeAtendimento1}", ft.Icons.ACCOUNT_BALANCE, col=True),
                    ]),
                    ft.Row([
                        ft.Text('RESUMO DA COBRANÇA POR GUIA', weight='bold', color=ft.Colors.BLUE_800)
                    ]),
                    ft.Column([
                        ft.Row([
                            field_box('Valor dos procedimentos', f"R$ {dados['valor_tot_proc']}", ft.Icons.ACCOUNT_BALANCE, col=True),
                            field_box('Valor das Diarias', f"R$ {dados['valor_tot_diarias']}", ft.Icons.ACCOUNT_BALANCE, col=True)
                        ]),
                        ft.Row([
                            field_box('Valor das Taxas de Alugueis', f"R$ {dados['valor_tot_tx_alugueis']}", ft.Icons.ACCOUNT_BALANCE, col=True),
                            field_box('Valor dos Materiais', f"R$ {dados['valor_tot_material']}", ft.Icons.ACCOUNT_BALANCE, col=True),
                        ]),
                        ft.Row([
                            field_box('Valor dos Medicamentos', f"R$ {dados['valor_tot_medicamento']}", ft.Icons.ACCOUNT_BALANCE, col=True),
                            field_box('Valor de OPME', f"R$ {dados['valor_tot_OPME']}", ft.Icons.ACCOUNT_BALANCE, col=True),
                        ]),
                        ft.Row([
                            field_box('Valor dos Gases Medicinais', f"R$ {dados['valor_tot_gases']}", ft.Icons.ACCOUNT_BALANCE, col=True),
                            field_box('Valor Total Geral', f"R$ {dados['valor_tot_geral']}", ft.Icons.ACCOUNT_BALANCE, col=True)
                        ])
                    ]),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    *(
                        [
                            ft.Row([
                                ft.Icon(ft.Icons.MEDICAL_SERVICES, size=16, color=ft.Colors.BLUE_800),
                                ft.Text("PROCEDIMENTOS", weight="bold", color=ft.Colors.BLUE_800),
                            ]),
                            *cards_procedimentos,
                        ] if cards_procedimentos else []
                    ),
                    *(
                        [
                            ft.Row([
                                ft.Icon(ft.Icons.RECEIPT_LONG, size=16, color=ft.Colors.BLUE_800),
                                ft.Text("OUTRAS DESPESAS", weight="bold", color=ft.Colors.BLUE_800),
                            ]),
                            *card_despesas,
                        ] if card_despesas else []
                    ),
                ]),
                margin=ft.margin.only(top=10, bottom=10),
                padding=40,
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
                width=800,
            )
        return ft.Container()
# ====================================================================================================================================================
    # Container para leitura da guia de resumo de internação
            







# ====================================================================================================================   
    # Adicionando a barra de busca
    search_field = ft.TextField(
        hint_text="Buscar guia...",
        prefix_icon=ft.Icons.SEARCH,
        suffix=ft.IconButton(
            icon=ft.Icons.CLEAR,
            icon_size=16,
            icon_color=ft.Colors.WHITE70,
            on_click=lambda e: limpar_pesquisa(),
        ),
        border_radius=20,
        width=180,
        height=40,
        text_size=13,
        content_padding=ft.padding.only(left=10, right=10, bottom=30),
        border_color=ft.Colors.WHITE30,
        focused_border_color=ft.Colors.WHITE,
        hint_style=ft.TextStyle(color=ft.Colors.WHITE54),
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        cursor_color=ft.Colors.WHITE,
        on_change=lambda e: filtrar_guias(e.control.value),
        on_submit=lambda e: filtrar_guias(e.control.value),
    )
# ====================================================================================================================
    # Criando um botão para fechar 
    btn_fechar = ft.IconButton(
        icon=ft.Icons.CLOSE,
        icon_color=ft.Colors.WHITE,
        tooltip='Fechar Documento',
        on_click=lambda e: fechar_documento(),
    )
    
    def fechar_documento():
        tela_documento.visible = False
        tela_upload.visible = True
        card_container.controls.clear()
        pagina_atual['index'] = 0
        page.update()

# ====================================================================================================================
    # Adicionando a top bar
    top_bar = ft.Container(
    content=ft.Row(
        [
            ft.Row(
                [search_field],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
            ),
            ft.Row(
                [btn_anterior, lbl_pagina, btn_proximo],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row([btn_fechar], alignment=ft.MainAxisAlignment.END,expand=True),
        ],
    ),
    bgcolor=ft.Colors.BLUE_800,
    padding=ft.padding.symmetric(horizontal=16, vertical=8),
    border_radius=ft.border_radius.only(top_left=15, top_right=15),
    width=800
)

# ====================================================================================================================
    # Container com todas as informações principais
    txt_tipo_guia = ft.Text('', size=20, weight="bold")
    txt_info_registro = ft.Text('', color=ft.Colors.GREY_600)
    txt_cnpj_origem = ft.Text('', size=16, weight="w500", color=ft.Colors.BLACK, selectable=True)
    txt_cnpj_destino = ft.Text('', size=16, weight="w500", color=ft.Colors.BLACK, selectable=True)
    d = data_registro
    documento = ft.Container(
        visible=True,
        content=ft.Column([
            top_bar,  # <-- barra entra aqui
            ft.Container(
                content=ft.Column([
                    # Linha 1
                    ft.Row([
                        ft.Icon(ft.Icons.DESCRIPTION_ROUNDED, size=40, color=ft.Colors.BLUE_800),
                        ft.Column([
                            txt_tipo_guia,
                            txt_info_registro,
                        ], spacing=0)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    # Linha 2
                    ft.Row([
                        ft.Container(content=ft.Column([
                            ft.Row([ft.Icon(ft.Icons.INVENTORY_2, size=16, color=ft.Colors.BLUE_700), ft.Text("CNPJ de Origem", size=12, weight="bold", color=ft.Colors.BLUE_GREY_400)]),
                            txt_cnpj_origem,
                        ], spacing=2), padding=10, border=ft.border.all(1, ft.Colors.GREY_800), border_radius=8, expand=True),
                        ft.Icon(ft.Icons.ARROW_FORWARD, size=40, color=ft.Colors.BLUE_800),
                        ft.Container(content=ft.Column([
                            ft.Row([ft.Icon(ft.Icons.INVENTORY_2, size=16, color=ft.Colors.BLUE_700), ft.Text("CNPJ de Destino", size=12, weight="bold", color=ft.Colors.BLUE_GREY_400)]),
                            txt_cnpj_destino,
                        ], spacing=2), padding=10, border=ft.border.all(1, ft.Colors.GREY_800), border_radius=8, expand=True),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT)
                ]),
                padding=40,
            )
        ], spacing=0),  # spacing=0 para a barra colar no conteúdo

        margin=ft.margin.all(20),
        bgcolor=ft.Colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        ),
        width=800,
    )


    
    # Tela de upload
    tela_upload = ft.Row([container], alignment=ft.MainAxisAlignment.CENTER,
                         vertical_alignment=ft.CrossAxisAlignment.CENTER,
                         #expand=True,
                         )
    
    # Tela do documento
    tela_documento = ft.Column([documento, card_container], 
                               horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                               scroll=ft.ScrollMode.AUTO,
                               visible=False,
                               expand=True
                               )
    



    page.add(tela_upload, tela_documento)

    


ft.app(target=main)
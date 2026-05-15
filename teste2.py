import flet as ft
import json
from xml_parser import cabecalho, guia_consulta, guia_sadt

with open("src/CBOS.json", "r", encoding="utf-8") as f:
    tabela_cbos = json.load(f)
with open("src/conselho.json", "r", encoding="utf-8") as f:
    tabela_conselho = json.load(f)
with open("src/UF.json", "r", encoding="utf-8") as f:
    tabela_conselho_UF = json.load(f)
with open("src/caraterAtendimento.json", "r", encoding="utf-8") as f:
    tabela_caraterAtendimento = json.load(f)
with open("src/regimeAtendimento.json", "r", encoding="utf-8") as f:
    tabela_regimeAtendimento = json.load(f)
with open("src/tipoAtendimento.json", "r", encoding="utf-8") as f:
    tabela_tipoAtendimento = json.load(f)
with open("src/indicacaoAcidente.json", "r", encoding="utf-8") as f:
    tabela_indicacaoAcidente = json.load(f)
with open("src/tecnicaUtilizada.json", "r", encoding="utf-8") as f:
    tabela_tecnicaUtilizada = json.load(f)
with open("src/viaAcesso.json", "r", encoding="utf-8") as f:
    tabela_viaAcesso = json.load(f)


def main(page: ft.Page):
    page.title = "Visualizador de Documento XML"
    page.bgcolor = ft.Colors.GREY_100
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.LIGHT

    # ── Estado da aplicação ──────────────────────────────────────────────────
    estado = {
        "lista_dados": [],
        "guias_consulta": [],
        "guias_sadt": [],
        "guias_outras": [],
        "lote": "",
        "data_registro": "",
        "hr_registro": "",
        "cnpj_origem": "",
        "cnpj_destino": "",
        "pagina_atual": 0,
        "termo_busca": "",
    }

    # ── Helpers ──────────────────────────────────────────────────────────────
    def field_box(label, value, icon, col=None):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, size=16, color=ft.Colors.BLUE_700),
                    ft.Text(label, size=12, weight="bold", color=ft.Colors.BLUE_GREY_400),
                ]),
                ft.Text(str(value or "-"), size=16, weight="w500", color=ft.Colors.BLACK, selectable=True),
            ], spacing=2),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            expand=col,
        )

    # ── Tela inicial (upload) ────────────────────────────────────────────────
    upload_view = ft.Container(
        visible=True,
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Container(
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
                    ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, size=64, color=ft.Colors.BLUE_600),
                    ft.Text("Carregar arquivo", size=16, weight=ft.FontWeight.W_500, color=ft.Colors.GREY_800),
                    ft.Container(height=8),
                    ft.ElevatedButton(
                        text="Selecione um arquivo",
                        icon=ft.Icons.FOLDER_OPEN_OUTLINED,
                        on_click=lambda e: file_picker.pick_files(allowed_extensions=["xml"]),
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_600,
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=24, vertical=14),
                        ),
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "Nenhum arquivo selecionado",
                        size=13,
                        color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6,
            ),
        ),
    )

    # ── Tela principal (documento + cards) ──────────────────────────────────
    main_view = ft.Column(
        visible=False,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    # ── Controles de paginação ───────────────────────────────────────────────
    lbl_pagina = ft.Text("", size=14, color=ft.Colors.WHITE, weight="bold")
    btn_anterior = ft.ElevatedButton("◀  Anterior", on_click=lambda e: navegar(-1), disabled=True)
    btn_proximo  = ft.ElevatedButton("Próximo ▶",   on_click=lambda e: navegar(1))

    search_field = ft.TextField(
        hint_text="Buscar guia...",
        prefix_icon=ft.Icons.SEARCH,
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
        suffix=ft.IconButton(
            icon=ft.Icons.CLEAR,
            icon_size=16,
            icon_color=ft.Colors.WHITE70,
            on_click=lambda e: limpar_pesquisa(),
        ),
    )

    card_container = ft.Column(spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # ── Navegação / filtro ───────────────────────────────────────────────────
    def obter_dados_filtrados():
        termo = estado["termo_busca"].strip()
        if not termo:
            return estado["lista_dados"]
        return [c for c in estado["lista_dados"] if termo in str(c.get("guia_prestador", ""))]

    def atualizar_card():
        card_container.controls.clear()
        dados_filtrados = obter_dados_filtrados()
        total = len(dados_filtrados)

        if total == 0:
            card_container.controls.append(
                ft.Container(
                    content=ft.Text("Nenhuma guia encontrada", color=ft.Colors.GREY_500, size=16),
                    padding=40,
                    alignment=ft.alignment.center,
                )
            )
            lbl_pagina.value = "0 / 0"
            btn_anterior.disabled = True
            btn_proximo.disabled = True
        else:
            idx = max(0, min(estado["pagina_atual"], total - 1))
            estado["pagina_atual"] = idx
            dados = dados_filtrados[idx]

            if len(estado["guias_consulta"]) > 0:
                card_container.controls.append(criar_card_consulta(dados))
            else:
                card_container.controls.append(criar_card_sadt(dados))

            lbl_pagina.value = f"{idx + 1} / {total}"
            btn_anterior.disabled = idx == 0
            btn_proximo.disabled  = idx == total - 1

        page.update()

    def navegar(direcao: int):
        estado["pagina_atual"] += direcao
        atualizar_card()

    def filtrar_guias(termo: str):
        estado["termo_busca"] = termo
        estado["pagina_atual"] = 0
        atualizar_card()

    def limpar_pesquisa():
        search_field.value = ""
        filtrar_guias("")

    # ── File picker ──────────────────────────────────────────────────────────
    def on_file_picked(e: ft.FilePickerResultEvent):
        if not e.files:
            return

        caminho = e.files[0].path
        if not caminho:
            return

        # Cabeçalho
        lote, data_reg, hr_reg, cnpj_orig, cnpj_dest = cabecalho(caminho)
        estado["lote"]          = lote
        estado["data_registro"] = data_reg
        estado["cnpj_origem"]   = cnpj_orig
        estado["cnpj_destino"]  = cnpj_dest

        # Guias
        lista_dados, guias_consulta = guia_consulta(caminho)
        if len(guias_consulta) == 0:
            lista_dados, guias_sadt, guias_outras = guia_sadt(caminho)
            estado["guias_sadt"]   = guias_sadt
            estado["guias_outras"] = guias_outras
        else:
            estado["guias_consulta"] = guias_consulta

        estado["lista_dados"]    = lista_dados
        estado["pagina_atual"]   = 0
        estado["termo_busca"]    = ""
        search_field.value       = ""

        # Monta o documento de cabeçalho
        construir_main_view()

        # Troca de tela
        upload_view.visible = False
        main_view.visible   = True
        page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    # ── Constrói a main_view após carregar o arquivo ─────────────────────────
    def construir_main_view():
        main_view.controls.clear()

        d = estado["data_registro"]
        data_br = f"{d[8:10]}/{d[5:7]}/{d[0:4]}" if len(d) >= 10 else d

        tipo_guia = "GUIA CONSULTA" if estado["guias_consulta"] else "GUIA SP/SADT"

        top_bar = ft.Container(
            content=ft.Row(
                [search_field, btn_anterior, lbl_pagina, btn_proximo],
                alignment=ft.MainAxisAlignment.END,
                spacing=6,
            ),
            bgcolor=ft.Colors.BLUE_800,
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
            border_radius=ft.border_radius.only(top_left=15, top_right=15),
            width=800,
        )

        cabecalho_container = ft.Container(
            content=ft.Column([
                top_bar,
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.DESCRIPTION_ROUNDED, size=40, color=ft.Colors.BLUE_800),
                            ft.Column([
                                ft.Text(tipo_guia, size=20, weight="bold"),
                                ft.Text(
                                    f"ID do Registro: {estado['lote']} | Data: {data_br}",
                                    color=ft.Colors.GREY_600,
                                ),
                            ], spacing=0),
                        ]),
                        ft.Row([
                            field_box("CNPJ de Origem", estado["cnpj_origem"], ft.Icons.INVENTORY_2, col=True),
                            ft.Icon(ft.Icons.ARROW_FORWARD, size=40, color=ft.Colors.BLUE_800),
                            field_box("CNPJ de Destino", estado["cnpj_destino"], ft.Icons.INVENTORY_2, col=True),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ]),
                    padding=40,
                ),
            ], spacing=0),
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

        main_view.controls.append(cabecalho_container)
        main_view.controls.append(card_container)
        atualizar_card()

    # ── Cards consulta / SADT (sem alterações na lógica) ────────────────────
    def criar_card_consulta(dados):
        d = str(dados.get("data_atendimento", ""))
        data_br = f"{d[8:10]}/{d[5:7]}/{d[0:4]}" if len(d) >= 10 else d

        codigo_cbo      = str(dados.get("cbos", ""))
        nome_esp        = tabela_cbos.get(codigo_cbo, "Especialidade não identificada")
        codigo_conselho = str(dados.get("cd_conselho", ""))
        nome_conselho   = tabela_conselho.get(codigo_conselho, "Conselho não identificado")

        return ft.Container(
            content=ft.Column([
                ft.Row([ft.Text("INFORMAÇÕES BÁSICAS", weight="bold", color=ft.Colors.BLUE_800)]),
                ft.Row([
                    field_box("Guia Prestador", dados.get("guia_prestador"), ft.Icons.ASSIGNMENT, col=True),
                    field_box("Guia Operadora",  dados.get("guia_operadora"),  ft.Icons.BUSINESS,   col=True),
                    field_box("Carteira",         dados.get("carteira"),         ft.Icons.CONTACT_EMERGENCY, col=True),
                ]),
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                ft.Row([ft.Text("INFORMAÇÕES DO PROFISSIONAL", weight="bold", color=ft.Colors.BLUE_800)]),
                ft.Row([
                    field_box("Nome do Profissional", dados.get("nome_prof"), ft.Icons.MEDICAL_SERVICES, col=True),
                    field_box("CBOS", f"{codigo_cbo} - {nome_esp}", ft.Icons.WORK_HISTORY, col=True),
                ]),
                ft.Row([
                    field_box("Código do Conselho", f"{codigo_conselho} - {nome_conselho}", ft.Icons.ACCOUNT_BALANCE, col=True),
                    field_box("Número do Conselho", dados.get("nr_conselho"),  ft.Icons.FINGERPRINT, col=True),
                    field_box("UF",                  dados.get("cd_uf"),         ft.Icons.MAP,         col=True),
                ]),
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                ft.Row([ft.Text("INFORMAÇÕES DO PROCEDIMENTO", weight="bold", color=ft.Colors.BLUE_800)]),
                ft.Row([
                    field_box("Data do Atendimento", data_br,                   ft.Icons.CALENDAR_MONTH, col=True),
                    field_box("Tipo do Atendimento",  dados.get("tp_atendimento"), ft.Icons.CATEGORY,       col=True),
                ]),
                ft.Row([
                    field_box("Código do Procedimento", dados.get("cd_proc"),    ft.Icons.NUMBERS,      col=True),
                    field_box("Código da Tabela",        dados.get("cd_tabela"),  ft.Icons.TABLE_CHART,  col=True),
                    field_box("Valor do Procedimento",   dados.get("vl_proc"),    ft.Icons.ATTACH_MONEY, col=True),
                ]),
            ]),
            margin=ft.margin.only(top=10, bottom=10),
            padding=40,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            width=800,
        )

    def criar_card_sadt(dados):
        codigo_cbo        = str(dados.get("CBOS_conselho_prof_solicitante", ""))
        nome_esp          = tabela_cbos.get(codigo_cbo, "Especialidade não identificada")
        codigo_conselho   = str(dados.get("conselho_prof_solicitante", ""))
        nome_conselho     = tabela_conselho.get(codigo_conselho, "Conselho não identificado")
        codigo_UF1        = tabela_conselho_UF.get(str(dados.get("UF_conselho_prof_solicitante", "")), "UF não identificado")
        codigo_carater1   = tabela_caraterAtendimento.get(str(dados.get("carater_atendimento", "")), "Não identificado")
        codigo_tp1        = tabela_tipoAtendimento.get(str(dados.get("tipo_atendimento", "")), "Não identificado")
        codigo_acidente1  = tabela_indicacaoAcidente.get(str(dados.get("indicacao_acidente", "")), "Não identificado")
        codigo_regime1    = tabela_regimeAtendimento.get(str(dados.get("regime_atendimento", "")), "Não identificado")

        d = str(dados.get("data_autorizacao", ""))
        data_aut_br = f"{d[8:10]}/{d[5:7]}/{d[0:4]}" if len(d) >= 10 else d

        def criar_card_procedimento(proc):
            dp = str(proc.get("data_execucao", ""))
            data_br = f"{dp[8:10]}/{dp[5:7]}/{dp[0:4]}" if len(dp) >= 10 else "-"
            hora_i  = str(proc.get("hora_inicial", "-") or "-")[:5]
            hora_f  = str(proc.get("hora_final",   "-") or "-")[:5]
            via     = tabela_viaAcesso.get(str(proc.get("via_acesso", "")), "Ausente")
            tec     = tabela_tecnicaUtilizada.get(str(proc.get("tecnica_utilizada", "")), "Ausente")
            cons10  = tabela_conselho.get(str(proc.get("conselho_equipe", "")), "")
            uf10    = tabela_conselho_UF.get(str(proc.get("UF_conselho_prof_equipe", "")), "")
            cbos10  = tabela_cbos.get(str(proc.get("CBOS_conselho_prof_equipe", "")), "")

            return ft.Container(
                content=ft.Column([
                    ft.Row([ft.Text(f"PROCEDIMENTO EXECUTADO - {proc.get('sequencial_item', '-')}", weight="bold", color=ft.Colors.BLUE_800)]),
                    ft.Row([
                        field_box("Data de Execução", data_br, ft.Icons.CALENDAR_MONTH,    col=True),
                        field_box("Hora Inicial",     hora_i,  ft.Icons.ACCESS_TIME,        col=True),
                        field_box("Hora Final",        hora_f,  ft.Icons.ACCESS_TIME_FILLED, col=True),
                    ]),
                    ft.Row([
                        field_box("Cód. Procedimento", proc.get("cd_procedimento"),  ft.Icons.ASSIGNMENT, col=True),
                        field_box("Cód. Tabela",        proc.get("codigo_tabela"),    ft.Icons.ASSIGNMENT, col=True),
                    ]),
                    ft.Row([field_box("Descrição", proc.get("desc_procedimento"), ft.Icons.ASSIGNMENT, col=True)]),
                    ft.Row([
                        field_box("Qtd. Executada",   proc.get("qtd_executada"),   ft.Icons.ASSIGNMENT, col=True),
                        field_box("Via de Acesso",    f"{proc.get('via_acesso') or ''} {via}", ft.Icons.ASSIGNMENT, col=True),
                        field_box("Técnica Utilizada", f"{proc.get('tecnica_utilizada') or ''} {tec}", ft.Icons.ASSIGNMENT, col=True),
                    ]),
                    ft.Row([ft.Text("VALORAÇÃO", weight="bold", color=ft.Colors.BLUE_800)]),
                    ft.Row([
                        field_box("Valor Unitário",     proc.get("valor_unitario"),    ft.Icons.ASSIGNMENT, col=True),
                        field_box("Valor Total",         proc.get("valor_total"),        ft.Icons.ASSIGNMENT, col=True),
                        field_box("Redução/Acréscimo",   proc.get("reducao_acrescimo"),  ft.Icons.ASSIGNMENT, col=True),
                    ]),
                    ft.Row([ft.Text("PROFISSIONAL", weight="bold", color=ft.Colors.BLUE_800)]),
                    ft.Row([
                        field_box("Nome",         proc.get("nome_prof_equipe") or "-", ft.Icons.ASSIGNMENT, col=True),
                        field_box("CPF Contratado", proc.get("cpf_contratado_equipe") or "-", ft.Icons.ASSIGNMENT, col=True),
                    ]),
                    ft.Row([
                        field_box("Cód. Conselho", f"{proc.get('conselho_equipe') or ''} - {cons10}", ft.Icons.ASSIGNMENT, col=True),
                        field_box("Nº Conselho",   proc.get("nr_conselho_prof_equipe") or "-",        ft.Icons.ASSIGNMENT, col=True),
                        field_box("UF Conselho",   f"{proc.get('UF_conselho_prof_equipe') or ''} - {uf10}", ft.Icons.ASSIGNMENT, col=True),
                    ]),
                    ft.Row([field_box("CBOS", f"{proc.get('CBOS_conselho_prof_equipe') or ''} - {cbos10}", ft.Icons.ASSIGNMENT, col=True)]),
                ]),
                margin=ft.margin.only(top=10),
                padding=20,
                bgcolor=ft.Colors.BLUE_50,
                border_radius=10,
                border=ft.border.all(1, ft.Colors.BLUE_100),
            )

        def card_outras_despesas(proc):
            d2 = str(proc.get("data_execucao2", ""))
            data_br2 = f"{d2[8:10]}/{d2[5:7]}/{d2[0:4]}" if len(d2) >= 10 else "-"
            hora_i = str(proc.get("hora_inicial2", "-") or "-")[:5]
            hora_f = str(proc.get("hora_final2",   "-") or "-")[:5]

            return ft.Container(
                content=ft.Column([
                    ft.Row([ft.Text(f"SERVIÇO EXECUTADO - {proc.get('sequencial_item2', '-')}", weight="bold", color=ft.Colors.BLUE_800)]),
                    ft.Row([
                        field_box("Data de Execução", data_br2, ft.Icons.CALENDAR_MONTH,    col=True),
                        field_box("Hora Inicial",     hora_i,   ft.Icons.ACCESS_TIME,        col=True),
                        field_box("Hora Final",        hora_f,   ft.Icons.ACCESS_TIME_FILLED, col=True),
                    ]),
                    ft.Row([
                        field_box("Cód. Procedimento", proc.get("codigo_procedimento2"), ft.Icons.ASSIGNMENT, col=True),
                        field_box("Cód. Tabela",        proc.get("codigo_tabela2"),       ft.Icons.ASSIGNMENT, col=True),
                    ]),
                    ft.Row([field_box("Descrição", proc.get("desc_proc2"), ft.Icons.ASSIGNMENT, col=True)]),
                    ft.Row([
                        field_box("Qtd. Executada",  proc.get("qtd_executada2"),  ft.Icons.ASSIGNMENT, col=True),
                        field_box("Cód. Despesa",    proc.get("codigo_despesa"),  ft.Icons.ASSIGNMENT, col=True),
                    ]),
                    ft.Row([ft.Text("VALORAÇÃO", weight="bold", color=ft.Colors.BLUE_800)]),
                    ft.Row([
                        field_box("Valor Unitário",   proc.get("valor_unitario2"),   ft.Icons.ASSIGNMENT, col=True),
                        field_box("Valor Total",       proc.get("valor_total2"),       ft.Icons.ASSIGNMENT, col=True),
                        field_box("Redução/Acréscimo", proc.get("reducao_acrescimo2"), ft.Icons.ASSIGNMENT, col=True),
                    ]),
                ]),
                margin=ft.margin.only(top=10),
                padding=20,
                bgcolor=ft.Colors.BLUE_50,
                border_radius=10,
                border=ft.border.all(1, ft.Colors.BLUE_100),
            )

        procedimentos  = dados.get("procedimentos", [])
        outras_despesas = dados.get("outras_despesas", [])

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("INFORMAÇÕES BÁSICAS", weight="bold", color=ft.Colors.BLUE_800),
                    ft.Text(f"Senha: {dados.get('senha')} | Data Autorização: {data_aut_br}", color=ft.Colors.GREY_600),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    field_box("Registro ANS",  dados.get("registro_ANS"),  ft.Icons.ASSIGNMENT, col=True),
                    field_box("Guia Prestador", dados.get("guia_prestador"), ft.Icons.ASSIGNMENT, col=True),
                    field_box("Guia Operadora", dados.get("guia_operadora"), ft.Icons.ASSIGNMENT, col=True),
                    field_box("Carteirinha",    dados.get("carteira"),        ft.Icons.ASSIGNMENT, col=True),
                ]),
                ft.Row([ft.Text("DADOS DO SOLICITANTE", weight="bold", color=ft.Colors.BLUE_800)]),
                ft.Row([
                    field_box("Nome",  (dados.get("contratado_solicitante") or "")[:13], ft.Icons.ASSIGNMENT, col=True),
                    field_box("CNPJ",   dados.get("cnpj_contratado"),                     ft.Icons.ASSIGNMENT, col=True),
                ]),
                ft.Row([
                    field_box("Nome do Profissional", dados.get("nome_prof_solicitante"),             ft.Icons.ASSIGNMENT,  col=True),
                    field_box("CBOS",                  f"{codigo_cbo} - {nome_esp}",                   ft.Icons.WORK_HISTORY, col=True),
                ]),
                ft.Row([
                    field_box("Cód. Conselho",  f"{codigo_conselho} - {nome_conselho}", ft.Icons.ACCOUNT_BALANCE, col=True),
                    field_box("Nº Conselho",    dados.get("nr_conselho_prof_solicitante"),              ft.Icons.ASSIGNMENT,    col=True),
                    field_box("UF do Conselho", f"{dados.get('UF_conselho_prof_solicitante')} - {codigo_UF1}", ft.Icons.WORK_HISTORY, col=True),
                ]),
                ft.Row([ft.Text("ATENDIMENTO", weight="bold", color=ft.Colors.BLUE_800)]),
                ft.Row([
                    field_box("Caráter de Atendimento", f"{dados.get('carater_atendimento')} - {codigo_carater1}", ft.Icons.ACCOUNT_BALANCE, col=True),
                    field_box("Indicação",               dados.get("indicacao_clinica"),                            ft.Icons.ASSIGNMENT,       col=True),
                ]),
                ft.Row([
                    field_box("Tipo de Atendimento",   f"{dados.get('tipo_atendimento')} - {codigo_tp1}",       ft.Icons.ACCOUNT_BALANCE, col=True),
                    field_box("Indicação de Acidente", f"{dados.get('indicacao_acidente')} - {codigo_acidente1}", ft.Icons.ACCOUNT_BALANCE, col=True),
                    field_box("Regime de Atendimento", f"{dados.get('regime_atendimento')} - {codigo_regime1}",   ft.Icons.ACCOUNT_BALANCE, col=True),
                ]),
                ft.Row([ft.Text("RESUMO DA COBRANÇA POR GUIA", weight="bold", color=ft.Colors.BLUE_800)]),
                ft.Row([
                    field_box("Valor dos Procedimentos",   f"R$ {dados.get('valor_tot_proc')}",         ft.Icons.ACCOUNT_BALANCE, col=True),
                    field_box("Valor das Diárias",          f"R$ {dados.get('valor_tot_diarias')}",       ft.Icons.ACCOUNT_BALANCE, col=True),
                ]),
                ft.Row([
                    field_box("Taxas e Aluguéis",  f"R$ {dados.get('valor_tot_tx_alugueis')}", ft.Icons.ACCOUNT_BALANCE, col=True),
                    field_box("Materiais",          f"R$ {dados.get('valor_tot_material')}",    ft.Icons.ACCOUNT_BALANCE, col=True),
                ]),
                ft.Row([
                    field_box("Medicamentos",  f"R$ {dados.get('valor_tot_medicamento')}", ft.Icons.ACCOUNT_BALANCE, col=True),
                    field_box("OPME",          f"R$ {dados.get('valor_tot_OPME')}",         ft.Icons.ACCOUNT_BALANCE, col=True),
                ]),
                ft.Row([
                    field_box("Gases Medicinais", f"R$ {dados.get('valor_tot_gases')}",     ft.Icons.ACCOUNT_BALANCE, col=True),
                    field_box("Total Geral",       f"R$ {dados.get('valor_tot_geral')}",     ft.Icons.ACCOUNT_BALANCE, col=True),
                ]),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                *(
                    [
                        ft.Row([
                            ft.Icon(ft.Icons.MEDICAL_SERVICES, size=16, color=ft.Colors.BLUE_800),
                            ft.Text("PROCEDIMENTOS", weight="bold", color=ft.Colors.BLUE_800),
                        ]),
                        *[criar_card_procedimento(p) for p in procedimentos],
                    ] if procedimentos else []
                ),
                *(
                    [
                        ft.Row([
                            ft.Icon(ft.Icons.RECEIPT_LONG, size=16, color=ft.Colors.BLUE_800),
                            ft.Text("OUTRAS DESPESAS", weight="bold", color=ft.Colors.BLUE_800),
                        ]),
                        *[card_outras_despesas(p) for p in outras_despesas],
                    ] if outras_despesas else []
                ),
            ]),
            margin=ft.margin.only(top=10, bottom=10),
            padding=40,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            width=800,
        )

    # ── Layout raiz ──────────────────────────────────────────────────────────
    page.add(
        ft.Stack(
            controls=[
                ft.Row([upload_view], alignment=ft.MainAxisAlignment.CENTER, expand=True),
                ft.Row([main_view],   alignment=ft.MainAxisAlignment.CENTER),
            ],
            expand=True,
        )
    )


ft.app(target=main)
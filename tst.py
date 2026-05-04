import flet as ft
import xml.etree.ElementTree as ET
import json
import importlib.resources
from xml_parser import cabecalho, guia_consulta

# Extraindo as informações do cabeçalho
caminho = r"C:\Users\luizvieira\Documents\Projeto\portinari\00000440322026010000000090203\4020010000000090000000000263322302026010000044032002203.xml"
lote, data_registro, hr_registro, cnpj_origem, cnpj_destino = cabecalho(caminho)


# Extraindo as informações de consulta
caminho1 = r"C:\Users\luizvieira\Documents\Projeto\portinari\00000440322026010000000090203\4020010000000090000000000263322302026010000044032002203.xml"
lista_dados = guia_consulta(caminho1)

# Extraindo as informações de especialidades
with open("src/CBOS.json", "r", encoding="utf-8") as f:
    tabela_cbos = json.load(f)

# Extraindo informações de conselho
with open("src/conselho.json", "r", encoding="utf-8") as f:
    tabela_conselho = json.load(f)


def main(page: ft.Page):
    page.title = "Visualizador de Documento XML"
    page.bgcolor = ft.Colors.GREY_100
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.LIGHT

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

    # Função para gerar um container para cada guia
    def criar_card_consulta(dados):
        # Formatação de data
        d = dados['data_atendimento']
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
                    ft.Text("INFORMAÇÕES BÁSICAS", weight="bold", color=ft.colors.BLUE_800)
                ]),
                ft.Row([
                    field_box("Guia Prestador", dados['guia_prestador'], ft.icons.ASSIGNMENT, col=True),
                    field_box("Guia Operadora", dados['guia_operadora'], ft.icons.BUSINESS, col=True),
                    field_box("Carteira", dados['carteira'], ft.icons.CONTACT_EMERGENCY, col=True)
                ]),

                ft.Divider(height=30, color=ft.colors.TRANSPARENT),

                ft.Row([
                    ft.Text('INFORMAÇÕES DO PROFISSIONAL', weight="bold", color=ft.colors.BLUE_800)
                ]),
                ft.Row([
                    field_box("Nome do Profissinal", dados['nome_prof'], ft.icons.MEDICAL_SERVICES, col=True),
                    field_box("CBOS", f'{dados['cbos']} - {nome_especialidade}', ft.icons.WORK_HISTORY, col=True)
                ]),
                ft.Row([
                    field_box("Códido do Conselho", f"{dados['cd_conselho']} - {nome_conselho}", ft.icons.ACCOUNT_BALANCE, col=True),
                    field_box("Número do Conselho", dados['nr_conselho'], ft.icons.FINGERPRINT, col=True),
                    field_box("UF", dados['cd_uf'], ft.icons.MAP, col=True)]),
                
                ft.Divider(height=30, color=ft.colors.TRANSPARENT),


                ft.Row([
                    ft.Text('INFORMAÇÕES DO PROCEDIMENTO', weight='bold', color=ft.colors.BLUE_800)
                ]),
                ft.Row([
                    field_box("Data do Atendimento", data_br, ft.icons.CALENDAR_MONTH, col=True),
                    field_box("Tipo do Atendimento", dados['tp_atendimento'], ft.icons.CATEGORY, col=True),
                ]),
                ft.Row([
                    field_box("Código do Procedimento", dados['cd_proc'], ft.icons.NUMBERS, col=True),
                    field_box("Código da Tabela", dados['cd_tabela'], ft.icons.TABLE_CHART, col=True),
                    field_box("Valor do Procedimento", dados['vl_proc'], ft.icons.ATTACH_MONEY, col=True),
                ])
            ]),
            margin=ft.margin.only(top=10, bottom=10),
            padding=40,
            bgcolor=ft.colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.colors.with_opacity(0.1, ft.colors.BLACK)),
            width=800,
        )



# ====================================================================================================================
    # Container com todas as informações principais
    d = data_registro
    documento = ft.Container(
        content=ft.Column([
            # Linha 1
            ft.Row([
                ft.Icon(ft.icons.DESCRIPTION_ROUNDED, size=40, color=ft.colors.BLUE_800),
                ft.Column([
                    ft.Text('GUIA CONSULTA', size=20, weight="bold"),
                    ft.Text(f"ID do Registro: {lote} | Data: {d[8:10]}/{d[5:7]}/{d[0:4]}", color=ft.colors.GREY_600),
                ], spacing=0)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            # Linha 2
            ft.Row([
                field_box("CNPJ de Origem", cnpj_origem, ft.icons.INVENTORY_2, col=True),
                ft.Icon(ft.icons.ARROW_FORWARD, size=40, color=ft.colors.BLUE_800),
                field_box("CNPJ de Destino", cnpj_destino, ft.icons.INVENTORY_2, col=True)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Divider(height=30, color=ft.colors.TRANSPARENT)
        ]), 
        
        # Estilização do Container Principal
        margin=ft.margin.all(20),
        padding=40,
        bgcolor=ft.colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
        ),
        width=800,
    ) 

    cards_column = ft.Column(spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    for c in lista_dados:
        cards_column.controls.append(criar_card_consulta(c))


    def filtrar_guias(termo: str):
        cards_column.controls.clear()
        termo = termo.strip()

        if not termo:
            for c in lista_dados:
                cards_column.controls.append(criar_card_consulta(c))
        else:
            encontrados = [c for c in lista_dados if termo in str(c['guia_prestador'])]
            if encontrados:
                for c in encontrados:
                    cards_column.controls.append(criar_card_consulta(c))
            else:
                cards_column.controls.append(
                    ft.Container(
                        content=ft.Text(
                            f'Nenhuma guia encontrada para "{termo}"',
                            color=ft.Colors.GREY_500,
                            size=16,
                        ),
                        padding=40,
                        alignment=ft.alignment.center,
                    )
                )
        page.update()

    def limpar_pesquisa():
        search_field.value = ""
        filtrar_guias("")
        page.update()

    search_field = ft.TextField(
        hint_text="Buscar guia...",
        prefix_icon=ft.Icons.SEARCH,
        suffix=ft.IconButton(
            icon=ft.Icons.CLEAR,
            icon_size=16,
            on_click=lambda e: limpar_pesquisa(),
        ),
        border_radius=10,
        width=150,
        height=40,
        text_size=13,
        content_padding=ft.padding.only(left=10, right=10, bottom=30),
        on_change=lambda e: filtrar_guias(e.control.value),
        on_submit=lambda e: filtrar_guias(e.control.value),
    )





    # Layout final
    layout = ft.Column(
            controls=[
                documento,
                cards_column,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    




    barra_flutuante = ft.Container(
        content=search_field,
        top=20,
        right=20,
    )

    page.add(
        ft.Stack(
            controls=[
                ft.Row([layout], alignment=ft.MainAxisAlignment.CENTER),
                barra_flutuante,
            ],
            expand=True,
        )
    )

ft.app(target=main)
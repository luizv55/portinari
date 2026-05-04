import flet as ft
import xml.etree.ElementTree as ET
from xml_parser import cabecalho

# Extraindo as informações do cabeçalho
caminho = r"C:\Users\Max\OneDrive\Documentos\Projeto\Portinari\00000440322026010000000090203\4020010000000090000000000263322302026010000044032001203.xml"
lote, data_registro, hr_registro, cnpj_origem, cnpj_destino = cabecalho(caminho)




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
                ft.Text(value, size=16, weight="w500", color=ft.Colors.BLACK),
            ], spacing=2),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            expand=col,
        )



    # Container com todas as informações principais
    documento = ft.Container(
        content=ft.Column([
            # Linha 1
            ft.Row([
                ft.Icon(ft.Icons.DESCRIPTION_ROUNDED, size=40, color=ft.Colors.BLUE_800),
                ft.Column([
                    ft.Text('GUIA CONSULTA', size=20, weight="bold"),
                    ft.Text(f"ID do Registro: {lote} | Data: {data_registro}", color=ft.Colors.GREY_600),
                ], spacing=0)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            
            ft.Text("INFORMAÇÕES BÁSICAS", weight="bold", color=ft.Colors.BLUE_800),
            
        ]),
         # Estilização do Container Principal (O Papel)
        margin=ft.margin.all(20),
        padding=40,
        bgcolor=ft.Colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        ),
        width=800,
    )








    page.add(documento)

ft.app(target=main)
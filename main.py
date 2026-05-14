import flet as ft
import threading

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.GREY_100

    def destroy():
        container.visible = False
        page.update()


    nome_arquivo = ""
    caminho_arquivo = ""
    def on_file_picked(e: ft.FilePickerResultEvent):
        nonlocal nome_arquivo, caminho_arquivo
        if e.files:
            nome_arquivo = e.files[0].name
            caminho_arquivo = e.files[0].path
            print(nome_arquivo)
            print(caminho_arquivo)
            page.update()
            destroy()


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

    page.add(container)

ft.app(target=main)
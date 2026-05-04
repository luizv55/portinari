import flet as ft
import xml.etree.ElementTree as ET

def main(page: ft.Page):
    page.title = "Visualizador de Documento XML"
    page.bgcolor = ft.Colors.GREY_100
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.LIGHT

    # Simulação de um XML mais robusto
    xml_data = """
    <produto>
        <id>4592</id>
        <data_cadastro>2023-10-25</data_cadastro>
        <informacoes_basicas>
            <nome>Monitor UltraWide 34"</nome>
            <categoria>Eletrônicos</categoria>
            <fornecedor>TechCorp Brasil</fornecedor>
        </informacoes_basicas>
        <financeiro>
            <preco_custo>1500.00</preco_custo>
            <preco_venda>2299.90</preco_venda>
            <moeda>BRL</moeda>
        </financeiro>
        <logistica>
            <estoque_atual>15</estoque_atual>
            <estoque_minimo>5</estoque_minimo>
            <peso_kg>6.5</peso_kg>
        </logistica>
    </produto>
    """
    root = ET.fromstring(xml_data)

    # Função auxiliar para criar campos de leitura estilizados
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

    # Estruturando o "Papel" do Formulário
    documento = ft.Container(
        content=ft.Column([
            # Cabeçalho do Documento
            ft.Row([
                ft.Icon(ft.Icons.DESCRIPTION_ROUNDED, size=40, color=ft.Colors.BLUE_800),
                ft.Column([
                    ft.Text("FICHA TÉCNICA DO PRODUTO", size=20, weight="bold"),
                    ft.Text(f"ID do Registro: {root.find('id').text} | Data: {root.find('data_cadastro').text}", color=ft.Colors.GREY_600),
                ], spacing=0)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

            # Seção 1: Informações Básicas
            ft.Text("INFORMAÇÕES BÁSICAS", weight="bold", color=ft.Colors.BLUE_800),
            ft.Row([
                field_box("Nome do Produto", root.find(".//nome").text, ft.Icons.INVENTORY_2, col=True),
            ]),
            ft.Row([
                field_box("Categoria", root.find(".//categoria").text, ft.Icons.CATEGORY, col=True),
                field_box("Fornecedor", root.find(".//fornecedor").text, ft.Icons.BUSINESS, col=True),
            ]),

            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

            # Seção 2: Valores e Logística (Lado a Lado)
            ft.Row([
                # Coluna Financeira
                ft.Column([
                    ft.Text("FINANCEIRO", weight="bold", color=ft.Colors.BLUE_800),
                    field_box("Preço de Venda", f"R$ {root.find('.//preco_venda').text}", ft.Icons.ATTACH_MONEY),
                    field_box("Moeda", root.find('.//moeda').text, ft.Icons.CURRENCY_EXCHANGE),
                ], expand=True),
                
                # Coluna Logística
                ft.Column([
                    ft.Text("LOGÍSTICA / ESTOQUE", weight="bold", color=ft.Colors.BLUE_800),
                    field_box("Qtd. em Estoque", root.find('.//estoque_atual').text, ft.Icons.STORE),
                    field_box("Peso Unitário", f"{root.find('.//peso_kg').text} kg", ft.Icons.SCALE),
                ], expand=True),
            ], alignment=ft.MainAxisAlignment.START, spacing=20),

            ft.Divider(height=40),
            
            # Rodapé com Botões de Ação
            ft.Row([
                ft.OutlinedButton("Imprimir PDF", icon=ft.Icons.PRINT),
                ft.ElevatedButton("Editar Informações", icon=ft.Icons.EDIT, bgcolor=ft.Colors.BLUE_800, color=ft.Colors.WHITE),
            ], alignment=ft.MainAxisAlignment.END, spacing=10)

        ], spacing=10),
        
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

    # Centraliza o formulário na tela
    page.add(
        ft.Row([documento], alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)
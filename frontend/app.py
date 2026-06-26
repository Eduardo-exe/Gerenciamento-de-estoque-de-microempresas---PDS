import flet as ft

AZUL = "#31708E"


def main(page: ft.Page):
    page.title = "G-Estoque"
    page.window_width = 1200
    page.window_height = 750
    page.padding = 0
    page.bgcolor = ft.Colors.WHITE

    # ================= LOGIN =================
    def tela_login():
        page.clean()

        esquerda = ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Image(
                src="G-Estoque.png",
                fit="contain",
            ),
        )

        direita = ft.Container(
            width=500,
            padding=50,
            bgcolor="#1E1F22",
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Login", size=32, color=ft.Colors.WHITE),

                    ft.TextField(label="Usuário", width=320),
                    ft.TextField(label="Senha", width=320, password=True),

                    ft.Container(height=10),

                    # ✔ botão no padrão correto
                    ft.TextButton(
                        content=ft.Text("Esqueci minha senha"),
                        on_click=lambda e: tela_recuperacao(),
                        style=ft.ButtonStyle(color=ft.Colors.WHITE70),
                    ),

                    ft.Container(height=20),

                    ft.ElevatedButton(
                        content=ft.Text("Acessar", color=ft.Colors.WHITE),
                        width=320,
                        bgcolor=AZUL,
                    ),
                ],
            ),
        )

        page.add(ft.Row([esquerda, direita], expand=True))
        page.update()

    # ================= RECUPERAÇÃO =================
    def tela_recuperacao():
        page.clean()

        page.add(
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Recuperar Senha", size=30, color=ft.Colors.BLACK),

                        ft.Container(height=20),

                        ft.TextField(
                            label="Digite seu e-mail",
                            width=320,
                        ),

                        ft.Container(height=20),

                        ft.ElevatedButton(
                            content=ft.Text("Enviar link de recuperação"),
                            width=320,
                            bgcolor=AZUL,
                            color=ft.Colors.WHITE,
                        ),

                        ft.Container(height=10),

                        ft.TextButton(
                            content=ft.Text("Voltar para o login"),
                            on_click=lambda e: tela_login(),
                        ),
                    ],
                ),
            )
        )

        page.update()

    # inicia no login
    tela_login()


ft.app(target=main, assets_dir=".")
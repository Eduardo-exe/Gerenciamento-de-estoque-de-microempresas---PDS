import flet as ft
from api.client import api
from state import set_state, get_state, clear_state
from views.estoquista import estoquista_view
from views.gerente import gerente_view

# ── Palette ───────────────────────────────────────────────────────────────────
BG     = "#1C1C1E"
INPUT  = "#2C2C2E"
ACCENT = "#2D7D9A"
TEXT   = "#F2F2F7"
MUTED  = "#8E8E93"
BORDER = "#3A3A3E"
ERR    = "#FF453A"


# ── Tela de login ─────────────────────────────────────────────────────────────

def login_view(page: ft.Page) -> ft.View:
    f_usuario = ft.TextField(
        hint_text="Usuário",
        hint_style=ft.TextStyle(color=MUTED),
        border_color=BORDER,
        focused_border_color=ACCENT,
        color=TEXT,
        bgcolor=INPUT,
        border_radius=8,
        text_size=15,
        content_padding=ft.Padding(left=16, right=16, top=14, bottom=14),
        border_width=1,
        width=320,
    )
    f_senha = ft.TextField(
        hint_text="Senha",
        password=True,
        can_reveal_password=True,
        hint_style=ft.TextStyle(color=MUTED),
        border_color=BORDER,
        focused_border_color=ACCENT,
        color=TEXT,
        bgcolor=INPUT,
        border_radius=8,
        text_size=15,
        content_padding=ft.Padding(left=16, right=16, top=14, bottom=14),
        border_width=1,
        width=320,
    )
    erro_txt = ft.Text("", color=ERR, size=13, visible=False, width=320, text_align=ft.TextAlign.CENTER)
    loading  = ft.ProgressRing(width=18, height=18, stroke_width=2, color=ACCENT, visible=False)

    def do_login(e):
        erro_txt.visible = False
        loading.visible  = True
        page.update()

        res = api.login(f_usuario.value or "", f_senha.value or "")

        loading.visible = False

        if "erro" in res:
            erro_txt.value   = res["erro"]
            erro_txt.visible = True
            page.update()
            return

        token = res.get("access_token", "")
        if "usuario" in res:
            tipo = res["usuario"].get("tipo", "estoquista")
            nome = res["usuario"].get("nome", "")
        else:
            tipo = res.get("tipo", "estoquista")
            nome = res.get("nome", "")

        api.set_token(token)
        set_state(token, tipo, nome)

        rotas = {
            "estoquista":    "/estoquista",
            "gerente":       "/gerente",
            "administrador": "/admin",
        }
        page.go(rotas.get(tipo, "/estoquista"))

    f_usuario.on_submit = do_login
    f_senha.on_submit   = do_login

    painel_logo = ft.Container(
        content=ft.Column([
            ft.Image(src="logo.png", width=110),
            ft.Container(height=16),
            ft.Text("G-Estoque", size=26, color="#1A1A2E", weight=ft.FontWeight.BOLD),
            ft.Text("Gestão Eficiente de Estoque", size=13, color="#6B7280"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True,
        bgcolor="#FFFFFF",
        alignment=ft.Alignment(0, 0),
    )

    painel_form = ft.Container(
        content=ft.Column([
            ft.Text("Login", size=30, color=TEXT, weight=ft.FontWeight.W_700),
            ft.Container(height=28),
            f_usuario,
            ft.Container(height=12),
            f_senha,
            ft.Container(height=8),
            ft.Container(
                content=ft.TextButton(
                    "Esqueci minha senha",
                    on_click=lambda e: page.go("/recuperar-senha"),
                    style=ft.ButtonStyle(color=MUTED),
                ),
                alignment=ft.Alignment(0, 0),
                width=320,
            ),
            ft.Container(height=8),
            erro_txt,
            ft.Row([loading], alignment=ft.MainAxisAlignment.CENTER, height=24),
            ft.Container(height=4),
            ft.Button(
                "Acessar",
                on_click=do_login,
                width=320,
                style=ft.ButtonStyle(
                    bgcolor=ACCENT,
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.Padding(top=16, bottom=16),
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0),
        expand=True,
        bgcolor=BG,
        alignment=ft.Alignment(0, 0),
    )

    return ft.View(
        route="/login",
        controls=[ft.Row([painel_logo, painel_form], expand=True, spacing=0)],
        bgcolor=BG,
        padding=0,
    )


# ── Roteamento ────────────────────────────────────────────────────────────────

def main(page: ft.Page):
    page.title             = "G-Estoque"
    page.bgcolor           = BG
    page.padding           = 0
    page.window_min_width  = 900
    page.window_min_height = 580

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        tipo = get_state("tipo")   # usa state.py, sem page.session

        if page.route == "/login" or not page.route:
            page.views.append(login_view(page))

        elif page.route == "/recuperar-senha":
            page.views.append(login_view(page))   # substitua pela sua view

        elif page.route == "/estoquista":
            if tipo != "estoquista":
                page.go("/login")
                return
            page.views.append(estoquista_view(page))

        elif page.route == "/gerente":
            if tipo != "gerente":
                page.go("/login")
                return
            page.views.append(gerente_view(page))

        # elif page.route == "/admin":
        #     from views.admin import admin_view
        #     page.views.append(admin_view(page))

        else:
            page.go("/login")
            return

        page.update()

    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        page.go(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop     = view_pop
    page.go("/login")


ft.run(main, assets_dir="assets")
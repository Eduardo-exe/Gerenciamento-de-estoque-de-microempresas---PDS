import requests
from typing import Optional, Dict, List

BASE_URL = "http://127.0.0.1:8000"


class ApiClient:
    def __init__(self):
        self.token: Optional[str] = None

    def set_token(self, token: str):
        self.token = token

    def clear(self):
        self.token = None

    @property
    def _headers(self) -> Dict:
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _safe_json(self, r: requests.Response) -> Dict:
        """Extrai JSON da resposta ou retorna erro legível."""
        try:
            data = r.json()
            # FastAPI retorna {"detail": "..."} em erros HTTP
            if not r.ok:
                detail = data.get("detail", f"Erro {r.status_code}")
                return {"erro": detail}
            return data
        except Exception:
            return {"erro": f"Erro {r.status_code} — resposta inválida do servidor."}

    # ── Auth ──────────────────────────────────────────────────────────────
    def login(self, login: str, senha: str) -> Dict:
        try:
            r = requests.post(
                f"{BASE_URL}/auth/login",
                json={"login": login, "senha": senha},
                timeout=5,
            )
            if r.status_code == 401:
                return {"erro": "Usuário ou senha incorretos."}
            return self._safe_json(r)
        except requests.exceptions.ConnectionError:
            return {"erro": "Servidor indisponível. Verifique se o backend está rodando."}
        except requests.exceptions.Timeout:
            return {"erro": "Tempo de resposta esgotado."}
        except Exception as e:
            return {"erro": str(e)}

    # ── Estoque ───────────────────────────────────────────────────────────
    def get_estoque(self) -> List:
        try:
            r = requests.get(f"{BASE_URL}/estoquista/estoque", headers=self._headers, timeout=5)
            if not r.ok:
                return []
            data = r.json()
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def registrar_entrada(self, codigo: int, nome: str, quantidade: int) -> Dict:
        try:
            r = requests.post(
                f"{BASE_URL}/estoquista/estoque/entrada",
                json={"codigo": codigo, "nome": nome, "quantidade": quantidade},
                headers=self._headers,
                timeout=5,
            )
            return self._safe_json(r)
        except requests.exceptions.ConnectionError:
            return {"erro": "Servidor indisponível."}
        except Exception as e:
            return {"erro": str(e)}

    def registrar_saida(self, codigo: int, nome: str, quantidade: int) -> Dict:
        try:
            r = requests.post(
                f"{BASE_URL}/estoquista/estoque/saida",
                json={"codigo": codigo, "nome": nome, "quantidade": quantidade},
                headers=self._headers,
                timeout=5,
            )
            return self._safe_json(r)
        except requests.exceptions.ConnectionError:
            return {"erro": "Servidor indisponível."}
        except Exception as e:
            return {"erro": str(e)}

    # ── Produtos ──────────────────────────────────────────────────────────
    def get_produtos(self) -> List:
        try:
            r = requests.get(f"{BASE_URL}/produtos", headers=self._headers, timeout=5)
            return r.json() if r.ok else []
        except Exception:
            return []

    def cadastrar_produto(self, codigo: int, nome: str) -> Dict:
        try:
            r = requests.post(
                f"{BASE_URL}/produtos",
                json={"codigo": codigo, "nome": nome},
                headers=self._headers,
                timeout=5,
            )
            return self._safe_json(r)
        except Exception as e:
            return {"erro": str(e)}

    # ── Fornecedores ──────────────────────────────────────────────────────
    def get_fornecedores(self) -> List:
        try:
            r = requests.get(f"{BASE_URL}/fornecedores", headers=self._headers, timeout=5)
            return r.json() if r.ok else []
        except Exception:
            return []

    def cadastrar_fornecedor(self, cnpj: str, nome: str, telefone: str) -> Dict:
        try:
            r = requests.post(
                f"{BASE_URL}/fornecedores",
                json={"cnpj": cnpj, "nome": nome, "telefone": telefone},
                headers=self._headers,
                timeout=5,
            )
            return self._safe_json(r)
        except Exception as e:
            return {"erro": str(e)}

    # ── Usuários ──────────────────────────────────────────────────────────
    def get_usuarios(self) -> List:
        try:
            r = requests.get(f"{BASE_URL}/usuarios", headers=self._headers, timeout=5)
            return r.json() if r.ok else []
        except Exception:
            return []

    def criar_usuario(self, nome: str, login: str, senha: str, tipo: str) -> Dict:
        try:
            r = requests.post(
                f"{BASE_URL}/usuarios",
                json={"nome": nome, "login": login, "senha": senha, "tipo": tipo},
                headers=self._headers,
                timeout=5,
            )
            return self._safe_json(r)
        except Exception as e:
            return {"erro": str(e)}

    # ── Relatório ─────────────────────────────────────────────────────────
    def gerar_relatorio(self) -> Dict:
        try:
            r = requests.get(f"{BASE_URL}/relatorios", headers=self._headers, timeout=10)
            return self._safe_json(r) if r.ok else {"erro": "Falha ao gerar relatório"}
        except Exception as e:
            return {"erro": str(e)}


api = ApiClient()
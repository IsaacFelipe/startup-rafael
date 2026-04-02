# testar_tudo.py
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

# Cores para o terminal
class Cores:
    VERDE = '\033[92m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    RESET = '\033[0m'
    NEGRITO = '\033[1m'

def print_titulo(texto):
    print(f"\n{Cores.AZUL}{Cores.NEGRITO}{'='*60}{Cores.RESET}")
    print(f"{Cores.AZUL}{Cores.NEGRITO}{texto.center(60)}{Cores.RESET}")
    print(f"{Cores.AZUL}{Cores.NEGRITO}{'='*60}{Cores.RESET}\n")

def print_teste(numero, nome):
    print(f"{Cores.AMARELO}[Teste {numero}] {nome}{Cores.RESET}")

def print_sucesso(mensagem):
    print(f"{Cores.VERDE}✅ PASSOU: {mensagem}{Cores.RESET}")

def print_erro(mensagem):
    print(f"{Cores.VERMELHO}❌ FALHOU: {mensagem}{Cores.RESET}")

def print_info(mensagem):
    print(f"   ℹ️  {mensagem}")

# Variável global para armazenar resultados
resultados = {
    'total': 0,
    'passou': 0,
    'falhou': 0
}

def registrar_resultado(passou):
    resultados['total'] += 1
    if passou:
        resultados['passou'] += 1
    else:
        resultados['falhou'] += 1

# ============= TESTES =============

def teste_1_health_check():
    print_teste(1, "Verificar se API está online")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'online':
                print_sucesso("API está rodando corretamente!")
                print_info(f"Resposta: {data}")
                registrar_resultado(True)
                return True
            else:
                print_erro("API respondeu mas sem status 'online'")
                registrar_resultado(False)
                return False
        else:
            print_erro(f"Status code incorreto: {response.status_code}")
            registrar_resultado(False)
            return False
            
    except requests.exceptions.ConnectionError:
        print_erro("Não conseguiu conectar! O Flask está rodando?")
        print_info("Execute: python aplicativo.py")
        registrar_resultado(False)
        return False
    except Exception as e:
        print_erro(f"Erro inesperado: {str(e)}")
        registrar_resultado(False)
        return False

def teste_2_registro_sucesso():
    print_teste(2, "Registrar novo usuário")
    try:
        # Usa timestamp para garantir email único
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        dados = {
            "nome": "Maria Silva Teste",
            "email": f"maria.teste.{timestamp}@exemplo.com",
            "senha": "senha123",
            "telefone": f"119999{timestamp[-5:]}"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/auth/registro",
            json=dados,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 201:
            data = response.json()
            if 'id' in data and data.get('email') == dados['email']:
                print_sucesso("Usuário registrado com sucesso!")
                print_info(f"ID: {data['id']}, Nome: {data['nome']}")
                registrar_resultado(True)
                return True, dados['email']
            else:
                print_erro("Resposta não contém os dados esperados")
                registrar_resultado(False)
                return False, None
        else:
            print_erro(f"Status code incorreto: {response.status_code}")
            print_info(f"Resposta: {response.text}")
            registrar_resultado(False)
            return False, None
            
    except Exception as e:
        print_erro(f"Erro: {str(e)}")
        registrar_resultado(False)
        return False, None

def teste_3_email_duplicado(email):
    print_teste(3, "Tentar registrar email duplicado (deve falhar)")
    try:
        dados = {
            "nome": "João Santos",
            "email": email,
            "senha": "outrasenha"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/auth/registro",
            json=dados,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 409:
            data = response.json()
            if 'erro' in data and 'cadastrado' in data['erro'].lower():
                print_sucesso("Sistema bloqueou email duplicado corretamente!")
                print_info(f"Mensagem: {data['erro']}")
                registrar_resultado(True)
                return True
            else:
                print_erro("Status 409 mas mensagem incorreta")
                registrar_resultado(False)
                return False
        else:
            print_erro(f"Deveria retornar 409, mas retornou: {response.status_code}")
            registrar_resultado(False)
            return False
            
    except Exception as e:
        print_erro(f"Erro: {str(e)}")
        registrar_resultado(False)
        return False

def teste_4_login_sucesso(email):
    print_teste(4, "Login com credenciais corretas")
    try:
        dados = {
            "email": email,
            "senha": "senha123"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=dados,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'msg' in data and 'sucedido' in data['msg'].lower():
                print_sucesso("Login realizado com sucesso!")
                print_info(f"Mensagem: {data['msg']}")
                registrar_resultado(True)
                return True
            else:
                print_erro("Status 200 mas resposta incorreta")
                registrar_resultado(False)
                return False
        else:
            print_erro(f"Status code incorreto: {response.status_code}")
            print_info(f"Resposta: {response.text}")
            registrar_resultado(False)
            return False
            
    except Exception as e:
        print_erro(f"Erro: {str(e)}")
        registrar_resultado(False)
        return False

def teste_5_login_senha_errada(email):
    print_teste(5, "Login com senha errada (deve falhar)")
    try:
        dados = {
            "email": email,
            "senha": "senhaerrada123"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=dados,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 401:
            data = response.json()
            if 'erro' in data and 'inválidas' in data['erro'].lower():
                print_sucesso("Sistema bloqueou login com senha errada!")
                print_info(f"Mensagem: {data['erro']}")
                registrar_resultado(True)
                return True
            else:
                print_erro("Status 401 mas mensagem incorreta")
                registrar_resultado(False)
                return False
        else:
            print_erro(f"Deveria retornar 401, mas retornou: {response.status_code}")
            registrar_resultado(False)
            return False
            
    except Exception as e:
        print_erro(f"Erro: {str(e)}")
        registrar_resultado(False)
        return False

def teste_6_listar_familiares():
    print_teste(6, "Listar todos os familiares cadastrados")
    try:
        response = requests.get(f"{BASE_URL}/api/familiares", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print_sucesso(f"Lista retornada com sucesso!")
                print_info(f"Total de familiares cadastrados: {len(data)}")
                if len(data) > 0:
                    print_info(f"Exemplo: {data[0].get('nome')} ({data[0].get('email')})")
                registrar_resultado(True)
                return True
            else:
                print_erro("Resposta não é uma lista")
                registrar_resultado(False)
                return False
        else:
            print_erro(f"Status code incorreto: {response.status_code}")
            registrar_resultado(False)
            return False
            
    except Exception as e:
        print_erro(f"Erro: {str(e)}")
        registrar_resultado(False)
        return False

def print_relatorio_final():
    print_titulo("RELATÓRIO FINAL")
    
    print(f"Total de testes: {resultados['total']}")
    print(f"{Cores.VERDE}Passaram: {resultados['passou']}{Cores.RESET}")
    print(f"{Cores.VERMELHO}Falharam: {resultados['falhou']}{Cores.RESET}")
    
    porcentagem = (resultados['passou'] / resultados['total'] * 100) if resultados['total'] > 0 else 0
    print(f"\n{Cores.NEGRITO}Taxa de sucesso: {porcentagem:.1f}%{Cores.RESET}")
    
    if resultados['falhou'] == 0:
        print(f"\n{Cores.VERDE}{Cores.NEGRITO}🎉 PARABÉNS! TODOS OS TESTES PASSARAM! 🎉{Cores.RESET}")
        print(f"{Cores.VERDE}Seu backend está funcionando perfeitamente!{Cores.RESET}")
    else:
        print(f"\n{Cores.AMARELO}⚠️  Alguns testes falharam. Verifique os erros acima.{Cores.RESET}")
        print(f"{Cores.AMARELO}Dicas:{Cores.RESET}")
        print(f"  - Verifique se o Flask está rodando (python aplicativo.py)")
        print(f"  - Confira a conexão com o MySQL")
        print(f"  - Veja os logs do Flask no terminal")

# ============= EXECUÇÃO PRINCIPAL =============

def main():
    print_titulo("TESTE AUTOMÁTICO DO BACKEND - STARTUP RAFAEL")
    print(f"⏰ Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🌐 URL Base: {BASE_URL}\n")
    
    # Teste 1: Health Check
    if not teste_1_health_check():
        print(f"\n{Cores.VERMELHO}❌ API não está acessível. Parando os testes.{Cores.RESET}")
        print(f"{Cores.AMARELO}Certifique-se de que o Flask está rodando!{Cores.RESET}")
        return
    
    print()
    
    # Teste 2: Registro
    sucesso, email_teste = teste_2_registro_sucesso()
    print()
    
    if sucesso and email_teste:
        # Teste 3: Email duplicado
        teste_3_email_duplicado(email_teste)
        print()
        
        # Teste 4: Login sucesso
        teste_4_login_sucesso(email_teste)
        print()
        
        # Teste 5: Login falha
        teste_5_login_senha_errada(email_teste)
        print()
    else:
        print(f"{Cores.AMARELO}⚠️  Pulando testes 3, 4 e 5 (dependem do teste 2){Cores.RESET}\n")
        resultados['total'] += 3
        resultados['falhou'] += 3
    
    # Teste 6: Listar
    teste_6_listar_familiares()
    print()
    
    # Relatório Final
    print_relatorio_final()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}⚠️  Testes interrompidos pelo usuário{Cores.RESET}")
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ Erro fatal: {str(e)}{Cores.RESET}")
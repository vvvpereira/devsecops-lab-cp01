import os

# Credenciais expostas no código (Hardcoded Secrets - Detectados por p/secrets)
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
STRIPE_API_KEY = "sk_live_51HzT1234567890abcdefghijklmnopqrstuvwxyz"


def main():
    print("Iniciando aplicação...")
    print(f"Conectando com a chave: {AWS_SECRET_ACCESS_KEY}")


if __name__ == "__main__":
    main()


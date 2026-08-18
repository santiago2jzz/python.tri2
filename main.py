"""
Calculadora de IMC (Índice de Massa Corporal)
-----------------------------------------------
- Calcula o IMC a partir de peso e altura
- Classifica o resultado e dá um feedback
- Guarda um histórico com data/hora em um arquivo CSV local
- Mostra uma tabela formatada com todos os cálculos já feitos
"""

import csv
import os
from datetime import datetime

ARQUIVO_HISTORICO = "historico_imc.csv"
CABECALHO = ["Data", "Nome", "Peso (kg)", "Altura (m)", "IMC", "Classificação", "Feedback"]


def calcular_imc(peso: float, altura: float) -> float:
    return peso / (altura ** 2)


def classificar_imc(imc: float) -> tuple[str, str]:
    if imc < 18.5:
        return (
            "Abaixo do peso",
            "Seu IMC está abaixo do ideal. Considere buscar orientação "
            "nutricional para avaliar se está tudo bem com sua alimentação."
        )
    elif imc < 25:
        return (
            "Peso normal",
            "Parabéns! Seu IMC está dentro da faixa considerada saudável. "
            "Continue mantendo hábitos equilibrados."
        )
    elif imc < 30:
        return (
            "Sobrepeso",
            "Seu IMC indica sobrepeso. Pequenos ajustes na alimentação e "
            "na rotina de exercícios podem fazer diferença."
        )
    elif imc < 35:
        return (
            "Obesidade grau I",
            "Seu IMC está na faixa de obesidade grau I. Vale a pena "
            "conversar com um profissional de saúde para um acompanhamento."
        )
    elif imc < 40:
        return (
            "Obesidade grau II",
            "Seu IMC está na faixa de obesidade grau II. É recomendável "
            "buscar acompanhamento médico e nutricional."
        )
    else:
        return (
            "Obesidade grau III",
            "Seu IMC está na faixa de obesidade grau III. Procure "
            "acompanhamento médico especializado o quanto antes."
        )


def ler_float(mensagem: str) -> float:
    
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor <= 0:
                print("O valor deve ser maior que zero. Tente novamente.")
                continue
            return valor
        except ValueError:
            print("Valor inválido. Digite apenas números (ex: 70.5).")


def garantir_arquivo():
    
    if not os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CABECALHO)


def salvar_registro(nome: str, peso: float, altura: float, imc: float, classificacao: str, feedback: str):
    garantir_arquivo()
    with open(ARQUIVO_HISTORICO, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%d/%m/%Y %H:%M"),
            nome,
            f"{peso:.1f}",
            f"{altura:.2f}",
            f"{imc:.2f}",
            classificacao,
            feedback,
        ])


def carregar_historico() -> list[list[str]]:
    garantir_arquivo()
    with open(ARQUIVO_HISTORICO, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        linhas = list(reader)
    return linhas[1:] if linhas else []  # remove o cabeçalho


def imprimir_tabela(linhas: list[list[str]]):
    if not linhas:
        print("\nAinda não há registros no histórico.\n")
        return

    # Define larguras de coluna com base no maior conteúdo (limitando o feedback)
    colunas = ["Data", "Nome", "Peso", "Altura", "IMC", "Classificação", "Feedback"]
    largura_feedback = 45

    linhas_formatadas = []
    for linha in linhas:
        feedback_curto = (linha[6][:largura_feedback - 3] + "...") if len(linha[6]) > largura_feedback else linha[6]
        linhas_formatadas.append([linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], feedback_curto])

    larguras = [len(c) for c in colunas]
    for linha in linhas_formatadas:
        for i, valor in enumerate(linha):
            larguras[i] = max(larguras[i], len(valor))

    def formatar_linha(valores):
        return " | ".join(str(v).ljust(larguras[i]) for i, v in enumerate(valores))

    separador = "-+-".join("-" * l for l in larguras)

    print("\n" + formatar_linha(colunas))
    print(separador)
    for linha in linhas_formatadas:
        print(formatar_linha(linha))
    print()


def menu():
    print("=" * 50)
    print("        CALCULADORA DE IMC")
    print("=" * 50)
    print("1 - Calcular novo IMC")
    print("2 - Ver histórico (tabela)")
    print("3 - Sair")
    print("=" * 50)
    return input("Escolha uma opção: ").strip()


def fluxo_calculo():
    print("\n--- Novo cálculo de IMC ---")
    nome = input("Nome (opcional, pressione Enter para pular): ").strip() or "Anônimo"
    peso = ler_float("Peso em kg (ex: 70.5): ")
    altura = ler_float("Altura em metros (ex: 1.75): ")

    imc = calcular_imc(peso, altura)
    classificacao, feedback = classificar_imc(imc)

    print(f"\nResultado de {nome}:")
    print(f"IMC: {imc:.2f}")
    print(f"Classificação: {classificacao}")
    print(f"Feedback: {feedback}\n")

    salvar_registro(nome, peso, altura, imc, classificacao, feedback)
    print("Resultado salvo no histórico!\n")


def main():
    while True:
        opcao = menu()
        if opcao == "1":
            fluxo_calculo()
        elif opcao == "2":
            historico = carregar_historico()
            imprimir_tabela(historico)
        elif opcao == "3":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    main()
"""
Calculadora de IMC
Calcula, classifica e salva os resultados em um arquivo CSV.
"""

import csv
import os
from datetime import datetime

"""Nome do arquivo onde o histórico será salvo."""
ARQUIVO_HISTORICO = "historico_imc.csv"

"""Nomes das colunas do arquivo CSV."""
CABECALHO = ["Data", "Nome", "Peso (kg)", "Altura (m)", "IMC", "Classificação", "Feedback"]


def calcular_imc(peso: float, altura: float) -> float:
    """
    Calcula o IMC usando o peso e a altura.
    """
    return peso / (altura ** 2)


def classificar_imc(imc: float) -> tuple[str, str]:
    """
    Recebe o IMC e retorna a classificação e o feedback.
    """
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
    """
    Pede um número ao usuário e verifica se ele é válido.
    """
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))

            """Verifica se o valor é maior que zero."""
            if valor <= 0:
                print("O valor deve ser maior que zero. Tente novamente.")
                continue

            return valor

        except ValueError:
            print("Valor inválido. Digite apenas números (ex: 70.5).")


def garantir_arquivo():
    """
    Cria o arquivo CSV caso ele ainda não exista.
    """
    if not os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CABECALHO)


def salvar_registro(nome: str, peso: float, altura: float, imc: float, classificacao: str, feedback: str):
    """
    Salva os dados do cálculo no arquivo CSV.
    """
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
            feedback
        ])


def carregar_historico() -> list[list[str]]:
    """
    Lê os cálculos salvos no arquivo.
    """
    garantir_arquivo()

    with open(ARQUIVO_HISTORICO, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        linhas = list(reader)

    """Remove o cabeçalho e retorna os registros."""
    return linhas[1:] if linhas else []


def imprimir_tabela(linhas: list[list[str]]):
    """
    Mostra o histórico completo no terminal.
    """
    if not linhas:
        print("\nAinda não há registros no histórico.\n")
        return

    """Mostra os dados principais de cada cálculo."""
    print("\n" + "=" * 70)
    print("HISTÓRICO DE CÁLCULOS")
    print("=" * 70)

    for linha in linhas:
        print(f"Data: {linha[0]}")
        print(f"Nome: {linha[1]}")
        print(f"Peso: {linha[2]} kg")
        print(f"Altura: {linha[3]} m")
        print(f"IMC: {linha[4]}")
        print(f"Classificação: {linha[5]}")
        print(f"Feedback: {linha[6]}")
        print("-" * 70)

    print()


def menu():
    """
    Mostra o menu e recebe a opção escolhida.
    """
    print("=" * 50)
    print("        CALCULADORA DE IMC")
    print("=" * 50)
    print("1 - Calcular novo IMC")
    print("2 - Ver histórico")
    print("3 - Sair")
    print("=" * 50)

    return input("Escolha uma opção: ").strip()


def fluxo_calculo():
    """
    Pede os dados, calcula o IMC e salva o resultado.
    """
    print("\n--- Novo cálculo de IMC ---")

    """Pede o nome do usuário."""
    nome = input("Nome (opcional, pressione Enter para pular): ").strip() or "Anônimo"

    """Pede o peso e a altura."""
    peso = ler_float("Peso em kg (ex: 70.5): ")
    altura = ler_float("Altura em metros (ex: 1.75): ")

    """Calcula e classifica o IMC."""
    imc = calcular_imc(peso, altura)
    classificacao, feedback = classificar_imc(imc)

    """Mostra o resultado completo."""
    print(f"\nResultado de {nome}:")
    print(f"IMC: {imc:.2f}")
    print(f"Classificação: {classificacao}")
    print(f"Feedback: {feedback}\n")

    """Salva o resultado no histórico."""
    salvar_registro(nome, peso, altura, imc, classificacao, feedback)

    print("Resultado salvo no histórico!\n")


def main():
    """
    Controla o funcionamento principal do programa.
    """
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


"""
Inicia o programa.
"""
if __name__ == "__main__":
    main()
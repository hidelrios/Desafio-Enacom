from pulp import *
import pandas as pd


def constraint_total_budget(projects: list, decision_variable: dict, expected_cost_info: dict):
    # Restrição: Orçamento total
    return lpSum(expected_cost_info[project] * decision_variable[project] for project in projects) <= 2400000


def constraint_at_least_one_high_risk_investment(projects: list, decision_variable: dict, investment_risk: dict):
    # Restrição: Pelo menos 1 investimento de risco alto
    return lpSum(decision_variable[project] for project in projects if investment_risk[project] == 'Alto') >= 1


def constraint_at_least_two_medium_risk_investment(projects: list, decision_variable: dict, investment_risk: dict):
    # Restrição: Pelo menos 2 investimentos de risco médio
    return lpSum(decision_variable[project] for project in projects if investment_risk[project] == 'Médio') >= 2


def constraint_at_least_two_low_risk_investment(projects: list, decision_variable: dict, investment_risk: dict):
    # Restrição: Pelo menos 2 investimentos de risco baixo
    return lpSum(decision_variable[project] for project in projects if investment_risk[project] == 'Baixo') >= 2


def constraint_maximum_cost_for_low_risk_investments(projects: list, decision_variable: dict, expected_cost_info: dict, investment_risk: dict):
    # Restrição: Custo máximo para investimentos de risco baixo
    return lpSum(expected_cost_info[project] * decision_variable[project] for project in projects if investment_risk[project] == 'Baixo') <= 1200000


def constraint_maximum_cost_for_medium_risk_investments(projects: list, decision_variable: dict, expected_cost_info: dict, investment_risk: dict):
    # Restrição: Custo máximo para investimentos de risco baixo
    return lpSum(expected_cost_info[project] * decision_variable[project] for project in projects if investment_risk[project] == 'Médio') <= 150000


def constraint_maximum_cost_for_high_risk_investments(projects: list, decision_variable: dict, expected_cost_info: dict, investment_risk: dict):
    # Restrição: Custo máximo para investimentos de risco baixo
    return lpSum(expected_cost_info[project] * decision_variable[project] for project in projects if investment_risk[project] == 'Alto') <= 900000


def main():

    # Adicionando arquivo com informações
    df = pd.read_csv(r'D:\Projetos\Desafio Enacom\teste.csv', sep=';')

    # Retorno esperado de cada projeto
    expect_return_info = {}

    # Custo de cada projeto
    expected_cost_info = {}

    # Risco do investimento
    investment_risk = {}

    projects = []

    # Tratamento das informações do arquivo
    for index, line in df.iterrows():
        project = line['Descrição']
        expect_return = line['Retorno esperado (R$)']
        expect_cost = line['Custo do investimento (R$)']
        risk = line['Risco do investimento']

        projects.append(project)

        expect_return_info[project] = expect_return
        expected_cost_info[project] = expect_cost
        investment_risk[project] = risk

    # Inicializa uma declaração do problema
    prob = LpProblem(name="Maximizar retorno", sense=LpMaximize)

    # Define as variáveis de decisão
    decision_variable = LpVariable.dicts(
        name="Selecionado", indices=projects, lowBound=0, upBound=1, cat=LpBinary)

    # Definição da função objetiva maximizar Z = Σ (retorno_esperado * variavel de decisão) para todos os projetos project
    prob += lpSum(expect_return_info[project] *
                  decision_variable[project] for project in projects)

    # Restrição: Orçamento total
    prob += constraint_total_budget(projects=projects,
                                    decision_variable=decision_variable, expected_cost_info=expected_cost_info)

    # Restrição: Pelo menos 1 investimento de risco alto
    prob += constraint_at_least_one_high_risk_investment(
        projects=projects, decision_variable=decision_variable, investment_risk=investment_risk)

    # Restrição: Pelo menos 2 investimentos de risco médio
    prob += constraint_at_least_two_medium_risk_investment(
        projects=projects, decision_variable=decision_variable, investment_risk=investment_risk)

    # Restrição: Pelo menos 2 investimentos de risco baixo
    prob += constraint_at_least_two_low_risk_investment(
        projects=projects, decision_variable=decision_variable, investment_risk=investment_risk)

    # Restrição: Custo máximo para investimentos de risco baixo
    prob += constraint_maximum_cost_for_low_risk_investments(
        projects=projects, decision_variable=decision_variable, expected_cost_info=expected_cost_info, investment_risk=investment_risk)

    # Restrição: Custo máximo para investimentos de risco médio
    prob += constraint_maximum_cost_for_medium_risk_investments(
        projects=projects, decision_variable=decision_variable, expected_cost_info=expected_cost_info, investment_risk=investment_risk)

    # Restrição: Custo máximo para investimentos de risco alto
    prob += constraint_maximum_cost_for_high_risk_investments(
        projects=projects, decision_variable=decision_variable, expected_cost_info=expected_cost_info, investment_risk=investment_risk)

    # Resolver o problema
    status = prob.solve()

    if status == 1:  # Problema resolvido com sucesso
        # Imprimir a solução
        print("Solução encontrada:")

        # Imprimindo a solução
        print("Status:", LpStatus[prob.status])
        print("Retorno Total Esperado: R$", value(prob.objective))

        for project in projects:
            if decision_variable[project].value() == 1:
                print(
                    f"Projeto {project}: Retorno Esperado = {expect_return_info[project]}, Custo = {expected_cost_info[project]}, Risco = {investment_risk[project]}")
    else:
        print("Não foi encontrada uma solução ótima.")


if __name__:
    main()

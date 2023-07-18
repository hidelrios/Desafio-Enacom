from pulp import LpMaximize, LpProblem, LpStatus, LpVariable
import pandas as pd


def constraint_total_budget(projects: list, decision_variable: list, expected_cost_info: list, total_budget: int):
    return sum(expected_cost_info[i] * decision_variable[i] for i in range(len(projects))) <= total_budget


def constraint_at_least_one_high_risk_investment(projects: list, decision_variable: list, investment_risk: list):
    return sum(decision_variable[i] for i in range(len(projects)) if investment_risk[i] == 'Alto') >= 1


def constraint_at_least_two_medium_risk_investment(projects: list, decision_variable: list, investment_risk: list):
    return sum(decision_variable[i] for i in range(len(projects)) if investment_risk[i] == 'Médio') >= 2


def constraint_at_least_two_low_risk_investment(projects: list, decision_variable: list, investment_risk: list):
    return sum(decision_variable[i] for i in range(len(projects)) if investment_risk[i] == 'Baixo') >= 2


def constraint_maximum_cost_for_low_risk_investments(projects: list, decision_variable: list, expected_cost_info: list, investment_risk: list, low_maximum_cost: int):
    return sum(expected_cost_info[i] * decision_variable[i] for i in range(len(projects)) if investment_risk[i] == 'Baixo') <= low_maximum_cost


def constraint_maximum_cost_for_medium_risk_investments(projects: list, decision_variable: list, expected_cost_info: list, investment_risk: list, average_maximum_cost: int):
    return sum(expected_cost_info[i] * decision_variable[i] for i in range(len(projects)) if investment_risk[i] == 'Médio') <= average_maximum_cost


def constraint_maximum_cost_for_high_risk_investments(projects: list, decision_variable: list, expected_cost_info: list, investment_risk: list, cost_maximum_high: int):
    return sum(expected_cost_info[i] * decision_variable[i] for i in range(len(projects)) if investment_risk[i] == 'Alto') <= cost_maximum_high


def optimizer(projects: list, expect_return_info: list, expected_cost_info: list, investment_risk: list, total_budget: int, cost_maximum_high: int, low_maximum_cost: int, average_maximum_cost: int):

    # Cria o problema de maximização
    problem = LpProblem("Otimização de Projetos", LpMaximize)

    # Definir variáveis de decisão
    xi = []
    for i in range(len(projects)):
        xi.append(LpVariable(f"x_{i}", lowBound=0, upBound=1, cat='Binary'))

    # Definir função objetivo
    objective_function = sum(
        expect_return_info[i] * xi[i] for i in range(len(projects)))
    problem.setObjective(objective_function)

    # Definir restrições
    # Restrição de orçamento total
    total_budget_restriction = constraint_total_budget(
        projects=projects, decision_variable=xi, expected_cost_info=expected_cost_info, total_budget=total_budget)
    problem.addConstraint(total_budget_restriction)

    # Restrição de pelo menos 1 investimento de risco alto
    high_risk_constrain = constraint_at_least_one_high_risk_investment(
        projects=projects, decision_variable=xi, investment_risk=investment_risk)
    problem.addConstraint(high_risk_constrain)

    # Restrição de pelo menos 2 investimentos de risco médio
    medium_risk_constrain = constraint_at_least_two_medium_risk_investment(
        projects=projects, decision_variable=xi, investment_risk=investment_risk)
    problem.addConstraint(medium_risk_constrain)

    # Restrição de pelo menos 2 investimentos de risco baixo
    low_risk_constrain = constraint_at_least_two_low_risk_investment(
        projects=projects, decision_variable=xi, investment_risk=investment_risk)
    problem.addConstraint(low_risk_constrain)

    # Restrição de custo máximo para investimentos de risco baixo
    constraint_cost_low = constraint_maximum_cost_for_low_risk_investments(
        projects=projects, decision_variable=xi, investment_risk=investment_risk, expected_cost_info=expected_cost_info, low_maximum_cost=low_maximum_cost)
    problem.addConstraint(constraint_cost_low)

    # Restrição de custo máximo para investimentos de risco médio
    constraint_cost_medium = constraint_maximum_cost_for_medium_risk_investments(
        projects=projects, decision_variable=xi, investment_risk=investment_risk, expected_cost_info=expected_cost_info, average_maximum_cost=average_maximum_cost)
    problem.addConstraint(constraint_cost_medium)

    # Restrição de custo máximo para investimentos de risco alto
    constraint_cost_high = constraint_maximum_cost_for_high_risk_investments(
        projects=projects, decision_variable=xi, investment_risk=investment_risk, expected_cost_info=expected_cost_info, cost_maximum_high=cost_maximum_high)
    problem.addConstraint(constraint_cost_high)

    # Resolver o problema
    status = problem.solve()

    if status == 1:  # Problema resolvido com sucesso
        print("Solução encontrada:")
        for i, value in enumerate(projects):
            if xi[i].value() == 1:
                print(
                    f"Projeto {i} - {value}: Retorno Esperado = {expect_return_info[i]}, Custo = {expected_cost_info[i]}, Risco = {investment_risk[i]}")
        return "Problema resolvido com sucesso"
    else:
        return "Não foi encontrada uma solução ótima"


def main():

    # Carrega informações
    df = pd.read_csv(r'D:\Projetos\Desafio Enacom\teste.csv', sep=';')

    # Retorno esperado de cada projeto
    expect_return_info = []
    
    # Custo de cada projeto
    expected_cost_info = []

    # Risco do investimento
    investment_risk = []

    # Projetos
    projects = []

    # Dados de exemplo
    total_budget = 2400000
    low_maximum_cost = 1200000
    average_maximum_cost = 1500000
    cost_maximum_high = 900000

    # Tratamento das informações do arquivo
    for index, line in df.iterrows():
        project = line['Descrição']
        expect_return = line['Retorno esperado (R$)']
        expect_cost = line['Custo do investimento (R$)']
        risk = line['Risco do investimento']

        projects.append(project)
        expect_return_info.append(expect_return)
        expected_cost_info.append(expect_cost)
        investment_risk.append(risk)

    optimizer(projects=projects, expect_return_info=expect_return_info, expected_cost_info=expected_cost_info, investment_risk=investment_risk,
               total_budget=total_budget, cost_maximum_high=cost_maximum_high, low_maximum_cost=low_maximum_cost, average_maximum_cost=average_maximum_cost)



if __name__ == '__main__':
    main()

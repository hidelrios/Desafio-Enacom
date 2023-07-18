import unittest
from main import *
from pulp import *


class TestOptimizer(unittest.TestCase):

    def setUp(self):
        self.projects = ['Ampliação da capacidade do armazém ZDP em 5%', 'Ampliação da capacidade do armazém MGL em 7%', 
                         'Compra de empilhadeira', 'Projeto de P&D I', 'Projeto de P&D II', 'Aquisição de novos equipamentos', 
                         'Capacitação de funcionários','Ampliação da estrutura de carga rodoviária', 'Construção de datacenter',
                         'Aquisição de empresa concorrente', 'Compra de serviços em nuvem', 'Criação de aplicativo mobile e desktop', 
                         'Terceirizar serviço de otimização da logística']
        self.expect_return = [410000, 330000, 140000, 250000, 320000,
                              320000, 90000, 190000, 120000, 450000, 80000, 120000, 380000]
        self.expected_cost = [470000, 400000, 170000, 270000, 340000,
                              230000, 50000, 440000, 320000, 800000, 120000, 150000, 300000]
        self.investment_risk = ['Baixo', 'Baixo', 'Médio', 'Médio', 'Médio',
                                'Médio', 'Médio', 'Alto', 'Alto', 'Alto', 'Baixo', 'Baixo', 'Médio']
        self.decision_variable = [LpVariable(
            f"x_{i}", lowBound=0, upBound=1, cat='Binary') for i in range(len(self.projects))]

    # Testa restrição orçamentaria total
    def test_total_budget_constraint(self):
        self.assertTrue(constraint_total_budget(projects=self.projects, decision_variable=self.decision_variable,
                        total_budget=2400000, expected_cost_info=self.expected_cost))

    # Testa se pelo menos 1 investimento de risco alto deve ser selecionado
    def test_constraint_at_least_one_high_risk_investment(self):
        self.assertTrue(constraint_at_least_one_high_risk_investment(
            self.projects, decision_variable=self.decision_variable, investment_risk=self.investment_risk))

    # Testa se pelo menos 2 investimento de risco medio deve ser selecionado
    def test_constraint_at_least_two_medium_risk_investment(self):
        self.assertTrue(constraint_at_least_two_medium_risk_investment(
            projects=self.projects, decision_variable=self.decision_variable, investment_risk=self.investment_risk))

    # Testa se pelo menos 2 investimento de risco baixo deve ser selecionado
    def test_constraint_at_least_two_low_risk_investment(self):
        self.assertTrue(constraint_at_least_two_low_risk_investment(projects=self.projects,
                        decision_variable=self.decision_variable, investment_risk=self.investment_risk))

    # Testa o custo máximo para investimentos de baixo risco
    def test_constraint_maximum_cost_for_low_risk_investments(self):
        self.assertTrue(constraint_maximum_cost_for_low_risk_investments(projects=self.projects, decision_variable=self.decision_variable,
                        expected_cost_info=self.expected_cost, investment_risk=self.investment_risk, low_maximum_cost=1200000))

    # Testa o custo máximo para investimentos de médio risco
    def test_constraint_maximum_cost_for_medium_risk_investments(self):
        self.assertTrue(constraint_maximum_cost_for_medium_risk_investments(projects=self.projects, decision_variable=self.decision_variable,
                        expected_cost_info=self.expected_cost, investment_risk=self.investment_risk, average_maximum_cost=1500000))

    # Testa o custo máximo para investimentos de baixo risco
    def test_constraint_maximum_cost_for_high_risk_investments(self):
        self.assertTrue(constraint_maximum_cost_for_high_risk_investments(projects=self.projects, decision_variable=self.decision_variable,
                        expected_cost_info=self.expected_cost, investment_risk=self.investment_risk, cost_maximum_high=900000))

    def test_optimizer_sucess(self):
        self.assertEqual(optimizer(projects=self.projects, expected_cost_info=self.expected_cost, expect_return_info=self.expect_return, investment_risk=self.investment_risk,
                         total_budget=2400000, low_maximum_cost=1200000, average_maximum_cost=1500000, cost_maximum_high=900000), "Problema resolvido com sucesso")

    def test_optimizer_failed(self):
        projects = ['projeto1', 'projeto2', 'projeto3', 'projeto4']
        expect_return = [1000000, 1500000,  2000000,  1200000]
        expected_cost = [8000000, 5000000, 7000000, 4000000]
        investment_risk = ['Baixo',  'Médio',  'Alto', 'Médio']
        self.assertEqual(optimizer(projects=projects, expected_cost_info=expected_cost, expect_return_info=expect_return, investment_risk=investment_risk,
                         total_budget=2400000, low_maximum_cost=1200000, average_maximum_cost=1500000, cost_maximum_high=900000), "Não foi encontrada uma solução ótima")


if __name__ == '__main__':
    unittest.main()

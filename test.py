import unittest
from main import *
from pulp import *


class TestTotalBudgetConstraint(unittest.TestCase):

    def set_up(self):
        self.projetos = ['projeto1','projeto2','projeto3','projeto4']
        self.retornos = {'projeto1': 100000, 'projeto2': 150000, 'projeto3': 200000, 'projeto4': 120000}
        self.custos = {'projeto1': 800000, 'projeto2': 500000, 'projeto3': 700000, 'projeto4': 400000}
        self.riscos = {'projeto1': 'Baixo', 'projeto2': 'Médio', 'projeto3': 'Alto', 'projeto4': 'Médio'}
        self.limite_custos = {'Baixo': 1200000, 'Médio': 1500000, 'Alto': 900000}
        self.decision_variable = LpVariable.dicts(name="Selecionado", indices=self.projetos, lowBound=0, upBound=1, cat=LpBinary)

    def test_total_budget_constraint(self):
        self.assertTrue(constraint_total_budget(self.projetos, self.decision_variable, self.retornos))

    def test_constraint_at_least_one_high_risk_investment(self):
        self.assertTrue(constraint_at_least_one_high_risk_investment(self.projetos, self.decision_variable, self.riscos))

    def test_constraint_at_least_two_medium_risk_investment(self):
        self.assertTrue(constraint_at_least_two_medium_risk_investment(self.projetos, self.decision_variable, self.riscos))

    def test_constraint_at_least_two_low_risk_investment(self):
        self.assertTrue(constraint_at_least_two_low_risk_investment(self.projetos, self.decision_variable, self.riscos))

    def test_constraint_maximum_cost_for_low_risk_investments(self):
        self.assertTrue(constraint_maximum_cost_for_low_risk_investments(self.projetos, self.decision_variable,self.custos, self.riscos))

    def test_constraint_maximum_cost_for_medium_risk_investments(self):
        self.assertTrue(constraint_maximum_cost_for_medium_risk_investments(self.projetos, self.decision_variable,self.custos, self.riscos))

    def test_constraint_maximum_cost_for_high_risk_investments(self):
        self.assertTrue(constraint_maximum_cost_for_high_risk_investments(self.projetos, self.decision_variable,self.custos, self.riscos))
    



if __name__ == '__main__':
    unittest.main()
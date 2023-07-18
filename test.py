import unittest
from main import *
from pulp import *


class TestTotalBudgetConstraint(unittest.TestCase):

    def setUp(self):
        self.projects = ['projeto1','projeto2','projeto3','projeto4']
        self.expect_return = [100000, 150000,  200000,  120000]
        self.expected_cost = [800000, 500000, 700000, 400000]
        self.investment_risk = ['Baixo',  'Médio',  'Alto', 'Médio']
        self.decision_variable = [LpVariable(f"x_{i}", lowBound=0, upBound=1, cat='Binary') for i in range(len(self.projects))]

    def test_total_budget_constraint(self):
        self.assertTrue(constraint_total_budget(projects=self.projects,decision_variable= self.decision_variable, total_budget=2400000, expected_cost_info=self.expected_cost))

    def test_constraint_at_least_one_high_risk_investment(self):
        self.assertTrue(constraint_at_least_one_high_risk_investment(self.projects,decision_variable= self.decision_variable,investment_risk= self.investment_risk))

    def test_constraint_at_least_two_medium_risk_investment(self):
        self.assertTrue(constraint_at_least_two_medium_risk_investment(projects=self.projects, decision_variable=self.decision_variable, investment_risk=self.investment_risk))

    def test_constraint_at_least_two_low_risk_investment(self):
        self.assertTrue(constraint_at_least_two_low_risk_investment(projects=self.projects,decision_variable= self.decision_variable, investment_risk=self.investment_risk))

    def test_constraint_maximum_cost_for_low_risk_investments(self):
        self.assertTrue(constraint_maximum_cost_for_low_risk_investments(projects=self.projects,decision_variable= self.decision_variable,expected_cost_info=self.expected_cost, investment_risk=self.investment_risk,low_maximum_cost=1200000))

    def test_constraint_maximum_cost_for_medium_risk_investments(self):
        self.assertTrue(constraint_maximum_cost_for_medium_risk_investments(projects=self.projects,decision_variable= self.decision_variable,expected_cost_info=self.expected_cost, investment_risk=self.investment_risk,average_maximum_cost=1500000))

    def test_constraint_maximum_cost_for_high_risk_investments(self):
        self.assertTrue(constraint_maximum_cost_for_high_risk_investments(projects=self.projects,decision_variable= self.decision_variable,expected_cost_info=self.expected_cost, investment_risk=self.investment_risk,cost_maximum_high=900000))  



if __name__ == '__main__':
    unittest.main()
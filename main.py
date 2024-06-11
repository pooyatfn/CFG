import json
from collections import defaultdict


class CFG:
    def __init__(self, v, t, p, s):
        self.v = v
        self.t = t
        self.p = p
        self.s = s

    @staticmethod
    def is_all_nullable(nullables_set: set, product: str):
        for char in product:
            if char not in nullables_set:
                return False
        return True

    def get_nullable_variables(self):
        new_null = {key for key, value in self.p.items() if '' in value}
        old_null = set()
        while old_null != new_null:
            old_null = new_null
            for key, value in self.p.items():
                any_all_nullable = False
                for item in value:
                    if self.is_all_nullable(old_null, item):
                        any_all_nullable = True
                        break
                if any_all_nullable:
                    new_null.update(key)

        return new_null

    def get_non_nullable_productions(self, production: str, nullables_set: set) -> set:
        res = set()
        size = len(production)
        if size < 1:
            return res
        for index in range(len(production)):
            if production[index] in nullables_set:
                res.update(
                    self.get_non_nullable_productions(production[:index] + production[index + 1:], nullables_set))
        res.add(production)

        return res

    def remove_lambda_rules(self):
        nullables = self.get_nullable_variables()

        res = defaultdict(lambda: [])
        for var, prods in self.p.items():
            for prod in prods:
                res[var] += self.get_non_nullable_productions(prod, nullables)
        if self.s in nullables:
            res[self.s].append('')

        res = {key: set(values) for key, values in res.items()}

        self.p = res

    def remove_unit_rules(self):
        new_values = self.p.copy()
        old_values = dict()
        while old_values != new_values:
            old_values = {key: values.copy() for key, values in new_values.items()}
            for key, values in new_values.items():
                for value in values:
                    if value in new_values.keys():
                        to_be_added = new_values[value].copy()
                        if key in to_be_added:
                            to_be_added.remove(key)
                        new_values[key].update(to_be_added)
                        new_values[key].remove(value)
                        break

        new_values = {key: set(values) for key, values in new_values.items()}
        self.p = new_values

    def remove_non_first_kind_useful_variable(self):
        old_variables = set()
        new_variables = set()
        for key, values in self.p.items():
            for value in values:
                if all(character in self.t for character in value):
                    new_variables.add(key)

        while old_variables != new_variables:
            old_variables = new_variables.copy()
            for key, values in self.p.items():
                for value in values:
                    should_add = True
                    for character in value:
                        if character in self.v and character not in old_variables:
                            should_add = False
                    if should_add:
                        new_variables.add(key)

        self.v = new_variables

    def remove_non_second_kind_useful_variable(self):
        old_variables = set()
        new_variables = set(self.s)

        while old_variables != new_variables:
            old_variables = new_variables.copy()
            for key, values in self.p.items():
                for value in values:
                    for character in value:
                        if character in self.v and key in new_variables:
                            new_variables.add(character)

        self.v = new_variables

    def remove_useless_productions_till_now(self):
        useful_productions: dict[str, list[str]] = {variable: self.p[variable].copy() for variable in self.v}
        for useful_variable in self.v:
            for value in self.p[useful_variable]:
                for character in value:
                    if character not in self.t and character not in self.v:
                        useful_productions[useful_variable].remove(value)
        self.p = useful_productions

    def remove_all_useless_productions(self):
        self.remove_non_first_kind_useful_variable()
        self.remove_useless_productions_till_now()
        self.remove_non_second_kind_useful_variable()
        self.remove_useless_productions_till_now()

    def simplify_cfg(self):
        self.remove_lambda_rules()
        self.remove_unit_rules()
        self.remove_all_useless_productions()

    def __str__(self):
        return f"""{{\n\tV: {self.v}\n\tT: {self.t}\n\tP: {self.p}\n\tS: {self.s}\n}}"""


with open("context_free_grammers.json") as file:
    test_cases = json.load(file)
    for num, test_case in test_cases.items():
        cfg = CFG(test_case["V"], test_case["T"], test_case["P"], test_case["S"])
        cfg.simplify_cfg()
        print(f"CFG {num} without lambda rules, unit rules and useless products: {cfg}")

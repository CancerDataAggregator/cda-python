import Q
def And(self, right: "Q"):
    return Q(self.query, "AND", right.query)

def Or(self, right: "Q"):
    return Q(self.query, "OR", right.query)

def From(self, right: "Q"):
    return Q(self.query, "SUBQUERY", right.query)

def Not(self):
    return Q(self.query, "NOT", None)
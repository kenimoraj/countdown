from collections import deque

OPERATORS = ["+", "-","*","/"]


def gcd(a, b):
    # print(a,b)
    if a < 0:
        a = -a
    if b < 0:
        b = -b

    x = max(a,b)
    y = min(a,b)
    if x == y:
        return x
    elif y == 1:
        return 1
    else:

        r = x % y
        if r == 0:
            return y
        else:
            return gcd(y, r)


class Fraction:
    def __init__(self,l,m):
        if l == 0:
            self.l = 0
            self.m = 1
        else:
            self.l = int(l/gcd(l,m))
            self.m = int(m/gcd(l,m))

    def __str__(self):
        if self.m > 1:
            return str(self.l)+"/"+str(self.m)
        else:
            return str(self.l)

    def add(self,other):
        newL = self.l*other.m + self.m*other.l
        newM = self.m*other.m

        return Fraction(newL,newM)

    def subtract(self,other):
        newL = self.l*other.m - self.m*other.l
        newM = self.m*other.m

        return Fraction(newL,newM)

    def multiply(self,other):
        newL = self.l*other.l
        newM = self.m*other.m

        return Fraction(newL,newM)

    def divide(self,other):
        newL = self.l*other.m
        newM = self.m*other.l

        return Fraction(newL,newM)

    def equals(self, other):

        return self.l == other.l and self.m == other.m


def get_bracket_pairs(expr: str):

    if expr is None:
        return None

    stack = deque()
    res = []
    for i in range(len(expr)):
        if expr[i] == '(':
            stack.append(i)
        elif expr[i] == ')':
            res.append((stack.pop(), i))
    res.sort(key=lambda x: x[0])
    return res


def choose(nums: list, k:int):
    nums_c = nums.copy()
    if k == 1:
        return [[n] for n in nums]


    res = []
    for i in range(len(nums)):

        x = nums_c.pop(0)
        nums_cc = nums_c.copy()
        prev = choose(nums_cc, k - 1)

        res += [[x]+p for p in prev]

    return res



def frac_eval(x: Fraction, y: Fraction, op: str) -> Fraction:
    if op == "+":
        return x.add(y)
    elif op == "-":
        return x.subtract(y)
    elif op == "*":
        return x.multiply(y)
    elif op == "/":
        return x.divide(y)


def possible_operations(k):
    li = OPERATORS.copy()
    if k == 0:
        return []
    if k == 1:
        return li

    prev = possible_operations(k - 1)
    result = []
    for p in prev:
        for l in li:
            result.append(p+l)

    return result


def evaluate(numlist: list[Fraction], opstr: str) -> tuple[str, Fraction]:
    result = numlist[0]
    resultstr = str(result)
    for i in range(len(opstr)):
        result = frac_eval(result, numlist[i+1], opstr[i])
        resultstr = f"(({resultstr}){opstr[i]}{numlist[i+1]})"
    return (resultstr, result)


def get_ans_numbers(goal: Fraction, nums: list[Fraction]):

    nums = [n for n in nums if n.l != 0]
    for n in nums:
        if n.equals(goal):
            return f"({n})"

    for k in range(2,6):
        choices = choose(nums, k)

        if len(choices) == 0:
            continue

        choices_set = []
        for cc in choices:
            if cc not in choices_set:
                choices_set.append(cc)

        poss_ops = possible_operations(k - 1)

        for c in choices_set:

            for op in poss_ops:

                xstr, x = evaluate(c,op)

                nums_c = nums.copy()

                for c_i in range(len(c)):
                    nums_c.remove(c[c_i])

                if x.equals(goal):
                    return xstr

                prev = get_ans_numbers(goal.subtract(x), nums_c)

                if prev is not None:
                    return f"({prev})+({xstr})"

                prev = get_ans_numbers(goal.add(x), nums_c)
                if prev is not None:
                    return f"({prev})-({xstr})"

                prev = get_ans_numbers(x.subtract(goal), nums_c)
                if prev is not None:
                    return f"({xstr})-({prev})"

                if x.l not in [0, 1]:

                    prev = get_ans_numbers(goal.divide(x), nums_c)
                    if prev is not None:
                        return f"({prev})*({xstr})"

                    prev = get_ans_numbers(goal.multiply(x), nums_c)
                    if prev is not None:
                        return f"({prev})/({xstr})"

                if goal.l not in [0, 1]:
                    prev = get_ans_numbers(x.divide(goal), nums_c)
                    if prev is not None:
                        return f"({xstr})/({prev})"


def simplify(expr: str):
    #Remove redundant brackets
    nonred_bra = []
    pairs = get_bracket_pairs(expr)
    for pair in pairs:
        left, right = pair[0], pair[1]
        subs = expr[left + 1: right]
        l = None
        r = None
        if left > 0:
            l = expr[left - 1]
        if right < len(expr) - 1:
            r = expr[right + 1]
        if "/" in [l,r]:
            if "*" in subs or "/" in subs:
                nonred_bra.append(pair)
        if l in ["*", "/", "-"] or r in ["*", "/"]:
            if ("+" in subs) or ("-" in subs):
                nonred_bra.append(pair)
    red_bra = [p for p in pairs if p not in nonred_bra]
    indices = [i for r in red_bra for i in r]
    result = ""
    for i in range(len(expr)):
        if i not in indices:
            result += expr[i]
    return result

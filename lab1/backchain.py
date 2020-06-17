from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

# A few restriction: Antecedents are not nested. Only consider AND and OR ops.

def backchain_to_goal_tree(rules, hypothesis):
    ors = [hypothesis]
    for rule in rules:
      consequents = rule.consequent()
      for consequent in consequents:

        matched_vars = match(consequent, hypothesis)

        # matched_vars match
        if matched_vars or consequent == hypothesis:
          antecedent = rule.antecedent()
          if isinstance(antecedent, str):
            populated = populate(antecedent, matched_vars)
            ors.append(populated)
            ors.append(backchain_to_goal_tree(rules, populated))
          else:
            ante_rules = [populate(rule, matched_vars) for rule in antecedent]
            ante_res = [backchain_to_goal_tree(rules, ante_rule) for ante_rule in ante_rules]
            if isinstance(antecedent, AND):
              ors.append(AND(ante_res))
            elif isinstance(antecedent, OR):
              ors.append(OR(ante_res))
            
    return simplify(OR(ors))


# Here's an example of running the backward chainer - uncomment
# it to see it work:
# print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')



def op_dup(stack):
    if len(stack) < 1:
        return False
    stack.append(stack[-1])
    return True
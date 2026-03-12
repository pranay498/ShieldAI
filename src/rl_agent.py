import random
import numpy as np

# possible states (threat levels)
states = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

# possible actions
actions = ["LOG", "ALERT", "BLOCK", "ISOLATE"]

# Q-table
q_table = np.zeros((len(states), len(actions)))

learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.2


def choose_action(state):

    state_index = states.index(state)

    if random.random() < epsilon:
        action_index = random.randint(0,3)
    else:
        action_index = np.argmax(q_table[state_index])

    return actions[action_index], state_index, action_index


def update_q_table(state_index, action_index, reward):

    best_next = np.max(q_table[state_index])

    q_table[state_index][action_index] = (
        q_table[state_index][action_index] +
        learning_rate * (reward + discount_factor * best_next - q_table[state_index][action_index])
    )


def get_reward(action, threat):

    if threat == "CRITICAL" and action in ["BLOCK","ISOLATE"]:
        return 10

    if threat == "HIGH" and action == "BLOCK":
        return 8

    if threat == "MEDIUM" and action == "ALERT":
        return 5

    if threat == "LOW" and action == "LOG":
        return 3

    return -3
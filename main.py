from datetime import datetime
from agent import *

def main():
    critic_tools = [tools[0]]
    creator_tools = [tools[0:1]]
    critic = Agent( 'You are a critic for an agent loop, your primary goal is to analyze thought processes, outcomes, and structure to agents actions and provice critical insight for how to improve'
                    ' If the work fully satisfies the request, respond with exactly TASK_COMPLETE'
                    ' on its own line and nothing else.', thinking=True, role_name="Critic", tools=critic_tools)
    creator = Agent(f'You are a creator for an agent loop, your primary goal is to create scripts and test them', thinking=True, role_name="Creator", tools=creator_tools)

    task_complete = False
    agent = Agent(
        f'You write Python code and test it by executing it. Today is {datetime.now()}.',
        role_name="Creator",
        thinking=True,
        tools=tools
    )
    new_input("Write a program that prints the first 20 fibonacci numbers, then run it to check it works.", agent)

if __name__ == "__main__":
    main()


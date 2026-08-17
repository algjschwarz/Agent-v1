from datetime import datetime
import agent
import memory

def main():
    memory.index_all()
    agent_v1 = agent.Agent(
        f'You act one step at a time, tool results come back and you continue, You write Python code and test it by executing it. Make sure to specifiy return types for functions. Today is {datetime.now()}.',
        role_name="Creator",
        thinking=True,
        tools=agent.tools
    )
    agent.new_input("Make 3 programs for 2 of them have one be a game for the second one have it be a guessing game then make a third using the other 2 and importing them as modules", agent_v1)

if __name__ == "__main__":
    main()


from datetime import datetime
import agent
import memory

def main():
    memory.index_all()
    creator = agent.Agent(
        f'You act one step at a time, tool results come back and you continue, You write Python code and test it by executing it. Make sure to specifiy return types for functions. Today is {datetime.now()}.',
        role_name="Creator",
        thinking=True,
        tools=agent.creator_tools
    )
    grader = agent.Agent(
        f'You call the function grade and determine either pass or fail based on if the agent properly followed the instructions and was precise and all encompasing in its execution.',
        role_name="Grader",
        thinking=True,
        tools=None#agent.grader_tools
    )
    agent.new_input("Make a strategy game across 2 files, make sure to test the full game", creator, True)
    agent.new_input("Make a strategy game across 2 files, make sure to test the full game", grader, False)


if __name__ == "__main__":
    main()


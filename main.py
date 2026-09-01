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
    grader = agent.Grader(
        f'You call the tool grade and determine either pass or fail based on if the agent properly followed the instructions and if the program it created does as well',
        role_name="Grader",
        thinking=True,
        tools=None#agent.grader_tools
    )
    creator.new_input("Make a file that says hi when ran", recall_enabled=True)
    grader.grade(creator)


if __name__ == "__main__":
    main()


from datetime import datetime
import agent
import memory
import tools

def main():
    memory.index_all_scripts()
    creator_system_prompt = f"""You act one step at a time, tool results come back and you continue, 
    If recall_scripts returns a script similar to what you are about to write call the tool "read_file" to check if it is sufficient. 
    Else you write Python code and test it by executing it. Make sure to specifiy return types for functions. Today is {datetime.now()}."""
    grader_system_prompt = f'Create a plan to test a program, execute those tests and then call the tool "grade" if all tests pass, send True else send false.'
    creator = agent.Agent(
        creator_system_prompt,
        role_name="Creator",
        thinking=True,
        tools=agent.creator_tools
    )
    grader = agent.Grader(
        grader_system_prompt,
        role_name="Grader",
        thinking=True,
        tools=agent.grader_tools
    )
    tools.agents = {creator.role_name : creator, grader.role_name : grader}

    orchastrator = agent.Agent(
        f"""You are an orchastrator who creates according to the user's input, high level plans and call tool 
        'delegate' to delgate lower levels tasks to these agents: {list(tools.agents.keys())}. 
        The agent's system prompts are '{creator_system_prompt}' and {grader_system_prompt}.""",
        role_name="Orchastrator",
        thinking=True,
        tools=agent.orchastrator_tools
    )
    orchastrator.new_input(input("Please input command for agent-v1: "), recall_enabled=False)   

if __name__ == "__main__":
    main()


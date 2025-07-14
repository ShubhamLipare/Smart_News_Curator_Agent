from langchain_core.prompts import ChatPromptTemplate

critic_template = """
You are an expert AI summarization critic.

Here is the summary to review:

{summary}

Evaluate the above summary and write Revised summary again if it required improvements :
- Is it too vague or generic?
- Does it lack specificity, facts, or examples?
- Could it be improved?

Respond using **this exact format**:

Evaluation: <write your critique here>

Revised Summary (if needed): <write your improved version here, write in bullet points. 1. 2. 3. >

"""

critic_prompt=ChatPromptTemplate.from_template(template=critic_template)
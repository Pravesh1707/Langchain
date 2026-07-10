

from langchain_core.prompts import PromptTemplate

template = PromptTemplate(template=""" You are an Senior {role} working in a 
                        company. You always have a {goal} in mind and you have {context} """,
                        input_variables=['role','goal','context'],validate_template=True)

template.save('pPromptT.json')
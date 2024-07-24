import openai

openai.api_key = "sk-proj-FvBebI9JwyY8I2f5e0HAT3BlbkFJJryzLp3H5CKkFEPnZ1qi"



def generate_insights(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, max_tokens=1000
    )
    return response.choices[0].text.strip()
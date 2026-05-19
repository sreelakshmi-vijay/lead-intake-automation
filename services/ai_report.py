import ollama


def generate_ai_report(company_data):

    prompt = f"""You are a senior B2B growth consultant. Generate a professional audit report.

    Use EXACTLY this format:

    Business Summary:
    ...

    Website Strengths:
    ...

    Website Weaknesses:
    ...

    SEO Improvements:
    ...

    Growth Opportunities:
    ...

    Automation Suggestions:
    ...

    Personalized Outreach:
    ...

    Company Data:
    {company_data}

    Keep it highly personalized and professional.
    """

    response = ollama.chat(
        model='mistral:7b',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    return response['message']['content']
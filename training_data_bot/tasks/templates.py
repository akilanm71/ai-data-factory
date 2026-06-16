class TaskTemplate:


    QA = """
Generate ONE question-answer pair from the text.

Return exactly in this format:

Question: <question>
Answer: <answer>

Text:
{text}
"""

    CLASSIFICATION = """
Classify the text.

Return exactly:

Label: <label>
Text:
{text}
"""

    SUMMARIZATION = """
Summarize the text.

Return exactly:

Summary: <summary>

Text:
{text}
"""


class PubMedTemplate:

    RESEARCH_SUMMARY = """
You are a biomedical research analyst.

Analyze the provided PubMed abstracts.

Return:

Research Topic:
<topic>

Key Findings:
<bullet points>

Clinical Implications:
<clinical impact>

Limitations:
<limitations>

Overall Summary:
<summary>

Text:
{text}
"""

    LITERATURE_REVIEW = """
Generate a literature review.

Return:

Background
Methods
Key Findings
Research Gaps
Future Directions

Text:
{text}
"""

    CLINICAL_SUMMARY = """
Generate a physician-focused summary.

Return:

Disease
Treatment Options
Clinical Outcomes
Recommendations

Text:
{text}
"""


    RESEARCH_GAP = """
Analyze the papers.

Return:

Current State
Limitations
Unanswered Questions
Future Research Directions

Text:
{text}
"""

    @staticmethod
    def custom_prompt(task):

        return f"""
You are a biomedical research analyst.

Task: 
{task}

Text:
{{text}}

Answer:
"""
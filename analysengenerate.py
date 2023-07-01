import openai

# Set up OpenAI API credentials
openai.api_key = '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'

# Define the biology themes
themes = [
    'Cell Biology',
    'Genetics',
    'Ecology',
    'Human Physiology',
    'Evolution',
    'Plant Biology',
    'Human Health and Disease',
    'Enzymes',
    'Reproduction',
    'Biotechnology'
]


# Function to classify the theme based on the paragraph
def classify_mistake(paragraph):
    # Concatenate the themes and paragraph
    input_text = 'Here are 10 biology themes:'.join(themes) + '\n Your task is to read paragraph below ' \
                                                              'and write the name of theme from previous themes, which is recommended to revise' + paragraph

    # Use OpenAI API to generate the classification
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=input_text,
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the predicted theme
    predicted_theme = response.choices[0].text.strip()

    return predicted_theme

# Example usage
biology_paragraph = "Cell Biology, Genetics, Ecology, Human Physiology, Evolution, Plant Biology, Human Health and Disease, Enzymes, Reproduction, and Biotechnology are all fascinating themes in the field of biology. Cell Biology explores the structure and function of cells, which are the fundamental units of life. Genetics delves into the study of heredity and the role of genes in determining traits. Ecology examines the interactions between organisms and their environment. Human Physiology focuses on the functioning of the human body's various systems. Evolution explains the process of species change over time through natural selection. Plant Biology investigates the life processes and adaptations of plants. Human Health and Disease explores the factors that influence well-being and the development of illnesses. Enzymes are crucial biological catalysts that facilitate chemical reactions in living organisms. Reproduction is the process by which living organisms produce offspring. Finally, Biotechnology involves the use of biological systems and organisms to develop useful products and technologies."
mistake_theme = classify_mistake(biology_paragraph)
print(mistake_theme)
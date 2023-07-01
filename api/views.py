from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from hackapp.models import Questions
import openai

openai.api_key = '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'

@api_view(['GET'])
def users(request):
    serializer = RegistrationSerializer(data=request.data)
    users = User.objects.all()
    user_data = []
    for user in users:
        user_data.append({
            'id': user.id,
            'username': user.username,
        })
    return Response(user_data)

@api_view(['POST'])
def signup(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "Registration successful.", "user_id": user.id})
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({"message": "Login successful."})
    else:
        return Response({"message": "Invalid username or password."}, status=401)


@api_view(['POST'])
def image(request):
    image = request.FILES.get('image')

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

    def classify_mistake(paragraph):
        input_text = 'Here are 10 biology themes:'.join(themes) + '\n Your task is to read paragraph below ' \
                                                                  'and write the name of theme from previous themes, which is recommended to revise' + paragraph

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

        predicted_theme = response.choices[0].text.strip()

        return predicted_theme


    biology_paragraph = "Cell Biology, Genetics, Ecology, Human Physiology, Evolution, Plant Biology, Human Health and Disease, Enzymes, Reproduction, and Biotechnology are all fascinating themes in the field of biology. Cell Biology explores the structure and function of cells, which are the fundamental units of life. Genetics delves into the study of heredity and the role of genes in determining traits. Ecology examines the interactions between organisms and their environment. Human Physiology focuses on the functioning of the human body's various systems. Evolution explains the process of species change over time through natural selection. Plant Biology investigates the life processes and adaptations of plants. Human Health and Disease explores the factors that influence well-being and the development of illnesses. Enzymes are crucial biological catalysts that facilitate chemical reactions in living organisms. Reproduction is the process by which living organisms produce offspring. Finally, Biotechnology involves the use of biological systems and organisms to develop useful products and technologies."
    mistake_theme = classify_mistake(biology_paragraph)

    filtered_questions = Questions.objects.filter(theme="Cell Biology")

    question_list = [
        {'theme': question.theme, 'question': question.question}
        for question in filtered_questions
    ]

    return Response(question_list)
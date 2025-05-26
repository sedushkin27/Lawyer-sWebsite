from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'services': [
            {
                'title': 'Кримінальна практика',
                'image': 'user_image/1.png',
            },
            {
                'title': 'Адміністративна практика',
                'image': 'user_image/2.png',
            },
            {
                'title': 'Міграційні послуги',
                'image': 'user_image/3.png',
            },
            {
                'title': 'Цивільна практика',
                'image': 'user_image/4.png',
            },
            {
                'title': 'Інтелектуальна власність',
                'image': 'user_image/5.png',
            },
            {
                'title': 'Податкова практика',
                'image': 'user_image/6.png',
            },
            {
                'title': 'Військове право',
                'image': 'user_image/7.png',
            },
            {
                'title': 'Адвокат для бізнесу',
                'image': 'user_image/8.png',
            },
            {
                'title': 'Трудове право',
                'image': 'user_image/9.png',
            },
        ],

        'consultations': [
            {
                'title': 'Сімейні справи',
                'image': 'user_image/10.png',
            },
            {
                'title': 'Житлові суперечки',
                'image': 'user_image/11.png',
            },
            {
                'title': 'Мобілізація у воєнний час',
                'image': 'user_image/12.png',
            },
        ],

        'reviews': [
            {
                'name': 'Ірина Коваленко',
                'stars': 4.3,
                'text': 'Ольга Бардадим – справжній професіонал своєї справи! Допомогла мені у складній справі з спадщиною, усе пояснила доступно і оперативно вирішила питання. Рекомендую всім, хто шукає надійного адвоката!',
            },
            {
                'name': 'Олег Петренко',
                'stars': 5,
                'text': 'Дуже вдячний пані Ользі за її підтримку у судовій справі. Завдяки її знанням і впевненості ми виграли справу, хоча шанси здавалися мінімальними. 5 зірок без сумнівів!',
            },
            {
                'name': 'Марія Сидорчук',
                'stars': 3.6,
                'text': 'Звернулася до Ольги Бардадим з питанням щодо розірвання договору. Усе було зроблено якісно, хоча процес трохи затягнувся через судові нюанси. Загалом задоволена результатом.',
            },
        ],
    }
    return render(request, 'main/index.html', context)

def about(request):
    return render(request, 'main/about_me.html')
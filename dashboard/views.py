# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.views import generic
# from django.contrib.auth.decorators import login_required
# import json
# import requests
# import wikipediaapi
# from youtubesearchpython import VideosSearch
# from .forms import *

# # Create your views here.

# def home(request):
#     return render(request, 'dashboard/home.html')

# @login_required
# def notes(request):
#     if request.method == 'POST':
#         form = NotesForm(request.POST)
#         if form.is_valid():
#             notes = Notes(user=request.user, title=form.cleaned_data['title'], description=form.cleaned_data['description'])
#             notes.save()
#             messages.success(request, f"Notes added successfully!")
#     else:
#         form = NotesForm()
    
#     notes = Notes.objects.filter(user=request.user)
#     context = {'notes': notes, 'form': form}
#     return render(request, 'dashboard/notes.html', context)

# @login_required
# def delete_note(request, pk=None):
#     Notes.objects.get(id=pk).delete()
#     return redirect("notes")

# class NotesDetailView(generic.DetailView):
#     model = Notes

# @login_required  
# def homework(request):
#     if request.method == "POST":
#         form = HomeworkForm(request.POST)
#         if form.is_valid():
#             finished = request.POST.get('is_finished', 'off') == 'on'
#             homeworks = Homework(user=request.user, subject=form.cleaned_data['subject'], 
#                                  title=form.cleaned_data['title'], description=form.cleaned_data['description'],
#                                  due=form.cleaned_data['due'], is_finished=finished)
#             homeworks.save()
#             messages.success(request, 'Homework added successfully!')
#     else:
#         form = HomeworkForm()
    
#     homework_list = Homework.objects.filter(user=request.user)
#     homework_done = not homework_list.exists()
#     context = {'homeworks': homework_list, 'homeworks_done': homework_done, 'form': form}
#     return render(request, 'dashboard/homework.html', context)

# @login_required
# def update_homework(request, pk=None):
#     homework = Homework.objects.get(id=pk)
#     homework.is_finished = not homework.is_finished
#     homework.save()
#     return redirect('homework')

# @login_required
# def delete_homework(request, pk=None):
#     Homework.objects.get(id=pk).delete()
#     return redirect("homework")

# def youtube(request):
#     form = DashboardForm(request.POST or None)
#     result_list = []
#     if request.method == "POST" and form.is_valid():
#         text = form.cleaned_data['text']
#         video_search = VideosSearch(text, limit=10)
        
#         for i in video_search.result()['result']:
#             result_dict = {
#                 'input': text,
#                 'title': i['title'],
#                 'duration': i['duration'],
#                 'thumbnail': i['thumbnails'][0]['url'],
#                 'channel': i['channel']['name'],
#                 'link': i['link'],
#                 'views': i['viewCount']['short'],
#                 'published': i['publishedTime'],
#                 'description': ' '.join(desc['text'] for desc in i['descriptionSnippet']) if i['descriptionSnippet'] else '',
#             }
#             result_list.append(result_dict)
    
#     context = {'form': form, 'results': result_list}
#     return render(request, 'dashboard/youtube.html', context)

# @login_required
# def todo(request):
#     form = TodoForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         finished = request.POST.get("is_finished", 'off') == 'on'
#         todos = Todo(user=request.user, title=form.cleaned_data['title'], is_finished=finished)
#         todos.save()
#         messages.success(request, f"Todo added successfully!")
    
#     todo_list = Todo.objects.filter(user=request.user)
#     todos_done = not todo_list.exists()
#     context = {'todos': todo_list, 'form': form, 'todos_done': todos_done}
#     return render(request, "dashboard/todo.html", context)

# @login_required
# def update_todo(request, pk=None):
#     todo = Todo.objects.get(id=pk)
#     todo.is_finished = not todo.is_finished
#     todo.save()
#     return redirect('todo')

# @login_required
# def delete_todo(request, pk=None):
#     Todo.objects.get(id=pk).delete()
#     return redirect("todo")

# def books(request):
#     form = DashboardForm(request.POST or None)
#     result_list = []
#     if request.method == "POST" and form.is_valid():
#         text = form.cleaned_data['text']
#         url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#             answer = response.json()
#             for item in answer.get('items', [])[:10]:  # Limit to 10 results
#                 result_dict = {
#                     'title': item['volumeInfo'].get('title'),
#                     'subtitle': item['volumeInfo'].get('subtitle'),
#                     'description': item['volumeInfo'].get('description'),
#                     'count': item['volumeInfo'].get('pageCount'),
#                     'categories': item['volumeInfo'].get('categories'),
#                     'rating': item['volumeInfo'].get('averageRating'),
#                     'thumbnail': item['volumeInfo'].get('imageLinks', {}).get('thumbnail'),
#                     'preview': item['volumeInfo'].get('previewLink'),
#                 }
#                 result_list.append(result_dict)
#         except requests.RequestException as e:
#             messages.error(request, f"An error occurred: {e}")

#     context = {'form': form, 'results': result_list}
#     return render(request, "dashboard/books.html", context)

# def dictionary(request):
#     form = DashboardForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         text = form.cleaned_data['text']
#         url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
#         try:
#             response = requests.get(url)
#             response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
#             answer = response.json()
#             phonetics = answer[0].get('phonetics', [{}])[0].get('text')
#             audio = answer[0].get('phonetics', [{}])[0].get('audio')
#             definition = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('definition')
#             example = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('example')
#             synonyms = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('synonyms')

#             context = {
#                 'form': form, 
#                 'input': text, 
#                 'phonetics': phonetics, 
#                 'audio': audio, 
#                 'definition': definition, 
#                 'example': example, 
#                 'synonyms': synonyms
#             }
#         except (requests.RequestException, json.JSONDecodeError, IndexError) as e:
#             context = {'form': form, 'input': '', 'error': str(e)}

#         return render(request, 'dashboard/dictionary.html', context)
    
#     context = {'form': form}
#     return render(request, 'dashboard/dictionary.html', context)

# def wiki(request):
#     form = DashboardForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         text = form.cleaned_data['text']
#         try:
#             search = wikipediaapi.Wikipedia('en').page(text)
#             context = {
#                 'form': form,
#                 'title': search.title,
#                 'link': search.fullurl,
#                 'details': search.summary
#             }
#         except Exception as e:
#             context = {'form': form, 'error': str(e)}
#         return render(request, "dashboard/wiki.html", context)

#     context = {'form': form}
#     return render(request, "dashboard/wiki.html", context)

# def conversion(request):
#     form = ConversionForm(request.POST or None)
#     if request.method == "POST":
#         measurement = request.POST['measurement']
#         measurement_form = ConversionLengthForm() if measurement == 'length' else ConversionMassForm()
        
#         if 'input' in request.POST:
#             first = request.POST['measure1']
#             second = request.POST['measure2']
#             input_value = request.POST['input']
#             answer = ''
            
#             if input_value and int(input_value) >= 0:
#                 if measurement == 'length':
#                     if first == 'yard' and second == 'foot':
#                         answer = f'{input_value} yard = {int(input_value) * 3} foot'
#                     elif first == 'foot' and second == 'yard':
#                         answer = f'{input_value} foot = {int(input_value) / 3} yard'
#                 elif measurement == 'mass':
#                     if first == 'pound' and second == 'kilogram':
#                         answer = f'{input_value} pound = {int(input_value) * 0.453592} kilogram'
#                     elif first == 'kilogram' and second == 'pound':
#                         answer = f'{input_value} kilogram = {int(input_value) * 2.20462} pound'
                    
#                 context = {'form': form, 'm_form': measurement_form, 'input': True, 'answer': answer}
#                 return render(request, "dashboard/conversion.html", context)

#     context = {'form': form, 'input': False}
#     return render(request, "dashboard/conversion.html", context)

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f"Account created for {username}!")
#             return redirect("login")
#     else:
#         form = UserRegistrationForm()
    
#     context = {'form': form}
#     return render(request, "dashboard/register.html", context)

# @login_required
# def profile(request):
#     homeworks = Homework.objects.filter(is_finished=False, user=request.user)
#     todos = Todo.objects.filter(is_finished=False, user=request.user)
#     homework_done = not homeworks.exists()
#     todos_done = not todos.exists()
#     context = {'homeworks': homeworks, 'todos': todos, 'homework_done': homework_done, 'todos_done': todos_done}
#     return render(request, "dashboard/profile.html", context)
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Hello, World!")

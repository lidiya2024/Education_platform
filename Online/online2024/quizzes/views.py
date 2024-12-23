from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Quiz, Question, Answer, QuizAttempt
from django.contrib import messages

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        score = 0
        for question in quiz.questions.all():
            selected_answer_id = request.POST.get(str(question.id))
            if selected_answer_id:
                selected_answer = Answer.objects.get(quiz=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1
        total_questions = quiz.questions.count()
        percentage_score = (score / total_questions) * 100 if total_questions > 0 else 0
        QuizAttempt.objects.create(student=request.user, quiz=quiz, score=percentage_score)
        messages.success(request, f"You scored {percentage_score:.2f}% on the quiz!")
        return redirect('quiz_list')
    return render(request, 'quizzes/take_quiz.html', {'quiz': quiz})

@login_required
def quiz_attempts(request):
    attempts = QuizAttempt.objects.select_related('student', 'quiz').all()
    context = {
        'attempts': attempts,
    }
    return render(request, 'quizzes/quiz_attempts.html', context)

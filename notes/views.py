from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Note
from .ai import search_top_k
from django.contrib.auth.decorators import login_required
from .models import Note, SearchHistory


# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):

    notes = Note.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]

    notes_count = Note.objects.filter(
        user=request.user
    ).count()

    favorites_count = Note.objects.filter(
        user=request.user,
        favorite=True
    ).count()

    categories_count = Note.objects.filter(
        user=request.user
    ).values("category").distinct().count()

    searches_count = SearchHistory.objects.filter(
        user=request.user
    ).count()

    context = {
        "notes": notes,
        "notes_count": notes_count,
        "favorites_count": favorites_count,
        "categories_count": categories_count,
        "searches_count": searches_count,
    }

    return render(
        request,
        "notes/dashboard.html",
        context
    )

# ---------------- ADD NOTE ----------------
from django.shortcuts import render, redirect
from .models import Note
@login_required
def add_note(request):

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")
        category = request.POST.get("category", "Other")

        if title and content:

            Note.objects.create(
    user=request.user,
    title=title,
    content=content,
    category=category
)

            return redirect("my_notes")

    return render(request, "notes/add_note.html")
# ---------------- MY NOTES ----------------
@login_required

def my_notes(request):

    query = request.GET.get("q", "")

    notes = Note.objects.filter(
    user=request.user
)

    if query:

        notes = notes.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    return render(
        request,
        "notes/my_notes.html",
        {
            "notes": notes,
            "query": query
        }
    )


# ---------------- AI SEARCH PAGE ----------------
@login_required

def search_page(request):

    return render(request, "notes/search.html")


# ---------------- AI SEARCH API ----------------
@login_required

def search_api(request):

    query = request.GET.get("q", "")

    results = []

    if query:

        

       SearchHistory.objects.create(
           user=request.user,
           query=query
       )

       notes = Note.objects.filter(
           user=request.user
       )

       results = search_top_k(query, notes)
    return JsonResponse({
        "results": results
    })
#------------Edit_Note-------------

@login_required

def edit_note(request, id):

    note = get_object_or_404(Note, id=id)

    if request.method == "POST":

        note.title = request.POST.get("title")
        note.content = request.POST.get("content")
        note.category = request.POST.get("category")

        note.save()

        return redirect("my_notes")

    return render(request, "notes/edit_note.html", {
        "note": note
    })

#--------------Delete_Note---------------


@login_required

def delete_note(request, id):

    note = get_object_or_404(Note, id=id)

    if request.method == "POST":

        note.delete()

        return JsonResponse({
            "success": True
        })

    return JsonResponse({
        "success": False
    })

from .ai import suggest_category
from django.http import JsonResponse
@login_required

def suggest_category_api(request):

    content = request.POST.get("content", "")

    category = suggest_category(content)

    return JsonResponse({
        "category": category
    })
    
@login_required
def view_note(request, id):

    note = get_object_or_404(
        Note,
        id=id,
        user=request.user
    )

    return render(
        request,
        "notes/view_note.html",
        {
            "note": note
        }
    )


from django.contrib import messages

@login_required
def settings_page(request):

    if request.method == "POST":

        user = request.user

        username = request.POST.get("username")
        email = request.POST.get("email")

        user.username = username
        user.email = email

        user.save()

        messages.success(request, "Profile updated successfully!")

        return redirect("settings")

    return render(request, "notes/settings.html")



from .ai import summarize_text

@login_required
def summarize_note(request, id):

    note = get_object_or_404(
        Note,
        id=id,
        user=request.user
    )

    summary = summarize_text(note.content)

    return JsonResponse({

        "summary": summary

    })
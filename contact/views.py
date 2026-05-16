from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ContactForm


def contact_page(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("/contact/?success=true")

    else:
        form = ContactForm()

    context = {
        "form": form
    }

    return render(
        request,
        "contact/contact.html",
        context
    )
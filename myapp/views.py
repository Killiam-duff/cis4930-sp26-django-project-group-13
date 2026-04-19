from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Record
from .forms import RecordForm

def home(request):
    return render(request, "myapp/home.html")

def record_list(request):
    records = Record.objects.all().order_by("-created_at")
    paginator = Paginator(records, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "myapp/list.html", {"page_obj": page_obj})

def record_detail(request, pk):
    record = get_object_or_404(Record, pk=pk)
    return render(request, "myapp/detail.html", {"record": record})

def record_create(request):
    form = RecordForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("records")

    return render(request, "myapp/form.html", {"form": form})

def record_update(request, pk):
    record = get_object_or_404(Record, pk=pk)
    form = RecordForm(request.POST or None, instance=record)

    if form.is_valid():
        form.save()
        return redirect("records")

    return render(request, "myapp/form.html", {"form": form})

def record_delete(request, pk):
    record = get_object_or_404(Record, pk=pk)

    if request.method == "POST":
        record.delete()
        return redirect("records")

    return render(request, "myapp/confirm_delete.html", {"record": record})

from django.shortcuts import render
import json

def home(request):
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/about.html")


# Items Page (placeholder for now)
def items(request):
    data = [
        {"id": 1, "name": "Notebook", "category": "Supplies", "price": 2.99},
        {"id": 2, "name": "Mouse", "category": "Electronics", "price": 12.99},
        {"id": 3, "name": "Bottle", "category": "Accessories", "price": 8.25},
    ]

    return render(request, "core/items.html", {"items": data})


# Students Page (optional / example page)
def students(request):
    data = [
        {"name": "Ava", "major": "CS", "gpa": 3.99},
        {"name": "Aidan", "major": "Math", "gpa": 3.4}
    ]

    return render(request, "core/students.html", {"students": data})


# Add Item Page (form placeholder)
def add_item(request):
    return render(request, "core/form.html")


# Analytics Page (placeholder)
def analytics(request):
    chart_data = {
        "labels": ["Jan", "Feb", "Mar", "Apr"],
        "values": [10, 25, 18, 30]
    }

    return render(request, "core/analytics.html", {
        "chart_json": json.dumps(chart_data)
    })

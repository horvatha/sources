from django.shortcuts import render
import coding


def home(request):
    return render(request, "djancoding/sourcestat.html", {})


def sourcestat_detail(request, id):
    sources = {
        1: coding.Source([.25]*4)
    }
    source = sources[int(id)]
    return render(request, "djancoding/sourcestat_detail.html", {"source": source})

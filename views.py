from django.shortcuts import render
import coding

sources = {
    1: (coding.Source([.25]*4), coding.Code("00 01 10 11")),
}


def home(request):
    return render(request, "sources/sourcestat.html", {})


def source_detail(request, id):
    source, _ = sources[int(id)]
    return render(
        request,
        "sources/sourcestat_detail.html",
        {"source": source}
    )


def sourcestat_default(request, id):
    source, code = sources[int(id)]
    return render(
        request,
        "sources/sourcestat_detail.html",
        {"source": source, "code": code}
    )

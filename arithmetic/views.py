from django.shortcuts import render  # , redirect
from coding import arithmetic
import random


def get_random_sample_and_text():
    word_parts = arithmetic.word_parts_hu
    sample = random.choice(list(word_parts))
    text = random.choice(word_parts[sample])
    return sample, text


def get_code_dict(sample, text):
    code = arithmetic.ArithmeticCode(sample)
    probability_and_intervals = []
    for symbol in code.intervals:
        lower, upper = code.intervals[symbol]
        probability_and_intervals.append(
            (symbol, upper-lower, lower, upper))
    code_value = code.coder(text)
    coder_intervals = code.coder_intervals(text)
    decoder_steps = code.decoder_steps(code_value, len(text))
    return {
        "sample": sample,
        "text": text,
        "probability_and_intervals": probability_and_intervals,
        "code_value": code_value,
        "coder_intervals": coder_intervals,
        "decoder_steps": decoder_steps,
    }


def home(request):
    return render(request, "arithmetic/home.html")


def coding_exercise(request):
    sample, text = get_random_sample_and_text()
    return render(
        request, "arithmetic/coding_exercise.html",
        get_code_dict(sample, text)
    )


def coding_solution(request):
    sample = request.POST["sample"]
    text = request.POST["text"]
    return render(
        request,
        "arithmetic/coding_solution.html",
        get_code_dict(sample, text)
    )


def decoding_exercise(request):
    sample, text = get_random_sample_and_text()
    return render(
        request, "arithmetic/decoding_exercise.html",
        get_code_dict(sample, text)
    )


def decoding_solution(request):
    sample = request.POST["sample"]
    text = request.POST["text"]
    return render(
        request,
        "arithmetic/decoding_solution.html",
        get_code_dict(sample, text)
    )

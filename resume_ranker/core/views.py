from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from core.pipelines.resume_pipeline import analyze_and_rank_resumes
import os
import uuid

# Allowed resume file extensions
ALLOWED_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png"]

def home(request):
    return render(request, "index.html")


def rank_resumes(request):
    if request.method != "POST":
        return render(request, "index.html")

    # -----------------------------
    # 1. Validate job description
    # -----------------------------
    job_description = request.POST.get("job_description", "").strip()

    if not job_description:
        messages.error(request, "Job description is required.")
        return render(request, "index.html")

    # -----------------------------
    # 2. Validate uploaded files
    # -----------------------------
    uploaded_files = request.FILES.getlist("resumes")

    if not uploaded_files:
        messages.error(request, "Please upload at least one resume.")
        return render(request, "index.html")

    fs = FileSystemStorage(location="media/resumes")
    file_paths = []

    # -----------------------------
    # 3. Save files safely
    # -----------------------------
    for f in uploaded_files:
        ext = os.path.splitext(f.name)[1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            messages.warning(
                request,
                f"File '{f.name}' skipped (unsupported format)."
            )
            continue

        # Prevent filename collision
        unique_name = f"{uuid.uuid4()}{ext}"
        filename = fs.save(unique_name, f)
        file_paths.append(fs.path(filename))

    if not file_paths:
        messages.error(request, "No valid resume files were uploaded.")
        return render(request, "index.html")

    # -----------------------------
    # 4. Analyze & rank resumes
    # -----------------------------
    try:
        ranked_results = analyze_and_rank_resumes(
            file_paths,
            job_description
        )
    except Exception as e:
        print("Pipeline error:", e)
        messages.error(
            request,
            "An error occurred while analyzing resumes. Please try again."
        )
        return render(request, "index.html")

    # -----------------------------
    # 5. Render results
    # -----------------------------
    return render(
        request,
        "results.html",
        {
            "results": ranked_results,
            "job_description": job_description
        }
    )

import os,re
template=open("fix_exam_template.txt","r",encoding="utf-8").read()
t_dir=os.path.join("resultportal","templates")
os.makedirs(t_dir,exist_ok=True)
t_path=os.path.join(t_dir,"take_exam_cbt.html")
with open(t_path,"w",encoding="utf-8") as f:f.write(template)
print("OK: Created "+t_path)
path="resultportal/views.py"
with open(path,"r",encoding="utf-8") as f:content=f.read()
new_func='''def take_exam(request, exam_id):
    student_class = request.GET.get("class", "").strip()
    try:
        ref_q = ExamQuestion.objects.get(id=exam_id)
    except ExamQuestion.DoesNotExist:
        from django.shortcuts import redirect
        return redirect("exam_list_page")
    subject = ref_q.subject
    term = ref_q.term
    year = ref_q.year
    if request.method == "POST":
        student_name = request.POST.get("student_name", "").strip()
        exam_number = request.POST.get("exam_number", "").strip()
        if not student_name:
            return render(request, "exam_detail.html", {"exam_id": exam_id, "subject": subject, "student_class": student_class, "term": term, "year": year, "error": "Please enter your full name."})
        questions = list(ExamQuestion.objects.filter(student_class=student_class, subject=subject, term=term, year=year).order_by("id").values("id", "question_text", "question_type", "option_a", "option_b", "option_c", "option_d", "marks"))
        if not questions:
            from django.shortcuts import redirect
            return redirect("exam_list_page")
        total_marks = sum(q["marks"] for q in questions)
        return render(request, "take_exam_cbt.html", {"questions": questions, "student_name": student_name, "exam_number": exam_number, "student_class": student_class, "subject": subject, "term": term, "year": year, "exam_id": exam_id, "total_marks": total_marks})
    return render(request, "exam_detail.html", {"exam_id": exam_id, "subject": subject, "student_class": student_class, "term": term, "year": year})'''
pattern=r"def take_exam\(request, exam_id\):.*?(?=\ndef [a-z_]|\nclass |\Z)"
new_content=re.sub(pattern,new_func+"\n\n",content,flags=re.DOTALL)
if new_content==content:
    pattern2=r"def take_exam\(request, exam_id\)[\s\S]*?(?=\ndef )"
    new_content=re.sub(pattern2,new_func+"\n\n",content)
with open(path,"w",encoding="utf-8") as f:f.write(new_content)
print("OK: Fixed take_exam")
print("DONE")

import streamlit as st
import streamlit.components.v1 as components
import json
import os

# إعدادات واجهة المنصة النهائية
st.set_page_config(
    page_title="أكاديمية الإنجليزية",
    page_icon="🎓",
    layout="wide"
)

# ملف الحفظ الدائم
DB_FILE = "academy_final_database.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "lectures": [],
        "quizzes": [],
        "announcements": ["📢 أهلاً بكم في أكاديمية الإنجليزية الرسمية."],
        "grades": {},
        "messages": {}
    }

def save_data():
    data = {
        "lectures": st.session_state.lectures,
        "quizzes": st.session_state.quizzes,
        "announcements": st.session_state.announcements,
        "grades": st.session_state.grades,
        "messages": st.session_state.messages
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تحميل البيانات
if "data_loaded" not in st.session_state:
    db = load_data()
    st.session_state.lectures = db["lectures"]
    st.session_state.quizzes = db["quizzes"]
    st.session_state.announcements = db["announcements"]
    st.session_state.grades = db["grades"]
    st.session_state.messages = db["messages"]
    st.session_state.data_loaded = True

if "is_teacher" not in st.session_state:
    st.session_state.is_teacher = False

# الشريط الجانبي (دخول الأستاذة أو تصفح القناة)
st.sidebar.title("🎓 أكاديمية الإنجليزية")

if not st.session_state.is_teacher:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 دخول الأستاذة فقط")
    t_email = st.sidebar.text_input("البريد الإلكتروني")
    t_pass = st.sidebar.text_input("كلمة المرور", type="password")
    if st.sidebar.button("تسجيل دخول الأستاذة"):
        if t_email == "teacher@academy.com" and t_pass == "123":
            st.session_state.is_teacher = True
            st.rerun()
        else:
            st.sidebar.error("خطأ ببيانات الدخول.")
    
    st.sidebar.markdown("---")
    menu = ["📢 قناة التنبيهات والتعاميم", "🎬 المحاضرات والملحقات", "🎙️ غرفة البث المباشر", "📝 اختبارات الأكاديمية", "💬 مراسلة الأستاذة"]
else:
    st.sidebar.success("مرحباً بكِ، دكتورة أمي 👩‍🏫")
    menu = ["📊 لوحة تحكم الأستاذة", "📢 نشر التنبيهات الرسمية", "✍️ إدارة ونشر الاختبارات", "💬 صندوق رسائل الطلاب", "🎬 إدارة المحاضرات والدروس", "🎙️ البث المباشر"]
    if st.sidebar.button("تسجيل خروج الأستاذة"):
        st.session_state.is_teacher = False
        st.rerun()

choice = st.sidebar.selectbox("القائمة الرئيسية", menu)

# ==========================
# لوحة تحكم الأستاذة
# ==========================
if st.session_state.is_teacher:
    if choice == "📊 لوحة تحكم الأستاذة":
        st.header("📊 لوحة تحكم الأستاذة الرسمية")
        st.success("متابعة درجات وإجابات الطلاب الواردة:")
        if st.session_state.grades:
            for student_record, score in st.session_state.grades.items():
                st.write(f"- الطالب: **{student_record}** | النتيجة: {score}")
        else:
            st.info("لا توجد نتائج اختبارات مرسلة حتى الآن.")

    elif choice == "📢 نشر التنبيهات الرسمية":
        st.header("📢 قناة إعلان التنبيهات (مثل التلغرام)")
        new_announcement = st.text_area("اكتب الإعلان أو التنبيه لنشره في القناة العامة:")
        if st.button("نشر في القناة"):
            if new_announcement:
                st.session_state.announcements.insert(0, new_announcement)
                save_data()
                st.success("تم نشر التنبيه في القناة بنجاح!")
            else:
                st.warning("يرجى كتابة نص التنبيه.")

    elif choice == "✍️ إدارة ونشر الاختبارات":
        st.header("✍️ نشر اختبار جديد (بلا حدود)")
        q_text = st.text_input("نص السؤال:")
        opt1 = st.text_input("الخيار الأول:")
        opt2 = st.text_input("الخيار الثاني:")
        opt3 = st.text_input("الخيار الثالث:")
        correct_opt = st.text_input("الإجابة الصحيحة بالضبط (نسخ دقيق لأحد الخيارات):")
        
        if st.button("نشر الاختبار في المنصة"):
            if q_text and opt1 and opt2 and opt3 and correct_opt:
                st.session_state.quizzes.append({
                    "question": q_text,
                    "options": [opt1, opt2, opt3],
                    "answer": correct_opt
                })
                save_data()
                st.success("تم نشر الاختبار بنجاح لجميع الطلاب!")
            else:
                st.warning("يرجى ملء كافة حقول السؤال والخيارات والإجابة الصحيحة.")

    elif choice == "💬 صندوق رسائل الطلاب":
        st.header("💬 صندوق رسائل الطلاب الواردة")
        if st.session_state.messages:
            for s_name, msg_list in st.session_state.messages.items():
                with st.expander(f"محادثة مع الطالب: {s_name}"):
                    for m in msg_list:
                        st.write(f"- {m}")
        else:
            st.info("لا توجد رسائل واردة حالياً.")

    elif choice == "🎬 إدارة المحاضرات والدروس":
        st.header("🎬 نشر المحاضرات والدروس")
        lec_title = st.text_input("عنوان المحاضرة:")
        lec_url = st.text_input("رابط فيديو يوتيوب:")
        if st.button("نشر المحاضرة"):
            if lec_title and lec_url:
                st.session_state.lectures.append({"title": lec_title, "url": lec_url})
                save_data()
                st.success("تم نشر المحاضرة بنجاح!")
            else:
                st.warning("يرجى إدخال العنوان والرابط.")

    elif choice == "🎙️ البث المباشر":
        st.header("🎙️ غرفة البث المباشر الرسمية")
        jitsi_html = '<iframe src="https://meet.jit.si/MomEnglishAcademy2026" height="550px" width="100%" style="border:none; border-radius:12px;" allow="camera; microphone; display-capture; autoplay"></iframe>'
        components.html(jitsi_html, height=570)

# ==========================
# واجهة الطالب العامة (بدون حسابات)
# ==========================
else:
    if choice == "📢 قناة التنبيهات والتعاميم":
        st.header("📢 قناة تنبيهات أكاديمية الإنجليزية")
        for ann in st.session_state.announcements:
            st.info(ann)

    elif choice == "🎬 المحاضرات والملحقات":
        st.header("🎬 محاضرات الفيديو")
        if st.session_state.lectures:
            for lec in st.session_state.lectures:
                st.subheader(f"📺 {lec['title']}")
                st.video(lec['url'])
                st.markdown("---")
        else:
            st.info("لم تنشر الأستاذة محاضرات جديدة بعد.")
        
        st.subheader("📁 ملحقات الدروس والملزمات")
        

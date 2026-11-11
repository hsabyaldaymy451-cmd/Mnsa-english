import streamlit as st
import streamlit.components.v1 as components
import json
import os

# إعدادات واجهة المنصة النهائية
st.set_page_config(
    page_title="أكاديمية الدكتورة أمي للغة الإنكليزية",
    page_icon="🎓",
    layout="wide"
)

# ملف الحفظ الدائم (النسخة النهائية)
DB_FILE = "academy_final_database.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "users": {
            "teacher@academy.com": {"password": "123", "role": "teacher", "name": "الدكتورة الأستاذة"}
        },
        "lectures": [],
        "quizzes": [],
        "announcements": ["📢 أهلاً بكم في النسخة النهائية لأكاديمية اللغة الإنكليزية."],
        "grades": {},
        "messages": {}
    }

def save_data():
    data = {
        "users": st.session_state.users,
        "lectures": st.session_state.lectures,
        "quizzes": st.session_state.quizzes,
        "announcements": st.session_state.announcements,
        "grades": st.session_state.grades,
        "messages": st.session_state.messages
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تحميل البيانات الثابتة
if "data_loaded" not in st.session_state:
    db = load_data()
    st.session_state.users = db["users"]
    st.session_state.lectures = db["lectures"]
    st.session_state.quizzes = db["quizzes"]
    st.session_state.announcements = db["announcements"]
    st.session_state.grades = db["grades"]
    st.session_state.messages = db["messages"]
    st.session_state.data_loaded = True

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# واجهة الدخول الرسمية
if not st.session_state.logged_in:
    st.title("🎓 أكاديمية الدكتورة أمي - البوابة التعليمية الرسمية")
    st.write("يرجى تسجيل الدخول بحسابك الدائم أو إنشاء حساب جديد كطالب.")
    
    tab1, tab2 = st.tabs(["تسجيل الدخول", "تسجيل طالب جديد"])
    
    with tab1:
        email = st.text_input("البريد الإلكتروني أو اسم المستخدم", key="final_login_email")
        password = st.text_input("كلمة المرور", type="password", key="final_login_pass")
        if st.button("دخول للمنصة الرسمية"):
            if email in st.session_state.users and st.session_state.users[email]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = email
                st.rerun()
            else:
                st.error("البريد الإلكتروني أو كلمة المرور غير صحيحة.")
                
    with tab2:
        new_name = st.text_input("الاسم الكامل للطالب", key="final_reg_name")
        new_email = st.text_input("البريد الإلكتروني الدائم", key="final_reg_email")
        new_pass = st.text_input("كلمة المرور", type="password", key="final_reg_pass")
        if st.button("إتمام التسجيل الدائم"):
            if new_email and new_pass and new_name:
                if new_email in st.session_state.users:
                    st.warning("هذا البريد مسجل مسبقاً، يرجى الانتقال لتبويب تسجيل الدخول!")
                else:
                    st.session_state.users[new_email] = {"password": new_pass, "role": "student", "name": new_name}
                    save_data()
                    st.success("تم إنشاء حساب الطالب بنجاح! انتقل لتبويب تسجيل الدخول الآن.")
            else:
                st.warning("يرجى ملء جميع الحقول المطلوبة.")
                
else:
    user_info = st.session_state.users[st.session_state.current_user]
    
    st.sidebar.title(f"👤 مرحبًا، {user_info['name']}")
    
    if user_info["role"] == "teacher":
        menu = ["📊 لوحة تحكم الأستاذة والطلاب", "📢 نشر التنبيهات الرسمية", "✍️ إدارة ونشر الاختبارات", "💬 صندوق رسائل الطلاب", "🎬 إدارة المحاضرات والدروس", "🎙️ البث المباشر"]
    else:
        menu = ["📢 قناة التنبيهات والتعاميم", "🎬 المحاضرات والملحقات", "🎙️ غرفة البث المباشر", "📝 اختبارات الأكاديمية", "💬 مراسلة الأستاذة"]
        
    choice = st.sidebar.selectbox("القائمة الرئيسية", menu)
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    # ==========================
    # لوحة تحكم الأستاذة (النسخة النهائية)
    # ==========================
    if user_info["role"] == "teacher":
        if choice == "📊 لوحة تحكم الأستاذة والطلاب":
            st.header("📊 لوحة تحكم الأستاذة الرسمية")
            st.success("متابعة الطلاب المسجلين ونتائجهم الدائمة:")
            
            st.subheader("👥 الطلاب المسجلين في الأكاديمية:")
            student_count = 0
            for mail, data in st.session_state.users.items():
                if data["role"] == "student":
                    student_count += 1
                    st.write(f"{student_count}. الطالب: **{data['name']}** (البريد: {mail})")
            if student_count == 0:
                st.info("لا توجد حسابات طلاب مسجلة حتى الآن.")
                    
            st.subheader("📝 درجات الطلاب في الاختبارات:")
            if st.session_state.grades:
                for student, score in st.session_state.grades.items():
                    st.write(f"- {student}: **{score}**")
            else:
                st.info("لا توجد نتائج اختبارات مسجلة حتى الآن.")

        elif choice == "📢 نشر التنبيهات الرسمية":
            st.header("📢 قناة إعلان التنبيهات")
            new_announcement = st.text_area("اكتب الإعلان أو التنبيه الهام للطلاب:")
            if st.button("نشر التنبيه رسمياً"):
                if new_announcement:
                    st.session_state.announcements.insert(0, new_announcement)
                    save_data()
                    st.success("تم نشر التنبيه بنجاح وسيظهر لجميع الطلاب فورا!")
                else:
                    st.warning("يرجى كتابة نص التنبيه.")

        elif choice == "✍️ إدارة ونشر الاختبارات":
            st.header("✍️ نظام إنشاء الاختبارات (بلا حدود)")
            st.info("أضف أي عدد من الاختبارات لتظهر كاستطلاعات تفاعلية للطلاب:")
            q_text = st.text_input("نص السؤال:")
            opt1 = st.text_input("الخيار الأول:")
            opt2 = st.text_input("الخيار الثاني:")
            opt3 = st.text_input("الخيار الثالث:")
            correct_opt = st.text_input("الإجابة الصحيحة بالضبط (نسخ دقيق لأحد الخيارات):")
            
            if st.button("نشر الاختبار نهائياً"):
                if q_text and opt1 and opt2 and opt3 and correct_opt:
                    st.session_state.quizzes.append({
                        "question": q_text,
                        "options": [opt1, opt2, opt3],
                        "answer": correct_opt
                    })
                    save_data()
                    st.success("تم نشر الاختبار بنجاح وصار متاحاً للطلاب!")
                else:
                    st.warning("يرجى تعبئة جميع حقول السؤال والخيارات والإجابة الصحيحة.")
            
            st.markdown("---")
            st.subheader("الاختبارات النشطة حالياً:")
            for idx, q in enumerate(st.session_state.quizzes):
                st.write(f"اختبار ({idx+1}): **{q['question']}** (الإجابة الصحيحة: `{q['answer']}`)")

        elif choice == "💬 صندوق رسائل الطلاب":
            st.header("💬 صندوق رسائل الطلاب الواردة")
            if st.session_state.messages:
                for student_email, msg_list in st.session_state.messages.items():
                    student_name = st.session_state.users.get(student_email, {}).get("name", student_email)
                    with st.expander(f"محادثة الطالب: {student_name}"):
                        for m in msg_list:
                            st.write(f"- {m}")
            else:
                st.info("لا توجد رسائل واردة حالياً.")

        elif choice == "🎬 إدارة المحاضرات والدروس":
            st.header("🎬 إدارة ونشر المحاضرات")
            lec_title = st.text_input("عنوان المحاضرة (مثلا: Unit 1 - Grammar):")
            lec_url = st.text_input("رابط فيديو يوتيوب للدرس:")
            if st.button("نشر المحاضرة للمنصة"):
                if lec_title and lec_url:
                    st.session_state.lectures.append({"title": lec_title, "url": lec_url})
                    save_data()
                    st.success("تم نشر المحاضرة بنجاح!")
                else:
                    st.warning("يرجى إدخال العنوان والرابط.")
            
            st.markdown("---")
            st.subheader("المحاضرات المسجلة:")
            for lec in st.session_state.lectures:
                st.write(f"- **{lec['title']}**")

        elif choice == "🎙️ البث المباشر":
            st.header("🎙️ غرفة البث المباشر الرسمية")
            st.success("ابدأ المحاضرة المرئية مع الطلاب مباشرة:")
            jitsi_html = '<iframe src="https://meet.jit.si/MomEnglishAcademy2026" height="550px" width="100%" style="border:none; border-radius:12px;" allow="camera; microphone; display-capture; autoplay"></iframe>'
            components.html(jitsi_html, height=570)

    # ==========================
    #

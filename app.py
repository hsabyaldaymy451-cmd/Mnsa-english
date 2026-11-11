import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(
    page_title="أكاديمية الدكتورة أمي للغة الإنكليزية",
    page_icon="🎓",
    layout="wide"
)

# تخزين المستخدمين والبيانات مؤقتاً (ذاكرة الجلسة)
if "users" not in st.session_state:
    st.session_state.users = {"teacher@academy.com": {"password": "123", "role": "teacher", "name": "الدكتورة الأستاذة"}}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "grades" not in st.session_state:
    st.session_state.grades = {}

# واجهة تسجيل الدخول أو إنشاء حساب
if not st.session_state.logged_in:
    st.title("🎓 تسجيل الدخول - أكاديمية اللغة الإنكليزية")
    st.write("يرجى تسجيل الدخول أو إنشاء حساب جديد للوصول إلى المنصة.")
    
    tab1, tab2 = st.tabs(["تسجيل الدخول", "حساب جديد للطالب"])
    
    with tab1:
        email = st.text_input("البريد الإلكتروني أو اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if email in st.session_state.users and st.session_state.users[email]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = email
                st.rerun()
            else:
                st.error("خطأ في البريد الإلكتروني أو كلمة المرور.")
                
    with tab2:
        new_name = st.text_input("الاسم الكامل للطالب")
        new_email = st.text_input("البريد الإلكتروني الجديد")
        new_pass = st.text_input("كلمة المرور الجديدة", type="password")
        if st.button("إنشاء الحساب الان"):
            if new_email and new_pass and new_name:
                st.session_state.users[new_email] = {"password": new_pass, "role": "student", "name": new_name}
                st.success("تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن.")
            else:
                st.warning("يرجى ملء جميع الحقول.")
                
else:
    user_info = st.session_state.users[st.session_state.current_user]
    
    # شريط التنقل الجانبي
    st.sidebar.title(f"👤 مرحبًا، {user_info['name']}")
    
    if user_info["role"] == "teacher":
        menu = ["📊 لوحة تحكم الأستاذة", "🎬 المحاضرات", "🎙️ البث المباشر"]
    else:
        menu = ["🎬 محاضراتي", "🎙️ غرفة البث المباشر", "📝 الاختبارات والواجبات"]
        
    choice = st.sidebar.selectbox("القائمة الرئيسية", menu)
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    # 1. لوحة تحكم الأستاذة (الخاصة بأمج)
    if choice == "📊 لوحة تحكم الأستاذة":
        st.header("📊 لوحة تحكم الأستاذة (إدارة الطلاب)")
        st.success("هنا تستطيعين متابعة جميع الطلاب المسجلين في الأكاديمية ودرجاتهم:")
        
        st.subheader("الطلاب المسجلين:")
        for mail, data in st.session_state.users.items():
            if data["role"] == "student":
                st.write(- f"الطالب: **{data['name']}** (البريد: {mail})")
                
        st.subheader("درجات الطلاب في الاختبارات:")
        if st.session_state.grades:
            for student, score in st.session_state.grades.items():
                st.write(f"- {student}: النتيجة = {score}")
        else:
            st.info("لا توجد نتائج اختبارات مرسلة حتى الآن.")

    # 2. قسم المحاضرات (للطلاب)
    elif "المحاضرات" in choice or "محاضراتي" in choice:
        st.header("🎬 المحاضرات والدروس المسجلة")
        st.info("💡 شاهد المحاضرات الخاصة بمنهج اللغة الإنكليزية.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("الوحدة الأولى: قواعد اللغة")
            st.text("الفيديو التعليمي الخاص بالدرس يظهر هنا...")
        with col2:
            st.subheader("الملحقات والملزمات")
            st.download_button("📥 تحميل ملزمة الشرح (PDF)", data="محتوى الملزمة", file_name="Unit1.pdf")

    # 3. قسم البث المباشر
    elif "البث المباشر" in choice:
        st.header("🎙️ قاعة البث المباشر والمكالمات")
        st.info("اضغط أدناه للدخول إلى قاعة المحاضرة المباشرة مع الأستاذة:")
        
        jitsi_html = """
        <iframe src="https://meet.jit.si/MomEnglishAcademy2026" 
                height="600px" width="100%" 
                style="border:none; border-radius:12px;"
                allow="camera; microphone; display-capture; autoplay">
        </iframe>
        """
        components.html(jitsi_html, height=620)

    # 4. قسم الاختبارات (للطلاب)
    elif choice == "📝 الاختبارات والواجبات":
        st.header("✍️ اختبار القواعد الأسبوعي")
        
        q1 = st.radio("اختر الخيار الصحيح: She ___ to school every day.", ["go", "goes", "going"])
        
        if st.button("إرسال الإجابة للأستاذة"):
            score = "صحيحة (10/10)" if q1 == "goes" else "خاطئة (0/10)"
            st.session_state.grades[user_info['name']] = score
            if q1 == "goes":
                st.success("أحسنتِ! تم إرسال إجابتكِ ودرجتكِ إلى لوحة تحكم الأستاذة بنجاح.")
            else:
                st.error("إجابة خاطئة، تم تسجيل المحاولة وإرسالها للأستاذة.")

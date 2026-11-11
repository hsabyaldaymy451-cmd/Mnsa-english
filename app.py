import streamlit as st
import streamlit.components.v1 as components

# إعدادات واجهة المنصة
st.set_page_config(
    page_title="أكاديمية الدكتورة أمي للغة الإنكليزية",
    page_icon="🎓",
    layout="wide"
)

# نظام تخزين البيانات الوهمي (الجلسة)
if "users" not in st.session_state:
    st.session_state.users = {
        "teacher@academy.com": {"password": "123", "role": "teacher", "name": "الدكتورة الأستاذة"}
    }
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "grades" not in st.session_state:
    st.session_state.grades = {}
if "announcements" not in st.session_state:
    st.session_state.announcements = ["📢 أهلاً بكم في الأكاديمية! ترقبوا المحاضرة الأولى قريباً."]
if "messages" not in st.session_state:
    st.session_state.messages = {}  
if "lectures" not in st.session_state:
    st.session_state.lectures = [
        {"title": "المحاضرة الأولى: شرح القواعد الأساسية", "url": "https://www.youtube.com/watch?v=kJQP7kiw5Fk"}
    ]

# 1. شاشة تسجيل الدخول أو إنشاء حساب
if not st.session_state.logged_in:
    st.title("🎓 بوابة تسجيل الدخول - أكاديمية اللغة الإنكليزية")
    st.write("يرجى تسجيل الدخول أو إنشاء حساب جديد للوصول إلى المنصة التعليمية.")
    
    tab1, tab2 = st.tabs(["تسجيل الدخول", "حساب جديد للطالب"])
    
    with tab1:
        email = st.text_input("البريد الإلكتروني أو اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للمنصة"):
            if email in st.session_state.users and st.session_state.users[email]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = email
                st.rerun()
            else:
                st.error("خطأ في البريد الإلكتروني أو كلمة المرور.")
                
    with tab2:
        new_name = st.text_input("الاسم الكامل للطالب")
        new_email = st.text_input("البريد الإلكتروني الجديد (أو اسم المستخدم)")
        new_pass = st.text_input("كلمة المرور الجديدة", type="password")
        if st.button("إنشاء الحساب الآن"):
            if new_email and new_pass and new_name:
                st.session_state.users[new_email] = {"password": new_pass, "role": "student", "name": new_name}
                st.success("تم إنشاء الحساب بنجاح! يمكنك الانتقال لتبويب تسجيل الدخول الآن.")
            else:
                st.warning("يرجى ملء جميع الحقول المطلوبة.")
                
else:
    user_info = st.session_state.users[st.session_state.current_user]
    
    st.sidebar.title(f"👤 مرحبًا، {user_info['name']}")
    
    if user_info["role"] == "teacher":
        menu = ["📊 لوحة التحكم وإدارة الطلاب", "📢 نشر التنبيهات (القناة)", "💬 صندوق رسائل الطلاب", "🎬 إدارة المحاضرات", "🎙️ البث المباشر"]
    else:
        menu = ["📢 قناة التنبيهات والتعاميم", "🎬 محاضراتي وملحقاتها", "🎙️ غرفة البث المباشر", "📝 الاختبارات والواجبات", "💬 مراسلة الأستاذة"]
        
    choice = st.sidebar.selectbox("القائمة الرئيسية", menu)
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    # ==========================
    # لوحات تحكم الأستاذة (أمكِ)
    # ==========================
    if user_info["role"] == "teacher":
        if choice == "📊 لوحة التحكم وإدارة الطلاب":
            st.header("📊 لوحة تحكم الأستاذة")
            st.success("هنا تستطيعين متابعة جميع الطلاب المسجلين ودرجاتهم:")
            
            st.subheader("👥 الطلاب المسجلين في الأكاديمية:")
            for mail, data in st.session_state.users.items():
                if data["role"] == "student":
                    st.write(f"- الطالب: **{data['name']}** (البريد: {mail})")
                    
            st.subheader("📝 درجات الطلاب في الاختبارات:")
            if st.session_state.grades:
                for student, score in st.session_state.grades.items():
                    st.write(f"- {student}: النتيجة = {score}")
            else:
                st.info("لا توجد نتائج اختبارات مرسلة حتى الآن.")

        elif choice == "📢 نشر التنبيهات (القناة)":
            st.header("📢 لوحة إعلان التنبيهات للطلاب")
            new_announcement = st.text_area("اكتب تنبيهاً جديداً أو إعلاناً للطلاب:")
            if st.button("نشر التنبيه فوراً"):
                if new_announcement:
                    st.session_state.announcements.insert(0, new_announcement)
                    st.success("تم نشر التنبيه بنجاح وسيراه جميع الطلاب في قناتهم!")
                else:
                    st.warning("يرجى كتابة نص التنبيه أولاً.")

        elif choice == "💬 صندوق رسائل الطلاب":
            st.header("💬 رسائل واستفسارات الطلاب الخاصة")
            if st.session_state.messages:
                for student_email, msg_list in st.session_state.messages.items():
                    student_name = st.session_state.users.get(student_email, {}).get("name", student_email)
                    with st.expander(f"محادثة مع الطالب: {student_name}"):
                        for m in msg_list:
                            st.write(f"- {m}")
            else:
                st.info("لا توجد رسائل جديدة من الطلاب حالياً.")

        elif choice == "🎬 إدارة المحاضرات":
            st.header("🎬 إضافة ونشر المحاضرات للطلاب")
            lec_title = st.text_input("عنوان المحاضرة (مثلا: Unit 1 - Grammar):")
            lec_url = st.text_input("رابط فيديو يوتيوب للدرس:")
            if st.button("نشر المحاضرة للمنصة"):
                if lec_title and lec_url:
                    st.session_state.lectures.append({"title": lec_title, "url": lec_url})
                    st.success("تم نشر المحاضرة بنجاح وصارت متاحة لجميع الطلاب!")
                else:
                    st.warning("يرجى إدخال العنوان والرابط معاً.")
            
            st.markdown("---")
            st.subheader("المحاضرات الحالية المنشورة:")
            for idx, lec in enumerate(st.session_state.lectures):
                st.write(f"{idx+1}. **{lec['title']}** -> ({lec['url']})")

        elif choice == "🎙️ البث المباشر":
            st.header("🎙️ غرفة البث المباشر الخاصة بالأستاذة")
            st.success("اضغط أدناه لبدء البث المباشر مع الطلاب:")
            jitsi_html = '<iframe src="https://meet.jit.si/MomEnglishAcademy2026" height="550px" width="100%" style="border:none; border-radius:12px;" allow="camera; microphone; display-capture; autoplay"></iframe>'
            components.html(jitsi_html, height=570)

    # ==========================
    # واجهات الطالب الشخصية
    # ==========================
    else:
        if choice == "📢 قناة التنبيهات والتعاميم":
            st.header("📢 قناة تنبيهات الأكاديمية")
            st.info("آخر الإعلانات والتوجيهات الصادرة من الأستاذة:")
            for ann in st.session_state.announcements:
                st.info(ann)

        elif choice == "🎬 محاضراتي وملحقاتها":
            st.header("🎬 المحاضرات والدروس المسجلة")
            for lec in st.session_state.lectures:
                st.subheader(f"📺 {lec['title']}")
                st.video(lec['url'])
                st.markdown("---")
            
            st.subheader("📁 ملحقات الدروس والملزمات")
            st.download_button("📥 تحميل ملزمة الشرح (PDF)", data="محتوى ملف الملزمة التجريبي", file_name="Academy_Notes.pdf")

        elif choice == "🎙️ غرفة البث المباشر":
            st.header("🎙️ قاعة المحاضرة المباشرة")
            st.success("انضم الآن إلى قاعة الدرس مع الأستاذة:")
            jitsi_html = '<iframe src="https://meet.jit.si/MomEnglishAcademy2026" height="550px" width="100%" style="border:none; border-radius:12px;" allow="camera; microphone; display-capture; autoplay"></iframe>'
            components.html(jitsi_html, height=570)

        elif choice == "📝 الاختبارات والواجبات":
            st.header("✍️ اختبار القواعد الأسبوعي (Quiz)")
            q1 = st.radio("اختر الخيار الصحيح للجملة: She ___ to school every day.", ["go", "goes", "going"])
            
            if st.button("إرسال الإجابة للأستاذة"):
                score = "صحيحة (10/10)" if q1 == "goes" else "خاطئة (0/10)"
                st.session_state.grades[user_info['name']] = score
                if q1 == "goes":
                    st.success("أحسنتِ! تم إرسال إجابتكِ ودرجتكِ إلى لوحة تحكم الأستاذة بنجاح.")
                else:
                    st.error("إجابة خاطئة، تم تسجيل المحاولة وإرسالها للأستاذة.")

        elif choice == "💬 مراسلة الأستاذة":
            st.header("💬 إرسال استفسار أو سؤال للأستاذة")
            user_msg = st.text_area("اكتب رسالتك أو سؤالك هنا:")
            if st.button("إرسال الرسالة"):
                if user_msg:
                    if st.session_state.current_user not in st.session_state.messages:
                        st.session_state.messages

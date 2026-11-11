import streamlit as st
import streamlit.components.v1 as components

# إعدادات واجهة المنصة وتنسيق الصفحة
st.set_page_config(
    page_title="أكاديمية اللغة الإنكليزية",
    page_icon="📚",
    layout="wide"
)

# تنسيق CSS لضبط المحاذاة واللغة العربية بشكل أنيق
st.markdown("""
    <style>
    body {
        direction: rtl;
        text-align: right;
    }
    .stApp {
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

# عنوان المنصة الرئيسي
st.title("📚 أكاديمية اللغة الإنكليزية - الدكتورة أمي الغالية")
st.write("أهلاً بكم في المنصة الرسمية الخاصة بمحاضرات ومكالمات مادة اللغة الإنكليزية.")
st.markdown("---")

# القائمة الجانبية للتنقل بين الأقسام
st.sidebar.title("📌 القوائم الرئيسية")
menu = [
    "🎬 المحاضرات والدروس",
    "🎙️ غرف البث المباشر والمكالمات",
    "📝 الاختبارات والواجبات",
    "📇 بطاقات المفردات (Flashcards)"
]
choice = st.sidebar.radio("اختر القسم:", menu)

# 1. قسم المحاضرات المسجلة
if choice == "🎬 المحاضرات والدروس":
    st.header("🎬 المحاضرات والدروس المسجلة")
    st.info("💡 مشاهدة الفيديوهات والملحقات متاحة لطلاب الأكاديمية.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📺 المحاضرة الأولى")
        # مكان رابط يوتيوب الخاص بأمج (يمكن وضعه لاحقاً)
        st.text("سيتم عرض فيديو الدرس هنا قريباً...")
        
    with col2:
        st.subheader("📁 ملحقات الدرس (الملزمة)")
        st.write("يمكن للطلاب تحميل ملزمة الشرح الخاصة بالدرس:")
        st.download_button(
            label="📥 تحميل ملزمة الشرح (PDF)",
            data="محتوى ملف الملزمة",
            file_name="Lesson1_Notes.pdf"
        )

# 2. قسم البث المباشر والمكالمات (Jitsi Meet المجاني بالكامل)
elif choice == "🎙️ غرف البث المباشر والمكالمات":
    st.header("🎙️ البث المباشر والمحادثة التفاعلية")
    st.success("✅ انقر أدناه للانضمام إلى قاعة المحاضرة المباشرة مع الأستاذة.")
    
    jitsi_room_html = """
    <iframe src="https://meet.jit.si/MomEnglishAcademy2026" 
            height="600px" 
            width="100%" 
            style="border:none; border-radius:12px;"
            allow="camera; microphone; display-capture; autoplay">
    </iframe>
    """
    components.html(jitsi_room_html, height=620)

# 3. قسم الاختبارات
elif choice == "📝 الاختبارات والواجبات":
    st.header("✍️ اختبار سريع (Quiz)")
    
    q1 = st.radio(
        "اختر الخيار الصحيح للجملة التالية: She ___ to school every day.",
        ["go", "goes", "going", "gone"]
    )
    
    if st.button("تسليم الإجابة"):
        if q1 == "goes":
            st.success("إجابة صحيحة! 🎉 أحسنتِ.")
        else:
            st.error("إجابة خاطئة! حاول مرة أخرى.")

# 4. قسم المفردات
elif choice == "📇 بطاقات المفردات (Flashcards)":
    st.header("📇 مراجعة وحفظ المفردات السريعة")
    
    st.subheader("الكلمة: Fluency")
    with st.expander("اضغط لإظهار المعنى والنطق"):
        st.write("📖 **المعنى:** الطلاقة (في التحدث والتعبير)")
        st.write("🔊 **النطق الصوتي:** /ˈfluː.ən.si/")

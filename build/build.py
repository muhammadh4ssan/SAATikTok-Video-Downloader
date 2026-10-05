#!/usr/bin/env python3
"""Generates the tool pages (video / mp3 / photo) in English, Urdu, Hindi and Arabic,
plus public/sitemap.xml.  Run:  python3 build/build.py
Ad code for every page lives in build/ads-head.html (leave empty for no ads)."""
import json, html, pathlib

DOMAIN = "https://saatik.site"
HERE = pathlib.Path(__file__).resolve().parent
PUB = HERE.parent / "public"
ADS = (HERE / "ads-head.html").read_text(encoding="utf-8").strip() if (HERE / "ads-head.html").exists() else ""
LASTMOD = "2026-10-05"

LANGS = ["en", "ur", "hi", "ar"]
PAGES = ["video", "mp3", "photo"]
SLUG = {"video": "", "mp3": "tiktok-mp3-downloader", "photo": "tiktok-photo-downloader"}

FONTS = {
    "en": "family=Outfit:wght@400;600;700",
    "ur": "family=Noto+Naskh+Arabic:wght@400;600;700",
    "ar": "family=Noto+Naskh+Arabic:wght@400;600;700",
    "hi": "family=Noto+Sans+Devanagari:wght@400;600;700",
}

L = {
"en": dict(
    dir="ltr", name="English",
    ph="Paste TikTok link here", paste="Paste", go="Download",
    how="How it works", faq="Frequently asked questions", other="Other tools",
    steps=["Open TikTok, tap Share, then Copy link.", "Paste the link in the box above.", "Tap Download and choose video, MP3 or photos."],
    footer="For personal use only. Respect the creator's rights. This site is not affiliated with TikTok.",
    nav=dict(video="TikTok Video Downloader", mp3="TikTok MP3 Converter", photo="TikTok Photo Downloader"),
    common=[("Is it free?", "Yes, it is free. No sign-up or app needed."),
            ("Does it work on iPhone, Android and PC?", "Yes. It works in any modern browser on iPhone, Android, Windows and Mac.")],
    T=dict(first="Paste a TikTok link first.", getting="Getting your file...", clip="Allow clipboard access, or paste the link manually.",
           hd="Download HD video", sd="Download video", mp3="Download MP3", all="Download all photos",
           photo="photo", photos="photos", save="Save", toLight="Switch to light theme", toDark="Switch to dark theme",
           err=dict(invalid="Paste a valid TikTok link.", notfound="Post not found. It may be private or removed.",
                    busy="The service is busy. Try again in a moment.", generic="Something went wrong.")),
    pages=dict(
        video=dict(title="TikTok Video Downloader Without Watermark (HD) - Saatik",
                   desc="Download TikTok videos in HD without watermark. Paste the link and save the video, MP3 or photos for free.",
                   h1="Download TikTok videos without watermark",
                   lead="Paste the link, get the HD video, the photos or just the music.",
                   faq=[("How do I download a TikTok video without watermark?", "Copy the video link from TikTok, paste it in the box above and tap Download. Then choose Download HD video."),
                        ("Can I download private videos?", "No. Only public videos can be downloaded. If a video is private or removed, you will see a 'not found' message.")]),
        mp3=dict(title="TikTok to MP3 Converter - Download TikTok Audio - Saatik",
                 desc="Convert TikTok videos to MP3. Paste the link and download the sound or music from any public TikTok for free.",
                 h1="TikTok to MP3 converter",
                 lead="Paste a TikTok link and save its sound as an MP3 file.",
                 faq=[("How do I convert a TikTok video to MP3?", "Paste the TikTok link above, tap Download, then choose Download MP3."),
                      ("Can I download only the music from a TikTok?", "Yes. The MP3 button saves the sound of the post without the video.")]),
        photo=dict(title="TikTok Photo Downloader - Save Slideshow Images - Saatik",
                   desc="Download TikTok photos and slideshow images in original quality. Save one photo or all of them for free.",
                   h1="TikTok photo downloader",
                   lead="Paste a TikTok photo post link and save every picture.",
                   faq=[("How do I download photos from a TikTok slideshow?", "Paste the link of the photo post above and tap Download. Tap any picture to save it, or use Download all photos."),
                        ("Why does it ask to allow multiple downloads?", "Download all photos saves the pictures one after another, so your browser may ask you to allow multiple downloads. Tap Allow.")]),
    )),

"ur": dict(
    dir="rtl", name="اردو",
    ph="یہاں TikTok لنک پیسٹ کریں", paste="پیسٹ", go="ڈاؤن لوڈ کریں",
    how="یہ کیسے کام کرتا ہے", faq="عام سوالات", other="دیگر ٹولز",
    steps=["TikTok کھولیں، Share دبائیں، پھر Copy link کریں۔", "لنک اوپر والے خانے میں پیسٹ کریں۔", "ڈاؤن لوڈ دبائیں اور ویڈیو، MP3 یا تصاویر چنیں۔"],
    footer="صرف ذاتی استعمال کے لیے۔ تخلیق کار کے حقوق کا احترام کریں۔ یہ سائٹ TikTok سے وابستہ نہیں ہے۔",
    nav=dict(video="TikTok ویڈیو ڈاؤن لوڈر", mp3="TikTok MP3 کنورٹر", photo="TikTok فوٹو ڈاؤن لوڈر"),
    common=[("کیا یہ مفت ہے؟", "جی ہاں، یہ مفت ہے۔ نہ سائن اپ چاہیے نہ کوئی ایپ۔"),
            ("کیا یہ iPhone، Android اور کمپیوٹر پر چلتا ہے؟", "جی ہاں، یہ ہر جدید براؤزر میں iPhone، Android، Windows اور Mac پر چلتا ہے۔")],
    T=dict(first="پہلے TikTok لنک پیسٹ کریں۔", getting="آپ کی فائل تیار ہو رہی ہے...", clip="کلپ بورڈ کی اجازت دیں، یا لنک خود پیسٹ کریں۔",
           hd="HD ویڈیو ڈاؤن لوڈ کریں", sd="ویڈیو ڈاؤن لوڈ کریں", mp3="MP3 ڈاؤن لوڈ کریں", all="تمام تصاویر ڈاؤن لوڈ کریں",
           photo="تصویر", photos="تصاویر", save="محفوظ کریں", toLight="لائٹ تھیم پر جائیں", toDark="ڈارک تھیم پر جائیں",
           err=dict(invalid="درست TikTok لنک پیسٹ کریں۔", notfound="پوسٹ نہیں ملی۔ ہو سکتا ہے وہ پرائیویٹ ہو یا ہٹا دی گئی ہو۔",
                    busy="سروس مصروف ہے۔ تھوڑی دیر بعد دوبارہ کوشش کریں۔", generic="کچھ غلط ہو گیا۔")),
    pages=dict(
        video=dict(title="TikTok ویڈیو ڈاؤن لوڈر بغیر واٹر مارک (HD) - Saatik",
                   desc="TikTok ویڈیو بغیر واٹر مارک HD میں ڈاؤن لوڈ کریں۔ لنک پیسٹ کریں اور ویڈیو، MP3 یا تصاویر مفت محفوظ کریں۔",
                   h1="TikTok ویڈیو بغیر واٹر مارک ڈاؤن لوڈ کریں",
                   lead="لنک پیسٹ کریں اور HD ویڈیو، تصاویر یا صرف میوزک حاصل کریں۔",
                   faq=[("TikTok ویڈیو بغیر واٹر مارک کیسے ڈاؤن لوڈ کریں؟", "TikTok سے ویڈیو کا لنک کاپی کریں، اوپر والے خانے میں پیسٹ کریں اور ڈاؤن لوڈ دبائیں۔ پھر HD ویڈیو ڈاؤن لوڈ کریں چنیں۔"),
                        ("کیا پرائیویٹ ویڈیو ڈاؤن لوڈ ہو سکتی ہے؟", "نہیں۔ صرف پبلک ویڈیوز ڈاؤن لوڈ ہو سکتی ہیں۔ اگر ویڈیو پرائیویٹ ہو یا ہٹا دی گئی ہو تو “نہیں ملی” کا پیغام آئے گا۔")]),
        mp3=dict(title="TikTok سے MP3 کنورٹر - TikTok آڈیو ڈاؤن لوڈ کریں - Saatik",
                 desc="TikTok ویڈیو کو MP3 میں بدلیں۔ لنک پیسٹ کریں اور کسی بھی پبلک TikTok کی آواز یا میوزک مفت ڈاؤن لوڈ کریں۔",
                 h1="TikTok سے MP3 کنورٹر",
                 lead="TikTok لنک پیسٹ کریں اور اس کی آواز MP3 فائل میں محفوظ کریں۔",
                 faq=[("TikTok ویڈیو کو MP3 میں کیسے بدلیں؟", "اوپر TikTok لنک پیسٹ کریں، ڈاؤن لوڈ دبائیں، پھر MP3 ڈاؤن لوڈ کریں چنیں۔"),
                      ("کیا TikTok سے صرف میوزک ڈاؤن لوڈ ہو سکتا ہے؟", "جی ہاں۔ MP3 بٹن ویڈیو کے بغیر صرف آواز محفوظ کرتا ہے۔")]),
        photo=dict(title="TikTok فوٹو ڈاؤن لوڈر - سلائیڈ شو کی تصاویر محفوظ کریں - Saatik",
                   desc="TikTok کی تصاویر اور سلائیڈ شو اصل کوالٹی میں ڈاؤن لوڈ کریں۔ ایک تصویر یا سب مفت محفوظ کریں۔",
                   h1="TikTok فوٹو ڈاؤن لوڈر",
                   lead="TikTok فوٹو پوسٹ کا لنک پیسٹ کریں اور ہر تصویر محفوظ کریں۔",
                   faq=[("TikTok سلائیڈ شو کی تصاویر کیسے ڈاؤن لوڈ کریں؟", "فوٹو پوسٹ کا لنک اوپر پیسٹ کریں اور ڈاؤن لوڈ دبائیں۔ کسی بھی تصویر پر ٹیپ کر کے محفوظ کریں، یا تمام تصاویر ڈاؤن لوڈ کریں استعمال کریں۔"),
                        ("براؤزر ایک سے زیادہ ڈاؤن لوڈ کی اجازت کیوں مانگتا ہے؟", "تمام تصاویر ڈاؤن لوڈ کریں تصاویر کو ایک کے بعد ایک محفوظ کرتا ہے، اس لیے براؤزر اجازت مانگ سکتا ہے۔ Allow دبائیں۔")]),
    )),

"hi": dict(
    dir="ltr", name="हिन्दी",
    ph="यहाँ TikTok लिंक पेस्ट करें", paste="पेस्ट", go="डाउनलोड करें",
    how="यह कैसे काम करता है", faq="अक्सर पूछे जाने वाले सवाल", other="अन्य टूल",
    steps=["TikTok खोलें, Share दबाएँ, फिर Copy link करें।", "लिंक ऊपर वाले बॉक्स में पेस्ट करें।", "डाउनलोड दबाएँ और वीडियो, MP3 या फ़ोटो चुनें।"],
    footer="केवल निजी उपयोग के लिए। क्रिएटर के अधिकारों का सम्मान करें। यह साइट TikTok से जुड़ी नहीं है।",
    nav=dict(video="TikTok वीडियो डाउनलोडर", mp3="TikTok MP3 कन्वर्टर", photo="TikTok फ़ोटो डाउनलोडर"),
    common=[("क्या यह मुफ़्त है?", "हाँ, यह मुफ़्त है। न साइन-अप चाहिए न कोई ऐप।"),
            ("क्या यह iPhone, Android और कंप्यूटर पर चलता है?", "हाँ, यह हर आधुनिक ब्राउज़र में iPhone, Android, Windows और Mac पर चलता है।")],
    T=dict(first="पहले TikTok लिंक पेस्ट करें।", getting="आपकी फ़ाइल तैयार हो रही है...", clip="क्लिपबोर्ड की अनुमति दें, या लिंक खुद पेस्ट करें।",
           hd="HD वीडियो डाउनलोड करें", sd="वीडियो डाउनलोड करें", mp3="MP3 डाउनलोड करें", all="सभी फ़ोटो डाउनलोड करें",
           photo="फ़ोटो", photos="फ़ोटो", save="सेव करें", toLight="लाइट थीम पर जाएँ", toDark="डार्क थीम पर जाएँ",
           err=dict(invalid="सही TikTok लिंक पेस्ट करें।", notfound="पोस्ट नहीं मिली। हो सकता है वह प्राइवेट हो या हटा दी गई हो।",
                    busy="सेवा व्यस्त है। थोड़ी देर बाद फिर कोशिश करें।", generic="कुछ गलत हो गया।")),
    pages=dict(
        video=dict(title="TikTok वीडियो डाउनलोडर बिना वॉटरमार्क (HD) - Saatik",
                   desc="TikTok वीडियो बिना वॉटरमार्क HD में डाउनलोड करें। लिंक पेस्ट करें और वीडियो, MP3 या फ़ोटो मुफ़्त सेव करें।",
                   h1="TikTok वीडियो बिना वॉटरमार्क डाउनलोड करें",
                   lead="लिंक पेस्ट करें और HD वीडियो, फ़ोटो या सिर्फ़ म्यूज़िक पाएँ।",
                   faq=[("TikTok वीडियो बिना वॉटरमार्क कैसे डाउनलोड करें?", "TikTok से वीडियो का लिंक कॉपी करें, ऊपर वाले बॉक्स में पेस्ट करें और डाउनलोड दबाएँ। फिर HD वीडियो डाउनलोड करें चुनें।"),
                        ("क्या प्राइवेट वीडियो डाउनलोड हो सकता है?", "नहीं। सिर्फ़ पब्लिक वीडियो डाउनलोड हो सकते हैं। अगर वीडियो प्राइवेट है या हटा दिया गया है तो “नहीं मिली” का संदेश आएगा।")]),
        mp3=dict(title="TikTok से MP3 कन्वर्टर - TikTok ऑडियो डाउनलोड करें - Saatik",
                 desc="TikTok वीडियो को MP3 में बदलें। लिंक पेस्ट करें और किसी भी पब्लिक TikTok की आवाज़ या म्यूज़िक मुफ़्त डाउनलोड करें।",
                 h1="TikTok से MP3 कन्वर्टर",
                 lead="TikTok लिंक पेस्ट करें और उसकी आवाज़ MP3 फ़ाइल में सेव करें।",
                 faq=[("TikTok वीडियो को MP3 में कैसे बदलें?", "ऊपर TikTok लिंक पेस्ट करें, डाउनलोड दबाएँ, फिर MP3 डाउनलोड करें चुनें।"),
                      ("क्या TikTok से सिर्फ़ म्यूज़िक डाउनलोड हो सकता है?", "हाँ। MP3 बटन वीडियो के बिना सिर्फ़ आवाज़ सेव करता है।")]),
        photo=dict(title="TikTok फ़ोटो डाउनलोडर - स्लाइडशो की तस्वीरें सेव करें - Saatik",
                   desc="TikTok की फ़ोटो और स्लाइडशो ओरिजिनल क्वालिटी में डाउनलोड करें। एक फ़ोटो या सभी मुफ़्त सेव करें।",
                   h1="TikTok फ़ोटो डाउनलोडर",
                   lead="TikTok फ़ोटो पोस्ट का लिंक पेस्ट करें और हर तस्वीर सेव करें।",
                   faq=[("TikTok स्लाइडशो की फ़ोटो कैसे डाउनलोड करें?", "फ़ोटो पोस्ट का लिंक ऊपर पेस्ट करें और डाउनलोड दबाएँ। किसी भी तस्वीर पर टैप करके सेव करें, या सभी फ़ोटो डाउनलोड करें इस्तेमाल करें।"),
                        ("ब्राउज़र कई डाउनलोड की अनुमति क्यों माँगता है?", "सभी फ़ोटो डाउनलोड करें तस्वीरों को एक के बाद एक सेव करता है, इसलिए ब्राउज़र अनुमति माँग सकता है। Allow दबाएँ।")]),
    )),

"ar": dict(
    dir="rtl", name="العربية",
    ph="الصق رابط TikTok هنا", paste="لصق", go="تنزيل",
    how="كيف يعمل", faq="الأسئلة الشائعة", other="أدوات أخرى",
    steps=["افتح TikTok واضغط على مشاركة ثم نسخ الرابط.", "الصق الرابط في الخانة أعلاه.", "اضغط تنزيل ثم اختر الفيديو أو MP3 أو الصور."],
    footer="للاستخدام الشخصي فقط. احترم حقوق صانع المحتوى. هذا الموقع غير تابع لـ TikTok.",
    nav=dict(video="تنزيل فيديوهات TikTok", mp3="محول TikTok إلى MP3", photo="تنزيل صور TikTok"),
    common=[("هل الخدمة مجانية؟", "نعم، مجانية ولا تحتاج إلى تسجيل أو تطبيق."),
            ("هل تعمل على iPhone وAndroid والكمبيوتر؟", "نعم، تعمل في أي متصفح حديث على iPhone وAndroid وWindows وMac.")],
    T=dict(first="الصق رابط TikTok أولاً.", getting="جارٍ تجهيز الملف...", clip="اسمح بالوصول إلى الحافظة أو الصق الرابط يدوياً.",
           hd="تنزيل فيديو HD", sd="تنزيل الفيديو", mp3="تنزيل MP3", all="تنزيل كل الصور",
           photo="صورة", photos="صور", save="حفظ", toLight="التبديل إلى الوضع الفاتح", toDark="التبديل إلى الوضع الداكن",
           err=dict(invalid="الصق رابط TikTok صالحاً.", notfound="لم يتم العثور على المنشور. قد يكون خاصاً أو محذوفاً.",
                    busy="الخدمة مشغولة. حاول مرة أخرى بعد قليل.", generic="حدث خطأ ما.")),
    pages=dict(
        video=dict(title="تنزيل فيديوهات TikTok بدون علامة مائية (HD) - Saatik",
                   desc="نزّل فيديوهات TikTok بدون علامة مائية وبجودة HD. الصق الرابط واحفظ الفيديو أو MP3 أو الصور مجاناً.",
                   h1="تنزيل فيديوهات TikTok بدون علامة مائية",
                   lead="الصق الرابط واحصل على الفيديو بجودة HD أو الصور أو الموسيقى فقط.",
                   faq=[("كيف أنزّل فيديو TikTok بدون علامة مائية؟", "انسخ رابط الفيديو من TikTok والصقه في الخانة أعلاه ثم اضغط تنزيل، واختر تنزيل فيديو HD."),
                        ("هل يمكن تنزيل فيديو خاص؟", "لا. يمكن تنزيل الفيديوهات العامة فقط. إذا كان الفيديو خاصاً أو محذوفاً ستظهر رسالة “لم يتم العثور”.")]),
        mp3=dict(title="محول TikTok إلى MP3 - تنزيل صوت TikTok - Saatik",
                 desc="حوّل فيديوهات TikTok إلى MP3. الصق الرابط ونزّل الصوت أو الموسيقى من أي منشور عام مجاناً.",
                 h1="محول TikTok إلى MP3",
                 lead="الصق رابط TikTok واحفظ صوته كملف MP3.",
                 faq=[("كيف أحوّل فيديو TikTok إلى MP3؟", "الصق رابط TikTok أعلاه واضغط تنزيل ثم اختر تنزيل MP3."),
                      ("هل يمكن تنزيل الموسيقى فقط من TikTok؟", "نعم. زر MP3 يحفظ صوت المنشور بدون الفيديو.")]),
        photo=dict(title="تنزيل صور TikTok - حفظ صور السلايد شو - Saatik",
                   desc="نزّل صور TikTok وعروض الشرائح بجودتها الأصلية. احفظ صورة واحدة أو كلها مجاناً.",
                   h1="تنزيل صور TikTok",
                   lead="الصق رابط منشور الصور في TikTok واحفظ كل صورة.",
                   faq=[("كيف أنزّل صور سلايد شو TikTok؟", "الصق رابط منشور الصور أعلاه واضغط تنزيل. اضغط على أي صورة لحفظها أو استخدم تنزيل كل الصور."),
                        ("لماذا يطلب المتصفح السماح بتنزيلات متعددة؟", "زر تنزيل كل الصور يحفظ الصور واحدة تلو الأخرى، لذلك قد يطلب المتصفح الإذن. اضغط سماح.")]),
    )),
}

EARLY = ("<script>try{var t=localStorage.getItem('theme')||(matchMedia('(prefers-color-scheme: light)').matches?'light':'dark');"
         "document.documentElement.setAttribute('data-theme',t)}catch(e){document.documentElement.setAttribute('data-theme','dark')}</script>")

TEMPLATE = """<!DOCTYPE html>
<html lang="{{lang}}" dir="{{dir}}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{{title}}</title>
{{early}}
<meta name="description" content="{{desc}}">
<link rel="canonical" href="{{canonical}}">
{{hreflang}}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#080812">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{{font}}&display=swap">
<link rel="stylesheet" href="/style.css">
{{ads}}
<script type="application/ld+json">{{jsonld}}</script>
</head>
<body>
<div class="orb o1"></div><div class="orb o2"></div>
<main class="wrap">
  <div class="top">
    <nav class="langs" aria-label="Language">{{langs}}</nav>
    <button class="tbtn" id="theme" type="button" aria-label="Theme"></button>
  </div>
  <h1>{{h1}}</h1>
  <p class="lead">{{lead}}</p>

  <div class="ad" id="ad-top"></div>

  <section class="glass box">
    <div class="in">
      <input id="url" dir="auto" type="url" inputmode="url" placeholder="{{ph}}" aria-label="{{ph}}" autocomplete="off">
      <button class="btn" id="paste" type="button">{{paste}}</button>
    </div>
    <button class="btn go" id="go" type="button">{{go}}</button>
    <div id="msg" role="status"></div>
  </section>

  <div class="ad" id="ad-mid"></div>

  <section class="glass res" id="res" hidden>
    <img id="cover" alt="" referrerpolicy="no-referrer">
    <div class="meta">
      <b id="title"></b>
      <span id="author"></span>
      <div class="acts">
        <a class="btn main" id="b-hd" href="#"></a>
        <a class="btn" id="b-sd" href="#"></a>
        <a class="btn" id="b-mp3" href="#"></a>
      </div>
    </div>
  </section>

  <section class="glass photos" id="photos" hidden>
    <div class="ph-head"><b id="ph-count"></b><button class="btn main" id="b-all" type="button"></button></div>
    <div class="grid" id="grid"></div>
  </section>

  <section class="glass how">
    <h2>{{how}}</h2>
    <ol>{{steps}}</ol>
  </section>

  <section class="glass faq">
    <h2>{{faqh}}</h2>
    {{faq}}
  </section>

  <nav class="related" aria-label="{{other}}">{{related}}</nav>

  <div class="ad" id="ad-bottom"></div>

  <footer>{{footer}}<br><a href="/privacy">Privacy Policy</a> &middot; <a href="/terms">Terms of Use</a></footer>
</main>
<script>window.T={{T}};</script>
<script src="/app.js"></script>
</body>
</html>
"""


def path(lang, page):
    base = "" if lang == "en" else "/" + lang
    return base + "/" + SLUG[page]


def out_file(lang, page):
    d = PUB if lang == "en" else PUB / lang
    d.mkdir(parents=True, exist_ok=True)
    return d / ("index.html" if page == "video" else SLUG[page] + ".html")


def esc(s):
    return html.escape(s, quote=True)


def build_page(lang, page):
    c = L[lang]
    p = c["pages"][page]
    faq = c["common"] + p["faq"]
    url = DOMAIN + path(lang, page)

    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{DOMAIN + path(l, page)}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{DOMAIN + path("en", page)}">'

    langs = "".join(
        f'<a href="{path(l, page)}" hreflang="{l}" lang="{l}"' + (' aria-current="page"' if l == lang else "") + f">{esc(L[l]['name'])}</a>"
        for l in LANGS)
    related = "".join(f'<a href="{path(lang, q)}">{esc(c["nav"][q])}</a>' for q in PAGES if q != page)
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
    steps = "".join(f"<li>{esc(s)}</li>" for s in c["steps"])
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
    }, ensure_ascii=False)

    t = TEMPLATE
    rep = {
        "lang": lang, "dir": c["dir"], "title": esc(p["title"]), "early": EARLY, "desc": esc(p["desc"]),
        "canonical": url, "hreflang": alts, "font": FONTS[lang], "ads": ADS, "jsonld": jsonld,
        "langs": langs, "h1": esc(p["h1"]), "lead": esc(p["lead"]), "ph": esc(c["ph"]), "paste": esc(c["paste"]),
        "go": esc(c["go"]), "how": esc(c["how"]), "steps": steps, "faqh": esc(c["faq"]), "faq": faq_html,
        "other": esc(c["other"]), "related": related, "footer": esc(c["footer"]),
        "T": json.dumps(c["T"], ensure_ascii=False),
    }
    for k, v in rep.items():
        t = t.replace("{{" + k + "}}", v)
    assert "{{" not in t, "unreplaced token"
    out_file(lang, page).write_text(t, encoding="utf-8")


def build_sitemap():
    urls = [path(l, p) for p in PAGES for l in LANGS] + ["/privacy", "/terms"]
    rows = "\n".join(
        f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{LASTMOD}</lastmod><priority>{'1.0' if u == '/' else '0.8' if u not in ('/privacy', '/terms') else '0.3'}</priority></url>"
        for u in urls)
    (PUB / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "\n</urlset>\n",
        encoding="utf-8")


if __name__ == "__main__":
    for lang in LANGS:
        for page in PAGES:
            build_page(lang, page)
    build_sitemap()
    print("built", len(LANGS) * len(PAGES), "pages + sitemap")

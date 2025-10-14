import random
from django.utils.text import slugify
from django.utils import timezone
from account.models import USER as User, UserSide
from blog.models import Blog, PostCategory, Tag, Comment, Fav, Save
from club.models import Club
from event.models import EventsCategory, Event, EventUser
from contact.models import Request, ContactMessage
from FileLibrary.models import FileLibrary
from send_email.models import EmailLog
from about.models import FAQ, TeamMember, AboutPage


def seed_data():
    u = User.objects.first()
    if not u:
        raise Exception("❌ هیچ کاربری وجود ندارد! ابتدا یک کاربر بساز.")

    # === UserSide ===
    for title in ["دانش‌آموز", "مدرس", "مدیر", "مشاور", "منتور"]:
        UserSide.objects.get_or_create(u_title=title)

    # === Categories ===
    cat_titles = ["روانشناسی", "توسعه فردی", "هوش مصنوعی", "یادگیری ماشینی", "تحلیل رفتار"]
    for title in cat_titles:
        PostCategory.objects.get_or_create(
            title=title,
            defaults={"post_bg_color": f"#{random.randint(0, 0xFFFFFF):06x}"}
        )

    # === Tags ===
    for tag in ["تمرکز", "خلاقیت", "ذهن‌آگاهی", "تکنولوژی", "تحلیل"]:
        Tag.objects.get_or_create(title=tag)

    # === Clubs ===
    for i in range(5):
        Club.objects.get_or_create(
            slug=f"club-{i+1}",
            defaults={
                "club_name": f"کلاب {i+1}",
                "club_color": f"#{random.randint(0, 0xFFFFFF):06x}"
            }
        )

    # === Event Categories ===
    for title in ["کارگاه آموزشی", "جلسه گفت‌وگو", "وبینار", "دوره تخصصی"]:
        EventsCategory.objects.get_or_create(title=title)

    # === Events ===
    clubs = list(Club.objects.all())
    ecats = list(EventsCategory.objects.all())
    event_titles = [
        "دوره آشنایی با هوش مصنوعی",
        "کارگاه افزایش تمرکز ذهن",
        "جلسه معرفی MindGuess",
        "رویداد تحلیل رفتار کاربران",
        "دوره روان‌شناسی مدرن"
    ]

    for title in event_titles:
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Event.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        ev, _ = Event.objects.get_or_create(
            slug=slug,
            defaults={
                "title": title,
                "club": random.choice(clubs),
                "teacher_name": "دکتر فرهادی",
                "price": random.randint(100000, 500000),
                "save_type": "P",
                "short_describe": f"توضیح کوتاه درباره {title}",
                "full_describ": f"این رویداد درباره {title} است و شامل مباحث جذاب و کاربردی می‌باشد.",
                "author": u,
            },
        )
        ev.event_cat.set(random.sample(ecats, k=min(2, len(ecats))))

    # === Blogs ===
    blog_titles = [
        "چگونه هوش مصنوعی ذهن انسان را درک می‌کند؟",
        "۵ روش برای افزایش تمرکز ذهنی",
        "روان‌شناسی تصمیم‌گیری در شرایط بحرانی",
        "نقش احساسات در تحلیل رفتاری کاربران",
        "آینده‌ی تعامل انسان و ماشین",
        "راز پشت انتخاب‌های ما چیست؟",
        "چطور ذهن ناخودآگاه را آموزش دهیم؟",
        "تحلیل الگوهای ذهنی در MindGuess",
        "هوش مصنوعی و مرزهای اخلاقی آن",
        "تأثیر خستگی ذهن بر عملکرد شناختی"
    ]

    categories = list(PostCategory.objects.all())
    tags = list(Tag.objects.all())

    for title in blog_titles:
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Blog.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        b, _ = Blog.objects.get_or_create(
            slug=slug,
            defaults={
                "title": title,
                "author": u,
                "save_type": "P",
                "text": f"در این مقاله به بررسی موضوع «{title}» می‌پردازیم و آن را از دیدگاه تحلیلی و روان‌شناختی MindGuess تحلیل می‌کنیم.",
            },
        )
        if categories:
            b.post_cat.set(random.sample(categories, k=min(3, len(categories))))
        if tags:
            b.post_tag.set(random.sample(tags, k=min(3, len(tags))))

    # === FileLibrary ===
    for i in range(5):
        FileLibrary.objects.get_or_create(title=f"فایل آموزشی {i+1}")

    # === ContactMessage ===
    for i in range(5):
        ContactMessage.objects.get_or_create(
            email=f"user{i+1}@example.com",
            defaults={
                "name": f"کاربر {i+1}",
                "subject": "سؤال درباره MindGuess",
                "message": f"چطور می‌توانم در دوره شماره {i+1} ثبت‌نام کنم؟"
            }
        )

    # === Request ===
    for i in range(5):
        Request.objects.get_or_create(
            user=u,
            lesson_title=f"درخواست مشاوره شماره {i+1}",
            defaults={"teacher_name": "استاد رضایی", "description": "نیاز به راهنمایی دارم."},
        )

    # === EventUser ===
    users = list(User.objects.all())
    events = list(Event.objects.all())
    for i in range(10):
        EventUser.objects.get_or_create(
            user=random.choice(users),
            event=random.choice(events),
            club=random.choice(clubs),
        )

    # === Comments (on Blog & Event) ===
    blogs = list(Blog.objects.all())
    for i in range(10):
        Comment.objects.get_or_create(
            user=random.choice(users),
            blog=random.choice(blogs),
            defaults={
                "message": f"مقاله فوق‌العاده بود! ({i+1})",
                "event": random.choice(events),
            },
        )

    # === Fav & Save ===
    for i in range(5):
        Fav.objects.get_or_create(
            user=u,
            blog=random.choice(blogs),
            event=random.choice(events),
        )
        Save.objects.get_or_create(
            user=u,
            blog=random.choice(blogs),
            event=random.choice(events),
        )

    # === FAQ ===
    faqs = {
        "چگونه در سایت ثبت‌نام کنم؟": "با ورود شماره تلفن و دریافت کد تأیید می‌توانید ثبت‌نام کنید.",
        "مایند‌کوین چیست؟": "واحد ارز داخلی اپلیکیشن برای تحلیل‌ها و پرسش‌هاست.",
        "آیا اطلاعات من محرمانه است؟": "بله، تمام داده‌ها هش شده و فقط برای تحلیل آماری استفاده می‌شوند.",
    }
    for q, a in faqs.items():
        FAQ.objects.get_or_create(question=q, defaults={"answer": a})

    # === TeamMember ===
    members = [
        ("حمید رضوی", "توسعه‌دهنده ارشد", "برنامه‌نویس بک‌اند و معمار سیستم MindGuess."),
        ("نرگس احمدی", "طراح رابط کاربری", "طراح تجربه کاربر و رابط کاربری سیستم."),
        ("مهدی شریفی", "کارشناس داده", "تحلیل‌گر داده و توسعه مدل‌های رفتاری."),
    ]
    for name, pos, bio in members:
        TeamMember.objects.get_or_create(full_name=name, defaults={"position": pos, "bio": bio})

    # === AboutPage ===
    about_pages = [
        ("تاریخچه MindGuess", "history", "پروژه MindGuess از سال 2023 آغاز شد..."),
        ("ماموریت ما", "mission", "هدف ما شناخت ذهن از طریق هوش مصنوعی است."),
        ("تیم ما", "team", "تیم ما متشکل از متخصصان حوزه روان‌شناسی و فناوری است."),
    ]
    for title, ptype, content in about_pages:
        AboutPage.objects.get_or_create(
            slug=slugify(title),
            defaults={"title": title, "page_type": ptype, "content": content},
        )

    # === EmailLog ===
    for i in range(5):
        EmailLog.objects.get_or_create(
            to_email=f"user{i+1}@example.com",
            subject="تست ایمیل",
            defaults={"message": "این یک ایمیل آزمایشی است.", "status": "sent", "created_by": u},
        )

    print("✅ داده‌های اولیه با موفقیت ساخته شدند!")



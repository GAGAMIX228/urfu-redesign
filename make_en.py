"""Собирает английские версии страниц (CatalogEn.dc.html, AdmissionEn.dc.html) из русских:
английская шапка и подвал берутся с MainEn.dc.html, тексты переводятся по словарю ниже.
Запуск: python make_en.py — после правок русских страниц английские пересобираются этой же командой."""
import os
import re
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
EN = open('MainEn.dc.html', encoding='utf-8').read()
EN_HEAD = '<div>' + EN[EN.index('<a href="#main" class="skip">'):EN.index('</header>') + len('</header>')]
EN_FOOT = EN[EN.index('<footer'):EN.index('</footer>') + len('</footer>')]

# ссылки между английскими страницами
EN_LINKS = {'Admission.dc.html': 'AdmissionEn.dc.html', 'Catalog.dc.html': 'CatalogEn.dc.html', 'Main.dc.html': 'MainEn.dc.html'}

PROGRAMS = [
    ('Алгоритмы искусственного интеллекта', 'Artificial Intelligence Algorithms'),
    ('Прикладной искусственный интеллект', 'Applied Artificial Intelligence'),
    ('Интеллектуальные системы в гуманитарной сфере', 'Intelligent Systems in the Humanities'),
    ('Инфокоммуникационные технологии и системы связи', 'Infocommunication Technologies and Communication Systems'),
    ('Информатика и вычислительная техника', 'Computer Science and Engineering'),
    ('Материаловедение и технологии материалов', 'Materials Science and Technology'),
    ('Электроэнергетика и электротехника', 'Electric Power and Electrical Engineering'),
    ('Ядерная энергетика и теплофизика', 'Nuclear Power and Thermal Physics'),
    ('Теплоэнергетика и теплотехника', 'Heat Power Engineering'),
    ('Информационная безопасность', 'Information Security'),
    ('Международные отношения', 'International Relations'),
    ('Программная инженерия', 'Software Engineering'),
    ('Прикладная информатика', 'Applied Computer Science'),
    ('Прикладная математика', 'Applied Mathematics'),
    ('Бизнес-информатика', 'Business Informatics'),
    ('Радиотехника', 'Radio Engineering'),
    ('Архитектура', 'Architecture'),
    ('Строительство', 'Civil Engineering'),
    ('Металлургия', 'Metallurgy'),
    ('Психология', 'Psychology'),
    ('Журналистика', 'Journalism'),
    ('Лингвистика', 'Linguistics'),
    ('Филология', 'Philology'),
    ('Менеджмент', 'Management'),
]
INSTITUTES = [('ИРИТ-РтФ', 'IRIT-RTF'), ('ИЕНиМ', 'INSM'), ('ИНМиТ', 'INMT'), ('УралЭНИН', 'UralENIN'), ('ИнЭУ', 'GSEM'), ('ИСА', 'ICEA'), ('УГИ', 'UIH'), ('ФТИ', 'IPT')]
EXAM_WORDS = [('творческое испытание', 'creative test'), ('иностранный язык', 'foreign language'), ('обществознание', 'social studies'),
              ('информатика', 'computer science'), ('математика', 'mathematics'), ('физика', 'physics'), ('химия', 'chemistry'),
              ('биология', 'biology'), ('история', 'history'), ('литература', 'literature'), ('русский', 'Russian'), (' или ', ' or ')]

COMMON = [
    ('[институт]', '[institute]'), ('[балл]', '[score]'), ('[число]', '[number]'), ('[дата]', '[date]'),
    ('Главная', 'Home'), ('Поступление', 'Admissions'), ('Обучение', 'Study'), ('Поступить', 'Admissions'),
    ('Например, 240', 'e.g. 240'), ('Например, дизайн', 'e.g. design'),
]

CATALOG = [
    ('Отметьте свои предметы ЕГЭ и баллы — покажем, куда вы можете поступить. Не знаете, с чего начать?',
     'Tick your Unified State Exam (EGE) subjects and enter your score — we will show where you can apply. International applicants may take UrFU entrance tests instead of the EGE.'),
    (' <a href="Quiz.dc.html">Подбор за 3 вопроса</a>', ''),
    ('Специалитет и магистратура открываются тем же каталогом — с другими фильтрами.', "Specialist and Master's programmes use the same catalogue with other filters."),
    ('После школы — бакалавриат (обычно 4 года) или специалитет (5–6 лет). Магистратура — следующая ступень после бакалавриата.', "After school you can apply for a Bachelor's (usually 4 years) or a Specialist degree (5–6 years). A Master's comes after a Bachelor's."),
    ('Отметьте ещё один предмет, смените область или сбросьте фильтры.', 'Tick another subject, change the field or reset the filters.'),
    ('С этими предметами программ не нашлось', 'No programmes match these subjects'),
    ('В прототипе показан бакалавриат', "The prototype shows Bachelor's programmes"),
    ('Вернуться к бакалавриату', "Back to Bachelor's"),
    ('Сравним с проходным баллом 2025 года', 'Compared with the 2025 pass mark'),
    ('Сравним с проходным баллом 2025 года', 'Compared with the 2025 pass mark'),
    ('Сначала — где хватает баллов', 'Where your score is enough comes first'),
    ('Проходной балл уточняется', 'Pass mark to be confirmed'),
    ('Ваших баллов хватает', 'Your score is enough'),
    ('Выбрано для сравнения:', 'Selected to compare:'),
    ('Сравнение программ', 'Compare programmes'),
    ('Каталог программ', 'Programme catalogue'),
    ('Название программы', 'Programme name'),
    ('Мои предметы ЕГЭ', 'My EGE subjects'),
    ('Моя сумма баллов', 'My total score'),
    ('Сбросить фильтры', 'Reset filters'),
    ('Можно сравнить до 3', 'Compare up to 3'),
    ('Введите сумму баллов', 'Enter your score'),
    ('Проходной уточняется', 'Pass mark TBC'),
    ('Бюджетных мест', 'State-funded places'), ('Стоимость в год', 'Tuition per year'), ('Проходной 2025', 'Pass mark 2025'),
    ('Экзамены ЕГЭ', 'EGE exams'), ('Цена в год', 'Per year'), ('Проходной балл {{p.sy}}', 'Pass mark {{p.sy}}'), ('Проходной балл 2025', 'Pass mark 2025'), ('Бюджетных мест', 'State-funded places'), ('Бюджет', 'Funded'),
    ('✓ В сравнении', '✓ Comparing'), ('+ Сравнить', '+ Compare'), ('Сравнить', 'Compare'),
    ('Мои баллы', 'My score'), ('Очистить', 'Clear'), ('Закрыть', 'Close'), ('Убрать', 'Remove'),
    ('Институт', 'Institute'), ('Область', 'Field'), ('Уровень', 'Level'), ('Найдено:', 'Found:'),
    ('Не хватает {{p.gap}} баллов', '{{p.gap}} points short'),
    ("'Не хватает ' + (sc - myN)", "(sc - myN) + ' points short'"),
    ("'Хватает'", "'Enough'"),
    ("tip = 'Добавьте ' + ACC[best] + ' — откроется ещё ' + c + ' ' + (c % 10 === 1 && c % 100 !== 11 ? 'программа' : (c % 10 >= 2 && c % 10 <= 4 && (c % 100 < 12 || c % 100 > 14)) ? 'программы' : 'программ') + '.';",
     "tip = 'Add ' + ACC[best] + ' to open ' + c + ' more programme' + (c === 1 ? '' : 's') + '.';"),
    ("const word = (m10 === 1 && m100 !== 11) ? 'программа' : (m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14)) ? 'программы' : 'программ';",
     "const word = n === 1 ? 'programme' : 'programmes';"),
    ("'Естественные науки'", "'Natural sciences'"), ("'Гуманитарные'", "'Humanities'"), ("'Инженерия'", "'Engineering'"), ("'Экономика'", "'Economics'"), ("'Все'", "'All'"),
    ("'Бакалавриат'", "'Bachelor'"), ("'Специалитет'", "'Specialist'"), ("'Магистратура'", "'Master'"),
    ("'Русский язык'", "'Russian'"), ("'Математика'", "'Mathematics'"), ("'Информатика'", "'Computer Science'"), ("'Физика'", "'Physics'"),
    ("'Химия'", "'Chemistry'"), ("'Биология'", "'Biology'"), ("'Обществознание'", "'Social Studies'"), ("'История'", "'History'"),
    ("'Литература'", "'Literature'"), ("'Иностранный язык'", "'Foreign language'"),
    ("'математику'", "'mathematics'"), ("'информатику'", "'computer science'"), ("'физику'", "'physics'"), ("'химию'", "'chemistry'"),
    ("'биологию'", "'biology'"), ("'обществознание'", "'social studies'"), ("'историю'", "'history'"), ("'литературу'", "'literature'"),
    ("'иностранный язык'", "'a foreign language'"),
    ("'Бакалавриат · '", "'Bachelor · '"),
    ('>ЕГЭ: {{p.exams}}<', '>EGE: {{p.exams}}<'), ('{{cmpCount}} из 3', '{{cmpCount}} of 3'), ("rus:'русский язык'", "rus:'Russian'"),
]

ADMISSION = [
    ('<a class="btn" href="Quiz.dc.html">Подобрать программу</a>', '<a class="btn" href="CatalogEn.dc.html">Find a programme</a>'),
    ('Пять шагов от выбора программы до заселения. Нажмите на шаг, чтобы увидеть подробности.',
     'Five steps from choosing a programme to moving into the dorm. Click a step to see the details. International applicants: the International Office helps with documents, visas and the Russian-language preparatory year — see Contacts.'),
    ('Как поступить в УрФУ', 'How to apply to UrFU'),
    ('По правилам приёма 2026 года — даты 2027 года появятся весной.', 'Based on the 2026 admission rules — the 2027 dates will be announced in spring.'),
    ('Окончание приёма для поступающих с внутренними испытаниями', 'Deadline for applicants taking UrFU entrance tests'),
    ('Окончание приёма на бюджет по результатам ЕГЭ', 'Deadline for state-funded places based on the EGE'),
    ('Окончание приёма на договор', 'Deadline for fee-paying places'),
    ('Приказы о зачислении на бюджет', 'Enrolment orders for state-funded places'),
    ('Начало августа', 'Early August'),
    ('Приказ о зачислении на бюджет', 'Enrolment order for state-funded places'),
    ('Начало приёма документов', 'Applications open'),
    ('Ключевые даты', 'Key dates'), ('Частые вопросы', 'FAQ'),
    ('Можно ли подать документы онлайн?', 'Can I apply online?'),
    ('Да: через Госуслуги или личный кабинет абитуриента. Ещё можно лично в приёмной комиссии или почтой: 620062, Екатеринбург, ул. Мира, 19.',
     "Yes: via the Gosuslugi portal or the applicant's personal account. You can also apply in person at the Admissions Office or by post: 19 Mira St, Yekaterinburg, 620062."),
    ('Сколько направлений можно выбрать?', 'How many programmes can I choose?'),
    ('До пяти направлений подготовки в одном вузе — и не больше пяти вузов. Внутри выбранных направлений вы расставляете приоритеты: какая программа важнее.', 'Up to five fields of study at one university, and no more than five universities. Within the chosen fields you rank programmes by priority.'),
    ('[Ответ по правилам приёма текущего года]', '[Answer based on the current admission rules]'),
    ('Как учитываются индивидуальные достижения?', 'How are individual achievements counted?'),
    ('Они добавляют баллы к сумме ЕГЭ. Например, аттестат с отличием — 6 баллов, волонтёрство — 2, золотой значок ГТО — 1.',
     'They add points to your EGE total. For example, a school certificate with honours gives 6 points, volunteering 2, a gold GTO badge 1.'),
    ('Когда дают общежитие?', 'When do I get a dorm place?'),
    ('Место получают все иногородние первокурсники, которые отметили потребность в общежитии при подаче документов.',
     'Every first-year student from outside Yekaterinburg who requested a dorm place in the application gets one.'),
    ('Подробнее об общежитиях', 'More about dorms'),
    ('Мой план: документы', 'My plan: documents'),
    ('Готово {{docDone}} из {{docTotal}} · отметки сохраняются в этом браузере', '{{docDone}} of {{docTotal}} ready · saved in this browser'),
    ('aria-label="Документы готовы"', 'aria-label="Documents ready"'),
    ('Задать вопрос комиссии', 'Ask the Admissions Office'),
    ('Подобрать программу', 'Find a programme'), ('Следующий шаг', 'Next step'), ('Шаг {{cur.n}} из 5', 'Step {{cur.n}} of 5'),
    ('>20 июня<', '>20 June<'), ('>15 июля<', '>15 July<'), ('>25 июля<', '>25 July<'), ('>20 августа<', '>20 August<'),
    ("'Паспорт'", "'Passport'"), ("'Аттестат или диплом'", "'School certificate or diploma'"), ("'СНИЛС'", "'SNILS (insurance number)'"),
    ("'Документы об индивидуальных достижениях'", "'Proof of individual achievements'"), ("'Документы о льготах, если есть'", "'Documents for special rights, if any'"),
    ("const dw = n => (n % 10 === 1 && n % 100 !== 11) ? 'день' : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14)) ? 'дня' : 'дней';", "const dw = n => n === 1 ? 'day' : 'days';"),
    ("dw(days) + ' до начала приёма документов'", "dw(days) + ' until applications open'"),
    ("'Приём документов идёт'", "'Applications are open'"),
    ("'Подайте заявление через Госуслуги или личный кабинет абитуриента.'", "'Apply via Gosuslugi or the applicant’s personal account.'"),
    ("'20 июня ' + start.getFullYear() + ' — по правилам приёма 2026 года; точная дата появится весной.'", "'20 June ' + start.getFullYear() + ' — based on the 2026 admission rules; the exact date will be announced in spring.'"),
    ("t:'Выберите программы'", "t:'Choose programmes'"),
    ("'Ответьте на 3 вопроса — покажем программы, куда вы проходите по своим ЕГЭ и баллам. Или откройте каталог и сравните программы между собой.'", "'Use the catalogue to filter programmes by your EGE subjects and score, and compare them side by side.'"),
    ("cta:'Подобрать за 3 вопроса', href:'Quiz.dc.html'", "cta:'Open the catalogue', href:'CatalogEn.dc.html'"),
    ("t:'Подайте документы'", "t:'Submit your documents'"),
    ("'Заявление подаётся онлайн через Госуслуги или личный кабинет абитуриента. Проверьте чек-лист документов справа.'", "'Apply online via Gosuslugi or the applicant’s personal account. Check the document list on the right.'"),
    ("'Чек-лист документов'", "'Document checklist'"),
    ("t:'Следите за списками'", "t:'Follow the ranking lists'"),
    ("'Конкурсные списки обновляются каждый день. Ваше место в списке видно в личном кабинете.'", "'Ranking lists are updated daily. Your position is shown in your personal account.'"),
    ("'Конкурсные списки'", "'Ranking lists'"),
    ("t:'Подайте согласие'", "t:'Confirm your choice'"),
    ("'Подтвердите, на какую программу хотите поступить, до даты окончания приёма согласий.'", "'Confirm which programme you want to enrol in before the consent deadline.'"),
    ("'Как подать согласие'", "'How to confirm'"),
    ("t:'Зачисление и заселение'", "t:'Enrolment and move-in'"),
    ("'После приказа о зачислении — заселение в общежитие и знакомство с институтом.'", "'After the enrolment order you move into the dorm and meet your institute.'"),
    ("'Об общежитиях'", "'About dorms'"),
]


def tr_exams(s):
    def one(m):
        v = m.group(2)
        for a, b in EXAM_WORDS:
            v = v.replace(a, b)
        return m.group(1) + v + "'"
    return re.sub(r"(exams:')([^']*)'", one, s)


def money(s):
    s = re.sub(r"(\d{1,3}) (\d{3}) ₽", r"\1,\2 ₽", s)
    return s.replace("'от ", "'from ").replace('>от ', '>from ')


def build(src, dst, title, desc, current, extra):
    s = open(src, encoding='utf-8').read()
    s = s.replace('<html lang="ru">', '<html lang="en">', 1)
    s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % title, s)
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % desc, s)
    a = s.index('<div><a href="#main" class="skip">'); b = s.index('</header>') + len('</header>')
    head = EN_HEAD.replace('<span aria-current="true">EN</span>', '<span aria-current="true">EN</span>')
    head = head.replace('<a href="Main.dc.html" lang="ru" aria-label="Русская версия">RU</a>', '<a data-ru="%s" lang="ru" aria-label="Русская версия">RU</a>' % src)
    for ru, en in EN_LINKS.items():
        head = head.replace('href="%s"' % ru, 'href="%s"' % en)
    head = head.replace('<a data-ru=', '<a href=')
    head = head.replace('>%s</a>' % current, ' aria-current="page">%s</a>' % current).replace('" aria-current="page"> aria-current', '" aria-current')
    head = re.sub(r'(<a href="[^"]+")( aria-current="page">%s</a>)' % re.escape(current), r'\1\2', head)
    s = s[:a] + head + s[b:]
    a = s.index('<footer'); b = s.index('</footer>') + len('</footer>')
    foot = EN_FOOT.replace('<a href="Main.dc.html" lang="ru">Русская версия</a>', '<a data-ru="%s" lang="ru">Русская версия</a>' % src)
    for ru, en in EN_LINKS.items():
        foot = foot.replace('href="%s"' % ru, 'href="%s"' % en)
    foot = foot.replace('<a data-ru=', '<a href=')
    s = s[:a] + foot + s[b:]
    body_start = s.index('<main')
    pre, body = s[:body_start], s[body_start:]
    body = tr_exams(body)
    for a_, b_ in PROGRAMS + extra + COMMON:
        body = body.replace(a_, b_)
    for a_, b_ in INSTITUTES:
        body = body.replace("'" + a_ + "'", "'" + b_ + "'").replace('>' + a_ + '<', '>' + b_ + '<')
    body = money(body)
    for ru, en in EN_LINKS.items():
        body = body.replace('href="%s"' % ru, 'href="%s"' % en).replace("href:'%s'" % ru, "href:'%s'" % en)
    body = body.replace('href="%s" lang="ru"' % dst, 'href="%s" lang="ru"' % src)  # ссылка «Русская версия» — на русскую страницу
    body = re.sub(r'^const IL = .*$', lambda m: "const IL = {'IRIT-RTF':['Radio electronics and IT','Institute of Radioelectronics and Information Technologies — RTF'],'INSM':['Natural sciences and mathematics','Institute of Natural Sciences and Mathematics'],'INMT':['New materials and technologies','Institute of New Materials and Technologies'],'UralENIN':['Power engineering','Ural Power Engineering Institute'],'ICEA':['Civil engineering and architecture','Institute of Civil Engineering and Architecture'],'UIH':['Humanities','Ural Institute of Humanities'],'GSEM':['Economics and management','Graduate School of Economics and Management'],'IPT':['Physics and technology','Institute of Physics and Technology']};", body, flags=re.M)
    s = pre + body
    open(dst, 'w', encoding='utf-8').write(s)
    # что осталось непереведённым в видимой части
    left = sorted(set(re.findall(r"[А-Яа-яЁё][А-Яа-яЁё ,.\-—«»:]{2,}", body.replace('Русская версия', ''))))
    print(dst, 'осталось по-русски:', left[:40])


if __name__ == '__main__':
    build('Catalog.dc.html', 'CatalogEn.dc.html', 'Programme catalogue — UrFU',
          'UrFU programme catalogue: filter by EGE subjects and score, compare up to three programmes.', 'Admissions', CATALOG)
    build('Admission.dc.html', 'AdmissionEn.dc.html', 'How to apply — UrFU',
          'How to apply to Ural Federal University: five steps, key dates, FAQ and a document checklist.', 'Admissions', ADMISSION)

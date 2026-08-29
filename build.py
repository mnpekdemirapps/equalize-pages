#!/usr/bin/env python3
"""Equalize yasal sayfalarını üretir.

Tek bir veri tablosundan bütün dillerin `privacy.html` / `terms.html`
dosyalarını yazar. Metni tek yerde tuttuğu için bir maddeyi düzeltmek altı
dosyayı elle güncellemek anlamına gelmiyor; yeni dil eklemek de yalnızca
LOCALES sözlüğüne bir girdi eklemek.

Kullanım:  python3 build.py
"""

from __future__ import annotations

import html
import os
import shutil

OUT = os.path.dirname(os.path.abspath(__file__))

APP = "Equalize"
EMAIL = "mnpekdemir.apps@gmail.com"
PACKAGE = "com.mnpekdemir.equalize"
EFFECTIVE = "2026-08-29"
BASE = "https://mnpekdemirapps.github.io/equalizer-pages"

# ── Diller ────────────────────────────────────────────────────────────────
# Sıra sayfadaki dil seçicinin sırasıdır.

LOCALES: dict[str, dict] = {
    "tr": {
        "name": "Türkçe",
        "dir": "ltr",
        "updated": "Son güncelleme",
        "back": "Ana sayfa",
        "other": "Diğer diller",
        "tagline": "Sayı mantığı bulmacası",
        "intro": (
            "Aşağıdaki belgeler {app} mobil oyununun gizlilik politikası ve "
            "kullanım koşullarıdır."
        ),
        "privacy_title": "Gizlilik Politikası",
        "terms_title": "Kullanım Koşulları",
        "contact_title": "İletişim",
        "contact_body": (
            "Bu belgelerle ya da oyunla ilgili her soru için bize "
            "yazabilirsiniz:"
        ),
        "privacy": [
            ("Kısaca", [
                "{app} hesap açmanızı istemez, sizden ad, e-posta, telefon "
                "numarası ya da konum bilgisi toplamaz.",
                "Oyun ilerlemeniz hesabımızın bulunduğu bir sunucuya "
                "gönderilmez; işletim sisteminiz bunu cihaz yedeğine alabilir.",
            ]),
            ("Cihazınızda saklanan veriler", [
                "Bölüm ilerlemesi, yıldızlar, ipucu sayınız ve ses/titreşim "
                "gibi ayarlar cihazınızın yerel depolamasında tutulur.",
                "Bu veriler oyunun çalışması içindir. Uygulamayı kaldırmak "
                "yerel veriyi genellikle siler; cihazınızın yedekleme ve geri "
                "yükleme ayarları verinin bir kopyasını koruyabilir.",
            ]),
            ("Reklamlar", [
                "Oyunda zorunlu reklam yoktur. Yalnızca siz isterseniz, "
                "ipucu kazanmak için ödüllü reklam izleyebilirsiniz.",
                "Reklamlar Google AdMob tarafından sunulur. iOS'ta Equalize "
                "tüm AdMob isteklerini kişiselleştirilmemiş gönderir, Mobile "
                "Ads başlamadan Google'ın yayıncı birinci taraf (same-app) "
                "kimliğini kapatır ve Apple ATT iznini istemez. Uygulama "
                "verilerini sizi başka şirketlerin uygulamaları veya internet "
                "siteleri arasında takip etmek için kullanmayız.",
                "Android'de reklam sunumu, kişiselleştirme dâhil, bölgenize, "
                "Google UMP izninize ve ayarlarınıza bağlı olabilir. Mevcut "
                "tercihleri uygulamanın gizlilik seçeneklerinden veya cihaz "
                "ayarlarından yönetebilirsiniz.",
                "Google'ın veri uygulamaları için: "
                "https://policies.google.com/technologies/partner-sites",
                "Firebase Crashlytics çökme tanılaması için kullanılır. "
                "Firebase Analytics varsayılan olarak açıktır ve Ayarlar'dan "
                "kapatılabilir. Firebase Remote Config, isteğe bağlı Diğer "
                "Oyunlar kataloğunu alırken bir kurulum kimliği kullanabilir.",
            ]),
            ("Satın almalar", [
                "Uygulama içi satın almalar Google Play ya da App Store "
                "üzerinden yapılır. Ödeme bilgileriniz doğrudan mağaza "
                "tarafından işlenir; biz kart bilgilerinizi görmeyiz ve "
                "saklamayız.",
                "Uygulama mağazanın bildirdiği native işlem kaydını cihazda "
                "kontrol eder. Sunucu taraflı makbuz/iade doğrulaması henüz "
                "bulunmadığından iade veya iptaller mağaza uzlaştırmasına bağlıdır.",
            ]),
            ("Çocuklar", [
                "{app} her yaşa uygun bir bulmaca oyunudur ve çocuklardan "
                "bilerek kişisel veri toplamaz.",
                "Çocuğunuza ait bir bilginin işlendiğini düşünüyorsanız bize "
                "yazın, gereken işlemi yapalım.",
            ]),
            ("Haklarınız", [
                "Yerel oyun verisini uygulama verilerini temizleyerek yönetebilir; "
                "analiz tercihini Ayarlar'dan ve reklam tercihlerini sunulan "
                "gizlilik seçeneklerinden değiştirebilirsiniz.",
                "Yine de sorularınız için bize yazabilirsiniz.",
            ]),
            ("Değişiklikler", [
                "Bu politikayı zaman zaman güncelleyebiliriz. Güncel sürüm "
                "her zaman bu sayfada yayımlanır ve üstteki tarih değişir.",
            ]),
        ],
        "terms": [
            ("Kabul", [
                "{app} uygulamasını indirerek ya da kullanarak bu koşulları "
                "kabul etmiş olursunuz. Kabul etmiyorsanız lütfen uygulamayı "
                "kullanmayın.",
            ]),
            ("Kullanım hakkı", [
                "Size {app} uygulamasını kişisel ve ticari olmayan amaçla "
                "kullanmanız için sınırlı, devredilemez bir hak veriyoruz.",
                "Uygulama satılmaz, kiralanmaz ya da başkasına devredilemez.",
            ]),
            ("İpuçları ve sanal ürünler", [
                "İpuçları oyun içi sanal öğelerdir. Gerçek para değeri "
                "taşımazlar, nakde çevrilemez ve oyun dışına aktarılamazlar.",
                "İpuçları ücretsiz kazanılabilir (ödüllü reklam) ya da satın "
                "alınabilir.",
                "Satın alma iadeleri, satın aldığınız mağazanın (Google Play "
                "veya App Store) iade kurallarına tabidir.",
            ]),
            ("Reklamlar", [
                "Ödüllü reklamlar tamamen isteğe bağlıdır. Reklamı sonuna "
                "kadar izlemezseniz ödül verilmez; bu bir hata değildir.",
                "Reklam içeriği reklam ağı tarafından belirlenir ve bizim "
                "denetimimizde değildir.",
            ]),
            ("Uygun kullanım", [
                "Uygulamayı tersine mühendisliğe tabi tutmak, kaydedilmiş "
                "verileri kurcalayarak ipucu veya ilerleme üretmek ya da "
                "hizmeti aksatmaya çalışmak yasaktır.",
            ]),
            ("Fikri mülkiyet", [
                "Oyunun tasarımı, kodu, bölümleri, grafikleri ve müziği "
                "geliştiriciye aittir ve telif hakkıyla korunur.",
            ]),
            ("Garanti reddi", [
                "Uygulama \"olduğu gibi\" sunulur. Kesintisiz ya da hatasız "
                "çalışacağına dair garanti verilmez.",
                "Yürürlükteki hukukun izin verdiği ölçüde, uygulamanın "
                "kullanımından doğan dolaylı zararlardan sorumlu değiliz.",
            ]),
            ("Değişiklikler", [
                "Bu koşulları güncelleyebiliriz. Güncellemeden sonra "
                "uygulamayı kullanmaya devam etmeniz yeni koşulları kabul "
                "ettiğiniz anlamına gelir.",
            ]),
            ("Uygulanacak hukuk", [
                "Bu koşullara Türkiye Cumhuriyeti hukuku uygulanır.",
            ]),
        ],
    },
    "en": {
        "name": "English",
        "dir": "ltr",
        "updated": "Last updated",
        "back": "Home",
        "other": "Other languages",
        "tagline": "A number logic puzzle",
        "intro": (
            "Below are the privacy policy and terms of use for the {app} "
            "mobile game."
        ),
        "privacy_title": "Privacy Policy",
        "terms_title": "Terms of Use",
        "contact_title": "Contact",
        "contact_body": (
            "For any question about these documents or the game, write to us:"
        ),
        "privacy": [
            ("In short", [
                "{app} does not ask you to create an account and does not "
                "collect your name, email address, phone number or location.",
                "Your progress is not sent to a server account operated by us; "
                "your operating system may include it in a device backup.",
            ]),
            ("Data stored on your device", [
                "Level progress, stars, your hint balance and settings such "
                "as sound and haptics are kept in your device's local "
                "storage.",
                "This data exists to make the game work. Removing the app "
                "normally deletes local data, but device backup and restore "
                "settings may retain a copy.",
            ]),
            ("Advertising", [
                "There are no forced ads. You may choose to watch a rewarded "
                "ad to earn hints — never required.",
                "Ads are served by Google AdMob. On iOS, Equalize always sends "
                "non-personalized AdMob requests, disables Google's publisher "
                "first-party (same-app) identifier before Mobile Ads starts, "
                "and does not request Apple's ATT permission. We do not use App "
                "data to track you across other companies' apps or websites.",
                "On Android, ad serving, including personalization, may depend "
                "on your region, Google UMP consent, and settings. You can "
                "manage available choices through the App's privacy options "
                "or your device settings.",
                "Google's data practices: "
                "https://policies.google.com/technologies/partner-sites",
                "Firebase Crashlytics is used for crash diagnostics. Firebase "
                "Analytics is on by default and can be turned off in Settings. "
                "Firebase Remote Config may use an installation identifier "
                "while retrieving the optional More Games catalog.",
            ]),
            ("Purchases", [
                "In-app purchases are handled by Google Play or the App "
                "Store. Your payment details are processed by the store; we "
                "never see or store your card information.",
                "The app checks the native transaction reported by the store "
                "on device. There is not yet authoritative server-side receipt "
                "or refund verification, so revocations depend on store reconciliation.",
            ]),
            ("Children", [
                "{app} is a puzzle game suitable for all ages and does not "
                "knowingly collect personal data from children.",
                "If you believe data about your child has been processed, "
                "please contact us and we will act on it.",
            ]),
            ("Your rights", [
                "You can manage local game data by clearing app data, change "
                "Analytics in Settings, and use the available privacy choices "
                "to manage advertising consent.",
                "You are still welcome to contact us with any question.",
            ]),
            ("Changes", [
                "We may update this policy from time to time. The current "
                "version is always published on this page and the date above "
                "changes accordingly.",
            ]),
        ],
        "terms": [
            ("Acceptance", [
                "By downloading or using {app} you agree to these terms. If "
                "you do not agree, please do not use the app.",
            ]),
            ("Licence", [
                "We grant you a limited, non-transferable right to use {app} "
                "for personal, non-commercial purposes.",
                "The app may not be sold, rented or transferred to anyone "
                "else.",
            ]),
            ("Hints and virtual items", [
                "Hints are virtual in-game items. They have no real-world "
                "monetary value, cannot be exchanged for cash and cannot be "
                "transferred out of the game.",
                "Hints can be earned for free (rewarded ads) or purchased.",
                "Refunds are subject to the refund rules of the store you "
                "purchased from (Google Play or the App Store).",
            ]),
            ("Advertising", [
                "Rewarded ads are entirely optional. If you do not watch an "
                "ad to the end, no reward is granted; this is not a fault.",
                "Ad content is determined by the ad network and is outside "
                "our control.",
            ]),
            ("Acceptable use", [
                "You may not reverse engineer the app, tamper with saved "
                "data to manufacture hints or progress, or attempt to disrupt "
                "the service.",
            ]),
            ("Intellectual property", [
                "The design, code, levels, artwork and music of the game "
                "belong to the developer and are protected by copyright.",
            ]),
            ("Disclaimer", [
                "The app is provided \"as is\". No warranty is given that it "
                "will run uninterrupted or error-free.",
                "To the extent permitted by law, we are not liable for "
                "indirect damages arising from use of the app.",
            ]),
            ("Changes", [
                "We may update these terms. Continuing to use the app after "
                "an update means you accept the new terms.",
            ]),
            ("Governing law", [
                "These terms are governed by the laws of the Republic of "
                "Türkiye.",
            ]),
        ],
    },
    "de": {
        "name": "Deutsch",
        "dir": "ltr",
        "updated": "Zuletzt aktualisiert",
        "back": "Startseite",
        "other": "Weitere Sprachen",
        "tagline": "Ein Zahlen-Logikrätsel",
        "intro": (
            "Nachfolgend finden Sie die Datenschutzerklärung und die "
            "Nutzungsbedingungen für das Mobilspiel {app}."
        ),
        "privacy_title": "Datenschutzerklärung",
        "terms_title": "Nutzungsbedingungen",
        "contact_title": "Kontakt",
        "contact_body": (
            "Bei Fragen zu diesen Dokumenten oder zum Spiel schreiben Sie uns:"
        ),
        "privacy": [
            ("Kurz gefasst", [
                "{app} verlangt kein Benutzerkonto und erhebt weder Ihren "
                "Namen noch E-Mail-Adresse, Telefonnummer oder Standort.",
                "Ihr Spielfortschritt wird nicht an ein von uns betriebenes "
                "Benutzerkonto gesendet; das Betriebssystem kann ihn sichern.",
            ]),
            ("Auf Ihrem Gerät gespeicherte Daten", [
                "Levelfortschritt, Sterne, Ihr Tipp-Guthaben sowie "
                "Einstellungen wie Ton und Vibration werden im lokalen "
                "Speicher Ihres Geräts abgelegt.",
                "Diese Daten dienen dem Betrieb des Spiels. Beim Entfernen der "
                "App werden lokale Daten üblicherweise gelöscht; Geräte-Backups "
                "können abhängig von Ihren Einstellungen eine Kopie behalten.",
            ]),
            ("Werbung", [
                "Es gibt keine erzwungene Werbung. Sie können freiwillig ein "
                "Belohnungsvideo ansehen, um Tipps zu erhalten.",
                "Die Werbung wird von Google AdMob ausgeliefert. Unter iOS "
                "sendet Equalize ausschließlich nicht personalisierte "
                "AdMob-Anfragen, deaktiviert Googles Publisher-First-Party-"
                "Kennung (Same-App) vor dem Start von Mobile Ads und fordert "
                "keine Apple-ATT-Berechtigung an. App-Daten werden nicht zur "
                "Nachverfolgung über Apps oder Websites anderer Unternehmen "
                "hinweg verwendet.",
                "Unter Android kann die Anzeigenauslieferung einschließlich "
                "Personalisierung von Region, Google-UMP-Einwilligung und "
                "Einstellungen abhängen. Verfügbare Optionen lassen sich in "
                "den Datenschutz- oder Geräteeinstellungen verwalten.",
                "Datenpraktiken von Google: "
                "https://policies.google.com/technologies/partner-sites",
                "Firebase Crashlytics dient der Fehlerdiagnose. Firebase "
                "Analytics ist standardmäßig aktiviert und kann in den "
                "Einstellungen deaktiviert werden. Remote Config kann für den "
                "optionalen Spielekatalog "
                "eine Firebase-Installations-ID verwenden.",
            ]),
            ("Käufe", [
                "In-App-Käufe werden über Google Play bzw. den App Store "
                "abgewickelt. Ihre Zahlungsdaten verarbeitet der jeweilige "
                "Store; wir sehen und speichern keine Kartendaten.",
                "Die App prüft den vom Store gemeldeten nativen Vorgang lokal. "
                "Eine serverseitige Beleg- und Erstattungsprüfung besteht noch "
                "nicht; Widerrufe hängen daher vom Store-Abgleich ab.",
            ]),
            ("Kinder", [
                "{app} ist ein Rätselspiel für jedes Alter und erhebt "
                "wissentlich keine personenbezogenen Daten von Kindern.",
                "Sollten Sie vermuten, dass Daten Ihres Kindes verarbeitet "
                "wurden, wenden Sie sich bitte an uns.",
            ]),
            ("Ihre Rechte", [
                "Lokale Spieldaten, Analytics und Werbeeinwilligung können über "
                "App-, Geräte- und Datenschutzeinstellungen verwaltet werden.",
                "Für Fragen können Sie uns dennoch jederzeit schreiben.",
            ]),
            ("Änderungen", [
                "Wir können diese Erklärung gelegentlich aktualisieren. Die "
                "jeweils gültige Fassung steht auf dieser Seite; das Datum "
                "oben ändert sich entsprechend.",
            ]),
        ],
        "terms": [
            ("Zustimmung", [
                "Mit dem Herunterladen oder Nutzen von {app} stimmen Sie "
                "diesen Bedingungen zu. Andernfalls nutzen Sie die App bitte "
                "nicht.",
            ]),
            ("Nutzungsrecht", [
                "Wir gewähren Ihnen ein beschränktes, nicht übertragbares "
                "Recht, {app} für private, nicht kommerzielle Zwecke zu "
                "nutzen.",
                "Die App darf nicht verkauft, vermietet oder weitergegeben "
                "werden.",
            ]),
            ("Tipps und virtuelle Gegenstände", [
                "Tipps sind virtuelle Gegenstände. Sie haben keinen realen "
                "Geldwert, können nicht ausgezahlt und nicht aus dem Spiel "
                "übertragen werden.",
                "Tipps können kostenlos verdient (Belohnungsvideo) oder "
                "gekauft werden.",
                "Erstattungen richten sich nach den Regeln des Stores, in dem "
                "Sie gekauft haben (Google Play oder App Store).",
            ]),
            ("Werbung", [
                "Belohnungsvideos sind vollständig freiwillig. Wird das Video "
                "nicht bis zum Ende angesehen, gibt es keine Belohnung; das "
                "ist kein Fehler.",
                "Die Werbeinhalte bestimmt das Werbenetzwerk; sie liegen "
                "außerhalb unserer Kontrolle.",
            ]),
            ("Zulässige Nutzung", [
                "Reverse Engineering, das Manipulieren der Speicherdaten zur "
                "Erzeugung von Tipps oder Fortschritt sowie Versuche, den "
                "Dienst zu stören, sind untersagt.",
            ]),
            ("Geistiges Eigentum", [
                "Design, Code, Level, Grafiken und Musik des Spiels gehören "
                "dem Entwickler und sind urheberrechtlich geschützt.",
            ]),
            ("Haftungsausschluss", [
                "Die App wird \"wie besehen\" bereitgestellt. Ein "
                "unterbrechungs- und fehlerfreier Betrieb wird nicht "
                "zugesichert.",
                "Soweit gesetzlich zulässig, haften wir nicht für indirekte "
                "Schäden aus der Nutzung der App.",
            ]),
            ("Änderungen", [
                "Wir können diese Bedingungen aktualisieren. Die weitere "
                "Nutzung nach einer Aktualisierung gilt als Zustimmung.",
            ]),
            ("Anwendbares Recht", [
                "Auf diese Bedingungen findet das Recht der Republik Türkei "
                "Anwendung.",
            ]),
        ],
    },
    "es": {
        "name": "Español",
        "dir": "ltr",
        "updated": "Última actualización",
        "back": "Inicio",
        "other": "Otros idiomas",
        "tagline": "Un rompecabezas de lógica numérica",
        "intro": (
            "A continuación encontrarás la política de privacidad y las "
            "condiciones de uso del juego móvil {app}."
        ),
        "privacy_title": "Política de Privacidad",
        "terms_title": "Condiciones de Uso",
        "contact_title": "Contacto",
        "contact_body": (
            "Para cualquier consulta sobre estos documentos o sobre el juego, "
            "escríbenos:"
        ),
        "privacy": [
            ("En resumen", [
                "{app} no te pide crear una cuenta ni recoge tu nombre, "
                "correo electrónico, teléfono o ubicación.",
                "Tu progreso no se envía a una cuenta de servidor operada por "
                "nosotros; el sistema operativo puede incluirlo en una copia.",
            ]),
            ("Datos guardados en tu dispositivo", [
                "El progreso de niveles, las estrellas, tus pistas y ajustes "
                "como el sonido y la vibración se guardan en el "
                "almacenamiento local de tu dispositivo.",
                "Estos datos sirven para que el juego funcione. Al eliminar la "
                "aplicación normalmente se borran los datos locales, aunque la "
                "configuración de copia y restauración puede conservarlos.",
            ]),
            ("Publicidad", [
                "No hay anuncios obligatorios. Puedes elegir ver un anuncio "
                "recompensado para ganar pistas.",
                "Los anuncios los ofrece Google AdMob. En iOS, Equalize siempre "
                "envía solicitudes de AdMob no personalizadas, desactiva el "
                "identificador propio del editor (same-app) de Google antes de "
                "iniciar Mobile Ads y no solicita el permiso ATT de Apple. No "
                "usamos datos de la aplicación para rastrearte entre aplicaciones "
                "o sitios web de otras empresas.",
                "En Android, la publicación y personalización de anuncios puede "
                "depender de tu región, consentimiento de Google UMP y ajustes. "
                "Puedes gestionar las opciones disponibles desde la privacidad "
                "de la aplicación o los ajustes del dispositivo.",
                "Prácticas de datos de Google: "
                "https://policies.google.com/technologies/partner-sites",
                "Firebase Crashlytics se usa para diagnosticar fallos. Firebase "
                "Analytics está activado por defecto y puede desactivarse en Ajustes. "
                "Remote Config puede usar un identificador de instalación al "
                "obtener el catálogo opcional de Otros juegos.",
            ]),
            ("Compras", [
                "Las compras dentro de la aplicación se realizan a través de "
                "Google Play o App Store. La tienda procesa tus datos de "
                "pago; nosotros no vemos ni guardamos los datos de tu "
                "tarjeta.",
                "La aplicación comprueba localmente la transacción nativa que "
                "comunica la tienda. Aún no hay validación autoritativa de recibos "
                "o reembolsos en servidor; las revocaciones dependen de la tienda.",
            ]),
            ("Menores", [
                "{app} es un juego de puzles apto para todas las edades y no "
                "recoge conscientemente datos personales de menores.",
                "Si crees que se han tratado datos de tu hijo o hija, "
                "escríbenos y actuaremos en consecuencia.",
            ]),
            ("Tus derechos", [
                "Puedes gestionar los datos locales, Analytics y el consentimiento "
                "publicitario mediante los ajustes de la aplicación, privacidad "
                "y dispositivo.",
                "Aun así, puedes escribirnos con cualquier duda.",
            ]),
            ("Cambios", [
                "Podemos actualizar esta política de vez en cuando. La "
                "versión vigente se publica siempre en esta página y la fecha "
                "superior cambia en consecuencia.",
            ]),
        ],
        "terms": [
            ("Aceptación", [
                "Al descargar o usar {app} aceptas estas condiciones. Si no "
                "estás de acuerdo, no utilices la aplicación.",
            ]),
            ("Licencia", [
                "Te concedemos un derecho limitado e intransferible de uso de "
                "{app} con fines personales y no comerciales.",
                "La aplicación no puede venderse, alquilarse ni transferirse "
                "a terceros.",
            ]),
            ("Pistas y objetos virtuales", [
                "Las pistas son objetos virtuales del juego. No tienen valor "
                "monetario real, no son canjeables por dinero ni "
                "transferibles fuera del juego.",
                "Las pistas se pueden conseguir gratis (anuncios "
                "recompensados) o comprar.",
                "Los reembolsos se rigen por las normas de la tienda donde "
                "realizaste la compra (Google Play o App Store).",
            ]),
            ("Publicidad", [
                "Los anuncios recompensados son totalmente opcionales. Si no "
                "ves el anuncio hasta el final no se entrega la recompensa; "
                "no es un error.",
                "El contenido de los anuncios lo determina la red "
                "publicitaria y queda fuera de nuestro control.",
            ]),
            ("Uso aceptable", [
                "No está permitido aplicar ingeniería inversa, manipular los "
                "datos guardados para generar pistas o progreso, ni intentar "
                "alterar el servicio.",
            ]),
            ("Propiedad intelectual", [
                "El diseño, el código, los niveles, los gráficos y la música "
                "del juego pertenecen al desarrollador y están protegidos por "
                "derechos de autor.",
            ]),
            ("Exención de garantías", [
                "La aplicación se ofrece \"tal cual\". No se garantiza un "
                "funcionamiento ininterrumpido ni libre de errores.",
                "En la medida permitida por la ley, no somos responsables de "
                "daños indirectos derivados del uso de la aplicación.",
            ]),
            ("Cambios", [
                "Podemos actualizar estas condiciones. Seguir usando la "
                "aplicación tras una actualización implica su aceptación.",
            ]),
            ("Legislación aplicable", [
                "Estas condiciones se rigen por la legislación de la "
                "República de Türkiye.",
            ]),
        ],
    },
    "fr": {
        "name": "Français",
        "dir": "ltr",
        "updated": "Dernière mise à jour",
        "back": "Accueil",
        "other": "Autres langues",
        "tagline": "Un casse-tête de logique numérique",
        "intro": (
            "Vous trouverez ci-dessous la politique de confidentialité et les "
            "conditions d'utilisation du jeu mobile {app}."
        ),
        "privacy_title": "Politique de Confidentialité",
        "terms_title": "Conditions d'Utilisation",
        "contact_title": "Contact",
        "contact_body": (
            "Pour toute question sur ces documents ou sur le jeu, "
            "écrivez-nous :"
        ),
        "privacy": [
            ("En bref", [
                "{app} ne demande aucun compte et ne collecte ni votre nom, "
                "ni votre adresse e-mail, ni votre téléphone, ni votre "
                "position.",
                "Votre progression n'est pas envoyée vers un compte serveur que "
                "nous exploitons ; le système peut l'inclure dans une sauvegarde.",
            ]),
            ("Données stockées sur votre appareil", [
                "La progression, les étoiles, votre solde d'indices et les "
                "réglages (son, vibrations) sont conservés dans le stockage "
                "local de votre appareil.",
                "Ces données servent au fonctionnement du jeu. Supprimer "
                "l'application efface normalement les données locales, mais les "
                "réglages de sauvegarde et restauration peuvent garder une copie.",
            ]),
            ("Publicité", [
                "Aucune publicité n'est imposée. Vous pouvez choisir de "
                "regarder une publicité récompensée pour gagner des indices.",
                "Les publicités sont diffusées par Google AdMob. Sur iOS, "
                "Equalize envoie toujours des requêtes AdMob non personnalisées, "
                "désactive l'identifiant propriétaire de l'éditeur Google "
                "(same-app) avant le démarrage de Mobile Ads et ne demande pas "
                "l'autorisation ATT d'Apple. Nous n'utilisons pas les données de "
                "l'App pour vous suivre entre les apps ou sites web d'autres "
                "entreprises.",
                "Sur Android, la diffusion et la personnalisation des annonces "
                "peuvent dépendre de votre région, du consentement Google UMP et "
                "des réglages. Vous pouvez gérer les choix disponibles dans les "
                "options de confidentialité de l'App ou de l'appareil.",
                "Pratiques de Google en matière de données : "
                "https://policies.google.com/technologies/partner-sites",
                "Firebase Crashlytics sert au diagnostic des pannes. Firebase "
                "Analytics est activé par défaut et peut être désactivé dans Réglages. "
                "Remote Config peut utiliser un identifiant d'installation pour "
                "le catalogue facultatif Autres jeux.",
            ]),
            ("Achats", [
                "Les achats intégrés passent par Google Play ou l'App Store. "
                "Vos informations de paiement sont traitées par la boutique ; "
                "nous ne voyons ni ne conservons vos données bancaires.",
                "L'application contrôle localement la transaction native signalée "
                "par la boutique. Il n'existe pas encore de validation serveur "
                "faisant autorité pour les reçus ou remboursements.",
            ]),
            ("Enfants", [
                "{app} est un jeu de réflexion adapté à tous les âges et ne "
                "collecte pas sciemment de données personnelles d'enfants.",
                "Si vous pensez que des données concernant votre enfant ont "
                "été traitées, contactez-nous et nous agirons.",
            ]),
            ("Vos droits", [
                "Vous pouvez gérer les données locales, Analytics et le consentement "
                "publicitaire dans les réglages de l'application, de confidentialité "
                "et de l'appareil.",
                "Vous pouvez malgré tout nous écrire pour toute question.",
            ]),
            ("Modifications", [
                "Cette politique peut être mise à jour. La version en vigueur "
                "est toujours publiée sur cette page et la date ci-dessus "
                "change en conséquence.",
            ]),
        ],
        "terms": [
            ("Acceptation", [
                "En téléchargeant ou en utilisant {app}, vous acceptez ces "
                "conditions. Si vous les refusez, n'utilisez pas "
                "l'application.",
            ]),
            ("Droit d'utilisation", [
                "Nous vous accordons un droit limité et non transférable "
                "d'utiliser {app} à des fins personnelles et non "
                "commerciales.",
                "L'application ne peut être vendue, louée ni cédée à un "
                "tiers.",
            ]),
            ("Indices et objets virtuels", [
                "Les indices sont des objets virtuels. Ils n'ont aucune "
                "valeur monétaire réelle, ne sont pas convertibles en argent "
                "et ne peuvent pas être transférés hors du jeu.",
                "Les indices peuvent être gagnés gratuitement (publicité "
                "récompensée) ou achetés.",
                "Les remboursements relèvent des règles de la boutique où "
                "l'achat a été effectué (Google Play ou App Store).",
            ]),
            ("Publicité", [
                "Les publicités récompensées sont entièrement facultatives. "
                "Si la publicité n'est pas regardée jusqu'au bout, aucune "
                "récompense n'est accordée ; ce n'est pas un "
                "dysfonctionnement.",
                "Le contenu publicitaire est déterminé par la régie et "
                "échappe à notre contrôle.",
            ]),
            ("Usage acceptable", [
                "Il est interdit de procéder à de l'ingénierie inverse, de "
                "modifier les données sauvegardées pour créer des indices ou "
                "de la progression, ou de tenter de perturber le service.",
            ]),
            ("Propriété intellectuelle", [
                "Le design, le code, les niveaux, les graphismes et la "
                "musique du jeu appartiennent au développeur et sont protégés "
                "par le droit d'auteur.",
            ]),
            ("Exclusion de garantie", [
                "L'application est fournie \"en l'état\". Aucun "
                "fonctionnement ininterrompu ou sans erreur n'est garanti.",
                "Dans la limite permise par la loi, nous ne sommes pas "
                "responsables des dommages indirects liés à l'utilisation de "
                "l'application.",
            ]),
            ("Modifications", [
                "Ces conditions peuvent être mises à jour. Continuer à "
                "utiliser l'application après une mise à jour vaut "
                "acceptation.",
            ]),
            ("Droit applicable", [
                "Ces conditions sont régies par le droit de la République de "
                "Türkiye.",
            ]),
        ],
    },
    "ar": {
        "name": "العربية",
        "dir": "rtl",
        "updated": "آخر تحديث",
        "back": "الصفحة الرئيسية",
        "other": "لغات أخرى",
        "tagline": "لعبة ألغاز منطقية بالأرقام",
        "intro": "فيما يلي سياسة الخصوصية وشروط الاستخدام للعبة {app}.",
        "privacy_title": "سياسة الخصوصية",
        "terms_title": "شروط الاستخدام",
        "contact_title": "التواصل",
        "contact_body": "لأي سؤال بخصوص هذه المستندات أو اللعبة، راسلنا:",
        "privacy": [
            ("باختصار", [
                "لا تطلب {app} إنشاء حساب ولا تجمع اسمك أو بريدك الإلكتروني "
                "أو رقم هاتفك أو موقعك.",
                "لا يُرسل تقدّمك إلى حساب خادم نديره، وقد يضمّه نظام التشغيل "
                "إلى نسخة احتياطية للجهاز.",
            ]),
            ("البيانات المحفوظة على جهازك", [
                "يُحفظ تقدّم المراحل والنجوم ورصيد التلميحات وإعدادات الصوت "
                "والاهتزاز في التخزين المحلي لجهازك.",
                "تُستخدم هذه البيانات لتشغيل اللعبة. تؤدي إزالة التطبيق عادةً "
                "إلى حذف البيانات المحلية، لكن إعدادات النسخ والاستعادة قد "
                "تحتفظ بنسخة منها.",
            ]),
            ("الإعلانات", [
                "لا توجد إعلانات إجبارية. يمكنك اختيار مشاهدة إعلان مكافأة "
                "للحصول على تلميحات.",
                "تُعرض الإعلانات عبر Google AdMob. على iOS ترسل Equalize دائمًا "
                "طلبات AdMob غير مخصّصة، وتعطّل معرّف الناشر التابع لـ Google "
                "(same-app) قبل بدء Mobile Ads، ولا تطلب إذن ATT من Apple. ولا "
                "نستخدم بيانات التطبيق لتتبّعك عبر تطبيقات أو مواقع شركات أخرى.",
                "على Android قد يعتمد عرض الإعلانات وتخصيصها على منطقتك وموافقة "
                "Google UMP وإعداداتك. ويمكنك إدارة الخيارات المتاحة من إعدادات "
                "الخصوصية في التطبيق أو من إعدادات الجهاز.",
                "ممارسات Google بشأن البيانات: "
                "https://policies.google.com/technologies/partner-sites",
                "يُستخدم Firebase Crashlytics لتشخيص الأعطال. ويكون Firebase "
                "Analytics مفعّلًا افتراضيًا ويمكن إيقافه من الإعدادات. وقد "
                "يستخدم Remote Config معرّف تثبيت لجلب كتالوج الألعاب الاختياري.",
            ]),
            ("عمليات الشراء", [
                "تتم عمليات الشراء داخل التطبيق عبر Google Play أو App "
                "Store. يعالج المتجر بيانات الدفع؛ نحن لا نرى بيانات بطاقتك "
                "ولا نحفظها.",
                "يتحقق التطبيق محليًا من المعاملة الأصلية التي يبلغ بها المتجر. "
                "ولا يوجد بعد تحقق سلطوي على الخادم من الإيصالات أو المبالغ "
                "المستردة؛ لذا تعتمد الإلغاءات على مزامنة المتجر.",
            ]),
            ("الأطفال", [
                "{app} لعبة ألغاز مناسبة لجميع الأعمار ولا تجمع عن قصد أي "
                "بيانات شخصية من الأطفال.",
                "إذا كنت تعتقد أن بيانات طفلك قد عولجت، فيرجى مراسلتنا "
                "وسنتصرف بشأنها.",
            ]),
            ("حقوقك", [
                "يمكنك إدارة البيانات المحلية والتحليلات وموافقة الإعلانات من "
                "إعدادات التطبيق والخصوصية والجهاز.",
                "ومع ذلك يمكنك مراسلتنا بأي سؤال.",
            ]),
            ("التغييرات", [
                "قد نُحدّث هذه السياسة من حين لآخر. تُنشر النسخة السارية "
                "دائمًا على هذه الصفحة ويتغير التاريخ أعلاه تبعًا لذلك.",
            ]),
        ],
        "terms": [
            ("القبول", [
                "بتنزيل {app} أو استخدامها فإنك توافق على هذه الشروط. إن لم "
                "توافق فيرجى عدم استخدام التطبيق.",
            ]),
            ("حق الاستخدام", [
                "نمنحك حقًا محدودًا وغير قابل للنقل لاستخدام {app} لأغراض "
                "شخصية غير تجارية.",
                "لا يجوز بيع التطبيق أو تأجيره أو نقله إلى طرف آخر.",
            ]),
            ("التلميحات والعناصر الافتراضية", [
                "التلميحات عناصر افتراضية داخل اللعبة، ليست لها قيمة نقدية "
                "حقيقية ولا يمكن استبدالها بالمال أو نقلها خارج اللعبة.",
                "يمكن الحصول على التلميحات مجانًا (إعلانات المكافأة) أو "
                "شراؤها.",
                "تخضع عمليات الاسترداد لقواعد المتجر الذي تم الشراء منه "
                "(Google Play أو App Store).",
            ]),
            ("الإعلانات", [
                "إعلانات المكافأة اختيارية تمامًا. إذا لم تُشاهد الإعلان حتى "
                "النهاية فلن تُمنح المكافأة، وهذا ليس خللًا.",
                "يحدد محتوى الإعلانات مزوّد الإعلانات وهو خارج عن سيطرتنا.",
            ]),
            ("الاستخدام المقبول", [
                "يُحظر إجراء هندسة عكسية للتطبيق، أو العبث بالبيانات المحفوظة "
                "لتوليد تلميحات أو تقدّم، أو محاولة تعطيل الخدمة.",
            ]),
            ("الملكية الفكرية", [
                "تصميم اللعبة وشيفرتها ومراحلها ورسومها وموسيقاها ملك للمطوّر "
                "ومحمية بحقوق النشر.",
            ]),
            ("إخلاء المسؤولية", [
                "يُقدَّم التطبيق \"كما هو\" دون ضمان عمله دون انقطاع أو دون "
                "أخطاء.",
                "وفي الحدود التي يسمح بها القانون، لا نتحمل المسؤولية عن "
                "الأضرار غير المباشرة الناتجة عن استخدام التطبيق.",
            ]),
            ("التغييرات", [
                "قد نُحدّث هذه الشروط. ويُعد استمرارك في استخدام التطبيق بعد "
                "التحديث قبولًا للشروط الجديدة.",
            ]),
            ("القانون الواجب التطبيق", [
                "تخضع هذه الشروط لقوانين جمهورية تركيا.",
            ]),
        ],
    },
}

# ── Şablon ────────────────────────────────────────────────────────────────

CSS = """
:root{--bg:#0E1117;--surface:#161B24;--stroke:#2E3646;--text:#F3F5F9;
--dim:#8A94A6;--faint:#5A6373;--accent:#34D399;--gold:#FBBF24}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);
font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,
"Helvetica Neue",Arial,sans-serif;-webkit-text-size-adjust:100%}
.wrap{max-width:760px;margin:0 auto;padding:32px 22px 72px}
header{display:flex;align-items:center;gap:14px;margin-bottom:6px}
.logo{width:52px;height:52px;flex:none;border-radius:15px;background:var(--surface);
border:1px solid var(--stroke);display:grid;place-items:center;
font-weight:800;font-size:21px;color:var(--accent)}
h1{font-size:26px;line-height:1.25;margin:0;font-weight:800}
.app{margin:0;color:var(--dim);font-size:14px}
.meta{color:var(--faint);font-size:13px;margin:14px 0 26px}
h2{font-size:18px;margin:30px 0 10px;font-weight:800}
p{margin:0 0 12px;color:#C9D0DC}
a{color:var(--accent)}
ul{margin:0 0 12px;padding-inline-start:20px;color:#C9D0DC}
li{margin-bottom:8px}
.card{background:var(--surface);border:1px solid var(--stroke);
border-radius:18px;padding:18px 20px;margin:26px 0}
.langs{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.langs a{display:inline-block;padding:7px 13px;border-radius:999px;
background:var(--surface);border:1px solid var(--stroke);
color:var(--dim);text-decoration:none;font-size:13.5px}
.langs a.on{color:var(--bg);background:var(--accent);border-color:var(--accent);
font-weight:700}
.docs{display:grid;gap:12px;margin:24px 0}
.docs a{display:block;padding:18px 20px;border-radius:18px;
background:var(--surface);border:1px solid var(--stroke);
text-decoration:none;color:var(--text);font-weight:700}
.docs a span{display:block;color:var(--faint);font-weight:400;font-size:13.5px;
margin-top:3px}
footer{margin-top:40px;color:var(--faint);font-size:13px}
[dir=rtl] ul{padding-inline-start:20px}
"""

PAGE = """<!doctype html>
<html lang="{lang}" dir="{dir}">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — {app}</title>
<meta name="description" content="{title} — {app}">
{alternates}
<style>{css}</style>
<div class="wrap">
<header>
  <div class="logo">=</div>
  <div>
    <h1>{title}</h1>
    <p class="app">{app} · {tagline}</p>
  </div>
</header>
<p class="meta">{updated}: {effective}</p>
{body}
<div class="card">
  <h2 style="margin-top:0">{contact_title}</h2>
  <p>{contact_body}</p>
  <p><a href="mailto:{email}">{email}</a></p>
</div>
<footer>
  <p>{other}</p>
  <div class="langs">{langs}</div>
  <p style="margin-top:18px"><a href="../index.html">{back}</a></p>
</footer>
</div>
"""

INDEX = """<!doctype html>
<html lang="{lang}" dir="{dir}">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{app} — {tagline}</title>
<meta name="description" content="{app} — {tagline}">
<style>{css}</style>
<div class="wrap">
<header>
  <div class="logo">=</div>
  <div>
    <h1>{app}</h1>
    <p class="app">{tagline}</p>
  </div>
</header>
<p style="margin-top:18px">{intro}</p>
<div class="docs">
  <a href="{lang}/privacy.html">{privacy_title}<span>{effective}</span></a>
  <a href="{lang}/terms.html">{terms_title}<span>{effective}</span></a>
</div>
<div class="card">
  <h2 style="margin-top:0">{contact_title}</h2>
  <p>{contact_body}</p>
  <p><a href="mailto:{email}">{email}</a></p>
</div>
<footer>
  <p>{other}</p>
  <div class="langs">{langs}</div>
</footer>
</div>
<script>
// Tarayıcı dili desteklediğimiz bir dilse o dilin sayfalarını gösterir.
// Kullanıcı bir dil seçtiyse (?lang=) karışmayız.
(function () {{
  var supported = {supported};
  var params = new URLSearchParams(location.search);
  if (params.get('lang')) return;
  var want = (navigator.language || 'en').slice(0, 2).toLowerCase();
  if (want === '{lang}' || supported.indexOf(want) < 0) return;
  location.replace(want + '/index.html');
}})();
</script>
"""

SUB_INDEX = """<!doctype html>
<html lang="{lang}" dir="{dir}">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{app} — {tagline}</title>
<style>{css}</style>
<div class="wrap">
<header>
  <div class="logo">=</div>
  <div>
    <h1>{app}</h1>
    <p class="app">{tagline}</p>
  </div>
</header>
<p style="margin-top:18px">{intro}</p>
<div class="docs">
  <a href="privacy.html">{privacy_title}<span>{effective}</span></a>
  <a href="terms.html">{terms_title}<span>{effective}</span></a>
</div>
<div class="card">
  <h2 style="margin-top:0">{contact_title}</h2>
  <p>{contact_body}</p>
  <p><a href="mailto:{email}">{email}</a></p>
</div>
<footer>
  <p>{other}</p>
  <div class="langs">{langs}</div>
  <p style="margin-top:18px"><a href="../index.html">{back}</a></p>
</footer>
</div>
"""


def linkify(text: str) -> str:
    """Düz metindeki adresleri bağlantıya çevirir."""
    out = html.escape(text)
    marker = "https://policies.google.com/technologies/partner-sites"
    return out.replace(marker, f'<a href="{marker}">{marker}</a>')


def render_sections(sections, app: str) -> str:
    parts = []
    for title, items in sections:
        parts.append(f"<h2>{html.escape(title.format(app=app))}</h2>")
        parts.append("<ul>")
        for item in items:
            parts.append(f"<li>{linkify(item.format(app=app))}</li>")
        parts.append("</ul>")
    return "\n".join(parts)


def lang_links(current: str, page: str, from_root: bool) -> str:
    out = []
    for code, data in LOCALES.items():
        prefix = "" if from_root else "../"
        href = f"{prefix}{code}/{page}"
        cls = ' class="on"' if code == current else ""
        out.append(f'<a href="{href}"{cls}>{html.escape(data["name"])}</a>')
    return "".join(out)


def alternates(page: str) -> str:
    tags = [
        f'<link rel="alternate" hreflang="{code}" '
        f'href="{BASE}/{code}/{page}">'
        for code in LOCALES
    ]
    tags.append(f'<link rel="alternate" hreflang="x-default" '
                f'href="{BASE}/en/{page}">')
    return "\n".join(tags)


def main() -> None:
    for code, data in LOCALES.items():
        folder = os.path.join(OUT, code)
        shutil.rmtree(folder, ignore_errors=True)
        os.makedirs(folder, exist_ok=True)

        common = dict(
            lang=code,
            dir=data["dir"],
            app=APP,
            css=CSS,
            effective=EFFECTIVE,
            email=EMAIL,
            updated=data["updated"],
            back=data["back"],
            other=data["other"],
            tagline=data["tagline"],
            contact_title=data["contact_title"],
            contact_body=data["contact_body"],
            privacy_title=data["privacy_title"],
            terms_title=data["terms_title"],
            intro=data["intro"].format(app=APP),
        )

        for page, key in (("privacy.html", "privacy"), ("terms.html", "terms")):
            with open(os.path.join(folder, page), "w", encoding="utf-8") as f:
                f.write(PAGE.format(
                    **common,
                    title=data[f"{key}_title"],
                    body=render_sections(data[key], APP),
                    langs=lang_links(code, page, from_root=False),
                    alternates=alternates(page),
                ))

        with open(os.path.join(folder, "index.html"), "w",
                  encoding="utf-8") as f:
            f.write(SUB_INDEX.format(
                **common,
                langs=lang_links(code, "index.html", from_root=False),
            ))

    # Kök sayfa Türkçe; tarayıcı dili farklıysa kendi klasörüne yönlendirir.
    root = LOCALES["tr"]
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX.format(
            lang="tr",
            dir=root["dir"],
            app=APP,
            css=CSS,
            effective=EFFECTIVE,
            email=EMAIL,
            other=root["other"],
            tagline=root["tagline"],
            contact_title=root["contact_title"],
            contact_body=root["contact_body"],
            privacy_title=root["privacy_title"],
            terms_title=root["terms_title"],
            intro=root["intro"].format(app=APP),
            langs=lang_links("tr", "index.html", from_root=True),
            supported=str(list(LOCALES)).replace("'", '"'),
        ))

    # GitHub Pages'in Jekyll'e sokmaması için.
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    print(f"{len(LOCALES)} dil yazıldı: {', '.join(LOCALES)}")
    print(f"Gizlilik : {BASE}/tr/privacy.html")
    print(f"Koşullar : {BASE}/tr/terms.html")
    print(f"Paket    : {PACKAGE}")


if __name__ == "__main__":
    main()

# equalize-pages

[Equalize](https://apps.apple.com/app/equalize) uygulamasının yasal sayfaları.
GitHub Pages ile yayımlanır: <https://mnpekdemirapps.github.io/equalize-pages/>

## Bu depo ELLE düzenlenmez

Sayfalar uygulama deposundan üretilir:

```sh
# equalize projesinde
dart run tool/build_pages.dart <bu-deponun-yolu>
```

Kaynak metin `lib/features/legal/legal_documents.dart` dosyasıdır ve
uygulamanın kendi Gizlilik / Kullanım Koşulları ekranını da o besler.
Sebebi: mağaza incelemesi listelemedeki politikayla uygulamadakini
karşılaştırıyor. İki ayrı kopya tutmak er geç ayrışıyor ve bu doğrudan ret
sebebi; tek kaynaktan üretmek ayrışmayı yapısal olarak imkânsız kılıyor.

Bir maddeyi değiştirmek için uygulama deposundaki metni düzenleyin, aracı
yeniden çalıştırın ve çıktıyı buraya commit edin.

## Yapı

```
index.html          dil seçimi
style.css           tek stil dosyası (koyu/açık tema)
app-ads.txt         AdMob yayıncı doğrulaması
<dil>/index.html    dil ana sayfası
<dil>/privacy.html  Gizlilik Politikası
<dil>/terms.html    Kullanım Koşulları
```

Diller: `ar` `de` `en` `es` `fr` `tr`. Uygulama cihaz diline göre doğrudan
`<dil>/privacy.html` adresini açar; dil listede yoksa `en` sürümüne düşer
(bkz. `lib/core/app_identity.dart`).

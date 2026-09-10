# equalize-pages

[Equalize](https://apps.apple.com/app/equalize) uygulamasının yasal sayfaları.
GitHub Pages ile yayımlanır: <https://mnpekdemirapps.github.io/equalize-pages/>

## Bu depo ELLE düzenlenmez

Sayfalar uygulama deposundan üretilir:

```sh
# equalize projesinde; bu site deposuna doğrudan çıktı yazmayın
dart run tool/build_pages.dart <ayri-staging-dizini>
```

Kaynak metin `lib/features/legal/legal_documents.dart` dosyasıdır ve
uygulamanın kendi Gizlilik / Kullanım Koşulları ekranını da o besler.
Sebebi: mağaza incelemesi listelemedeki politikayla uygulamadakini
karşılaştırıyor. İki ayrı kopya tutmak er geç ayrışıyor ve bu doğrudan ret
sebebi; tek kaynaktan üretmek ayrışmayı yapısal olarak imkânsız kılıyor.

Bir maddeyi değiştirmek için uygulama deposundaki metni düzenleyin ve aracı
ayrı bir staging dizinine çalıştırın. Sonra yalnız değişiklik kapsamında
incelenmiş HTML dosyalarını buraya aktarın. Privacy güncellemesinde altı
`<dil>/privacy.html` dosyası yeterlidir; stylesheet gerçekten değişmişse onu
ayrıca inceleyin. İlgisiz ana sayfa, support veya terms dosyalarını ezmeyin.

**Onaylı `app-ads.txt` dosyasını hiçbir zaman üretim çıktısından kopyalamayın
veya değiştirmeyin.** Dart exporter staging dizininde bu dosyayı da üretir;
staging dosyasının varlığı onu siteye aktarma yetkisi değildir.

Bu depodaki eski Python `build.py` artık çalışmayı bir açıklama ile durdurur.
İçindeki bağımsız metin tablosu canonical değildir; yeniden etkinleştirmek eski
“iOS'ta ATT istenmez” beyanlarını geri getirir. Uygulama içi belgeler ve web
belgeleri aynı Dart kaynağından beslenmelidir.

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

# URL Kontrol Aracı

Bu Python aracı, verilen URL'lerin erişilebilir olup olmadığını kontrol eder ve sonuçları farklı formatlarda kaydeder.

## Özellikler

- URL'lerin erişilebilirlik kontrolü
- Eş zamanlı URL kontrolü
- Otomatik yönlendirme takibi
- SSL sertifika kontrolü
- Yeniden deneme mekanizması
- PDF ve TXT formatında sonuç raporlama
- Renkli konsol çıktısı
- Detaylı loglama

## Gereksinimler

- Python 3.6 veya üzeri
- requests
- colorama
- tqdm
- reportlab (PDF çıktısı için)

## Kurulum

1. Gerekli Python paketlerini yükleyin:
```bash
pip install requests colorama tqdm reportlab
```

2. Projeyi klonlayın veya indirin.

## Kullanım

1. `urls.txt` dosyasına kontrol edilecek URL'leri her satıra bir tane olacak şekilde ekleyin:
```
https://example.com
https://example.org
```

2. İsteğe bağlı olarak `config.json` dosyasını düzenleyin:
```json
{
    "timeout": 0,
    "concurrent_scan": 1,
    "retry_count": 0,
    "retry_delay": 0,
    "verify_ssl": false,
    "method": "GET",
    "output_format": "txt",
    "headers": {
        "User-Agent": "Mozilla/5.0 ...",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }
}
```

3. Programı çalıştırın:
```bash
python url_checker.py
```

## Çıktılar

Program çalıştığında aşağıdaki dosyalar oluşturulur:

- `active.txt`: Erişilebilir URL'lerin listesi
- `inactive.txt`: Erişilemeyen URL'lerin listesi
- `url_checker_results.pdf`: Detaylı sonuç raporu (PDF formatında)
- `url_checker.log`: Program log dosyası

## Yapılandırma Seçenekleri

- `timeout`: URL kontrolü için maksimum bekleme süresi (saniye)
- `concurrent_scan`: Aynı anda kontrol edilecek URL sayısı
- `retry_count`: Başarısız URL'ler için yeniden deneme sayısı
- `retry_delay`: Yeniden denemeler arası bekleme süresi (saniye)
- `verify_ssl`: SSL sertifika doğrulaması yapılıp yapılmayacağı
- `method`: HTTP istek metodu (GET, POST, HEAD vb.)
- `output_format`: Sonuç formatı (txt veya pdf)
- `headers`: HTTP istek başlıkları

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir özellik dalı oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Dalınıza push yapın (`git push origin feature/amazing-feature`)
5. Bir Pull Request oluşturun 

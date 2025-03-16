# URL Validator

URL'lerin erişilebilirliğini kontrol eden, eş zamanlı tarama yapabilen ve sonuçları TXT formatında kaydeden bir Python aracı.

## 🚀 Özellikler

- Eş zamanlı URL kontrolü
- Yönlendirme takibi
- Özelleştirilebilir timeout süresi
- Yeniden deneme mekanizması
- Detaylı hata raporlama
- Renkli konsol çıktısı
- TXT formatında sonuç kaydı

## 📋 Gereksinimler

- Python 3.6 veya üzeri
- pip (Python paket yöneticisi)

## 🔧 Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/seyitahmettanriver/url-validator.git
cd url-validator
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. `config.json` dosyasını düzenleyin:
```json
{
    "timeout": 5,
    "concurrent_scan": 1,
    "retry_count": 0,
    "retry_delay": 0,
    "method": "GET",
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }
}
```

## 💻 Kullanım

1. `urls.txt` dosyasına kontrol edilecek URL'leri her satıra bir tane olacak şekilde ekleyin:
```
https://example.com
https://example.org
example.net
```

2. Programı çalıştırın:
```bash
python url_checker.py
```

3. Sonuçlar `active.txt` ve `inactive.txt` dosyalarına kaydedilecektir.

## ⚙️ Yapılandırma

`config.json` dosyasındaki ayarlar:

| Ayar | Açıklama | Varsayılan |
|------|-----------|------------|
| timeout | URL kontrolü için maksimum bekleme süresi (saniye) | 5 |
| concurrent_scan | Eş zamanlı kontrol edilecek URL sayısı | 1 |
| retry_count | Başarısız denemelerde yeniden deneme sayısı | 0 |
| retry_delay | Yeniden denemeler arası bekleme süresi (saniye) | 0 |
| method | HTTP istek metodu (GET, POST, vb.) | GET |
| headers | HTTP istek başlıkları | Varsayılan tarayıcı başlıkları |

## 📝 Çıktılar

Program çalıştığında:
- Konsolda renkli ve detaylı ilerleme bilgisi gösterilir
- `active.txt`: Erişilebilir URL'ler
- `inactive.txt`: Erişilemeyen URL'ler
- `url_checker.log`: Detaylı log kayıtları

## 🤝 Katkıda Bulunma

1. Bu repoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

- GitHub: [@seyitahmettanriver](https://github.com/seyitahmettanriver)
- Proje URL: [https://github.com/seyitahmettanriver/url-validator](https://github.com/seyitahmettanriver/url-validator)

## 🙏 Teşekkürler

- [requests](https://requests.readthedocs.io/) - HTTP istekleri için
- [tqdm](https://tqdm.github.io/) - İlerleme çubuğu için
- [colorama](https://pypi.org/project/colorama/) - Renkli konsol çıktısı için 

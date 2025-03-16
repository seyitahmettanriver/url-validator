import requests
import time
import logging
import json
import traceback
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import colorama
from urllib.parse import urlparse

# Initialize colorama
colorama.init()

# Logging ayarlarını basitleştir
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler('url_checker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def log_info(message: str):
    """Bilgi mesajı logla."""
    logger.info(f"{colorama.Fore.CYAN}{message}{colorama.Style.RESET_ALL}")

def log_success(message: str):
    """Başarı mesajı logla."""
    logger.info(f"{colorama.Fore.GREEN}{message}{colorama.Style.RESET_ALL}")

def log_error(message: str):
    """Hata mesajı logla."""
    logger.error(f"{colorama.Fore.RED}{message}{colorama.Style.RESET_ALL}")

def log_warning(message: str):
    """Uyarı mesajı logla."""
    logger.warning(f"{colorama.Fore.YELLOW}{message}{colorama.Style.RESET_ALL}")

def clean_url(url: str) -> str:
    """URL'yi temizle ve düzenle."""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url

def is_success_status(status_code: int) -> bool:
    """HTTP durum kodunun başarılı olup olmadığını kontrol et."""
    return 200 <= status_code < 400

def load_config():
    """Load configuration from config.json file."""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        log_error("config.json dosyası bulunamadı! Varsayılan ayarlar kullanılacak.")
        return get_default_config()
    except json.JSONDecodeError:
        log_error("config.json dosyası geçersiz! Varsayılan ayarlar kullanılacak.")
        return get_default_config()

def get_default_config() -> Dict[str, Any]:
    """Get default configuration settings."""
    return {
        "timeout": 0,
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

def check_url(url: str, config: dict) -> Tuple[str, bool, str, Dict[str, Any]]:
    """Check if a URL is accessible."""
    url = clean_url(url.strip())
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    retry_count = 0
    while retry_count <= config['retry_count']:
        try:
            if retry_count > 0:
                print(f"{colorama.Fore.YELLOW}[Yeniden Deneme {retry_count}/{config['retry_count']}] {url}{colorama.Style.RESET_ALL}")
                time.sleep(config['retry_delay'])
            else:
                print(f"\n{colorama.Fore.CYAN}[Kontrol] {url}{colorama.Style.RESET_ALL}")
            
            # HTTP isteği
            response = requests.request(
                method=config['method'],
                url=url,
                timeout=config['timeout'],
                allow_redirects=True,
                headers=config['headers']
            )
            
            # 403 hatası durumunda bile site erişilebilir kabul edilebilir
            if response.status_code == 403:
                print(f"{colorama.Fore.YELLOW}[403] Erişim Reddedildi - Site muhtemelen erişilebilir: {url}{colorama.Style.RESET_ALL}")
                return url, True, url, {
                    "status_code": 403,
                    "error": None,
                    "response_time": response.elapsed.total_seconds(),
                    "content_length": len(response.content) if response.content else 0
                }
            
            is_success = is_success_status(response.status_code)
            final_url = response.url
            
            # Eğer yönlendirme varsa ve başarılıysa
            if final_url != url and is_success:
                print(f"{colorama.Fore.BLUE}[Yönlendirme] {url} -> {final_url}{colorama.Style.RESET_ALL}")
            
            if is_success:
                print(f"{colorama.Fore.GREEN}[Başarılı] {url} (Durum Kodu: {response.status_code}){colorama.Style.RESET_ALL}")
            else:
                print(f"{colorama.Fore.RED}[Başarısız] {url} (Durum Kodu: {response.status_code}){colorama.Style.RESET_ALL}")
            
            return url, is_success, final_url, {
                "status_code": response.status_code,
                "error": None,
                "response_time": response.elapsed.total_seconds(),
                "content_length": len(response.content) if response.content else 0
            }
            
        except requests.Timeout:
            print(f"{colorama.Fore.RED}[Timeout] {url} - {config['timeout']} saniye içinde yanıt alınamadı{colorama.Style.RESET_ALL}")
            retry_count += 1
            if retry_count > config['retry_count']:
                return url, False, url, {"status_code": 0, "error": "Timeout", "response_time": 0, "content_length": 0}
            
        except requests.ConnectionError:
            print(f"{colorama.Fore.RED}[Bağlantı Hatası] {url} - Siteye bağlanılamadı{colorama.Style.RESET_ALL}")
            retry_count += 1
            if retry_count > config['retry_count']:
                return url, False, url, {"status_code": 0, "error": "Connection Error", "response_time": 0, "content_length": 0}
            
        except requests.RequestException as e:
            print(f"{colorama.Fore.RED}[Hata] {url} - {str(e)}{colorama.Style.RESET_ALL}")
            retry_count += 1
            if retry_count > config['retry_count']:
                return url, False, url, {"status_code": 0, "error": str(e), "response_time": 0, "content_length": 0}
            
        except Exception as e:
            print(f"{colorama.Fore.RED}[Hata] {url} - {str(e)}{colorama.Style.RESET_ALL}")
            retry_count += 1
            if retry_count > config['retry_count']:
                return url, False, url, {"status_code": 0, "error": str(e), "response_time": 0, "content_length": 0}
    
    return url, False, url, {"status_code": 0, "error": "Max retries exceeded", "response_time": 0, "content_length": 0}

def save_results(active_urls: List[Dict[str, Any]], inactive_urls: List[Dict[str, Any]], config: dict):
    """Save results in TXT format."""
    try:
        with open('active.txt', 'w', encoding='utf-8') as f:
            for item in active_urls:
                f.write(f"{item.get('url', '')}\n")
        
        with open('inactive.txt', 'w', encoding='utf-8') as f:
            for item in inactive_urls:
                f.write(f"{item.get('url', '')}\n")
        
        log_success("Sonuçlar kaydedildi")
            
    except Exception as e:
        log_error(f"Sonuçları kaydetme hatası: {str(e)}")
        raise

def process_urls(urls: List[str], config: dict) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Process URLs with concurrent scanning based on configuration."""
    active_urls = []
    inactive_urls = []
    
    try:
        urls = [clean_url(url) for url in urls]
        urls = [url for url in urls if url]
        
        print(f"\n{colorama.Fore.CYAN}=== Tarama Başlıyor ==={colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.CYAN}Toplam URL Sayısı: {len(urls)}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.CYAN}Eş Zamanlı Tarama: {config['concurrent_scan']}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.CYAN}Timeout Süresi: {config['timeout']} saniye{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.CYAN}====================={colorama.Style.RESET_ALL}\n")
        
        with tqdm(
            total=len(urls),
            desc=f"{colorama.Fore.CYAN}İlerleme{colorama.Style.RESET_ALL}",
            unit="url",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            colour="green"
        ) as pbar:
            with ThreadPoolExecutor(max_workers=config['concurrent_scan']) as executor:
                futures = []
                for url in urls:
                    future = executor.submit(check_url, url, config)
                    futures.append(future)
                
                for future in futures:
                    try:
                        url, is_active, final_url, details = future.result()
                        result = {
                            "url": url,
                            "final_url": final_url,
                            **details
                        }
                        
                        if is_active:
                            active_urls.append(result)
                        else:
                            inactive_urls.append(result)
                    except Exception as e:
                        log_error(f"URL işlenirken hata oluştu: {str(e)}")
                    finally:
                        pbar.update(1)
        
        return active_urls, inactive_urls
    except Exception as e:
        log_error(f"URL işleme hatası: {str(e)}")
        raise

def main():
    try:
        # Load configuration
        config = load_config()
        
        # Read URLs from file
        try:
            with open('urls.txt', 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
        except Exception as e:
            log_error(f"urls.txt dosyası okuma hatası: {str(e)}")
            raise
        
        if not urls:
            log_error("urls.txt dosyasında URL bulunamadı")
            return
        
        # Process URLs
        active_urls, inactive_urls = process_urls(urls, config)
        
        # Save results
        save_results(active_urls, inactive_urls, config)
        
        # Print summary
        print(f"\n{colorama.Fore.CYAN}=== Tarama Tamamlandı ==={colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.GREEN}Erişilebilir URL'ler: {len(active_urls)}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.RED}Erişilemeyen URL'ler: {len(inactive_urls)}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.CYAN}========================{colorama.Style.RESET_ALL}")
        
    except FileNotFoundError:
        log_error("urls.txt dosyası bulunamadı!")
    except Exception as e:
        log_error(f"Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_error(f"Program çalıştırma hatası: {str(e)}") 
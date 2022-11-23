

## Python ile Linkedin Webscraping Nasıl Yapılır?

**Yazının İngilizce hali için** → https://medium.com/@denizbarankara3/how-to-webscrape-linkedin-with-python-ea04144946fc

Arkadaşımla küçük bir yan proje yapmaya başladığımızda bu sorunun cevabını arıyorduk. Fakat piyasada iyi bir açık kaynaklı Linkedin Webscraping projesi bulamadık.

Bulduğumuz projeler ya ücretli, ya eksik ya da eskiydi. İlanlardan detaylı bilgileri almak yerine sadece basit bir şekilde ilan başlık verisini çekmişlerdi. Bizde kendi Linkedin Webscraper’ımızı yapma kararı aldık. Bunun için öncelikle bir plan kurmamız gerekti şimdi size bundan bahsedeceğim. <br>
![enter image description here](https://miro.medium.com/max/1400/1*7SxyDgnzJ3v5nVeBDwzsrw.jpeg)


## PLAN

1. Veri Çekilecek Kaynağı Belirlemek: İş ilanı verilerini analiz etmek için bir çok iş ilanı sitesi var fakat en çok iş ilanı bulunan site Linkedin’di bende tercihi bu yönde yaptım.<br><br>
2. İş İlanı Verilerini Kazmak: İlanın; başlığı, tarihi, konumu, açıklaması gibi birçok veriyi çekmek istiyordum. Bu kısmı yapması kolay fakat zor olansa çalışma şekli ve açıklama verilerini çekmekti. Bu iki veriyi çekmek için iş ilanlarına tıklamamızı gerekiyordu, ancak sorun bu değildi. Sorun, çalışma şekli verisinin iş ilanı veren firmaya göre değişken bir XPATH’e sahip olmasıydı.<br><br>
3. Verileri Veri Tabanına Aktarmak: Bu projede MySQL kullandık, fakat eğer isterseniz birkaç değişiklikle verileri CSV dosyasına da kaydedebilirsiniz.<br><br>

## Gerekli Bileşenler

1. **Python:** Python’u resmi web sitesinden kolayca yükleyebilirsiniz. Ücretsizdir ve lisans gerektirmez. Kodu yazmak ve düzenlemek için Visual Studio Code’u öneririm.<br><br>
2. **Selenium:** Python ve diğer birçok yazılım dili için yaygın olarak kullanılan açık kaynaklı bir webscraping kütüphanesidir.<br><br>
```python
pip install selenium
```
Windows dışında başka bir işletim sistemi kullanıyorsanız, adımlar biraz farklı olabilir ve ayrıca Selenium kodunu çalıştırabilmek için bir Selenium web sürücüsü yüklemeniz gerekir. Ancak Selenium kurulumunda daha çok detaya girmeyeceğim. Selenium kurulumu için veya genel olarak Selenium hakkında daha fazla bilgi almak istiyorsanız bu siteyi ziyaret edin.<br>
→[Selenium Resmi Sitesi](https://selenium-python.readthedocs.io/installation.html)

## Gerekli Kütüphanelerin ve MySQL’in Bağlantısı
```python
    #Projeye gerekli kütüphanelerin eklenmesi.
    from asyncio.windows_events import NULL
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    import mysql.connector
    import time
    
    
    #Yerel veri tabanı bağlantısı.
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "selenium_test"
    )
```
## Linkedin’de İş İlanı Araması

Aşağıdaki kodda bir class oluşturuyor ve Selenium sürücümüzün dosya konumunu belirtiyoruz. Bu konum sizin sürücüyü kurduğunuz yere göre değişiklik gösterecektir.

Oluşturduğumuz “search()” fonksiyonunda Linkedin iş arama sayfasına ulaşacak ve verdiğimiz parametreleri o sayfanın arama kutularına yazdıracağız.

Arama kutularında işlem yapmadan önce sayfamızın tamamen yüklenmesini istediğimiz için 1 saniyelik time.sleep() veriyoruz.
```python
    mycursor = db.cursor()
    
    driver = webdriver.Chrome("C:\Drivers\chromedriver")
    
    class Linkedin:
        def __init__(self, job, location):
            self.job = job
            self.location = location
        def search(self):
            driver.get("https://www.linkedin.com/jobs")
            driver.maximize_window()
            time.sleep(1)
            
            name_Input = driver.find_element("name", "keywords")
            name_Input.send_keys(self.job)
        
            location_Input = driver.find_element("name", "location")
            location_Input.clear()
            location_Input.send_keys(self.location)
            location_Input.send_keys(Keys.ENTER)
```
## İş Verilerini Çekme

Öncelikle sayfadaki tüm iş ilanlarının yüklenmesi için bir saniyelik duraklamalarla sayfayı en alta kadar indiriyoruz. Bunun nedeni, Linekdin’in Javascript tabanlı bir “yüklemek için kaydır” sistemi kullanmasıdır.

Sayfadaki tüm iş ilanları yüklendikten sonra XPATH ile ulaştığımız verileri sırasını kaybetmemek için indeks yardımıyla iş verilerini tek tek çekiyoruz.

Bundan ve bazı küçük hata işlemlerini de çözdükten sonra, verilerimizi MySQL veritabanımıza ekliyoruz.
```python
    def jobList(self):
            time.sleep(3)
    
            for x in range (10):
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(1)
            
            job_Titles = driver.find_elements(By.CSS_SELECTOR, ".jobs-search__results-list h3")
            job_Locations = driver.find_elements(By.CSS_SELECTOR, ".job-search-card__location")
            job_CompanyNames = driver.find_elements(By.CSS_SELECTOR, ".jobs-search__results-list h4")
            job_PostDates = []
                
            for x in range (len(job_Titles)):
                print(f"[{x+1}]:")
                print(job_Titles[x].text)
                print(job_Locations[x].text)
                print(job_CompanyNames[x].text)
                y = x + 1
                try:
                    a = driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{y}]/div/div[2]/div/time').text
                    job_PostDates.append(a)
                    print(driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{y}]/div/div[2]/div/time').text)
                except:       
                    b = (driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{y}]/a/div[2]/div/time').text)
                    job_PostDates.append(b)
                    print(driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{y}]/a/div[2]/div/time').text)
    
                print("\n")
                mycursor.execute(f"INSERT INTO jobs (title, location, company_name, post_date) VALUES ('{job_Titles[x].text}', '{job_Locations[x].text}', '{job_CompanyNames[x].text}', '{job_PostDates[x]}');")
                db.commit()  
```
      

## İş İlanlarına Tıklamak

Projenin kolay kısmı bitti, artık tıklama sistemimizi oluşturabiliriz. Aşağıdaki kod bloğunda sadece iş ilanlarına tıklayıp açıklama verilerini ve çalışma türü verilerini (Staj/Tam Zamanlı/Yarı Zamanlı vb.) çekiyoruz. Burada Linkedin’de bir sorun olduğunu belirtmekte fayda var. Webscraper bazı iş ilanlarına tıkladığında sağ taraftaki iş ilanı detaylarında zaman zaman boş beyaz bir ekran göreceksiniz. O beyaz ekranı aldığınızda, verilerinizi çekemezsiniz.

Bu kısımda “time.sleep()” kullanmanın sorunu çözeceğini düşünebilirsiniz fakat durum öyle değil. Bazen o beyaz ekran çıkınca beklemekle geçmiyor. Çözüm olarak bir önceki tıkladığınız iş ilanına tekrar tıklamanız ve ardından sorun yaşadığınız iş ilanına tekrar tıklayıp veriyi çekmeniz muhtemelen işe yarayacaktır. Olmazsa, botunuz veri yüklenene kadar bu işlemi tekrarlayacak ve bu boş veri sorununu çözecektir.
```python
        job_Type = NULL
        job_Description = NULL
        click_Count = 1
        
        for click in range (150):
            try:
                driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{click_Count}]/div/a').click()
            except:
                try:  
                    driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{click_Count}]/a').click()
                except:
                    break
                 
            
            j = 0
            while(True):
                time.sleep(0.5)
                try:
                    job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span').text
                except:   

                    try:
                        job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li/span').text                                   
                    except:
                        job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section/div/ul/li/span').text
                
                if(job_Type != ""):
                    try:
                        job_Description = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div').text
                    except:
                        job_Description = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div[2]/section/div').text
                    break
                j = j + 1
                if(j > 5):
                    try:
                        driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{click_Count-1}]/div/a').click()
                        time.sleep(1)
                        driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{click_Count}]/div/a').click()
                        
                        time.sleep(0.5)
                        try:
                            job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span').text
                        except:   

                            try:
                                job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li/span').text                                   
                            except:
                                job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section/div/ul/li/span').text
                        
                        if(job_Type != ""):
                            try:
                                job_Description = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div').text
                                if(job_Type != ""):
                                    break
                            except:
                                job_Description = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div[2]/section/div').text
                                break


                    except:
                        driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{click_Count-1}]/a').click() 
                        time.sleep(1)
                        driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{click_Count}]/div/a').click()
                        
                        time.sleep(0.5)
                        try:
                            job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span').text
                        except:   

                            try:
                                job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li/span').text                                   
                            except:
                                job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section/div/ul/li/span').text
                        
                        if(job_Type != ""):
                            try:
                                job_Description = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div').text
                            except:
                                job_Description = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div[2]/section/div').text
                            break
```                        
Bu kod bloğunda yaptığımız şey, iş ilanlarına tıklayıp açıklama ve çalışma tipi verilerini çekmeye çalışmaktır. Bunu abartabilir ve iş ilanının içinde belirtilen diğer veri türlerini çekebilirsiniz.

Şimdi bu yazının başında da belirttiğim gibi iş tipi verilerimizin (Staj / Tam Zamanlı vb.) sabit bir yeri ya da yolu yok. Bunlar, firmaların iş ilanlarını nasıl yayınladıklarına göre değişmektedir. Fakat merak etmeyin olabileceği 3–4 yer var ve bunlardan birisinde olacaktır. Aradığımız verileri bulana kadar bu yerleri tek tek kontrol ediyoruz.

## Çekilen Diğer Verileri Veri Tabanına Aktarmak

Verilerimizi veri tabanımıza ilk aktardığımızda açıklama ve iş tipimizi boş bırakmıştık, artık bu iki veriyi de veri tabanımıza aktarabiliriz.

İlan açıklamalarındaki çift tırnak(“) sembollerini tek tırnak(‘) ile değiştireceğiz, böylece SQL sorgumuzda sorunlara neden olmayacak.

Artık fonksiyonlarımızı çağırabilir ve Web Scraper’ımıza parametreler vererek kullanabiliriz. Fonksiyonları çağırmadan önce bir zamanlayıcı çağırıyor ve kod bitiminde kodumuzun çalışma süresini ölçüyoruz.

        
```python
        job_Description = job_Description.replace('"', "'")
                mycursor.execute(f'UPDATE jobs SET description = "{job_Description}" WHERE id = {click_Count};')
                db.commit() 
                mycursor.execute(f"UPDATE jobs SET job_type = '{job_Type}' WHERE id = {click_Count};")
                db.commit()         
                print(f"[{click_Count}]: {job_Type}")
                print(f"[{click_Count}]: {job_Description[:300]}...")
     
                click_Count += 1
    
    #Class'ımız burada sona eriyor.
    start = time.time() #Zaman sayacı başlatıyoruz.
    
    linkedin = Linkedin("C++", "istanbul") #Buraya aramak istediğiniz parametreleri girin.
    linkedin.search()
    linkedin.jobList() 
    
    end = time.time() #Zaman sayacını bitiriyoruz.
    print(f"\nExecution time: {end - start}") #Kodun çalışma süresini hesaplıyoruz.
```
Kodun tam versiyonuna ulaşmak için → [python-linkedin-webscraper.py](https://github.com/onderfatihkoca/python-linkedin-webscraper)

*Buraya kadar okuduğunuz için teşekkürler, bu benim ilk projelerimden birisiydi eğer eksik veya yanlış olduğunu düşündüğünüz bir kısım varsa geri dönüşlerinizi beklerim.*

**İletişim Bilgilerim:**<br>
Email: onderfatihkoca@gmail.com<br>
Linkedin: [Önder Fatih KOCA](https://www.linkedin.com/in/%C3%B6nder-fatih-koca-939999252/)<br>
GitHub: [onderfatihkoca](https://github.com/onderfatihkoca)

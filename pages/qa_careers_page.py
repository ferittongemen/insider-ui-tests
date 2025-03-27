def verify_job_listings(self):
    print("🧪 Sayfada QA + Istanbul job'ları var mı kontrol ediliyor...")

    # Scroll to the job list area to trigger potential lazy-load
    try:
        first_card = self.driver.find_element(By.XPATH, self.job_card_xpath)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", first_card)
        time.sleep(1)  # slight wait for content to stabilize
    except:
        print("⚠️ Job kartı bulunamadı, yine de devam ediliyor...")

    # Wait for job cards to be visible
    self.wait_for_job_cards_to_load()

    # Add short delay in JS to make sure all DOM elements are painted
    job_texts = self.driver.execute_script("""
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(Array.from(document.querySelectorAll(".position-list-item"))
                    .map(el => el.innerText.trim()));
            }, 100);
        });
    """)

    print(f"🔍 DOM'dan çekilen job kartı sayısı: {len(job_texts)}")

    valid_jobs = 0
    for i, text in enumerate(job_texts, 1):
        print(f"📋 JS Job {i}:\n{text}\n")
        lower_text = text.lower()
        if "quality assurance" in lower_text and "istanbul" in lower_text:
            print(f"✅ Job {i} UYUMLU: QA + Istanbul")
            valid_jobs += 1
        else:
            print(f"⚠️ Job {i} UYUMLU DEĞİL")

    print(f"🎯 Toplam geçerli iş ilanı: {valid_jobs}")
    return valid_jobs > 0

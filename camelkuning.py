from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import multiprocessing
import undetected_chromedriver as uc

auth_page = "https://academic.ui.ac.id/main/Authentication/"
home_page = "https://academic.ui.ac.id/main/Welcome/Index"
siak_page = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
user_agent = ""
def war(stop_event,num):
    while not stop_event.is_set():
        options = uc.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        # options.add_argument('--headless')  # Run Chrome in headless mode
        options.add_argument('--disable-gpu')
        options.add_argument(f'--user-agent={user_agent}')
        driver = uc.Chrome(options=options)
        driver_ua = driver.execute_script("return navigator.userAgent")
        print("User agent:")
        print(driver_ua)

        # use line below if you want more refresh in shorter time, might impact login time
        # maybe useful when your faculty goes to war on the same time as other faculty
        # driver.set_page_load_timeout(5)

        username = ""
        password = ""
        display_name = ""
        common_matkul = ""
        chosen_matkul = ""

        creds = [
            "ezar.akhdan", #Username
            "@1Dewi1@", #Password
            "EZAR AKHDAN SHADA SURAHMAN", #SIAK Display name
            "DDP", #Common Matkul
            "DDP", #Chosen Matkul
        ]

        username = creds[0]
        password = creds[1]
        display_name = creds[2]
        common_matkul = creds[3]
        chosen_matkul = creds[4]
        
        print_bot("====INFO AKUN====",num)
        print_bot(f"Username: {username}",num)
        print_bot(f"Password: {password}",num)
        print_bot(f"Display name: {display_name}",num)
        print_bot(f"Common matkul: {common_matkul}",num)
        print_bot(f"Chosen matkul: {chosen_matkul}",num)

        matkul={
            "BerpikirKompu01" : "756280-2" #Nama Matkul (spasi) Kode-SKS
        }

        print_bot("====INFO MATKUL====",num)
        print_bot("Matkul Dipilih:",num)
        for name, code in matkul.items():
            print_bot(f"{name} {code}",num)

        login(driver, username, password, display_name,num)
        
        while not stop_event.is_set():
            try:
                
                driver.get(siak_page)
                

                if ("Anda tidak dapat mengisi IRS" in driver.page_source):
                    print_bot("SIAK-War belum dimulai, mencoba ulang...",num)
                    raise NoSuchElementException
                
                # Keep this up to date
                if (
                    "Pesan untuk pembimbing akademis" in driver.page_source
                    or common_matkul in driver.page_source
                    or chosen_matkul in driver.page_source
                ):
                    print_bot("Masuk ke halaman SIAK-War!")
                    break

                raise NoSuchElementException

            except NoSuchElementException:
                
                logout(driver,num)
                
                login(driver, username, password, display_name,num)

        while not stop_event.is_set():
            try:
                for name, code in matkul.items():
                    try:
                        radio_button = driver.find_element(By.XPATH, '//input[@value="{}"]'.format(code))
                        
                        if(not radio_button.is_selected()):
                            radio_button.click()
                            print_bot(f"{name} terpilih! (code: {code})",num)
                        else:
                            print_bot(f"{name} sudah dipilih! (code: {code})",num)

                    except NoSuchElementException:
                        print_bot(f"Matkul {name} tidak ditemukan! (code: {code})",num)
                        continue

                driver.find_element(By.NAME, 'submit').click()

                if ("IRS berhasil tersimpan!" in driver.page_source or "Daftar IRS" in driver.page_source):
                    for name, code in matkul.items():
                        if (name not in driver.page_source):
                            print_bot(f"Matkul {name} tidak ditemukan! (code: {code})",num)
                            print_bot("Retrying...",num)
                            raise NoSuchElementException
                    break

                raise NoSuchElementException

            except NoSuchElementException:
                
                driver.get(siak_page)

        print_bot("SIAK-War selesai....",num)
        stop_event.set()
        driver.close()

def login(driver, username, password, display_name,num):
    print_bot("Mencoba Login...",num)

    while True:
        try:
            
            driver.get(auth_page)
            
            element = driver.find_element(By.ID, "u")
            element.send_keys(username)
            element = driver.find_element(By.NAME, "p")
            element.send_keys(password)
            
            element.send_keys(Keys.RETURN)

        except Exception as e:
            if ("Logout Counter" in driver.page_source or display_name in driver.page_source):
                print_bot("Logged in!",num)
                break

            continue

        try:
            
            driver.get(home_page)
            
            if ("Logout Counter" in driver.page_source or display_name in driver.page_source):
                print_bot("Logged in!",num)
                break
            raise Exception
        except:
            continue
        
def logout(driver,num):
    print_bot("Logging out...",num)

    while True:
        try:
            
            driver.get(home_page)
            
            driver.find_element(By.PARTIAL_LINK_TEXT, 'Logout').click()
        except:
            try:
                driver.find_element(By.ID, "u")
                print_bot("Logged out!",num)
                break
            except:
                continue

        try:
            
            driver.get(auth_page)
            driver.find_element(By.ID, "u")
            print_bot("Logged out!",num)
            break
        except:
            continue

def main():
    processes = []
    stop_event = multiprocessing.Event()
    num_instances = int(input("Masukkan jumlah bot: "))  # Number of instances you want to run

    try:
        for i in range(num_instances):
            p = multiprocessing.Process(target=war, args=(stop_event,i+1))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("Mengakhiri bot...")
        stop_event.set()
        for p in processes:
            p.terminate()
            p.join()
        print("Semua bot telah musnah.")

def print_bot(message,bot_num):
    print(f"Bot {bot_num}: {message}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    print("==================")
    print("|| Camel Kuning ||")
    print("==================")
    print("ACAK ACAK SIAKNG")
    main()
    input("Press enter to exit.")
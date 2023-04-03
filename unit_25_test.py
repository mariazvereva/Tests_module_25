import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver




@pytest.fixture(autouse=True)
def testing_authorization():
   pytest.driver = webdriver.Chrome('C:\skillfactory\Driver\chromedriver.exe')

   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   field_email = pytest.driver.find_element(By.ID, "email")
   field_email.clear()
   field_email.send_keys("mariachizhova@mail.ru")

   field_pass = pytest.driver.find_element(By.ID, "pass")
   field_pass.clear()
   field_pass.send_keys("04082017")

   btn_submit = pytest.driver.find_element(By.XPATH, "//button[@type='submit']")
   btn_submit.click()

   yield

   pytest.driver.quit()

def test_all_pets_presents_on_page():
   '''Проверяем, что на странице со списком питомцев пользователя присутствуют все питомцы'''

   btn_my_pets = pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы")
   btn_my_pets.click()

   wait = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
   #явное ожидание появления информации о профиле пользователя

   pets_data = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")
   number_of_pets_statistic = pets_data[0].text.split('\n')
   number_of_pets_statistic = number_of_pets_statistic[1].split(' ')
   number_of_pets_statistic = int(number_of_pets_statistic[1])

   number_of_pets_visible = len(pytest.driver.find_elements(By.XPATH, "//th[@scope='row']"))

   assert number_of_pets_statistic == number_of_pets_visible

def test_pets_have_photos():
   '''Проверяем, что хотя бы у половины питомцев есть фото'''

   btn_my_pets = pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы")
   btn_my_pets.click()

   wait = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//th/img')))

   pets_photos=pytest.driver.find_elements(By.XPATH, '//th/img')

   photos=0
   for i in range(len(pets_photos)):
      if pets_photos[i].get_attribute('src') !='':
         photos+=1

   pets_data = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")
   number_of_pets_statistic = pets_data[0].text.split('\n')
   number_of_pets_statistic = number_of_pets_statistic[1].split(' ')
   half_number_of_pets_statistic = (int(number_of_pets_statistic[1]))*0.5
   #умножаю на 0.5 для вычисления количетсва половины питомцев

   assert photos>=half_number_of_pets_statistic


def test_pets_have_name_age_breed():
   '''Проверяем,что у всех питомцев есть имя, возраст и порода.'''

   btn_my_pets = pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы")
   btn_my_pets.click()

   wait = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table')))

   name=pytest.driver.find_elements(By.XPATH, '//table[1]/tbody[1]/tr/td[1]')
   names=0
   for i in range(len(name)):
      if name[i].text != '':
         names += 1

   age=pytest.driver.find_elements(By.XPATH, '//table[1]/tbody[1]/tr/td[3]')
   ages=0
   for i in range(len(age)):
      if age[i].text != '':
         ages += 1

   breed=pytest.driver.find_elements(By.XPATH, '//table[1]/tbody[1]/tr/td[2]')
   breeds=0
   for i in range(len(breed)):
      if breed[i].text != '':
         breeds += 1

   assert names==ages==breeds



def test_pets_do_not_have_duplicate_names():
   '''Проверяем, что у всех питомцев разные имена.'''

   btn_my_pets = pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы")
   btn_my_pets.click()

   wait = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table')))

   name=pytest.driver.find_elements(By.XPATH, '//table[1]/tbody[1]/tr/td[1]')

   names=[]
   for i in range(len(name)):
      names.append(name[i].text)


   duplicate_names=0
   for i in range(len(names)):
      if names.count(names[i]) > 1:
         duplicate_names += 1


   assert duplicate_names == 0



def test_no_duplicate_pets():
   '''Проверяем, что в списке нет повторяющихся питомцев.'''

   btn_my_pets = pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы")
   btn_my_pets.click()

   wait = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table')))

   name=pytest.driver.find_elements(By.XPATH, '//table[1]/tbody[1]/tr/td[1]')
   age = pytest.driver.find_elements(By.XPATH, '//table[1]/tbody[1]/tr/td[3]')
   breed = pytest.driver.find_elements(By.XPATH, '//table[1]/tbody[1]/tr/td[2]')

   pets_data=[]
   for i in range(len(name)):
      pets_data.append([name[i].text, age[i].text, breed[i].text])

   duplicate_pets = 0
   for i in range(len(pets_data)):
      if pets_data.count(pets_data[i]) > 1:
         duplicate_pets += 1

   assert duplicate_pets == 0








from selenium.webdriver.common.by import By
import pytest
from selenium import webdriver

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:\skillfactory\Driver\chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()


def test_show_my_pets():
   # Устанавливаем неявное ожидание
   pytest.driver.implicitly_wait(5)

   pytest.driver.find_element(By.ID, 'email').send_keys('mariachizhova@mail.ru')

   pytest.driver.find_element(By.ID, 'pass').send_keys('04082017')

   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   pytest.driver.implicitly_wait(5)

   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0
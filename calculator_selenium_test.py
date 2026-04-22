from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import unittest
import time

class CalculatorTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.base_url = "file:///c:/Users/28983/Desktop/软件测试/Performance%20Testing%20and%20Automated%20Testing%20Script/calculator.html"
        cls.wait = WebDriverWait(cls.driver, 10)
        
    def setUp(self):
        self.driver.get(self.base_url)
        time.sleep(1)
    
    def test_01_page_title(self):
        print("\n【测试用例1】验证页面标题")
        expected_title = "简单计算器"
        actual_title = self.driver.title
        self.assertEqual(expected_title, actual_title, f"标题不匹配：期望'{expected_title}'，实际'{actual_title}'")
        print("✓ 页面标题验证通过")
    
    def test_02_display_exists(self):
        print("\n【测试用例2】验证显示屏存在")
        display = self.driver.find_element(By.ID, "display")
        self.assertIsNotNone(display)
        print("✓ 显示屏元素存在")
    
    def test_03_buttons_exist(self):
        print("\n【测试用例3】验证所有按钮存在")
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        button_count = len(buttons)
        self.assertGreaterEqual(button_count, 16, f"按钮数量不足，期望至少16个，实际{button_count}个")
        print(f"✓ 所有{button_count}个按钮都存在")
    
    def test_04_addition(self):
        print("\n【测试用例4】测试加法运算: 5 + 3 = 8")
        self._click_button('5')
        self._click_button('+')
        self._click_button('3')
        self._click_button('=')
        
        result = self._get_display_value()
        self.assertEqual(result, '8', f"加法结果错误：期望'8'，实际'{result}'")
        print(f"✓ 加法测试通过：5 + 3 = {result}")
    
    def test_05_subtraction(self):
        print("\n【测试用例5】测试减法运算: 9 - 4 = 5")
        self._click_button('9')
        self._click_button('-')
        self._click_button('4')
        self._click_button('=')
        
        result = self._get_display_value()
        self.assertEqual(result, '5', f"减法结果错误：期望'5'，实际'{result}'")
        print(f"✓ 减法测试通过：9 - 4 = {result}")
    
    def test_06_multiplication(self):
        print("\n【测试用例6】测试乘法运算: 6 * 7 = 42")
        self._click_button('6')
        self._click_button('*')
        self._click_button('7')
        self._click_button('=')
        
        result = self._get_display_value()
        self.assertEqual(result, '42', f"乘法结果错误：期望'42'，实际'{result}'")
        print(f"✓ 乘法测试通过：6 × 7 = {result}")
    
    def test_07_division(self):
        print("\n【测试用例7】测试除法运算: 15 / 3 = 5")
        self._click_button('1')
        self._click_button('5')
        self._click_button('/')
        self._click_button('3')
        self._click_button('=')
        
        result = self._get_display_value()
        self.assertEqual(result, '5', f"除法结果错误：期望'5'，实际'{result}'")
        print(f"✓ 除法测试通过：15 ÷ 3 = {result}")
    
    def test_08_decimal_operation(self):
        print("\n【测试用例8】测试小数运算: 2.5 + 1.5 = 4")
        self._click_button('2')
        self._click_button('.')
        self._click_button('5')
        self._click_button('+')
        self._click_button('1')
        self._click_button('.')
        self._click_button('5')
        self._click_button('=')
        
        result = self._get_display_value()
        self.assertEqual(result, '4', f"小数运算错误：期望'4'，实际'{result}'")
        print(f"✓ 小数运算测试通过：2.5 + 1.5 = {result}")
    
    def test_09_clear_function(self):
        print("\n【测试用例9】测试清除功能")
        self._click_button('9')
        self._click_button('+')
        self._click_button('8')
        self._click_button('C')
        
        result = self._get_display_value()
        self.assertEqual(result, '', f"清除后显示屏应为空，实际显示'{result}'")
        print("✓ 清除功能测试通过")
    
    def test_10_delete_function(self):
        print("\n【测试用例10】测试删除最后一位功能")
        self._click_button('1')
        self._click_button('2')
        self._click_button('3')
        self._click_button('←')
        
        result = self._get_display_value()
        self.assertEqual(result, '12', f"删除后应显示'12'，实际显示'{result}'")
        print(f"✓ 删除功能测试通过：123 → {result}")
    
    def test_11_complex_calculation(self):
        print("\n【测试用例11】测试复杂运算: (10 + 5) * 2 - 8 = 12")
        self._click_button('1')
        self._click_button('0')
        self._click_button('+')
        self._click_button('5')
        self._click_button('*')
        self._click_button('2')
        self._click_button('-')
        self._click_button('8')
        self._click_button('=')
        
        result = self._get_display_value()
        self.assertEqual(result, '12', f"复杂运算错误：期望'12'，实际'{result}'")
        print(f"✓ 复杂运算测试通过：(10+5)×2-8 = {result}")
    
    def test_12_division_by_zero(self):
        print("\n【测试用例12】测试除以零的错误处理")
        self._click_button('5')
        self._click_button('/')
        self._click_button('0')
        self._click_button('=')
        
        result = self._get_display_value()
        self.assertIn(result, ['错误', 'Infinity'], 
                       f"除以零时应显示错误或Infinity，实际显示'{result}'")
        print(f"✓ 除以零错误处理测试通过：显示'{result}'")
    
    def _click_button(self, text):
        try:
            if text == '=':
                button = self.driver.find_element(By.XPATH, "//button[text()='=']")
            elif text == 'C':
                button = self.driver.find_element(By.XPATH, "//button[text()='C']")
            elif text == '←':
                button = self.driver.find_element(By.XPATH, "//button[text()='←']")
            elif text == '+':
                button = self.driver.find_element(By.XPATH, "//button[text()='+']")
            elif text == '-':
                button = self.driver.find_element(By.XPATH, "//button[text()='-']")
            elif text == '*':
                button = self.driver.find_element(By.XPATH, "//button[text()='×']")
            elif text == '/':
                button = self.driver.find_element(By.XPATH, "//button[text()='÷']")
            else:
                button = self.driver.find_element(By.XPATH, f"//button[text()='{text}']")
            
            button.click()
            time.sleep(0.2)
            
        except NoSuchElementException:
            raise Exception(f"未找到按钮：{text}")
    
    def _get_display_value(self):
        display = self.driver.find_element(By.ID, "display")
        return display.get_attribute("value")
    
    @classmethod
    def tearDownClass(cls):
        input("按Enter键关闭浏览器...")
        cls.driver.quit()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CalculatorTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"总测试数：{result.testsRun}")
    print(f"成功：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败：{len(result.failures)}")
    print(f"错误：{len(result.errors)}")
    print("="*60)
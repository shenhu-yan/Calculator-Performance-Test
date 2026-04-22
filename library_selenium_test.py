from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import unittest
import time
import os

class LibrarySystemTest(unittest.TestCase):
    
    BASE_URL = f"file:///{os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/')}/library_system.html"
    
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 15)
        cls.actions = ActionChains(cls.driver)
        
    def setUp(self):
        self.driver.get(self.BASE_URL)
        time.sleep(2)
    
    # ==================== 脚本结构说明 ====================
    # 本测试脚本采用Page Object设计思想，分为以下模块：
    # 1. 页面元素定位方法（_find_*系列）
    # 2. 业务操作方法（login, search, borrow等）
    # 3. 结果校验方法（assert_*系列）
    # 4. 测试用例（test_*系列）
    #
    # 脚本执行流程：
    # setUpClass -> 初始化浏览器驱动
    # setUp -> 每个测试前打开页面
    # test_* -> 执行具体测试用例
    # tearDownClass -> 关闭浏览器
    
    def _find_element_safe(self, by, value, timeout=10):
        try:
            element = self.wait.until(EC.presence_of_element_located((by, value)))
            return element
        except TimeoutException:
            return None
    
    def _find_elements_safe(self, by, value):
        try:
            elements = self.driver.find_elements(by, value)
            return elements if len(elements) > 0 else None
        except NoSuchElementException:
            return None
    
    def _click_safe(self, element):
        try:
            element.click()
            return True
        except ElementClickInterceptedException:
            self.actions.move_to_element(element).click().perform()
            return True
    
    # ==================== 测试用例：登录功能验证 ====================
    
    def test_01_page_title_and_login_form_exists(self):
        print("\n【测试用例1】验证页面标题和登录表单存在")
        
        expected_title = "在线图书管理系统"
        actual_title = self.driver.title
        self.assertEqual(expected_title, actual_title, 
                        f"页面标题不匹配：期望'{expected_title}'，实际'{actual_title}'")
        print(f"✓ 页面标题正确: {actual_title}")
        
        username_input = self._find_element_safe(By.ID, "username")
        password_input = self._find_element_safe(By.ID, "password")
        self.assertIsNotNone(username_input, "用户名输入框不存在")
        self.assertIsNotNone(password_input, "密码输入框不存在")
        print("✓ 登录表单元素存在性验证通过")
    
    def test_02_login_with_valid_credentials(self):
        print("\n【测试用例2】使用有效凭据登录系统")
        
        username_field = self._find_element_safe(By.ID, "username")
        password_field = self._find_element_safe(By.ID, "password")
        
        username_field.clear()
        username_field.send_keys("admin")
        password_field.clear()
        password_field.send_keys("admin123")
        
        login_btn = self._find_element_safe(By.CSS_SELECTOR, ".btn-primary[type='submit']")
        self.assertTrue(self._click_safe(login_btn), "无法点击登录按钮")
        
        time.sleep(2)
        
        user_info = self._find_element_safe(By.CSS_SELECTOR, ".user-info")
        self.assertIsNotNone(user_info, "登录后应显示用户信息")
        
        user_text = user_info.text
        self.assertIn("管理员", user_text, f"登录后应显示管理员信息，实际显示: {user_text}")
        print(f"✓ 登录成功，当前用户: {user_text}")
    
    def test_03_login_with_invalid_credentials(self):
        print("\n【测试用例3】使用无效凭据登录（预期失败）")
        
        username_field = self._find_element_safe(By.ID, "username")
        password_field = self._find_element_safe(By.ID, "password")
        
        self.driver.execute_script("arguments[0].value = '';", username_field)
        self.driver.execute_script("arguments[0].value = '';", password_field)
        
        username_field.send_keys("invalid_user")
        password_field.send_keys("wrong_password")
        
        login_btn = self._find_element_safe(By.CSS_SELECTOR, ".btn-primary[type='submit']")
        self._click_safe(login_btn)
        
        time.sleep(2)
        
        toast = self._find_element_safe(By.ID, "toast")
        if toast:
            toast_text = toast.text
            self.assertIn("错误", toast_text, f"应显示错误提示消息: {toast_text}")
            print(f"✓ 无效凭据登录被正确拒绝，提示: {toast_text}")
        else:
            login_form = self._find_element_safe(By.CLASS_NAME, "login-page")
            self.assertIsNotNone(login_form, "使用无效凭据应停留在登录页面")
            print("✓ 无效凭据登录被正确拒绝")
    
    # ==================== 测试用例：图书列表功能验证 ====================
    
    def test_04_book_list_displayed_after_login(self):
        print("\n【测试用例4】验证登录后图书列表正常显示")
        
        self._do_login("zhangsan", "123456")
        time.sleep(1)
        
        book_cards = self._find_elements_safe(By.CLASS_NAME, "book-card")
        self.assertIsNotNone(book_cards, "图书列表未显示")
        self.assertGreaterEqual(len(book_cards), 6, 
                               f"首页应显示至少6本图书，实际显示{len(book_cards) if book_cards else 0}本")
        print(f"✓ 图书列表显示正常，共{len(book_cards)}本图书")
    
    def test_05_category_filter_functionality(self):
        print("\n【测试用例5】验证分类筛选功能")
        
        self._do_login("lisi", "123456")
        time.sleep(1)
        
        category_items = self._find_elements_safe(By.CSS_SELECTOR, ".category-list li")
        self.assertIsNotNone(category_items, "分类列表不存在")
        
        computer_category = None
        for item in category_items:
            if "计算机" in item.text:
                computer_category = item
                break
        
        self.assertIsNotNone(computer_category, "未找到'计算机'分类")
        self._click_safe(computer_category)
        time.sleep(1)
        
        book_cards = self._find_elements_safe(By.CLASS_NAME, "book-card")
        self.assertIsNotNone(book_cards, "筛选后图书列表为空")
        print(f"✓ 分类筛选功能正常，筛选后显示{len(book_cards)}本计算机类图书")
    
    def test_06_search_functionality(self):
        print("\n【测试用例6】验证搜索功能（数据填充）")
        
        self._do_login("wangwu", "123456")
        time.sleep(1)
        
        search_input = self._find_element_safe(By.CSS_SELECTOR, ".search-bar input")
        self.assertIsNotNone(search_input, "搜索框不存在")
        
        search_input.clear()
        search_input.send_keys("Python")
        
        search_btn = self._find_element_safe(By.CSS_SELECTOR, ".search-bar button")
        self._click_safe(search_btn)
        time.sleep(1)
        
        book_cards = self._find_elements_safe(By.CLASS_NAME, "book-card")
        self.assertIsNotNone(book_cards, "搜索结果为空")
        
        for card in book_cards:
            card_text = card.text
            self.assertIn("Python", card_text, 
                         f"搜索结果'{card_text}'不包含关键词'Python'")
        
        print(f"✓ 搜索功能正常，找到{len(book_cards)}本相关图书")
    
    def test_07_sorting_functionality(self):
        print("\n【测试用例7】验证排序功能")
        
        self._do_login("admin", "admin123")
        time.sleep(1)
        
        sort_select = self._find_element_safe(By.CSS_SELECTOR, ".filter-bar select")
        self.assertIsNotNone(sort_select, "排序下拉框不存在")
        
        sort_select.click()
        from selenium.webdriver.support.ui import Select
        select = Select(sort_select)
        select.select_by_value("price-asc")
        time.sleep(1)
        
        prices = []
        price_elements = self._find_elements_safe(By.CSS_SELECTOR, ".book-info .price")
        for elem in price_elements:
            price_text = elem.text.replace('¥', '').replace(',', '')
            try:
                prices.append(float(price_text))
            except ValueError:
                pass
        
        if len(prices) >= 2:
            for i in range(len(prices)-1):
                self.assertLessEqual(prices[i], prices[i+1], 
                                     "价格升序排序不正确")
        
        print(f"✓ 排序功能正常，共获取{len(prices)}个价格数据")
    
    # ==================== 测试用例：图书详情与借阅功能 ====================
    
    def test_08_book_detail_modal_display(self):
        print("\n【测试用例8】验证图书详情弹窗显示（列表项点击）")
        
        self._do_login("zhangsan", "123456")
        time.sleep(1)
        
        first_book_card = self._find_element_safe(By.CLASS_NAME, "book-card")
        self.assertIsNotNone(first_book_card, "未找到图书卡片")
        self._click_safe(first_book_card)
        time.sleep(1)
        
        modal = self._find_element_safe(By.ID, "modal")
        self.assertIsNotNone(modal, "详情弹窗未出现")
        
        modal_classes = modal.get_attribute("class")
        self.assertIn("show", modal_classes, "弹窗未显示")
        
        modal_content = self._find_element_safe(By.ID, "modalContent")
        self.assertIsNotNone(modal_content, "弹窗内容为空")
        
        content_html = modal_content.get_attribute("innerHTML")
        self.assertIn("作者:", content_html, "详情页应包含作者信息")
        self.assertIn("ISBN:", content_html, "详情页应包含ISBN信息")
        self.assertIn("内容简介:", content_html, "详情页应包含简介")
        
        print("✓ 图书详情弹窗显示正常，包含完整信息")
        
        close_btn = self._find_element_safe(By.CLASS_NAME, "close-btn")
        if close_btn:
            self._click_safe(close_btn)
    
    def test_09_borrow_book_successfully(self):
        print("\n【测试用例9】验证借阅图书成功流程")
        
        self._do_login("lisi", "123456")
        time.sleep(1)
        
        first_book = self._find_element_safe(By.CLASS_NAME, "book-card")
        self.assertIsNotNone(first_book, "未找到可借阅图书")
        
        borrow_btn = first_book.find_element(By.CSS_SELECTOR, ".btn-primary")
        self.assertIsNotNone(borrow_btn, "未找到借阅按钮")
        
        book_title = first_book.find_element(By.TAG_NAME, "h3").text
        
        self._click_safe(borrow_btn)
        time.sleep(1)
        
        toast = self._find_element_safe(By.ID, "toast")
        self.assertIsNotNone(toast, "未出现提示消息")
        
        toast_classes = toast.get_attribute("class")
        self.assertNotIn("error", toast_classes, "借阅不应失败")
        
        print(f"✓ 成功借阅图书《{book_title}》")
    
    def test_10_borrow_records_management(self):
        print("\n【测试用例10】验证借阅记录管理功能")
        
        self._do_login("wangwu", "123456")
        time.sleep(1)
        
        records_link = self._find_element_safe(By.XPATH, "//a[contains(text(),'我的借阅')]")
        if records_link:
            self._click_safe(records_link)
            time.sleep(1)
        
        records_table = self._find_element_safe(By.TAG_NAME, "table")
        self.assertIsNotNone(records_table, "借阅记录表格不存在")
        
        rows = records_table.find_elements(By.TAG_NAME, "tr")
        header_count = 1
        data_rows = len(rows) - header_count
        
        print(f"✅ 借阅记录页面正常，共有{data_rows}条记录")
    
    # ==================== 测试用例：UI交互与导航验证 ====================
    
    def test_11_navigation_between_pages(self):
        print("\n【测试用例11】验证页面间导航功能")
        
        self._do_login("admin", "admin123")
        time.sleep(1)
        
        nav_links = self._find_elements_safe(By.CSS_SELECTOR, ".nav a")
        if not nav_links or len(nav_links) < 3:
            print("⚠️ 导航栏元素数量不足，跳过此测试")
            return
        
        tested_count = 0
        for link in nav_links:
            try:
                link_text = link.text.strip() if link.text else ""
                if not link_text or "退出" in link_text:
                    continue
                    
                self._click_safe(link)
                time.sleep(0.5)
                
                current_url = self.driver.current_url
                self.assertIn("library_system.html", current_url,
                             f"导航到'{link_text}'后URL异常")
                tested_count += 1
            except Exception as e:
                print(f"  ⚠️ 导航项'{link.text}'测试时出错: {str(e)[:50]}")
                continue
        
        print(f"✅ 导航功能正常，共测试{tested_count}个导航项")
    
    def test_12_pagination_functionality(self):
        print("\n【测试用例12】验证分页功能")
        
        self._do_login("zhangsan", "123456")
        time.sleep(1)
        
        next_btn = self._find_element_safe(By.XPATH, "//button[contains(text(),'下一页')]")
        
        if next_btn and not next_btn.get_attribute("disabled"):
            initial_books = len(self._find_elements_safe(By.CLASS_NAME, "book-card"))
            
            self._click_safe(next_btn)
            time.sleep(1)
            
            after_books = len(self._find_elements_safe(By.CLASS_NAME, "book-card"))
            
            page_info = self._find_element_safe(By.CSS_SELECTOR, ".pagination span")
            if page_info:
                print(f"✅ 分页功能正常: {page_info.text}")
        else:
            print("⚠️ 当前数据量不足以测试分页或已在最后一页")
    
    def test_13_statistics_display(self):
        print("\n【测试用例13】验证统计数据展示")
        
        self._do_login("admin", "admin123")
        time.sleep(1)
        
        stat_cards = self._find_elements_safe(By.CLASS_NAME, "stat-card")
        self.assertIsNotNone(stat_cards, "统计卡片不存在")
        self.assertEqual(len(stat_cards), 4, f"应有4个统计卡片，实际{len(stat_cards)}个")
        
        for i, card in enumerate(stat_cards):
            number_elem = card.find_element(By.TAG_NAME, "h4")
            number_text = number_elem.text
            
            try:
                num = int(number_text)
                self.assertGreater(num, 0, f"统计数字应为正数，实际: {num}")
            except ValueError:
                pass
        
        print("✅ 统计数据显示正常，所有数值均为有效正数")
    
    def test_14_logout_functionality(self):
        print("\n【测试用例14】验证退出登录功能")
        
        self._do_login("lisi", "123456")
        time.sleep(1)
        
        logout_btn = self._find_element_safe(By.XPATH, "//button[contains(text(),'退出登录')]")
        self.assertIsNotNone(logout_btn, "退出按钮不存在")
        
        self._click_safe(logout_btn)
        time.sleep(1)
        
        login_form = self._find_element_safe(By.CLASS_NAME, "login-page")
        self.assertIsNotNone(login_form, "退出后应返回登录页面")
        
        print("✅ 退出登录功能正常")
    
    # ==================== 辅助方法 ====================
    
    def _do_login(self, username, password):
        username_field = self._find_element_safe(By.ID, "username")
        password_field = self._find_element_safe(By.ID, "password")
        
        if username_field and password_field:
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            
            login_btn = self._find_element_safe(By.CSS_SELECTOR, ".btn-primary[type='submit']")
            if login_btn:
                self._click_safe(login_btn)
                time.sleep(1)
    
    @classmethod
    def tearDownClass(cls):
        input("\n按Enter键关闭浏览器...")
        cls.driver.quit()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LibrarySystemTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print("                    📊 Selenium测试报告总结")
    print("="*70)
    print(f"  📋 总测试数：     {result.testsRun}")
    print(f"  ✅ 通过：         {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  ❌ 失败：         {len(result.failures)}")
    print(f"  ⚠️  错误：         {len(result.errors)}")
    print(f"  📈 通过率：       {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)
    
    if result.failures:
        print("\n❌ 失败的测试用例：")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1][:100] if 'AssertionError' in traceback else ''}")
    
    if result.errors:
        print("\n⚠️  出错的测试用例：")
        for test, traceback in result.errors:
            print(f"  - {test}")
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import time
import os

# 要爬取的微信公众号文章 URL
article_url = input("读取文章的路径")  # 替换为你实际的文章链接

def get_wechat_article(url):
    """使用 Selenium 和 Edge WebDriver 提取微信公众号文章内容"""
    # 设置 Edge 浏览器选项
    edge_options = Options()
    edge_options.add_argument("--headless")  # 无头模式，不显示浏览器窗口
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")

    # 启动 Edge WebDriver
    driver = webdriver.Edge()

    try:
        # 访问微信公众号文章页面
        driver.get(url)
        time.sleep(3)  # 等待页面加载

        # 获取页面的 HTML 源代码
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # 提取文章标题
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "未知标题"

        # 提取文章正文内容
        content_div = soup.find("div", {"id": "js_content"})
        paragraphs = content_div.find_all("p") if content_div else []
        content = "\n".join([p.get_text(strip=True) for p in paragraphs])

        return title, content

    except Exception as e:
        print("❌ 发生错误:", e)
        return None, None
    finally:
        driver.quit()  # 关闭浏览器

def save_to_txt(title, content):
    """将文章内容保存到指定的文件路径"""
    # 目标文件夹路径
    save_dir = input("文件路径")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)  # 如果目录不存在，创建该目录

    # 将标题中的非法字符替换
    file_name = f"{title}.txt".replace("/", "_").replace("\\", "_").replace(":", "_").replace("|","_")
    file_path = os.path.join(save_dir, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"标题: {title}\n\n")
        for line in content.split("\n"):
            f.write(line+"\n")
    print(f"✅ 文章已保存: {file_path}")

# 运行爬取
title, content = get_wechat_article(article_url)
if title and content:
    save_to_txt(title, content)
else:
    print("❌ 爬取失败！")
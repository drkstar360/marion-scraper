# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
#
# process = CrawlerProcess(get_project_settings())
#
# # 'followall' is the name of one of the spiders of the project.
# process.crawl("marionfl")
# process.start()

from scrapy import cmdline
cmdline.execute("scrapy crawl marionfl".split())
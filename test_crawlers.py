
import pytest
from crawlers import CrawlerTribunal

def test_get_1degree():
    crawler_tjal = CrawlerTribunal('tjal')
    result = crawler_tjal.get_1degree('0721604-73.2022.8.02.0001')
    assert isinstance(result, dict)


def test_check_2grau():
    crawler_tjal = CrawlerTribunal('tjal')
    crawler_tjce = CrawlerTribunal('tjce')
    should_get_2grau1 = crawler_tjal.check_2grau('0721604-73.2022.8.02.0001')
    should_get_2grau2 = crawler_tjce.check_2grau('0721604-73.2022.8.02.0001')  # número do TJAL
    should_get_2grau3 = crawler_tjce.check_2grau('0170599-97.2018.8.06.0001')
    assert should_get_2grau1 == True
    assert should_get_2grau2 == False
    assert should_get_2grau3 == True
    


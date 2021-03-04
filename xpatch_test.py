import lxml.html as html
import requests
from io import StringIO

response = requests.get('https://www.starwars.com/news/15-star-wars-quotes-to-use-in-everyday-life')
tree = html.parse(StringIO(response.content.decode()))

print(tree.xpath('//p/strong/text()'))
print(tree.xpath('//p'))
print(tree.xpath('//p[contains(text(),"Use")]/text()'))
print(tree.xpath('//img[contains(@class, "alignnone")]/@src'))
print(tree.xpath('//header[@class="article-header"]/descendant::node()/text()'))
print(tree.xpath('//li[@class="related-post"]/a[1]/@href'))



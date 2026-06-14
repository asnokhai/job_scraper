import httpx

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
    "Referer": "https://www.bmwgroup.jobs/en/jobfinder.html",
    "X-Requested-With": "XMLHttpRequest",
}

COOKIES = {
    "bm_sv": "3C70955017869C0A2B46B582120D8427~YAAQBPsQYKliroyeAQAA8dNbxgBrHxxGnLUOPmSbbEP4ceyeVvDrJPLbqJpHmQRx9XTHDenqWVAuHMWM1iKTo6KwyWaSA0RkzwPsx8yh9dNf8W4ovgdAeKfmnnW2RCi/aDaLS2Vx1mgsZktqsc7zr+tsXRIMW0glRYGmp15/irZq6zSyMyDLgF6HapSWByddaJ1ZjSD6HJgyM7a+vhGS/Mofxiocx5Qqhn/vJO7Yg0R5VjEJ8z9fUv2TXc/uMxabSrhdQQ==~1",
    "ak_bmsc": "318AEF9EA9903EF8D93F418746D002F2~000000000000000000000000000000~YAAQVQcQAkGnWbieAQAAQnr9xQD9nSSqpIedpUJWmJtPOevDYUFqmOhIvEzPL1yzL1QrD+QAr+PwTQBI4JzV7dZLIwpgDwQy6RnPxZC9fWBBTb3ZtErIcCFgM5jCMDjAY+X9xxBlRQ56OSIO9//pz1gTwzsZCBXr+n+GAlHjeXczqoDSI5KhLeqQhvQhjvvS1LrQdGURkJmHCsQ+EDc76WzNAdSNoIAAaX+6ZDKkkjDmNpTgWXk7V0r1NAb9NGwu+4gUw9Tm1SgLiWACzywaOKxjwG8pOqq7qp71Cbg87EUh3ITkNGwZc//9MXBbVkx33bzki3/sjcchm6If5zO8LTteiCxkMs8WshG76V9Ke5Y53FYR11torpu7IweZ7N6qsyDKVbYTnkbi1nSAD9aXC3TegLjWNKjkHFe93suF7VyMaQxaqV+omOIMON0eAojyLErBbNRA4a6DUzqu0pvRNV9UIrwxMItvEyggTrscWypR8PMHvrBq7heO0MQ=",
}

url = "https://www.bmwgroup.jobs/en/_jcr_content/main/layoutcontainer_5337/jobfinder30.jobfinder_table.content.html"
params = {"textSearch": "", "rowIndex": 0, "blockCount": 5}
r = httpx.get(url, headers=HEADERS, params=params, cookies=COOKIES)
print(r.text)
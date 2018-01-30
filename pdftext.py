import pdfkit

config = pdfkit.configuration(wkhtmltopdf="C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe")
url = 'http://permit.mep.gov.cn/permitExt/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid=32402cc58cc64f318c70bf67dce03975'
downloc = 'D:\何方辉\排污许可\爬虫练习\out2.pdf'
pdfkit.from_url(url, downloc,configuration = config)
#pdfkit.from_file('test.html', 'out.pdf',configuration = config)
#pdfkit.from_string('Hello!', '2.pdf',configuration = config)
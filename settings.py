# Steps Execution sequence
AUTO_EXECUTION_SEQUENCE = "1 2 3 4 0"

USER_AGENT_LIST = [
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.36 Safari/525.19",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10",
"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/6.0.481.0 Safari/534.4",
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.3 Safari/532.2",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.201.1 Safari/532.0",
"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.173.1 Safari/530.5",
"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.558.0 Safari/534.10",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.600.0 Safari/534.14",
"Mozilla/5.0 (X11; U; Windows NT 6; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16",
"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.792.0 Safari/535.1",
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
"Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19",
"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.38 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3) Gecko/20090305 Firefox/3.1b3 GTB5",
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; ko; rv:1.9.1b2) Gecko/20081201 Firefox/3.1b2",
"Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:1.9b5) Gecko/2008032620 Firefox/3.0b5",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.12) Gecko/20080214 Firefox/2.0.0.12",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; cs; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8",
"Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8.0.5) Gecko/20060819 Firefox/1.5.0.5",
"Mozilla/5.0 (Windows; U; Windows NT 5.0; es-ES; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3",
"Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.7.9) Gecko/20050711 Firefox/1.0.5",
"Mozilla/5.0 (Windows; Windows NT 6.1; rv:2.0b2) Gecko/20100720 Firefox/4.0b2",
"Mozilla/5.0 (X11; Linux x86_64; rv:2.0b4) Gecko/20100818 Firefox/4.0b4",
"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6 GTB7.1",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b7) Gecko/20101111 Firefox/4.0b7",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b8pre) Gecko/20101114 Firefox/4.0b8pre",
"Mozilla/5.0 (X11; Linux x86_64; rv:2.0b9pre) Gecko/20110111 Firefox/4.0b9pre",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b9pre) Gecko/20101228 Firefox/4.0b9pre",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a1pre) Gecko/20110324 Firefox/4.2a1pre",
"Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2",
"Mozilla/5.0 (X11; Linux i686 on x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
"Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2",
"Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0",
"Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0",
"Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:25.0) Gecko/20100101 Firefox/25.0",
"Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0",
"Mozilla/5.0 (X11; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0",
"Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
# "Opera/5.11 (Windows 98; U) [en]",
# "Mozilla/4.0 (compatible; MSIE 5.0; Windows 98) Opera 5.12 [en]",
# "Opera/6.0 (Windows 2000; U) [fr]",
# "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 4.0) Opera 6.01 [en]",
# "Opera/7.03 (Windows NT 5.0; U) [en]",
# "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1) Opera 7.10 [en]",
# "Opera/9.02 (Windows XP; U; ru)",
# "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.24",
# "Opera/9.51 (Macintosh; Intel Mac OS X; U; en)",
# "Opera/9.70 (Linux i686 ; U; en) Presto/2.2.1",
"Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.2.15 Version/10.00",
"Opera/9.80 (Windows NT 6.1; U; sv) Presto/2.7.62 Version/11.01",
"Opera/9.80 (Windows NT 6.1; U; en-GB) Presto/2.7.62 Version/11.00",
"Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01",
"Opera/9.80 (Windows NT 6.0; U; en) Presto/2.8.99 Version/11.10",
"Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11",
# "Opera/9.80 (Windows NT 5.1) Presto/2.12.388 Version/12.14",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.12 Safari/537.36 OPR/14.0.1116.4",
# "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.29 Safari/537.36 OPR/15.0.1147.24 (Edition Next)",
# "Opera/9.80 (Linux armv6l ; U; CE-HTML/1.0 NETTV/3.0.1;; en) Presto/2.6.33 Version/10.60",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36 OPR/20.0.1387.91",
# "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Oupeng/10.2.1.86910 Safari/534.30",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2376.0 Safari/537.36 OPR/31.0.1857.0",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 OPR/32.0.1948.25",
# "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; fi-fi) AppleWebKit/420+ (KHTML, like Gecko) Safari/419.3",
# "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.7",
# "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/312.8 (KHTML, like Gecko) Safari/312.6",
# "Mozilla/5.0 (Windows; U; Windows NT 5.1; cs-CZ) AppleWebKit/523.15 (KHTML, like Gecko) Version/3.0 Safari/523.15",
# "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
# "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_6; it-it) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
# "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-HK) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
# "Mozilla/5.0 (Windows; U; Windows NT 6.1; sv-SE) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
# "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17",
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/6.1.3 Safari/537.75.14",
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/600.3.10 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.10",
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.39 (KHTML, like Gecko) Version/9.0 Safari/601.1.39",
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/603.1.13 (KHTML, like Gecko) Version/10.1 Safari/603.1.13",
# "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT;)",
# "Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
# "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; GTB5; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0)",
# "Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)",
# "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727)",
# "Mozilla/4.0 (compatible; MSIE 5.0b1; Mac_PowerPC)",
# "Mozilla/2.0 (compatible; MSIE 4.0; Windows 98)",
# "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT)",
# "Mozilla/4.0 (compatible; MSIE 5.23; Mac_PowerPC)",
# "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; GTB6; Ant.com Toolbar 1.6; MSIECrawler)",
# "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2; .NET CLR 3.5.21022; .NET CLR 3.5.30729; MS-RTC LM 8; OfficeLiveConnector.1.4; OfficeLivePatch.1.3; .NET CLR 3.0.30729)",
# "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
# "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)",
# "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
# "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
# "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
# "Mozilla/5.0 (IE 11.0; Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C; rv:11.0) like Gecko",
# "Mozilla/5.0 (IE 11.0; Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko"
]

LINKEDIN = [
  # {"username": "alina.jose1102@gmail.com", "password": "ajency#123"},
  {"username": "ralph110293@gmail.com", "password": "ajency#123"},
  {"username": "gopaul3212@gmail.com", "password": "ajency#123"},
  {"username": "testaj14aj@gmail.com", "password": "ajtest@123"},
  {"username": "testaj13aj@gmail.com", "password": "ajtest@123"},
  {"username": "testaj11aj@gmail.com", "password": "testaj@123"},
  {"username": "pnitin3103@gmail.com", "password": "ajency#123"}
]
GMAIL = [
  {"username": "gopaul3212@gmail.com", "password": "ajency#123"},
  {"username": "testaj14aj@gmail.com", "password": "ajtest@123"},
  {"username": "testaj13aj@gmail.com", "password": "ajtest@123"},
  {"username": "testaj11aj@gmail.com", "password": "testaj@123"},
  {"username": "pnitin3103@gmail.com", "password": "ajency#123"}
]



ACCOUNTS = [
  {
    "linkedIn": {"username": "ralph110293@gmail.com", "password": "ajency#123"},
    "email":{
      "gmail": [
        {"username": "gopaul3212@gmail.com", "password": "ajency#123"},
        {"username": "testaj14aj@gmail.com", "password": "ajtest@123"}
      ],
      "outlook": [
        {"username": "gopaul3212@outlook.com", "password": "ajency#123"}
      ]
    }
  },
  {
    "linkedIn": {"username": "gopaul3212@gmail.com", "password": "ajency#123"},
    "email":{
      "gmail": [
        {"username": "testaj13aj@gmail.com", "password": "ajtest@123"}
      ]
    }
  },
  {
    "linkedIn": {"username": "testaj14aj@gmail.com", "password": "ajtest@123"},
    "email":{
      "gmail": [
        {"username": "testaj11aj@gmail.com", "password": "testaj@123"}
      ]
    }
  }
]
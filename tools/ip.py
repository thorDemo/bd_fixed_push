
ips = open('ip.txt', 'r', encoding='utf-8')
for line in ips:
    print('iptables -I INPUT -s %s -j DROP' % line.strip())
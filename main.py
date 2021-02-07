import os
import search
import config
import ip_config
import video_model

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # 获取代理地址
    #ip_config.get_http()
    config.alertInfo('你想看什么电视')
    key = input()
    s = search.zuida_search(key=key)
    config.alertInfo('开始搜索')
    result = s.start_search()

    if len(result):
        config.alertInfo('搜索到以下结果')
    else:
        config.alertError('没有搜索到任何结果')

    info = video_model.video_info()
    while True:
        i = 1
        for r in result:
            print('%s:%s' % (i, r['title']))
            i += 1
        config.alertInfo('你想看哪个？输入数字选择')
        select_index = input()
        if int(select_index) > len(result):
            config.alertError('输入有误，重新输入')
            continue
        select_video = result[int(select_index)-1]
        config.alertInfo('开始获取影片详细信息')
        info = s.get_item_detail(select_video['href'])
        config.alertInfo('影片详细信息：')
        print(info.information)
        config.alertInfo('要下载这个吗？？？（1：就下载这个；0：我再选一个别的）')
        confirm_index = input()
        if confirm_index == '1':
            break

    config.alertInfo('开始准备下载')
    if len(info.videos_m3u8):
        with open("m3u8_input.txt", "w+") as f:
            for v in info.videos_m3u8:
                line = ('%s%s,%s\n' % (info.title, v.title, v.href))
                f.write(line)
            f.close()

        os.system('python3 ./m3u8_downloader.py %s' % info.title)

    elif len(info.videos_online):
        with open("m3u8_input.txt", "w+") as f:
            for v in info.videos_online:
                line = ('%s%s,%s\n' % (info.title, v.title, s.parsing_m3u8(v.href)))
                f.write(line)
            f.close()
        os.system('python3 ./m3u8_downloader.py %s' % info.title)

    elif len(info.videos_mp4):
        for mp4 in info.videos_mp4:
            config.downloadFile(savePath='/Users/chenzhe/Downloads', filePath=mp4.href, fileName=key+mp4.title)

    # s.parsing_m3u8('https://dalao.wahaha-kuyun.com/share/77b830096c1888016b4d7a730bbe9731')
    # print(s.video_info.videos_mp4)
    # config.downloadFile(savePath='/Users/chenzhe/Downloads', filePath='http://xiazai.suanmiao-zuida.com/2012/流金岁月-01.mp4', fileName='流金岁月第01集')

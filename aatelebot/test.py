import tb_bot

A = tb_bot.get_post_object('https://vk.com/absolutelyrandomcontent?w=wall-83906457_55301')
A = tb_bot.get_video_info([A])[0]
print(A)
tb_bot.send_post(A)
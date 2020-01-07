import tb_bot

A = tb_bot.get_post_object('https://vk.com/libertarian_public?w=wall-98677363_152891')
A = tb_bot.get_video_info([A])[0]
print(A)
tb_bot.sendPost(A, '-1001430319971')
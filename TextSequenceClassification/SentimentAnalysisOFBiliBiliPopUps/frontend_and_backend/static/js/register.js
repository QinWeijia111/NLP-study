$(function () {
    function bindCaptchaBtnClick() {
        $("#captcha-btn").click(function (event) {
            let $this = $(this);
            let email = $("input[name='email']").val();
            if (!email) {
                alert("请输入你的邮箱");
                return;
            }
            // 发送ajax请求
            $.ajax('/auth/captcha?email=' + email, {
                method: 'GET',
                success: function (result) {
                    if (result['code'] == 200) {
                        alert("验证码发送成功！");
                    } else {
                        alert(result['message']);
                    }
                },
                fail: function (error) {
                    console.log(error);
                }
            })

            //取消按钮的点击事件
            $this.off('click');
            let countdown = 10;
            let timer = setInterval(function () {
                if (countdown <= 0) {
                    $this.text('获取验证码');
                    clearInterval(timer);
                    bindCaptchaBtnClick();
                } else {
                    countdown--;
                    $this.text(countdown + 's');
                }
            }, 1000);
        })
    }

    bindCaptchaBtnClick();
});
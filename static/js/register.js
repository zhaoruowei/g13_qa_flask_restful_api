function bindCaptchaBtnClick()
{
    $("#button-captcha").on("click", function(event)
    {
        var $this = $(this);
        var email = $("input[name='email']").val();
        if(!email)
        {
            alert("No email!");
            return;
        }
        $.ajax({
            url: "https://<external IP>/user/captcha",
            method: "POST",
            data: {
                "email": email
            },
            success: function(res)
            {
                var code = res['code'];
                if(code === 200)
                {
                    $this.off("click");
                    var countDown = 60;
                    var timer = setInterval(function()
                    {
                        if(countDown > 0)
                        {
                            $this.text(countDown+"s");
                        }
                        else
                        {
                            $this.text("Get Captcha");
                            bindCaptchaBtnClick();
                            clearInterval(timer);
                        }
                        countDown -= 1;
                    }, 1000);
                    alert("Get Success!");
                }
                else
                {
                    alert(res['message']);
                }
            }
        })
    })
}

$(function ()
{
    bindCaptchaBtnClick();
})

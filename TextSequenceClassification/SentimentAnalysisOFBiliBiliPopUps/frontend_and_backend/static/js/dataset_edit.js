window.onload = function () {
    $("#submit-btn").click(function (event) {
        //需要阻止表单默认行为，因为表单中包含了富文本编辑器，需要通过ajax请求来完成数据的提交
        //向数据库中提交的内容是一个html文件，需要通过Ajax来完成
        event.preventDefault();
        let formData = new FormData();
        formData.append('name', $("#DatasetName").val());
        formData.append('category', $("#category-select").val());
        formData.append('content', editor.getHtml());
        formData.append('csrfmiddlewaretoken', $("input[name = 'csrfmiddlewaretoken']").val());
        // 修改的过程中未必修改文件，因此跳过这个验证
        if ($("#file-upload")[0].files.length > 0) {
            formData.append('file', $("#file-upload")[0].files[0]);
        }
        $.ajax("/dataset/edit/" + dataset_id, {
            method: "POST",
            data: formData,
            processData: false, // 告诉 jQuery 不要处理发送的数据
            contentType: false, // 告诉 jQuery 不要设置 Content-Type 请求头
            success: function (result) {
                if (result['code'] === 200) {
                    let dataset_id = result['data']['dataset_id'];
                    window.location = '/dataset/details/' + dataset_id;
                } else {
                    alert(result['message']);
                }
            }
        });
    });
}
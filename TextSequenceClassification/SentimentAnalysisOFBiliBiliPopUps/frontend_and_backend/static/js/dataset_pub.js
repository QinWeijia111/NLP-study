window.onload = function () {
    const {createEditor, createToolbar} = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
            const html = editor.getHtml()
            console.log('editor content', html)
            // 也可以同步到 <textarea>
        }
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

    $("#submit-btn").click(function (event) {
        //需要阻止表单默认行为，因为表单中包含了富文本编辑器，需要通过ajax请求来完成数据的提交
        //向数据库中提交的内容是一个html文件，需要通过Ajax来完成
        event.preventDefault();
        let formData = new FormData();
        formData.append('name', $("#DatasetName").val());
        formData.append('category', $("#category-select").val());
        formData.append('content', editor.getHtml());
        formData.append('csrfmiddlewaretoken', $("input[name = 'csrfmiddlewaretoken']").val());
        formData.append('file', $("#file-upload")[0].files[0]);
        // formData格式支持将数据打包成表单发送给后端。
        // let name = $("#DatasetName").val();
        // let category = $("#category-select").val();
        // let content = editor.getHtml();
        // let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").val();
        // let file = $("input[name = 'file']")[0].files[0];
        console.log("代码开始执行"); // 添加的测试代码
        for (let pair of formData.entries()) {
            console.log(pair[0] + ': ' + pair[1]);
        }
        $.ajax("/dataset/pub", {
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
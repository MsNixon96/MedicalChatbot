function renderDropDwon(drop_down_data) {

    let drop_down_options = "";

    for (let i = 0; i < drop_down_data.length; i += 1) {

        drop_down_options += `<li><button class="listButton" value="${drop_down_data[i].value}">${drop_down_data[i].label}</button></li>`;

    }
    const drop_down_list = `<div class="dropDownList"><ul>${drop_down_options}</ul></div>`;

    $(".chats").append(drop_down_list);
    scrollToBottomOfResults();
    // add event handler if user selects an option.
    // eslint-disable-next-line func-names
    $(".listButton").on("click", function () {

        let value = $(this).val();

        let intent = payload.split("{")[0]

        let slot = payload.split("{")[1].split(":")[0]

        let id = payload.split("{")[1].split(":")[1].split("}")[0]

        let result = intent + "{" + '"' + slot + '"' + ':' + '"' + id + '"' + '}'

        // eslint-disable-next-line no-use-before-define
        send(result);
        $(".dropDownList").remove();
        showBotTyping();
    });

}

$(() => {
    $("#verify").on("click", async () => {
        $("#challenges").empty();
        let username = $("#username").val();
        let response = null;
        try {
            response = await $.getJSON(`/challenge/${username}/verify`);
        }
        catch (error) {
            $("#challenges").append($(`<span class="error">Invalid user.</span>`))
            return;
        }
        for (const [challenge, result] of Object.entries(response["results"]))
        {
            let text = null;
            let color = null;
            if (result["status"] == "pass")
            {
                text = "Pass";
                color = "green";
            }
            else
            {
                text = `Fail: ${result["reason"]}`;
                color = "red";
            }

            $("#challenges").append($(`
                <div class="challenge">
                    <span class="title">${challenge}</span>
                    <span class="${color} result">${text}</span>
                </div>
            `))
        }
    });
});

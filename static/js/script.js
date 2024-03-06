function nextScramble() {
    edgeBuffer = document.getElementById('edgeBuffer').innerText
    cornerBuffer = document.getElementById('cornerBuffer').innerText
    edgeFlips = document.getElementById('edgeFlips').innerText
    cornerTwists = document.getElementById('cornerTwists').innerText

    $.ajax({
        url:"/gen_scramble",
        type:"POST",
        contentType: "application/json",
        data: JSON.stringify({'edgeBuffer': edgeBuffer, 'cornerBuffer': cornerBuffer, 'edgeFlips': edgeFlips, 'cornerTwists': cornerTwists}),

        success: function(scr) {
            document.getElementById('scr').textContent = scr.result
        },
        error: function(xhr, status, error) {
            // Handle errors
            console.error(error);
        }})

}

function changeOption(option, id_name) {
    document.getElementById(id_name).innerText = option;
    nextScramble()
}

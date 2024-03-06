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
            scramble = scr.result;
            document.getElementById('scr').textContent = scr.result
            document.getElementById('twisty-player').setAttribute('alg', scramble)
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

// Initial timer variables
let runTimer = false;
let centi = 0; // elapsed time in centiseconds
let second = 0;
let minute = 0;

function timerStart() {
    // timerRunning = true;
    if (runTimer) {
        centi++;
        if (centi==100) {
            second++;
            centi = 0;
        }

        if (second == 60) { 
            minute++; 
            second = 0; 
        }

        if (minute < 1) {
            document.getElementById("timer").innerText = second;
        }
        else {
            if (second < 10) {
                document.getElementById("timer").innerText = minute + ":" + "0" + second;
            }
            else {
                document.getElementById("timer").innerText = minute + ":" + second;
            } 
        }   
        setTimeout(timerStart, 10); // delay by 10 milliseconds, or 1 centisecond
    } 
}

function timerStop() {

    runTimer = false;

    if (minute < 1) {
        if (centi < 10) {
            document.getElementById("timer").innerText = second + ".0" + centi;
        }
        else {
            document.getElementById("timer").innerText = second + "." + centi;
        }
    }
    else {
        if (centi < 10) {
            if (second < 10) {
                document.getElementById("timer").innerText = minute + ":0" + second + ".0" + centi;
            }
            else {
                document.getElementById("timer").innerText = minute + ":" + second + ".0" + centi;
            }
        }
        else {
            if (second < 10) {
                document.getElementById("timer").innerText = minute + ":0" + second + "." + centi;
            }
            else {
                document.getElementById("timer").innerText = minute + ":" + second + "." + centi;
            }
        }   
    }
    
    centi = 0;
    second = 0;
    minute = 0;
    nextScramble();
}


// if user holds down space bar and timer isn't currently running, change text to green
document.addEventListener('keydown', function(e) {
    if (e.key == " ") {
        if (!runTimer) {
            document.getElementById("timer").style.color = '#00ff00';
        }    
    }

})

// once user releases space bar, start/stop timer depending on whether timer is already running currently
document.addEventListener('keyup', function(e) {
    if (e.key == " ") { // if space
        document.getElementById("timer").style.color = '#ffffff'
        if (!runTimer) {
            runTimer = true;
            timerStart();
        }
        else {
            timerStop()
        }
    }
});


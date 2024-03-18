let scrambles = [];
let genScramsOpen = false;


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
            if (scrambles.length == 2 && document.getElementById('scr').textContent == scrambles[0]) {
                scramble = scrambles[1]
            } else {
                scramble = scr.result;
                scrambles.push(scramble)
            }
            
            document.getElementById('scr').textContent = scramble
            document.getElementById('twisty-player').setAttribute('alg', scramble)
        },
        error: function(xhr, status, error) {
            // Handle errors
            console.error(error);
        }})

}

function lastScramble() {
    if (scrambles.length >= 2) {
        // we only care about current scramble and last scramble
        scrambles = scrambles.splice(scrambles.length - 2);
        document.getElementById('scr').textContent = scrambles[0];
        document.getElementById('twisty-player').setAttribute('alg', scrambles[0]);
    }
}

function showScram(scr, time) {
    let scrPopup = document.createElement("div");
    time_scr = time + " — " + scr;
    scrPopup.innerText = time_scr;
    scrPopup.className = "showScram";
    scrPopup.id = "scrPopup";
    document.body.appendChild(scrPopup);
    
    // copy button
    let copy = document.createElement("button");
    copy.className = "copy";
    copy.innerText = "Copy";
    copy.addEventListener('click', function () {
        navigator.clipboard.writeText(time_scr);
        copy.innerText = "Copied!";
    })
    scrPopup.append(copy);

    // close button
    let close = document.createElement("button");
    close.className = "close";
    close.innerText = 'Close';
    close.addEventListener('click', function() {
        this.parentNode.remove(); return false;
    })
    scrPopup.append(close);

    let drawScram = document.createElement("twisty-player");
    drawScram.setAttribute("visualization", "2D");
    drawScram.setAttribute("alg",scr);
    drawScram.setAttribute("background","none");
    drawScram.setAttribute("control-panel","none");
    // center horizontally in the popup
    drawScram.style.marginLeft = 'auto';
    drawScram.style.marginRight = 'auto';
    drawScram.style.width = '24vw';
    drawScram.style.height = '16vw';
    scrPopup.append(drawScram);

}

// function to make the pop up window for generating scrambles
function genScramsWindow() {
    if (genScramsOpen === false) {
        genScramsOpen = true;
        let gen_scrams = document.createElement("div");
        gen_scrams.className = "gen_scrams";
        gen_scrams.id = 'genScrams'
        document.body.appendChild(gen_scrams);

        // close button
        let close = document.createElement("button");
        close.className = "close";
        close.innerText = 'Close';
        close.addEventListener('click', function() {
            this.parentNode.remove(); 
            genScramsOpen = false;
            return false;
        })
        gen_scrams.append(close);

        // edge buffer text
        edgeBuffer = document.createElement("div");
        edgeBuffer.id = 'edgeBufferText'
        edgeBuffer.innerText = 'Edge Buffer: ' + document.getElementById('edgeBuffer').innerText
        edgeBuffer.style.float = 'left';
        gen_scrams.append(edgeBuffer);
        gen_scrams.append(document.createElement("br"));

        // corner buffer text
        cornerBuffer = document.createElement("div");
        cornerBuffer.id = 'cornerBufferText'
        cornerBuffer.innerText = 'Corner Buffer: ' + document.getElementById('cornerBuffer').innerText
        cornerBuffer.style.float = 'left';
        gen_scrams.append(cornerBuffer)
        gen_scrams.append(document.createElement("br"));
        gen_scrams.append(document.createElement("br"));

        // edge flips selection
        edgeFlips = document.createElement("div");
        edgeFlips.id = 'edgeFlipsText';
        edgeFlips.innerText = 'Edge Flips: ';
        edgeFlips.style.float = 'left';
        let checkboxE = document.createElement("input");
        checkboxE.type = "checkbox";
        checkboxE.className = "checkbox"
        checkboxE.id = 'edgeFlips_random'
        checkboxE.value = 'Random'
        checkboxE.checked = true;
        var label = document.createElement('label');
        label.htmlFor = 'edgeFlips_random';
        label.appendChild(document.createTextNode('Random'));
        edgeFlips.appendChild(checkboxE);
        edgeFlips.appendChild(label);
        for (let i = 0; i < 12; i++) {
            let checkbox = document.createElement("input");
            checkbox.type = 'checkbox'
            checkbox.className = 'checkbox'
            checkbox.id = 'edgeFlips_' + i;
            checkbox.value = i;
            var label = document.createElement('label');
            label.htmlFor = 'edgeFlips_' + i;
            label.appendChild(document.createTextNode(i));

            edgeFlips.appendChild(checkbox);
            edgeFlips.appendChild(label);

        }   
        gen_scrams.append(edgeFlips);

        // corner twists selection
        cornerTwists = document.createElement("div");
        cornerTwists.id = 'cornerTwistsText';
        cornerTwists.innerText = 'Corner Twists: ';
        cornerTwists.style.float = 'left';
        let checkboxC = document.createElement("input");
        checkboxC.type = "checkbox";
        checkboxC.className = "checkbox"
        checkboxC.id = 'cornerTwists_random'
        checkboxC.value = 'Random'
        checkboxC.checked = true;
        var label = document.createElement('label');
        label.htmlFor = 'cornerTwists_random';
        label.appendChild(document.createTextNode('Random'));
        cornerTwists.appendChild(checkboxC);
        cornerTwists.appendChild(label);
        for (let i = 0; i < 8; i++) {
            let checkbox = document.createElement("input");
            checkbox.type = 'checkbox'
            checkbox.className = 'checkbox'
            checkbox.id = 'cornerTwists_' + i;
            checkbox.value = i;
            var label = document.createElement('label');
            label.htmlFor = 'cornerTwists_' + i;
            label.appendChild(document.createTextNode(i));

            cornerTwists.appendChild(checkbox);
            cornerTwists.appendChild(label);

        }   
        gen_scrams.append(cornerTwists);
        gen_scrams.append(document.createElement("br"));
        gen_scrams.append(document.createElement("br"));
        gen_scrams.append(document.createElement("br"));

        let numScramsDiv = document.createElement("div");
        numScramsDiv.style.float = 'left';
        numScramsDiv.appendChild(document.createTextNode('Number of Scrambles (1-100): '))
        let numScramsInput = document.createElement("input");
        numScramsInput.id = 'numScramsInput'
        numScramsInput.style.width = '1.2vw';
        numScramsDiv.appendChild(numScramsInput);

        // gen_scrams.append(document.createTextNode('Number of Scrambles: '))
        gen_scrams.append(numScramsDiv);
        gen_scrams.append(document.createElement("br"));
        gen_scrams.append(document.createElement("br"));

        // generate button
        let generate = document.createElement("button");
        generate.className = "generate_button";
        generate.innerText = 'Generate!';
        generate.addEventListener('click', genScrams)
        gen_scrams.appendChild(generate);
    }
}

function genScrams() {

    // edge and corner buffers
    edgeBuffer = document.getElementById('edgeBuffer').innerText
    cornerBuffer = document.getElementById('cornerBuffer').innerText

    // edge flip check boxes
    let edgeCBs = document.getElementById('edgeFlipsText').querySelectorAll('input[type="checkbox"]');
    let edgeFlipOptions = [];
    edgeCBs.forEach(function(checkbox) {
        if (checkbox.checked) {
            edgeFlipOptions.push(checkbox.value);
        }
    });

    // corner twist checkboxes
    let cornerCBs = document.getElementById('cornerTwistsText').querySelectorAll('input[type="checkbox"]');
    let cornerTwistOptions = [];
    cornerCBs.forEach(function(checkbox) {
        if (checkbox.checked) {
            cornerTwistOptions.push(checkbox.value);
        }
    });

    // no of scrambles
    let numScrams = document.getElementById('numScramsInput').value;
    if (!(1 <= Number(numScrams) && Number(numScrams) <= 100)) {
        alert("Invalid number of scrambles!");
        return;
    }
    numScrams = Number(numScrams);

    $.ajax({
        url:"/gen_mult_scrambles",
        type:"POST",
        contentType: "application/json",
        data: JSON.stringify({'edgeBuffer': edgeBuffer, 'cornerBuffer': cornerBuffer, 'edgeFlipOptions': edgeFlipOptions, 'cornerTwistOptions': cornerTwistOptions, 'numScrams': numScrams}),

        success: function(scrs) {
            let gennedScrams = scrs.result;
            gennedScramsText = ""
            for (i = 1; i <= numScrams; i++) {
                gennedScramsText += i + ". " + gennedScrams[i-1] + '\n'
            }
            gennedScramsText = gennedScramsText.trimEnd();
            navigator.clipboard.writeText(gennedScramsText);
            alert("Copied to clipboard!\n" + "\n" + gennedScramsText);
        },
        error: function(xhr, status, error) {
            // Handle errors
            console.error(error);
        }})
    
    

}

function changeOption(option, id_name) {
    document.getElementById(id_name).innerText = option;
    if (document.getElementById('genScrams') !== null) {
        document.getElementById('edgeBufferText').innerText = 'Edge Buffer: ' + document.getElementById('edgeBuffer').innerText;
        document.getElementById('cornerBufferText').innerText = 'Corner Buffer: ' + document.getElementById('cornerBuffer').innerText;
    }
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

    console.log(document.getElementById("timer").innerText)
    console.log(document.getElementById('scr').innerText)

    let time_list = document.getElementById('time_list');
    // create list element
    let entry = document.createElement('li');
    // entry.textContent = document.getElementById("timer").innerText;
    
    // create a button for the time
    let time = document.createElement("button");
    time.className = "time";
    time.innerText = document.getElementById("timer").innerText;
    // save scramble associated with the time
    time.setAttribute("scr", document.getElementById('scr').innerText)
    // save time
    time.setAttribute("time", document.getElementById("timer").innerText)
    // on click, show scramble
    time.addEventListener("click", function() {
        if (document.getElementById("scrPopup") === null) {
            showScram(time.getAttribute("scr"), time.getAttribute("time"));
            this.blur();
        }
    });
    
    entry.append(time)

    // add new time to top of list
    time_list.insertBefore(entry,time_list.firstChild);

    nextScramble();
}


// if user holds down space bar and timer isn't currently running, change text to green
document.addEventListener('keydown', function(e) {
    if (e.key == " ") {
        if (!runTimer) {
            document.getElementById("timer").style.color = '#00ff00';
        }    
    }

});

// once user releases space bar, start/stop timer depending on whether timer is already running currently
document.addEventListener('keyup', function(e) {
    if (e.key == " ") { // if space
        document.getElementById("timer").style.color = '#ffffff'
        if (!runTimer) {
            runTimer = true;
            timerStart();
        }
        else {
            timerStop();
        }
    }
});

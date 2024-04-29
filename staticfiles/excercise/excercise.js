const excerciseForm = document.getElementById('excercise-form')
const excerciseBox = document.getElementById('excercise-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')
const url = window.location.href

let timerInterval
const activateTimer = (time) => {
    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    } else {
        timerBox.innerHTML = `<b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    const timer = setInterval(() => {
        seconds--
        if (seconds < 0) {
            seconds = 59
            minutes--
        }

        if (minutes.toString().length < 2) {
            displayMinutes = '0'+minutes
        } else {
            displayMinutes = minutes
        }

        if (seconds.toString().length < 2) {
            displaySeconds = '0'+seconds
        } else {
            displaySeconds = seconds
        }

        if (minutes === 0 && seconds === 0){
            timerBox.innerHTML = `<b>00:00</b>`
            setTimeout(() => {
                clearInterval(timer)
                alert('Sorry bud, its over')
                sendData()
            }, 500);
        }

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
    }, 1000);

    timerInterval = setInterval(() => {
        clearInterval(timer)
        timerBox.innerHTML = `<b>00:00</b>`
    }, 1000);
}

$.ajax({
    type: 'GET',
    url: `${url}time`,
    success: function (response) {
        activateTimer(response.time)
    },
    error: function(error) {
        console.log(error)
    }
})

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(element => {
        if (element.checked) {
            data[element.name] = element.value
        } else {
            if (!data[element.name]) {
                data[element.name] = null
            }
        }
    })

    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function (response) {
            const results = response.results
            excerciseForm.classList.add('visually-hidden')
            scoreBox.innerHTML = `<hr><h5 class="text"> score: ${response.score} / 100 </h5>`

            results.forEach(result => {
                const resultDiv = document.createElement("div")
                const cls = ['mb-0', 'pb-1', 'pt-1']
                resultDiv.classList.add(...cls)
                resultDiv.innerHTML+='<hr class="mt-3">'

                for (const [question, response] of Object.entries(result)) {
                    const answerDiv = document.createElement("div")
                    resultDiv.innerHTML += `<h6 class="text mb-2"> ${question} </h6>`

                    if (response == 'not answered') {
                        answerDiv.innerHTML += '<p class="m-0"> not answered </p>'
                        answerDiv.classList.add('text-danger')
                    } else {
                        const answer = response['answered']
                        const correct = response['correct_answer']

                        if (answer == correct) {
                            answerDiv.classList.add('text-success')
                            answerDiv.innerHTML += `<p class="m-0"> answered: ${answer} </p>`
                        } else {
                            answerDiv.classList.add('text-danger')
                            answerDiv.innerHTML += `<p class="m-0"> answered: ${answer} </p>`
                            answerDiv.innerHTML += `<p class="m-0"> correct answer: ${correct} </p>`
                        }
                    }
                    resultDiv.append(answerDiv)
                }
                resultBox.append(resultDiv)
            })
        },
        error: function (error) {
            console.log(error)
        }
    })
}

excerciseForm.addEventListener('submit', event => {
    event.preventDefault()
    clearInterval(timerInterval)
    sendData()
})
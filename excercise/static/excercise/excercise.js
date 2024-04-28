const excerciseForm = document.getElementById('excercise-form')
const excerciseBox = document.getElementById('excercise-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const url = window.location.href

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(element=>{
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
        success: function(response) {
            console.log(response)
        },
        error: function(error) {
            console.log(error)
        }
    })
}

excerciseForm.addEventListener('submit', event=>{
    event.preventDefault()
    sendData()
})
const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')

modalBtns.forEach(modalBtn=>modalBtn.addEventListener('click', () => {
    const course = modalBtn.getAttribute('data-course-title')
    const url = modalBtn.getAttribute('data-url')
    const name = modalBtn.getAttribute('data-name')
    const time = modalBtn.getAttribute('data-time')
    const numQuestion = modalBtn.getAttribute('data-num-question')

    modalBody.innerHTML = 
    `
        <div class"mb-3">${name}</div>
        <div class="text-muted">
            <ul>
                <li>course: ${course}</li>
                <li>excercise duration: ${time} minutes</li>
                <li>number of question: ${numQuestion}</li>
            </ul>
        </div>
    `

    startBtn.addEventListener('click', () => {
        window.location.href = url
    })
}))
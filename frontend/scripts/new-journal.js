const BACKEND_URL = 'http://localhost:5000/diarist';

const journalForm = document.getElementById('journal-form');
const thoughtTextArea = document.getElementById('thought-text-area');
const winTextArea = document.getElementById('win-text-area');
const goalTextArea = document.getElementById('goal-text-area');
const exerciseSelectMenu = document.getElementById('exercise-select-menu');
const moodAngry = document.getElementById('mood-angry');
const moodMeh = document.getElementById('mood-meh');
const moodGrin = document.getElementById('mood-grin');
const moodSadTear = document.getElementById('mood-sad-tear');

if (!sessionStorage.getItem('token')) {
    window.location.replace("index.html");
}

function getMoodValues(moods) {
    let output = 0
    moods.forEach((mood) => {
        output += mood.checked ? Number(mood.value) : 0
    })
    return output
}

journalForm.addEventListener('submit', (e) =>{
    e.preventDefault()
    axios
        .post(BACKEND_URL, {
            token: sessionStorage.getItem('token'),
            body1: thoughtTextArea.value,
            body2: winTextArea.value,
            body3: goalTextArea.value,
            exercise: Boolean(Number(exerciseSelectMenu.value)),
            mood: getMoodValues([moodAngry, moodMeh, moodGrin, moodSadTear])
        })
        .then((res) => {
            console.log('success')
            if (res.status === 200) {
                window.location.href = 'journal.html'
            }
        })
        .catch((err) => {
            console.error(err)
        });
});